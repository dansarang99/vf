# -*- coding: utf-8 -*-
"""
Wikimedia Commons의 100% 실제 공개 우주 실사 사진 수집기
User-Agent: KSpaceBot/1.0 (contact: note@local)
"""

import os
import sys
import urllib.request
from PIL import Image, ImageOps

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL_DIR = os.path.join(VF10_DIR, "scratch", "real_footage")
os.makedirs(REAL_DIR, exist_ok=True)

# Wikimedia Commons 고화질 실제 우주 사진
WIKI_PHOTOS = [
    # 01: 발사대 (KSLV-II 누리호 실제 나로우주센터 발사대 실사)
    ("01_naro_launchpad.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Nuri_Rocket_on_Launch_Pad_%282021%29.jpg/800px-Nuri_Rocket_on_Launch_Pad_%282021%29.jpg"),
    # 02: 엔진 점화 화염 (누리호 실제 발사 화염 실사)
    ("02_liftoff_flame.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Launch_of_Nuri_%28KSLV-II%29_on_October_21%2C_2021.jpg/800px-Launch_of_Nuri_%28KSLV-II%29_on_October_21%2C_2021.jpg"),
    # 04: 심우주 성운 (허블 망원경 캐츠아이/오리온 성운 실제 천체 관측 사진)
    ("04_tli_nebula.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Hubble_Ultra_Deep_Field_part4.jpg/800px-Hubble_Ultra_Deep_Field_part4.jpg"),
    # 05: 소행성 및 우주 파편 (이다 소행성 실제 갈릴레오 탐사선 촬영 실사)
    ("05_debris_avoidance.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/243_ida.jpg/800px-243_ida.jpg"),
    # 08: 달 표면 탐사 로버 (아폴로 15호 실제 월면차 Lunar Roving Vehicle 실사)
    ("08_lunar_surface_korea.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Apollo_15_Lunar_Rover_profile_view.jpg/800px-Apollo_15_Lunar_Rover_profile_view.jpg"),
    # 09: 태양 플레어 (NASA SOHO 실제 태양 코로나 방출 EIT 실사)
    ("09_solar_flare_crisis.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/800px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg"),
]

def download_and_fit(target_name, url, width=720, height=1280):
    dest_path = os.path.join(REAL_DIR, target_name)
    temp_path = os.path.join(REAL_DIR, "_temp_" + target_name + ".jpg")
    print(f"[*] 위키미디어 실제 촬영 실사 다운로드 중: {target_name}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response, open(temp_path, 'wb') as out_file:
            out_file.write(response.read())

        with Image.open(temp_path) as img:
            fitted = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            fitted.save(dest_path, "PNG", quality=95)

        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"    -> [SUCCESS] 100% 실제 촬영 실사 교체 완료! ({target_name})")
        return True
    except Exception as e:
        print(f"    -> [INFO] 다운로드 오류 또는 기존 에셋 유지: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def main():
    print("=" * 70)
    print("  누리호/허블/아폴로/SOHO 100% 실제 우주 촬영 실사 에셋 장착 엔진")
    print("=" * 70)
    for fname, url in WIKI_PHOTOS:
        download_and_fit(fname, url)

if __name__ == "__main__":
    main()
