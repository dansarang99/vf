#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
multi_char_tts_engine.py : 10대 VOICE 캐릭터 다중 화자 드라마 TTS 엔진
=============================================================================
- [배역명] 태그 기반 화자별 음색/피치/속도 자동 스위칭 합성
- 조각 오디오 무손실 결합(MP3 Frame Concatenation)을 통한 완제 오디오북 생성
- result/ [001]~[999] 무손실 순차 번호 자동 매김 탑재
"""

import os
import sys
import re
import json
import asyncio
import argparse
import subprocess

def ensure_dependencies():
    for pkg in ["requests", "edge_tts"]:
        try:
            __import__(pkg)
        except ImportError:
            print(f"[INFO] {pkg} 모듈 자동 설치 중...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_dependencies()
import edge_tts


# 10대 배역 표준 튜닝 프리셋
CHARACTER_PRESETS = {
    # 1. 메인 해설
    "해설": {"voice": "ko-KR-InJoonNeural", "pitch": "-2Hz", "rate": "-7%", "volume": "+0%"},
    "나레이터": {"voice": "ko-KR-InJoonNeural", "pitch": "-2Hz", "rate": "-7%", "volume": "+0%"},
    "NARRATOR": {"voice": "ko-KR-InJoonNeural", "pitch": "-2Hz", "rate": "-7%", "volume": "+0%"},

    # 2. 남주인공
    "주인공": {"voice": "ko-KR-HyunsuNeural", "pitch": "+1Hz", "rate": "+3%", "volume": "+5%"},
    "남주인공": {"voice": "ko-KR-HyunsuNeural", "pitch": "+1Hz", "rate": "+3%", "volume": "+5%"},
    "에이스": {"voice": "ko-KR-HyunsuNeural", "pitch": "+1Hz", "rate": "+3%", "volume": "+5%"},
    "HERO": {"voice": "ko-KR-HyunsuNeural", "pitch": "+1Hz", "rate": "+3%", "volume": "+5%"},

    # 3. 여주인공
    "여주인공": {"voice": "ko-KR-SunHiNeural", "pitch": "+1Hz", "rate": "-2%", "volume": "+0%"},
    "관제사": {"voice": "ko-KR-SunHiNeural", "pitch": "+1Hz", "rate": "-2%", "volume": "+0%"},
    "HEROINE": {"voice": "ko-KR-SunHiNeural", "pitch": "+1Hz", "rate": "-2%", "volume": "+0%"},

    # 4. 사령관/스승/노인
    "사령관": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "-12%", "volume": "+5%"},
    "장군": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "-12%", "volume": "+5%"},
    "스승": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "-12%", "volume": "+5%"},
    "노인": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "-12%", "volume": "+5%"},
    "MENTOR": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "-12%", "volume": "+5%"},

    # 5. 악역/라이벌
    "악역": {"voice": "ko-KR-InJoonNeural", "pitch": "-3Hz", "rate": "-1%", "volume": "-2%"},
    "라이벌": {"voice": "ko-KR-InJoonNeural", "pitch": "-3Hz", "rate": "-1%", "volume": "-2%"},
    "VILLAIN": {"voice": "ko-KR-InJoonNeural", "pitch": "-3Hz", "rate": "-1%", "volume": "-2%"},

    # 6. 따뜻한 조연/어머니
    "어머니": {"voice": "ko-KR-SunHiNeural", "pitch": "-3Hz", "rate": "-8%", "volume": "-3%"},
    "조연여": {"voice": "ko-KR-SunHiNeural", "pitch": "-3Hz", "rate": "-8%", "volume": "-3%"},
    "SUPPORT_F": {"voice": "ko-KR-SunHiNeural", "pitch": "-3Hz", "rate": "-8%", "volume": "-3%"},

    # 7. 유쾌한 친구/조력자
    "친구": {"voice": "ko-KR-HyunsuNeural", "pitch": "+4Hz", "rate": "+10%", "volume": "+3%"},
    "조력자": {"voice": "ko-KR-HyunsuNeural", "pitch": "+4Hz", "rate": "+10%", "volume": "+3%"},
    "FRIEND": {"voice": "ko-KR-HyunsuNeural", "pitch": "+4Hz", "rate": "+10%", "volume": "+3%"},

    # 8. 소년/어린이
    "소년": {"voice": "ko-KR-SunHiNeural", "pitch": "+5Hz", "rate": "+8%", "volume": "+4%"},
    "아이": {"voice": "ko-KR-SunHiNeural", "pitch": "+5Hz", "rate": "+8%", "volume": "+4%"},
    "어린이": {"voice": "ko-KR-SunHiNeural", "pitch": "+5Hz", "rate": "+8%", "volume": "+4%"},
    "CHILD": {"voice": "ko-KR-SunHiNeural", "pitch": "+5Hz", "rate": "+8%", "volume": "+4%"},

    # 9. 차가운 라이벌녀/엘리트
    "라이벌녀": {"voice": "ko-KR-SunHiNeural", "pitch": "+0Hz", "rate": "+3%", "volume": "+2%"},
    "엘리트": {"voice": "ko-KR-SunHiNeural", "pitch": "+0Hz", "rate": "+3%", "volume": "+2%"},
    "RIVAL_F": {"voice": "ko-KR-SunHiNeural", "pitch": "+0Hz", "rate": "+3%", "volume": "+2%"},

    # 10. 시스템/경보/상황실
    "시스템": {"voice": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+0%", "volume": "+0%"},
    "경보": {"voice": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+0%", "volume": "+0%"},
    "상황실": {"voice": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+0%", "volume": "+0%"},
    "SYSTEM": {"voice": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+0%", "volume": "+0%"}
}


def get_next_result_index(result_dir: str) -> int:
    os.makedirs(result_dir, exist_ok=True)
    pattern = re.compile(r"^\[(\d{3})\]")
    max_idx = 0
    for fname in os.listdir(result_dir):
        match = pattern.match(fname)
        if match:
            idx = int(match.group(1))
            if idx > max_idx:
                max_idx = idx
    return max_idx + 1


def parse_script_lines(script_content: str):
    """
    [배역명] 대사 형식의 텍스트를 파싱하여 (배역명, 대사) 리스트 반환
    """
    lines = script_content.strip().split("\n")
    parsed = []
    current_char = "해설"

    tag_pattern = re.compile(r"^\[(.*?)\]\s*(.*)$")

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = tag_pattern.match(line)
        if match:
            char_name = match.group(1).strip()
            speech = match.group(2).strip()
            if speech:
                parsed.append((char_name, speech))
            current_char = char_name
        else:
            # 태그가 없는 줄은 이전 화자의 대사로 연결
            parsed.append((current_char, line))

    return parsed


async def synthesize_line(text: str, char_name: str, tmp_path: str):
    """단일 대사를 해당 캐릭터 프리셋으로 합성"""
    # 프리셋 검색 (없으면 해설 기본값)
    preset = CHARACTER_PRESETS.get(char_name)
    if not preset:
        # 부분 일치 검색
        for k in CHARACTER_PRESETS:
            if k in char_name:
                preset = CHARACTER_PRESETS[k]
                break
    if not preset:
        preset = CHARACTER_PRESETS["해설"]

    communicate = edge_tts.Communicate(
        text=text,
        voice=preset["voice"],
        rate=preset["rate"],
        pitch=preset["pitch"],
        volume=preset["volume"]
    )
    await communicate.save(tmp_path)


async def build_multi_character_audio(script_content: str, final_mp3_path: str, temp_dir: str):
    parsed = parse_script_lines(script_content)
    print(f"[INFO] 총 {len(parsed)}개의 캐릭터 대사를 순차 합성합니다...")

    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    for idx, (char_name, speech) in enumerate(parsed, 1):
        tmp_mp3 = os.path.join(temp_dir, f"segment_{idx:04d}_{char_name}.mp3")
        print(f"  [{idx}/{len(parsed)}] [{char_name}] : \"{speech[:25]}...\"")
        await synthesize_line(speech, char_name, tmp_mp3)
        temp_files.append(tmp_mp3)

    # 무손실 MP3 프레임 결합
    print(f"\n[INFO] 모든 캐릭터 세그먼트를 단일 완제 오디오로 병합합니다...")
    os.makedirs(os.path.dirname(os.path.abspath(final_mp3_path)), exist_ok=True)
    with open(final_mp3_path, "wb") as outfile:
        for f in temp_files:
            if os.path.exists(f):
                with open(f, "rb") as infile:
                    outfile.write(infile.read())
                # 임시 파일 삭제
                try:
                    os.remove(f)
                except:
                    pass

    # 임시 디렉터리 정리
    try:
        os.rmdir(temp_dir)
    except:
        pass

    print(f"[SUCCESS] ★ 10대 다중 캐릭터 완제 오디오 결합 완료: {os.path.abspath(final_mp3_path)}")


def main():
    parser = argparse.ArgumentParser(description="10대 VOICE 캐릭터 다중 화자 드라마 TTS 엔진")
    parser.add_argument("--file", type=str, required=True, help="화자 태그가 포함된 대본 파일 경로")
    parser.add_argument("--name", type=str, default="multi_char_drama", help="결과물 식별자 이름")
    parser.add_argument("--output", type=str, help="출력 mp3 파일 경로 (생략 시 result/ [NNN] 자동 매김)")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result_dir = os.path.join(base_dir, "result")
    temp_dir = os.path.join(base_dir, "scratch", "multi_tts_tmp")

    if not os.path.exists(args.file):
        print(f"[ERROR] 대본 파일을 찾을 수 없습니다: {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        script_content = f.read()

    # 출력 경로 결정
    if args.output:
        output_mp3 = args.output
        output_txt = os.path.splitext(output_mp3)[0] + ".txt"
    else:
        next_idx = get_next_result_index(result_dir)
        tag = f"[{next_idx:03d}]"
        clean_name = re.sub(r"[^\w\s-]", "", args.name).strip().replace(" ", "_")
        output_mp3 = os.path.join(result_dir, f"{tag}_{clean_name}_voice.mp3")
        output_txt = os.path.join(result_dir, f"{tag}_{clean_name}_script.txt")

    # 대본 복제 보존
    with open(output_txt, "w", encoding="utf-8") as out_t:
        out_t.write(script_content)
    print(f"[SAVED] 대본 텍스트 보존 완료: {output_txt}")

    # 합성 실행
    asyncio.run(build_multi_character_audio(script_content, output_mp3, temp_dir))

    print(f"\n=====================================================================")
    print(f"[다중 캐릭터 드라마 결과물 보존 완료]")
    print(f"  - 대본 : {os.path.abspath(output_txt)}")
    print(f"  - 음성 : {os.path.abspath(output_mp3)}")
    print(f"=====================================================================\n")


if __name__ == "__main__":
    main()
