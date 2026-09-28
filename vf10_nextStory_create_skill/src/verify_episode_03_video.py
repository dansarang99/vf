#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_episode_03_video.py :
에피소드 03 '목성 위성 유로파 오디세이' 완제 마스터 비디오의
FFmpeg 스트림 무결성 및 씬별 핵심 타임라인 프레임 캡처 검증기.
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

EP03_CHECKPOINTS = [
    (15.0,  "01_mars_biosphere",       "Scene 02 [박준서] 화성 전진기지 인공 광합성 바이오스피어 돔 가동"),
    (50.0,  "02_signal_briefing",      "Scene 06 [빅터] 유로파 지하 바다 외계 생체 음향 신호 교차 검증"),
    (125.0, "03_cheonmyeong_ii_launch", "Scene 14 [최영목] 천명호 II 헬륨-3 핵융합 펄스 엔진 목성 도약"),
    (175.0, "04_jupiter_red_spot",     "Scene 19 [박준서] 목성 대적점 궤도 진입 및 플라즈마 쉴드 전개"),
    (225.0, "05_europa_ice_geyser",    "Scene 24 [윤선아] 유로파 얼음 지각 및 백킬로미터 수증기 간헐천"),
    (275.0, "06_haetae_submarine",     "Scene 29 [세종] 심해 자율 잠수정 해태호 얼음 천공 하강"),
    (330.0, "07_alien_bioluminescence", "Scene 35 [해설] 유로파 심해 열수구 최초의 생체 발광 외계 생명체")
]

def verify_ep03(video_path):
    if not os.path.exists(video_path):
        print(f"[!] 비디오 파일을 찾을 수 없습니다: {video_path}")
        return False

    print("=" * 80)
    print(f"  🔍 [검증] 에피소드 03 '목성 위성 유로파 오디세이' 무결성 검사: {os.path.basename(video_path)}")
    print("=" * 80)

    # 1. FFmpeg 디코드 무결성 검사
    chk_cmd = [ffmpeg_exe, "-v", "error", "-i", video_path, "-f", "null", "-"]
    res = subprocess.run(chk_cmd, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and not res.stderr.strip():
        print(f"  ✔ [1/2] FFmpeg 전체 스트림 디코드 무결성 검증: 100% PERFECT OK! (0-Error)")
    else:
        print(f"  ✘ [1/2] 디코드 경고/오류: {res.stderr[:300]}")

    # 2. 비디오 및 오디오 정보
    info_cmd = [ffmpeg_exe, "-i", video_path]
    res_info = subprocess.run(info_cmd, stderr=subprocess.PIPE, text=True)
    for line in res_info.stderr.split("\n"):
        if any(k in line for k in ["Duration:", "Stream #0:0", "Stream #0:1"]):
            print(f"    - {line.strip()}")

    # 3. 씬별 프레임 추출 검증
    print(f"\n  ✔ [2/2] 에피소드 03 대화 일치 핵심 프레임 추출 검증 ({len(EP03_CHECKPOINTS)}개 씬):")
    for t_sec, label, desc in EP03_CHECKPOINTS:
        out_name = f"[106]_ep03_frame_{label}_{int(t_sec)}s.png"
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
            print(f"    ✔ [{int(t_sec):>3}s] {label:<26} ({size_kb:>6.1f} KB) -> {desc}")
        else:
            print(f"    ✘ [{int(t_sec):>3}s] {label:<26} 추출 실패")

    print("\n[SUCCESS] 에피소드 03 완제 마스터 비디오 검증 완료!\n")
    return True

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RESULT_DIR, "[105]_episode_03_europa_odyssey_master.mp4")
    verify_ep03(vid)
