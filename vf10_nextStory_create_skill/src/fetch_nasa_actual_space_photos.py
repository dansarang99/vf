# -*- coding: utf-8 -*-
"""
fetch_nasa_actual_space_photos.py :
NASA 및 공인 우주 아카이브의 실제 촬영 사진(Actual Real Photography)을 수집하여
720x1280 시네마틱 규격으로 정밀 매핑하는 엔진 (토큰 소모량: 0)
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

# Wikimedia / NASA 실제 공개 고해상도 실사 사진 URL (Wikimedia Commons Public Domain / NASA)
ACTUAL_PHOTOS = [
    # 01: 발사대 (NASA 케네디 우주센터 SLS 실제 발사대 실사)
    ("01_naro_launchpad.png", "https://images-assets.nasa.gov/image/KSC-20220317-PH-KLS01_0003/KSC-20220317-PH-KLS01_0003~medium.jpg"),
    # 02: 엔진 점화 화염 (SLS Artemis 1 실제 리프트오프 화염 실사)
    ("02_liftoff_flame.png", "https://images-assets.nasa.gov/image/KSC-20221116-PH-FGE01_0001/KSC-20221116-PH-FGE01_0001~medium.jpg"),
    # 03: 지구 저궤도 (ISS 실제 지구 지평선 촬영 실사)
    ("03_earth_orbit.png", "https://images-assets.nasa.gov/image/iss064e007861/iss064e007861~medium.jpg"),
    # 04: 심우주 성운 (허블/제임스웹 오리온 성운 실제 천체 관측 실사)
    ("04_tli_nebula.png", "https://images-assets.nasa.gov/image/PIA04224/PIA04224~medium.jpg"),
    # 05: 소행성 및 우주 파편 (베누/류구 실제 소행성 근접 촬영 실사)
    ("05_debris_avoidance.png", "https://images-assets.nasa.gov/image/PIA23447/PIA23447~medium.jpg"),
    # 06: 달 궤도 분화구 (아폴로 11호 실제 달 궤도 크레이터 촬영 실사)
    ("06_lunar_orbit.png", "https://images-assets.nasa.gov/image/as11-44-6667/as11-44-6667~medium.jpg"),
    # 07: 달 착륙 (아폴로 15호 실제 달 표면 착륙선 실사)
    ("07_shackleton_landing.png", "https://images-assets.nasa.gov/image/as15-88-11866/as15-88-11866~medium.jpg"),
    # 08: 달 표면 탐사 로버 (아폴로 16호 실제 월면차 Lunar Rover 실사)
    ("08_lunar_surface_korea.png", "https://images-assets.nasa.gov/image/as16-107-17520/as16-107-17520~medium.jpg"),
    # 09: 태양 플레어 (NASA SDO 위성 실제 태양 플레어 폭발 실사)
    ("09_solar_flare_crisis.png", "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000438/GSFC_20171208_Archive_e000438~medium.jpg"),
    # 10: 화성 실제 지평선 (퍼시비어런스 로버 실제 화성 Jezero 크레이터 파노라마 실사)
    ("10_towards_mars.png", "https://images-assets.nasa.gov/image/PIA24424/PIA24424~medium.jpg"),
]

def download_and_fit(target_name, url, width=720, height=1280):
    dest_path = os.path.join(REAL_DIR, target_name)
    temp_path = os.path.join(REAL_DIR, "_temp_" + target_name + ".jpg")
    print(f"[*] 실제 NASA 아카이브 실사 다운로드 중: {target_name}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as response, open(temp_path, 'wb') as out_file:
            out_file.write(response.read())

        # 720x1280 세로 규격으로 고화질 스마트 크롭
        with Image.open(temp_path) as img:
            fitted = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            fitted.save(dest_path, "PNG", quality=95)

        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"    -> [SUCCESS] 100% 실제 우주 촬영 실사 장착 완료! ({os.path.basename(dest_path)})")
        return True
    except Exception as e:
        print(f"    -> [INFO] 다운로드 건너뜀 또는 유지: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def main():
    print("=" * 70)
    print("  NASA 및 공인 우주기관 실제 100% 촬영 실사(Actual Footage) 에셋 파이프라인")
    print("=" * 70)
    success_count = 0
    for fname, url in ACTUAL_PHOTOS:
        if download_and_fit(fname, url):
            success_count += 1
    print(f"\n[DONE] 총 {success_count}/{len(ACTUAL_PHOTOS)}개 실제 우주 촬영 실사 에셋이 매핑되었습니다.")

if __name__ == "__main__":
    main()
