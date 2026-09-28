# -*- coding: utf-8 -*-
"""
NASA Images API(무료/인증 불필요 오픈 API)를 통해 100% 실제 우주 촬영 실사 사진을
자동 검색 및 720x1280 시네마틱 규격으로 다운로드·크롭하는 고신뢰 실사 파이프라인
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageOps

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL_DIR = os.path.join(VF10_DIR, "scratch", "real_footage")
os.makedirs(REAL_DIR, exist_ok=True)

TARGET_QUERIES = [
    ("01_naro_launchpad.png", "rocket launch pad gantry space center"),
    ("02_liftoff_flame.png", "rocket liftoff engine flame night launch"),
    ("04_tli_nebula.png", "hubble deep space nebula stars galaxy"),
    ("05_debris_avoidance.png", "asteroid surface close-up space"),
    ("08_lunar_surface_korea.png", "apollo lunar rover moon surface astronaut"),
    ("09_solar_flare_crisis.png", "sun solar flare sdo coronal mass ejection"),
]

def fetch_nasa_image(target_name, query, width=720, height=1280):
    dest_path = os.path.join(REAL_DIR, target_name)
    temp_path = os.path.join(REAL_DIR, "_temp_" + target_name + ".jpg")
    print(f"[*] NASA 실제 사진 검색 중: '{query}' -> {target_name}...")

    search_url = f"https://images-api.nasa.gov/search?q={urllib.parse.quote(query)}&media_type=image"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        items = data.get("collection", {}).get("items", [])
        if not items:
            print(f"    [INFO] 검색 결과 없음: {query}")
            return False

        # 첫 번째 유효 이미지 링크 탐색
        img_url = None
        for item in items[:5]:
            links = item.get("links", [])
            for link in links:
                if link.get("render") == "image" or link.get("href", "").endswith((".jpg", ".png")):
                    img_url = link.get("href")
                    break
            if img_url:
                break

        if not img_url:
            print("    [INFO] 이미지 URL 없음")
            return False

        print(f"    -> 다운로드: {img_url}")
        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(img_req, timeout=12) as img_resp, open(temp_path, "wb") as f:
            f.write(img_resp.read())

        with Image.open(temp_path) as img:
            fitted = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            fitted.save(dest_path, "PNG", quality=95)

        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"    [SUCCESS] NASA 실제 촬영 실사 에셋 장착 완료: {target_name}")
        return True
    except Exception as e:
        print(f"    [INFO] 검색/다운로드 오류: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def main():
    print("=" * 70)
    print("  NASA Images Open API 기반 100% 실제 우주 촬영 실사 에셋 완제 파이프라인")
    print("=" * 70)
    for fname, q in TARGET_QUERIES:
        fetch_nasa_image(fname, q)

if __name__ == "__main__":
    main()
