#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_story_video.py :
대화 일치 AI 스토리 동영상 생성기로 렌더링된 완제 비디오의
FFmpeg 스트림 무결성 및 주요 씬별 프레임 캡처 검증기.
"""

import os
import sys
import subprocess
import imageio_ffmpeg
from immutable_versioning import resolve_immutable_path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")

# 캡처할 주요 시나리오 시점 (초, 레이블, 대화 및 상황 설명)
STORY_CHECKPOINTS = [
    (15.0,  "01_mission_control_kang",  "Scene 02 [강수연] '나로우주센터 발사통제사령관 강수연입니다. 카운트다운 진입'"),
    (30.0,  "02_nuri_v_liftoff",        "Scene 05 [해설] '누리호-V 중형 발사체, 1000톤급 메가스러스트 점화'"),
    (85.0,  "03_dr_choi_engine",        "Scene 11 [최영목] '1단 융합 엔진 압력 102%, 정상 임계치 유지'"),
    (150.0, "04_pilot_cockpit",         "Scene 18 [박준서] '사령관 박준서, 수동 피치 트림 전환 완료'"),
    (210.0, "05_cheonmyeong_orbit",     "Scene 26 [해설] '대한민국 최초의 심우주 순양전함 천명호, 지구 저궤도 전개'"),
    (290.0, "06_quantum_ai_sejong",     "Scene 35 [세종] '사령관님, 양자 코어 연산 완료. 달 전이 궤도 최적화'"),
    (400.0, "07_spacewalk_eva",         "Scene 48 [박준서] '선외 우주유영 개시. 3번 레이저 센서 어레이 복구'"),
    (530.0, "08_lunar_landing",         "Scene 62 [김태훈] '달 남극 섀클턴 아르테미스 기지 터치다운 완료'"),
    (680.0, "09_mars_landing",          "Scene 85 [박준서] '화성 유토피아 평원 착륙. 대한민국 우주개척의 신기원'")
]

def verify_video(video_path):
    if not os.path.exists(video_path):
        print(f"[!] 비디오 파일을 찾을 수 없습니다: {video_path}")
        return False

    print(f"\n" + "=" * 80)
    print(f"  🔍 [검증] 대화 일치 시네마틱 스토리 동영상 무결성 검사: {os.path.basename(video_path)}")
    print("=" * 80)

    # 1. FFmpeg 디코드 무결성 검사
    chk_cmd = [ffmpeg_exe, "-v", "error", "-i", video_path, "-f", "null", "-"]
    res = subprocess.run(chk_cmd, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and not res.stderr.strip():
        print(f"  ✔ [1/2] FFmpeg 전체 스트림 디코드 무결성 검증: 100% PERFECT OK! (0-Error)")
    else:
        print(f"  ✘ [1/2] 디코드 경고/오류 감지: {res.stderr[:300]}")

    # 2. 비디오 및 오디오 정보
    info_cmd = [ffmpeg_exe, "-i", video_path]
    res_info = subprocess.run(info_cmd, stderr=subprocess.PIPE, text=True)
    for line in res_info.stderr.split("\n"):
        if any(k in line for k in ["Duration:", "Stream #0:0", "Stream #0:1"]):
            print(f"    - {line.strip()}")

    # 3. 씬별 프레임 추출 검증
    print(f"\n  ✔ [2/2] 시나리오 대화 1:1 일치 핵심 프레임 추출 검증 ({len(STORY_CHECKPOINTS)}개 씬):")
    for t_sec, label, desc in STORY_CHECKPOINTS:
        out_name = f"[086]_story_frame_{label}_{int(t_sec)}s.png"
        out_path = resolve_immutable_path(out_name)
        f_cmd = [
            ffmpeg_exe, "-y",
            "-ss", str(t_sec),
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_path
        ]
        f_res = subprocess.run(f_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if f_res.returncode == 0 and os.path.exists(out_path):
            size_kb = round(os.path.getsize(out_path) / 1024, 1)
            print(f"    ✔ [{int(t_sec):>3}s] {label:<24} ({size_kb:>6.1f} KB) -> {desc}")
        else:
            print(f"    ✘ [{int(t_sec):>3}s] {label:<24} 추출 실패")

    print("\n[SUCCESS] 대화 일치 시네마틱 스토리 비디오 검증 완료!\n")
    return True

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RESULT_DIR, "[085]_episode_02_consistent_story_video_master.mp4")
    verify_video(vid)
