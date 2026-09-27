#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_202_master_script.py : 1,124씬 10인 배역 1인 다역 자동 매핑 및 마스터 대본 생성
- 출력: vf09_FullScene_VideoRemaker_skill/result/[202]_episode_01_10char_1124scenes_master_script.txt 및 .md
"""

import os
import json
import re

vf09_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vf08_dir = os.path.join(os.path.dirname(vf09_dir), "vf08_VOICE.md")
json_path = os.path.join(vf08_dir, "youtube_full_transcript.json")
result_dir = os.path.join(vf09_dir, "result")
os.makedirs(result_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    raw_snippets = json.load(f)

# 1,124개 씬 병합
scenes = []
current_sentence = ""
start_time = 0.0
end_time = 0.0

for s in raw_snippets:
    text = s["text"].strip()
    s_start = s["start"]
    s_dur = s["duration"]
    s_end = s_start + s_dur

    if not current_sentence:
        start_time = s_start
        current_sentence = text
        end_time = s_end
    else:
        if text.startswith(">>") or (s_start - end_time > 1.8):
            scenes.append({
                "start": start_time,
                "end": end_time,
                "duration": round(end_time - start_time, 2),
                "text": current_sentence.replace(">>", "").strip()
            })
            start_time = s_start
            current_sentence = text
            end_time = s_end
        else:
            current_sentence += " " + text
            end_time = s_end

        if any(current_sentence.endswith(p) for p in [".", "?", "!"]):
            scenes.append({
                "start": start_time,
                "end": end_time,
                "duration": round(end_time - start_time, 2),
                "text": current_sentence.replace(">>", "").strip()
            })
            current_sentence = ""

if current_sentence:
    scenes.append({
        "start": start_time,
        "end": end_time,
        "duration": round(end_time - start_time, 2),
        "text": current_sentence.replace(">>", "").strip()
    })

print(f"[INFO] 1,124씬 병합 완료: 총 {len(scenes)}개 씬.")

# 10대 배역 1인 다역 자동 분류 함수
def assign_character(text, prev_char="해설"):
    t = text.lower()
    
    # 1. 시스템/경보/관제기계
    if any(k in t for k in ["경고", "시스템", "고도", "속도", "비상", "mhz", "피트", "노트", "엔진 2번", "좌표"]):
        return "시스템"
    # 2. 사령관/장군/스승/교관
    if any(k in t for k in ["장군", "사령관", "교관", "명령", "조종사", "훈련", "자네", "본부", "육군", "공군", "사령부"]):
        return "사령관"
    # 3. 어머니/가족
    if any(k in t for k in ["엄마", "어머니", "아들", "아이들", "기도", "살려", "주님", "무사히", "가족"]):
        return "어머니"
    # 4. 소년/아이/어린이
    if any(k in t for k in ["무서워", "어떻게 돼", "형아", "누나", "아저씨", "불나요", "어린"]):
        return "소년"
    # 5. 친구/익살꾼/동기
    if any(k in t for k in ["야 ", "임마", "인마", "짜식", "치맥", "대박", "미쳤냐", "너 믿는다", "고등학교", "착지했잖아"]):
        return "친구"
    # 6. 악역/비아냥 라이벌
    if any(k in t for k in ["흥", "고철", "낙오", "주제에", "감히", "꼴에", "비웃", "어디 한번", "한심"]):
        return "악역"
    # 7. 라이벌녀/도도한 엘리트 관료
    if any(k in t for k in ["규정", "각도", "동강", "접지", "수치", "데이터", "오차", "통계", "원칙대로"]):
        return "라이벌녀"
    # 8. 여주인공/관제탑 여성 엘리트
    if any(k in t for k in ["관제탑", "침착하세요", "레이더", "활주로", "스카이", "오빠", "믿어요", "지수"]):
        return "여주인공"
    # 9. 주인공 (청년 에이스 파일럿)
    if any(k in t for k in ["제가", "조종간", "내가", "비틀겠다", "성원", "준혁", "에이스", "버텨", "추진력"]):
        return "주인공"
    
    # 대화체 기호가 있거나 구어체일 경우 주인공 또는 직전 화자 계승
    if any(t.endswith(p) for p in ["잖아", "거야", "있어", "됐어", "하냐", "말이야"]):
        return "주인공" if prev_char == "해설" else prev_char

    # 기본값: 메인 해설
    return "해설"


# 전 씬 배역 배정 및 타임코드 대본 생성
script_md = os.path.join(result_dir, "[202]_episode_01_10char_1124scenes_master_script.md")
script_txt = os.path.join(result_dir, "[202]_episode_01_10char_1124scenes_master_script.txt")

char_stats = {}
last_char = "해설"

with open(script_md, "w", encoding="utf-8") as out_m, open(script_txt, "w", encoding="utf-8") as out_t:
    out_m.write("# [MASTER_SCRIPT] 제1편 1,124씬 10인 배역 1인 다역 전수 대본\n")
    out_m.write(f"> **문서 번호**: `[202]`\n")
    out_m.write(f"> **총 씬 수**: {len(scenes)}개 씬 / **총 상영시간**: {scenes[-1]['end']:.1f}초 ({scenes[-1]['end']/60:.1f}분)\n\n---\n\n")

    for idx, sc in enumerate(scenes, 1):
        char = assign_character(sc["text"], last_char)
        last_char = char
        char_stats[char] = char_stats.get(char, 0) + 1

        # 다음 씬과의 간극(무음 대기시간)
        next_gap = round(scenes[idx]["start"] - sc["end"], 2) if idx < len(scenes) else 0.0
        if next_gap < 0: next_gap = 0.0

        m_s = int(sc["start"]) // 60
        s_s = int(sc["start"]) % 60
        m_e = int(sc["end"]) // 60
        s_e = int(sc["end"]) % 60

        out_m.write(f"### Scene {idx:04d} `[{m_s:02d}:{s_s:02d} ~ {m_e:02d}:{s_e:02d}]` (지속: {sc['duration']}s | 대기: {next_gap}s)\n")
        out_m.write(f"**[{char}]**: {sc['text']}\n\n")

        out_t.write(f"[{char}] {sc['text']}\n")

print(f"[SUCCESS] [202] 마스터 대본 생성 완료!")
print(f"  - 마크다운: {script_md}")
print(f"  - 텍스트: {script_txt}")
print("\n[10대 배역별 씬 배분 통계]")
for c, cnt in sorted(char_stats.items(), key=lambda x: -x[1]):
    pct = (cnt / len(scenes)) * 100
    print(f"  - [{c}] : {cnt}개 씬 ({pct:.1f}%)")
