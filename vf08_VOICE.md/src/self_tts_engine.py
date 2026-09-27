#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
self_tts_engine.py : 내 진짜 목소리(Voice Clone) 기반 맞춤형 TTS 엔진
=============================================================================
[듀얼 엔진 아키텍처]
1. 모드 A (내 목소리 100% 복제): ElevenLabs Multilingual v2 + 사용자 Voice ID
2. 모드 B (오프라인 경량 모드): Edge-TTS Neural Synthesis (Fallback)
"""

import os
import sys
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
        """오프라인 Fallback 신경망 합성"""
        print(f"[RUN] 오프라인 신경망 합성 엔진 실행 (Voice Clone 설정 전 임시 모드)...")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        communicate = edge_tts.Communicate(
            text=text,
            voice="ko-KR-InJoonNeural",
            rate=rate,
            pitch=pitch
        )
        await communicate.save(output_path)
        print(f"[SUCCESS] 임시 음성 파일 생성 완료: {os.path.abspath(output_path)}")


def main():
    parser = argparse.ArgumentParser(description="내 목소리 승계 TTS 생성기 (self_tts_engine)")
    parser.add_argument("--text", type=str, help="합성할 텍스트 문장")
    parser.add_argument("--file", type=str, help="합성할 텍스트 파일 (.txt 또는 .md)")
    parser.add_argument("--output", type=str, default="result/my_voice_output.mp3", help="출력 mp3 파일 경로")
    parser.add_argument("--rate", type=str, default="-7%", help="발화 속도 (기본: -7%%)")
    parser.add_argument("--pitch", type=str, default="-2Hz", help="음높이 피치 (기본: -2Hz)")

    args = parser.parse_args()

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
        sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_script.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "안녕하세요. 대표님의 고유한 목소리로 새롭게 생성된 인공지능 음성입니다."

    tts = RealVoiceTTS()
    if tts.is_clone_ready():
        success = tts.synthesize_with_real_voice(content, args.output)
        if not success:
            print("[INFO] Fallback 엔진으로 재시도합니다...")
            asyncio.run(tts.synthesize_fallback(content, args.output, rate=args.rate, pitch=args.pitch))
    else:
        print("\n" + "="*70)
        print("[안내] 현재 ElevenLabs Voice ID가 등록되지 않아 임시 모드로 생성합니다.")
        print("대표님의 '진짜 내 목소리'로 100% 생성하시려면 아래 명령을 1회 실행하세요:")
        print("  1. https://elevenlabs.io 에서 무료 API Key 복사")
        print("  2. python src/create_clone_voice.py --api-key YOUR_API_KEY")
        print("="*70 + "\n")
        asyncio.run(tts.synthesize_fallback(content, args.output, rate=args.rate, pitch=args.pitch))


if __name__ == "__main__":
    main()
