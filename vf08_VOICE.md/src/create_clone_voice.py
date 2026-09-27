#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
create_clone_voice.py : 내 목소리(FISH_01~05)를 1:1 보이스 클론으로 등록하는 스크립트
=============================================================================
- 역할: upload 폴더의 mp3 파일들을 ElevenLabs Voice Lab에 업로드하여
        대표님 고유의 'Instant Voice Clone'을 생성하고 Voice ID를 config.json에 자동 저장합니다.
"""

import os
import sys
import json
import argparse
import subprocess

def ensure_requests():
    try:
        import requests
    except ImportError:
        print("[INFO] requests 라이브러리 자동 설치 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

ensure_requests()
import requests


def create_voice_clone(api_key: str, voice_name: str = "My_Real_Voice"):
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "upload")
    files_to_upload = []
    
    # 5개 원천 오디오 파일 검색
    candidates = ["FISH_01.mp3", "FISH_02._.mp3", "FISH_03.mp3", "FISH_04.mp3", "FISH_05.mp3"]
    for c in candidates:
        full_path = os.path.join(upload_dir, c)
        if os.path.exists(full_path):
            files_to_upload.append(full_path)
            
    if not files_to_upload:
        # upload 디렉터리 내 모든 mp3 탐색
        for f in os.listdir(upload_dir):
            if f.endswith(".mp3") or f.endswith(".wav"):
                files_to_upload.append(os.path.join(upload_dir, f))

    if not files_to_upload:
        print(f"[ERROR] upload 폴더({upload_dir})에서 음성 파일을 찾을 수 없습니다.")
        return None

    print(f"[INFO] 대표님의 고유 목소리 파일 {len(files_to_upload)}개를 발견했습니다:")
    for f in files_to_upload:
        print(f"  - {os.path.basename(f)}")

    print(f"\n[INFO] ElevenLabs Voice Cloning API를 호출하여 대표님 전용 보이스를 생성합니다...")
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {
        "xi-api-key": api_key
    }
    data = {
        "name": voice_name,
        "description": "VOICE.md 기반 8대 DNA를 승계한 대표님 고유 목소리 클론 (FISH_01~05 기반)",
        "labels": json.dumps({"accent": "Korean", "gender": "male", "age": "50s", "use_case": "lecture"})
    }

    # 다중 파일 멀티파트 업로드
    file_handles = []
    try:
        multipart_files = []
        for file_path in files_to_upload:
            fh = open(file_path, "rb")
            file_handles.append(fh)
            multipart_files.append(("files", (os.path.basename(file_path), fh, "audio/mpeg")))

        response = requests.post(url, headers=headers, data=data, files=multipart_files)

        if response.status_code == 200:
            res_json = response.json()
            voice_id = res_json.get("voice_id")
            print(f"\n[SUCCESS] 축하합니다! 대표님의 목소리 클론 모델이 성공적으로 생성되었습니다!")
            print(f"  - Voice Name : {voice_name}")
            print(f"  - Voice ID   : {voice_id}")

            # config.json에 자동 저장
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
            config = {
                "ELEVENLABS_API_KEY": api_key,
                "VOICE_ID": voice_id,
                "VOICE_NAME": voice_name,
                "MODEL_ID": "eleven_multilingual_v2"
            }
            with open(config_path, "w", encoding="utf-8") as cfg_file:
                json.dump(config, cfg_file, indent=2, ensure_ascii=False)
            print(f"[SAVED] 설정 정보가 config.json 에 영구 저장되었습니다.")
            return voice_id
        else:
            print(f"[ERROR] 보이스 클론 등록 실패 (코드: {response.status_code})")
            print(response.text)
            return None

    finally:
        for fh in file_handles:
            fh.close()


def main():
    parser = argparse.ArgumentParser(description="내 목소리(FISH_01~05) ElevenLabs 보이스 클론 생성기")
    parser.add_argument("--api-key", type=str, help="ElevenLabs API Key (기존에 발급받으신 키)")
    parser.add_argument("--name", type=str, default="Representative_Voice", help="생성할 보이스 이름")

    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        # 기존 config.json 확인
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                api_key = cfg.get("ELEVENLABS_API_KEY")

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("\n" + "="*70)
        print("[안내] ElevenLabs API 키가 필요합니다.")
        print("  1. https://elevenlabs.io 무료 가입 후 우측 상단 프로필 -> Profile + API Key 확인")
        print("  2. 실행 명령어:")
        print("     python src/create_clone_voice.py --api-key YOUR_API_KEY")
        print("="*70 + "\n")
        sys.exit(1)

    create_voice_clone(api_key, args.name)


if __name__ == "__main__":
    main()
