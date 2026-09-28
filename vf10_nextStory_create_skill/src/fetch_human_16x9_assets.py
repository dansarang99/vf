# -*- coding: utf-8 -*-
"""
fetch_human_16x9_assets.py :
16:9 와이드스크린(1280x720) 규격의 실제 사람(우주비행사, 콕핏 조종사, 지상 관제센터 요원, 엔지니어)
실사 사진을 NASA Open API에서 자동 수집 및 16:9 스마트 크롭하는 엔진 (토큰 소모량: 0)
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
SCRATCH_DIR = os.path.join(VF10_DIR, "scratch")
HUMAN_16X9_DIR = os.path.join(SCRATCH_DIR, "human_16x9_footage")
os.makedirs(HUMAN_16X9_DIR, exist_ok=True)

TARGET_HUMAN_QUERIES = [
    # 01: 관제센터 요원 & 디렉터
    ("human_01_mission_control.png", "flight controllers mission control center briefing"),
    # 02: 발사대 콘솔 엔지니어들
    ("human_02_launch_engineers.png", "launch control room engineers firing room"),
    # 03: 콕핏 우주복 사령관
    ("human_03_commander_cockpit.png", "astronaut in cockpit space shuttle commander"),
    # 04: 조종석 부조종사
    ("human_04_copilot_operations.png", "astronaut flight deck controls cockpit"),
    # 05: 선외 우주유영 비행사
    ("human_05_spacewalk_eva.png", "astronaut spacewalk earth background iss eva"),
    # 06: 달 궤도 창밖 응시 비행사
    ("human_06_lunar_observer.png", "astronaut look out window earth moon cupola"),
    # 07: 달 표면 착륙 우주비행사
    ("human_07_lunar_surface.png", "astronaut moon surface apollo flag lunar"),
    # 08: 월면 로버 탑승 비행사
    ("human_08_rover_astronaut.png", "astronaut driving lunar rover moon surface"),
    # 09: 관제소 환호와 축하
    ("human_09_celebration.png", "mission control celebration applause success"),
    # 10: 헬멧 바이저 얼굴 클로즈업
    ("human_10_visor_portrait.png", "astronaut helmet visor reflection space exploration"),
]

def fetch_and_crop_16x9(filename, query, width=1280, height=720):
    dest_path = os.path.join(HUMAN_16X9_DIR, filename)
    temp_path = os.path.join(HUMAN_16X9_DIR, "_temp_" + filename + ".jpg")
    print(f"[*] [16:9 사람 실사] 검색 중: '{query}' -> {filename}...")

    search_url = f"https://images-api.nasa.gov/search?q={urllib.parse.quote(query)}&media_type=image"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        items = data.get("collection", {}).get("items", [])
        if not items:
            print(f"    [INFO] 결과 없음: {query}")
            return False

        img_url = None
        for item in items[:6]:
            links = item.get("links", [])
            for link in links:
                if link.get("render") == "image" or link.get("href", "").endswith((".jpg", ".png")):
                    img_url = link.get("href")
                    break
            if img_url:
                break

        if not img_url:
            print("    [INFO] 이미지 링크 없음")
            return False

        print(f"    -> 다운로드 URL: {img_url}")
        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(img_req, timeout=15) as img_resp, open(temp_path, "wb") as f:
            f.write(img_resp.read())

        # 16:9 (1280x720) 스마트 고화질 와이드 크롭
        with Image.open(temp_path) as img:
            fitted = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            fitted.save(dest_path, "PNG", quality=95)

        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"    [SUCCESS] 16:9 사람 실사 에셋 장착 완료: {filename} ({width}x{height})")
        return True
    except Exception as e:
        print(f"    [INFO] 오류 발생: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def main():
    print("=" * 75)
    print("  [vf10] 16:9 와이드스크린 실제 사람(인물/비행사/관제사) 실사 에셋 수집 파이프라인")
    print("  ★ 규격: 1280 x 720 (16:9 Cinematic Widescreen) / 토큰 소모량: 0")
    print("=" * 75)

    success_cnt = 0
    for fname, q in TARGET_HUMAN_QUERIES:
        if fetch_and_crop_16x9(fname, q):
            success_cnt += 1

    print("\n" + "=" * 75)
    print(f"[DONE] 총 {success_cnt}/{len(TARGET_HUMAN_QUERIES)}개 16:9 사람 실사 에셋 수집 완료!")
    print(f"       저장 경로: {HUMAN_16X9_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    main()
