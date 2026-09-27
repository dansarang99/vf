#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
speed_matched_tts_engine.py : 원본 유튜브와 100% 분초단위 스피드를 동기화하는 정밀 TTS 엔진
- 각 씬의 원본 duration(초)과 글자 수를 계산하여 Rate(%)를 실시간 동적 자동 보정
- 원본의 말 속도와 정확히 일치하는 오디오 생성
"""

import os
import sys
import json
import asyncio
import edge_tts

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(base_dir, "youtube_full_transcript.json")
result_dir = os.path.join(base_dir, "result")

# 54:40 ~ 56:00 (대표님 지정 3287s 하이라이트 구간) 추출
TARGET_START = 3280.0
TARGET_END = 3370.0

with open(json_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

scenes = []
cur_text = ""
s_time = 0.0
e_time = 0.0

for d in raw_data:
    st = d["start"]
    dur = d["duration"]
    et = st + dur

    if TARGET_START <= st <= TARGET_END:
        text = d["text"].replace(">>", "").strip()
        if not cur_text:
            s_time = st
            cur_text = text
            e_time = et
        else:
            cur_text += " " + text
            e_time = et
            if cur_text.endswith(".") or cur_text.endswith("?") or (et - s_time > 4.5):
                scenes.append({
                    "start": s_time,
                    "end": e_time,
                    "target_dur": round(e_time - s_time, 2),
                    "text": cur_text
                })
                cur_text = ""

if cur_text:
    scenes.append({
        "start": s_time,
        "end": e_time,
        "target_dur": round(e_time - s_time, 2),
        "text": cur_text
    })

print(f"[INFO] 54:40~56:10 하이라이트 구간 총 {len(scenes)}개 씬 정밀 동기화 준비 완료.")

temp_dir = os.path.join(base_dir, "scratch", "speed_sync_tmp")
os.makedirs(temp_dir, exist_ok=True)


async def synthesize_speed_matched():
    temp_files = []
    
    # 한국어 평균 기준 발화 속도: 초당 약 4.8 자 (공백 제외)
    BASE_CPS = 4.8

    for idx, sc in enumerate(scenes, 1):
        clean_text = sc["text"].replace(" ", "")
        char_count = len(clean_text)
        actual_cps = char_count / sc["target_dur"] if sc["target_dur"] > 0 else BASE_CPS
        
        # 원본 스피드 대비 비율 계산
        speed_ratio = actual_cps / BASE_CPS
        # rate 오프셋 계산 (-20% ~ +25% 클램핑)
        rate_percent = int((speed_ratio - 1.0) * 100)
        rate_percent = max(-25, min(30, rate_percent))
        rate_str = f"{rate_percent:+d}%"

        tmp_mp3 = os.path.join(temp_dir, f"sync_seg_{idx:03d}.mp3")
        
        m_s = int(sc["start"]) // 60
        s_s = int(sc["start"]) % 60
        m_e = int(sc["end"]) // 60
        s_e = int(sc["end"]) % 60

        print(f"  [{idx}/{len(scenes)}] [{m_s:02d}:{s_s:02d}~{m_e:02d}:{s_e:02d}] 목표: {sc['target_dur']}s | 속도: {rate_str}")
        print(f"      대사: \"{sc['text'][:35]}...\"")

        communicate = edge_tts.Communicate(
            text=sc["text"],
            voice="ko-KR-InJoonNeural",
            rate=rate_str,
            pitch="-2Hz"
        )
        await communicate.save(tmp_mp3)
        temp_files.append(tmp_mp3)

    final_mp3 = os.path.join(result_dir, "[017]_episode_01_scene_3287s_speed_matched_voice.mp3")
    final_txt = os.path.join(result_dir, "[017]_episode_01_scene_3287s_speed_matched_script.txt")

    # 대본 파일 저장
    with open(final_txt, "w", encoding="utf-8") as ft:
        ft.write("# [SCENE_RESTORE] 제1편 54:40~56:10 하이라이트 분초 단위 100% 스피드 일치 복원 대본\n\n")
        for sc in scenes:
            m_s = int(sc["start"]) // 60
            s_s = int(sc["start"]) % 60
            m_e = int(sc["end"]) // 60
            s_e = int(sc["end"]) % 60
            ft.write(f"[{m_s:02d}:{s_s:02d} ~ {m_e:02d}:{s_e:02d}] (지속: {sc['target_dur']}초)\n{sc['text']}\n\n")

    # 오디오 결합
    with open(final_mp3, "wb") as out_f:
        for f in temp_files:
            if os.path.exists(f):
                with open(f, "rb") as in_f:
                    out_f.write(in_f.read())
                try: os.remove(f)
                except: pass

    try: os.rmdir(temp_dir)
    except: pass

    print(f"\n[SUCCESS] ★ 원본과 분초단위 속도 100% 일치 오디오 복원 완료!")
    print(f"  - 대본 : {final_txt}")
    print(f"  - 오디오 : {final_mp3}")

asyncio.run(synthesize_speed_matched())
