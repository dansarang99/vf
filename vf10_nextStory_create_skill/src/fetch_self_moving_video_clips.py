# -*- coding: utf-8 -*-
"""
fetch_self_moving_video_clips.py :
NASA Video Open API에서 실제 움직이는 고화질 MP4 비디오 클립(Moving Video Footage)들을
로컬 디스크(scratch/moving_video_clips/)로 자동 다운로드하는 하이브리드 비디오 수집기
- 토큰 소모량: 0
"""

import os
import sys
import json
import urllib.request
import urllib.parse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH_DIR = os.path.join(VF10_DIR, "scratch")
CLIPS_DIR = os.path.join(SCRATCH_DIR, "moving_video_clips")
os.makedirs(CLIPS_DIR, exist_ok=True)

TARGET_VIDEO_QUERIES = [
    ("video_01_rocket_launch.mp4", "rocket launch slow motion"),
    ("video_02_mission_control.mp4", "mission control center flight controllers"),
    ("video_03_earth_orbit_iss.mp4", "earth view orbit timelapses space station"),
    ("video_04_spacewalk_eva.mp4", "spacewalk astronaut outside iss"),
    ("video_05_lunar_surface.mp4", "apollo lunar surface moon landing"),
    ("video_06_mars_rover.mp4", "mars rover driving landing"),
]

def fetch_moving_video(dest_filename, query):
    dest_path = os.path.join(CLIPS_DIR, dest_filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100 * 1024:
        print(f"[*] 이미 존재하는 실제 비디오 클립 유지: {dest_filename} ({os.path.getsize(dest_path)/1024:.1f} KB)")
        return True

    print(f"\n[*] NASA 실제 동영상(MP4) 검색 중: '{query}' -> {dest_filename}...")
    search_url = f"https://images-api.nasa.gov/search?q={urllib.parse.quote(query)}&media_type=video"

    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        items = data.get("collection", {}).get("items", [])
        if not items:
            print(f"    [INFO] 비디오 검색 결과 없음: {query}")
            return False

        # 비디오 컬렉션 JSON 조회
        mp4_url = None
        for item in items[:5]:
            col_url = item.get("href")
            try:
                col_req = urllib.request.Request(col_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(col_req, timeout=10) as c_resp:
                    asset_links = json.loads(c_resp.read().decode('utf-8'))
                
                # 우선순위: medium.mp4 -> mobile.mp4 -> orig.mp4
                medium_links = [l for l in asset_links if "medium.mp4" in l]
                mobile_links = [l for l in asset_links if "mobile.mp4" in l]
                orig_links = [l for l in asset_links if l.endswith(".mp4")]

                if medium_links:
                    mp4_url = medium_links[0]
                elif mobile_links:
                    mp4_url = mobile_links[0]
                elif orig_links:
                    mp4_url = orig_links[0]

                if mp4_url:
                    break
            except Exception:
                continue

        if not mp4_url:
            print("    [INFO] MP4 다운로드 링크를 찾을 수 없음")
            return False

        # http -> https 치환
        mp4_url = mp4_url.replace("http://", "https://")
        print(f"    -> 실제 MP4 다운로드 시작: {mp4_url}")

        tmp_dest = dest_path + ".tmp"
        dl_req = urllib.request.Request(mp4_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(dl_req, timeout=30) as dl_resp, open(tmp_dest, "wb") as out_f:
            out_f.write(dl_resp.read())

        if os.path.exists(dest_path):
            os.remove(dest_path)
        os.rename(tmp_dest, dest_path)

        size_mb = round(os.path.getsize(dest_path) / (1024 * 1024), 2)
        print(f"    [SUCCESS] 실제 움직이는 비디오 클립 수집 완료: {dest_filename} ({size_mb} MB)")
        return True
    except Exception as e:
        print(f"    [ERROR] 비디오 다운로드 실패: {e}")
        return False

def main():
    print("=" * 75)
    print("  [vf10] NASA Video Open API 100% 실제 움직이는 비디오(Moving Video) 수집 엔진")
    print("  ★ 정지화면 0% 완전 박멸 / 실제 우주 비디오 스트림 구축")
    print("=" * 75)

    success_cnt = 0
    for fname, q in TARGET_VIDEO_QUERIES:
        if fetch_moving_video(fname, q):
            success_cnt += 1

    print("\n" + "=" * 75)
    print(f"[DONE] 총 {success_cnt}/{len(TARGET_VIDEO_QUERIES)}개 실제 움직이는 MP4 비디오 클립 준비 완료!")
    print(f"       저장 경로: {CLIPS_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    main()
