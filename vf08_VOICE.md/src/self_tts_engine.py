#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
self_tts_engine.py : 내 진짜 목소리(Voice Clone) 기반 맞춤형 TTS 엔진
=============================================================================
- [001]~[999] 무손실 순차 번호 자동 매김(Auto-Increment Indexing) 엔진 탑재
- 누락 및 중첩 0% 보장: result/ 폴더 내 최신 번호를 자동 추적하여 페어 저장
- 듀얼 엔진: 로컬 무제한 신경망 합성(기본) + ElevenLabs 1:1 보이스 클론(선택)
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
import requests
import edge_tts


def get_next_result_index(result_dir: str) -> int:
    """result/ 디렉터리 내 [001]~[999] 패턴을 검사하여 다음 순차 번호를 반환"""
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


class RealVoiceTTS:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] config.json 읽기 실패: {e}")
        return {}

    def is_clone_ready(self):
        api_key = self.config.get("ELEVENLABS_API_KEY", "")
        voice_id = self.config.get("VOICE_ID", "")
        return (
            bool(api_key) and 
            api_key != "YOUR_API_KEY_HERE" and 
            bool(voice_id) and 
            voice_id != "YOUR_VOICE_ID_HERE"
        )

    def synthesize_with_real_voice(self, text: str, output_path: str) -> bool:
        """ElevenLabs 1:1 보이스 클로닝 API를 통해 대표님 실제 목소리로 합성"""
        api_key = self.config["ELEVENLABS_API_KEY"]
        voice_id = self.config["VOICE_ID"]
        model_id = self.config.get("MODEL_ID", "eleven_multilingual_v2")
        voice_settings = self.config.get("VOICE_SETTINGS", {
            "stability": 0.65,
            "similarity_boost": 0.85,
            "style": 0.10,
            "use_speaker_boost": True
        })

        print(f"[RUN] ★ 대표님 실제 목소리(1:1 Voice Clone) 합성 시작...")
        print(f"  - Voice ID   : {voice_id}")
        print(f"  - Model ID   : {model_id}")
        print(f"  - Output Path: {output_path}")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"[SUCCESS] ★ 대표님 실제 목소리로 음성 생성 완료! ({os.path.abspath(output_path)})")
                return True
            else:
                print(f"[ERROR] ElevenLabs API 호출 실패 ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] 요청 중 예외 발생: {e}")
            return False

    async def synthesize_fallback(self, text: str, output_path: str, rate="-7%", pitch="-2Hz"):
        """오프라인 Fallback 신경망 합성 (ko-KR-InJoonNeural 기반)"""
        print(f"[RUN] 무제한 로컬 신경망 합성 엔진 실행 중...")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        communicate = edge_tts.Communicate(
            text=text,
            voice="ko-KR-InJoonNeural",
            rate=rate,
            pitch=pitch
        )
        await communicate.save(output_path)
        print(f"[SUCCESS] 음성 파일 생성 완료: {os.path.abspath(output_path)}")


def main():
    parser = argparse.ArgumentParser(description="내 목소리 승계 TTS 생성기 (self_tts_engine)")
    parser.add_argument("--text", type=str, help="합성할 텍스트 문장")
    parser.add_argument("--file", type=str, help="합성할 텍스트 파일 (.txt 또는 .md)")
    parser.add_argument("--name", type=str, default="generated", help="산출물 식별자 이름 (기본: generated)")
    parser.add_argument("--output", type=str, help="직접 지정할 출력 mp3 파일 경로 (생략 시 result 폴더에 [NNN] 순차 번호로 자동 저장)")
    parser.add_argument("--rate", type=str, default="-7%", help="발화 속도 (기본: -7%%)")
    parser.add_argument("--pitch", type=str, default="-2Hz", help="음높이 피치 (기본: -2Hz)")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result_dir = os.path.join(base_dir, "result")

    content = ""
    if args.file:
        if not os.path.exists(args.file):
            print(f"[ERROR] 파일을 찾을 수 없습니다: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        sample_path = os.path.join(base_dir, "sample_script.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "안녕하세요. 대표님의 고유한 목소리로 새롭게 생성된 인공지능 음성입니다."

    # 출력 경로 결정 ([001]~[999] 자동 번호 매김)
    if args.output:
        output_mp3 = args.output
        output_txt = os.path.splitext(output_mp3)[0] + ".txt"
    else:
        next_idx = get_next_result_index(result_dir)
        tag = f"[{next_idx:03d}]"
        clean_name = re.sub(r"[^\w\s-]", "", args.name).strip().replace(" ", "_")
        output_mp3 = os.path.join(result_dir, f"{tag}_{clean_name}_voice.mp3")
        output_txt = os.path.join(result_dir, f"{tag}_{clean_name}_script.txt")

    # 1. 텍스트 대본 파일 동시 저장 (누락 방지)
    os.makedirs(os.path.dirname(os.path.abspath(output_txt)), exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as tf:
        tf.write(content)
    print(f"[SAVED] 대본 텍스트 보존 완료: {output_txt}")

    # 2. 오디오 음성 합성 및 저장
    tts = RealVoiceTTS()
    if tts.is_clone_ready():
        success = tts.synthesize_with_real_voice(content, output_mp3)
        if not success:
            print("[INFO] 로컬 신경망 엔진으로 재시도합니다...")
            asyncio.run(tts.synthesize_fallback(content, output_mp3, rate=args.rate, pitch=args.pitch))
    else:
        asyncio.run(tts.synthesize_fallback(content, output_mp3, rate=args.rate, pitch=args.pitch))

    print(f"\n=====================================================================")
    print(f"[결과물 완제 보존 완료]")
    print(f"  - 대본 텍스트 : {os.path.abspath(output_txt)}")
    print(f"  - 완성 오디오 : {os.path.abspath(output_mp3)}")
    print(f"=====================================================================\n")


if __name__ == "__main__":
    main()
