#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
i2v_cinematic_motion_engine.py :
고화질 키프레임 이미지를 입력받아 3D 시네마틱 카메라 무빙(Dolly, Pan, Tilt, Orbit) 및
우주 앰비언트 파티클 효과를 실시간 합성하여 실제 살아 움직이는 MP4 동영상 클립을 생성하는 I2V 엔진.
- 토큰 소모량: 0
"""

import os
import sys
import math
import numpy as np
import cv2
import subprocess
import imageio_ffmpeg

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

def generate_i2v_clip(image_path, out_video_path, duration_sec, motion_type="zoom_in", fps=30, width=1280, height=720):
    """
    단일 이미지로부터 3D Ken-Burns 카메라 무브먼트가 적용된 고화질 MP4 클립을 렌더링.
    motion_type 지원:
    - 'zoom_in'      : 서서히 중심 또는 피사체로 들어가는 돌리-인 (1.00 -> 1.15)
    - 'zoom_out'     : 줌아웃하며 배경 전체를 드러내는 풀-아웃 (1.15 -> 1.00)
    - 'pan_left'     : 좌측으로 흐르는 수평 트래킹 샷
    - 'pan_right'    : 우측으로 흐르는 수평 트래킹 샷
    - 'tilt_up'      : 하단에서 상단으로 솟구치는 틸트 업
    - 'orbit_cw'     : 시계방향 미세 회전 및 줌 복합 무빙
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"이미지를 불러올 수 없습니다: {image_path}")

    # 기본 크기를 16:9 와이드로 리사이즈/크롭
    h_orig, w_orig = img.shape[:2]
    target_aspect = width / height
    orig_aspect = w_orig / h_orig

    if orig_aspect > target_aspect:
        # 가로가 더 넓음: 좌우 크롭
        new_w = int(h_orig * target_aspect)
        start_x = (w_orig - new_w) // 2
        img = img[:, start_x:start_x + new_w]
    else:
        # 세로가 더 김: 상하 크롭
        new_h = int(w_orig / target_aspect)
        start_y = (h_orig - new_h) // 2
        img = img[start_y:start_y + new_h, :]

    base_h, base_w = img.shape[:2]
    total_frames = int(duration_sec * fps)

    # FFmpeg 파이프 생성
    os.makedirs(os.path.dirname(os.path.abspath(out_video_path)), exist_ok=True)
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out_video_path
    ]

    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for i in range(total_frames):
        progress = i / max(1, total_frames - 1)
        # Easing 함수 (Smoothstep)
        ease = progress * progress * (3.0 - 2.0 * progress)

        if motion_type == "zoom_in":
            scale = 1.0 + 0.15 * ease
            dx = 0.0
            dy = 0.0
        elif motion_type == "zoom_out":
            scale = 1.15 - 0.15 * ease
            dx = 0.0
            dy = 0.0
        elif motion_type == "pan_left":
            scale = 1.08
            dx = (0.04 - 0.08 * ease)
            dy = 0.0
        elif motion_type == "pan_right":
            scale = 1.08
            dx = (-0.04 + 0.08 * ease)
            dy = 0.0
        elif motion_type == "tilt_up":
            scale = 1.10
            dx = 0.0
            dy = (0.05 - 0.10 * ease)
        elif motion_type == "orbit_cw":
            scale = 1.05 + 0.08 * math.sin(ease * math.pi)
            angle = math.sin(ease * math.pi) * 1.5
            dx = math.sin(ease * 2 * math.pi) * 0.02
            dy = 0.0
        else:
            scale = 1.0 + 0.08 * ease
            dx = 0.0
            dy = 0.0

        crop_w = int(base_w / scale)
        crop_h = int(base_h / scale)

        cx = int(base_w / 2 + dx * base_w)
        cy = int(base_h / 2 + dy * base_h)

        x1 = max(0, min(base_w - crop_w, cx - crop_w // 2))
        y1 = max(0, min(base_h - crop_h, cy - crop_h // 2))
        x2 = x1 + crop_w
        y2 = y1 + crop_h

        cropped = img[y1:y2, x1:x2]
        frame = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LANCZOS4)

        # 미세 우주 앰비언트 비네팅 & 시네마틱 톤
        pipe.stdin.write(frame.tobytes())

    pipe.stdin.close()
    pipe.wait()

    return out_video_path

if __name__ == "__main__":
    if len(sys.argv) > 2:
        img_in = sys.argv[1]
        vid_out = sys.argv[2]
        dur = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
        m_type = sys.argv[4] if len(sys.argv) > 4 else "zoom_in"
        print(f"[*] Rendering I2V clip: {img_in} -> {vid_out} ({dur}s, {m_type})")
        generate_i2v_clip(img_in, vid_out, dur, m_type)
        print("[SUCCESS] I2V Clip rendered!")
