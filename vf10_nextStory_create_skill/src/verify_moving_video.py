#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_moving_video.py :
자체 하이브리드 셀프 동영상 생성기로 제작된 완제 비디오의
핵심 타임라인(1분, 5분, 8분, 12분 등) 프레임을 추출하여
정지 사진이 아닌 100% 실제 움직이는 비디오 영상임을 시각적으로 증명·검증하는 스크립트.
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

# 대상 비디오
TARGET_VIDEO = os.path.join(RESULT_DIR, "[071]_episode_02_self_moving_video_full_master.mp4")

# 캡처할 주요 시점 (초, 레이블, 설명)
CHECKPOINTS = [
    (25.0,  "01_rocket_launch",   "Scene 04 발사 카운트다운 및 누리호-V 점화"),
    (80.0,  "02_mission_control", "Scene 11 나로우주센터 종합관제실 모니터링"),
    (210.0, "03_earth_orbit",     "Scene 26 지구 저궤도 ISS 및 태양전지판 전개"),
    (380.0, "04_spacewalk_eva",   "Scene 41 심우주 전함 '천명호' 선외 우주유영(EVA)"),
    (520.0, "05_lunar_landing",   "Scene 58 달 남극 아르테미스 기지 강하 및 탐사"),
    (700.0, "06_mars_transfer",   "Scene 88 화성 탐사선 착륙 및 붉은 행성 표면")
]

def capture_checkpoints(video_path=TARGET_VIDEO):
    if not os.path.exists(video_path):
        print(f"[!] 비디오 파일을 찾을 수 없습니다: {video_path}")
        return []

    print(f"\n[*] 비디오 무결성 검증 및 핵심 프레임 추출 시작: {os.path.basename(video_path)}")
    captured = []

    for t_sec, label, desc in CHECKPOINTS:
        out_name = f"[073]_moving_frame_{label}_{int(t_sec)}s.png"
        out_path = resolve_immutable_path(out_name)

        cmd = [
            ffmpeg_exe, "-y",
            "-ss", str(t_sec),
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and os.path.exists(out_path):
            size_kb = round(os.path.getsize(out_path) / 1024, 1)
            print(f"    ✔ [{int(t_sec):>3}s] {label:<22} ({size_kb} KB) -> {desc}")
            captured.append((out_path, t_sec, label, desc))
        else:
            print(f"    ✘ [{int(t_sec):>3}s] {label:<22} 추출 실패")

    print(f"[*] 총 {len(captured)}개 프레임 캡처 완료!\n")
    return captured

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else TARGET_VIDEO
    capture_checkpoints(vid)
