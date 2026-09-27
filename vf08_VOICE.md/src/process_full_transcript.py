#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
process_full_transcript.py : 유튜브 2시간(7,077초) 풀텍스트 복제 및 정제
- 2,687개 스니펫을 문맥 및 문장 단위로 자동 병합(Context Merging)
- 분초 단위 타임스탬프 [HH:MM:SS ~ HH:MM:SS] 및 목표 지속시간(초) 정밀 산출
- result/[016]_episode_01_full_script_with_timestamps.md 생성
"""

import os
import json
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(base_dir, "youtube_full_transcript.json")
output_md = os.path.join(base_dir, "result", "[016]_episode_01_full_script_with_timestamps.md")

with open(json_path, "r", encoding="utf-8") as f:
    raw_snippets = json.load(f)

print(f"[INFO] 원천 스니펫 총 {len(raw_snippets)}개 로드 완료.")

# 문장 단위 병합 로직
merged_sentences = []
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
        # '>>' 기호가 나오거나 일정 시간 이상 공백이 있으면 새 화자/문장으로 분리
        if text.startswith(">>") or (s_start - end_time > 1.8):
            merged_sentences.append({
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

        # 마침표, 물음표, 느낌표로 끝나면 문장 완결
        if re.search(r"[\.\?\!]$", current_sentence):
            merged_sentences.append({
                "start": start_time,
                "end": end_time,
                "duration": round(end_time - start_time, 2),
                "text": current_sentence.replace(">>", "").strip()
            })
            current_sentence = ""

if current_sentence:
    merged_sentences.append({
        "start": start_time,
        "end": end_time,
        "duration": round(end_time - start_time, 2),
        "text": current_sentence.replace(">>", "").strip()
    })

print(f"[INFO] 문장 단위 병합 완료: 총 {len(merged_sentences)}개 대화/서사 씬 추출.")

# 마크다운 문서 생성
with open(output_md, "w", encoding="utf-8") as out:
    out.write("# [FULL_SCRIPT] 제1탄 전편 풀텍스트 및 분초 단위 타임스탬프 마스터 대본\n")
    out.write("> **원천 영상**: `조롱받던 낙오 청년, 항공 위기에서 기적의 착륙!` (ID: `rmOqIP-D75A`)\n")
    out.write(f"> **총 영상 길이**: 7,077초 (1시간 57분 57초) / **총 문장 수**: {len(merged_sentences)}개\n")
    out.write("> **목적**: 100% 동일한 보이스 스피드 및 분초 단위 오차 0% 복원을 위한 타임코드 대본\n\n---\n\n")

    for i, s in enumerate(merged_sentences, 1):
        s_m = int(s["start"]) // 60
        s_s = int(s["start"]) % 60
        e_m = int(s["end"]) // 60
        e_s = int(s["end"]) % 60
        
        # 속도 계산 (WPM 및 음절당 시간)
        char_count = len(s["text"].replace(" ", ""))
        cps = round(char_count / s["duration"], 2) if s["duration"] > 0 else 0
        
        out.write(f"### Scene {i:04d} `[{s_m:02d}:{s_s:02d} ~ {e_m:02d}:{e_s:02d}]` (길이: {s['duration']}s | 속도: {cps}자/초)\n")
        out.write(f"**대본**: {s['text']}\n\n")

print(f"[SUCCESS] 풀텍스트 마크다운 파일 저장 완료: {output_md}")
