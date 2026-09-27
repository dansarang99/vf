#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_cinematic_mp4.py : 맑은고딕 폰트 기반 완벽한 한글 자막 켄번스 시네마틱 MP4 렌더러
- PIL (Pillow) ImageDraw를 통한 완벽한 한글 렌더링 (C:\Windows\Fonts\malgun.ttf)
- 씬별 미세 줌인(Ken-Burns) 모션 효과
- 넷플릭스 스타일 시네마틱 자막 바
- 복원된 오디오와 무손실 AAC 결합
- 출력: vf09_FullScene_VideoRemaker_skill/result/[206]_episode_01_scene_3287s_remake_master.mp4
"""

import os
import sys
import json
import cv2
import numpy as np
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

vf09_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vf08_dir = os.path.join(os.path.dirname(vf09_dir), "vf08_VOICE.md")
result_dir = os.path.join(vf09_dir, "result")
temp_dir = os.path.join(vf09_dir, "scratch", "mp4_tmp")
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 한글 폰트 로드 (Windows 맑은 고딕)
font_path = "C:\\Windows\\Fonts\\malgun.ttf"
font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
if not os.path.exists(font_bold_path):
    font_bold_path = font_path

font_title = ImageFont.truetype(font_bold_path, 28)
font_meta = ImageFont.truetype(font_path, 22)
font_badge = ImageFont.truetype(font_bold_path, 22)
font_sub = ImageFont.truetype(font_bold_path, 30)

# 54:40~56:10 하이라이트 씬 대본 로드
json_path = os.path.join(vf08_dir, "youtube_full_transcript.json")
with open(json_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

TARGET_START = 3280.0
TARGET_END = 3370.0

scenes = []
cur_text = ""
s_time = 0.0
e_time = 0.0

for d in raw_data:
    st = d["start"]
    dur = d["duration"]
    et = st + dur

    if TARGET_START <= st <= TARGET_END:
        text = d["text"].replace(">>", "").strip()
        if not cur_text:
            s_time = st
            cur_text = text
            e_time = et
        else:
            cur_text += " " + text
            e_time = et
            if cur_text.endswith(".") or cur_text.endswith("?") or (et - s_time > 4.5):
                scenes.append({
                    "start": s_time,
                    "end": e_time,
                    "duration": round(e_time - s_time, 2),
                    "text": cur_text
                })
                cur_text = ""

if cur_text:
    scenes.append({
        "start": s_time,
        "end": e_time,
        "duration": round(e_time - s_time, 2),
        "text": cur_text
    })

def get_char(t):
    if any(k in t for k in ["비행", "사원", "성원"]): return "동기 파일럿"
    if any(k in t for k in ["실력", "조작", "절차", "멘타", "전투기"]): return "교관 / 장군"
    if any(k in t for k in ["오빠", "만점", "첫 수업"]): return "여후배 조종사"
    if any(k in t for k in ["한심", "환국", "늦지"]): return "라이벌 경쟁자"
    if any(k in t for k in ["전생", "에이스", "괴롭혔다"]): return "주인공 (한성원)"
    return "해설 나레이터"

for sc in scenes:
    sc["char"] = get_char(sc["text"])

print(f"[INFO] 하이라이트 씬 총 {len(scenes)}개 한글 자막 렌더링 시작...")

width, height = 1280, 720
fps = 30
silent_video = os.path.join(temp_dir, "silent_video.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(silent_video, fourcc, fps, (width, height))

THEME_COLORS = [
    (24, 30, 40), (32, 28, 42), (25, 38, 32), (40, 32, 22),
    (30, 24, 36), (22, 35, 40), (38, 25, 25), (26, 32, 42)
]

for idx, sc in enumerate(scenes, 1):
    dur = max(0.5, sc["duration"])
    total_frames = int(dur * fps)
    char_name = sc["char"]
    text = sc["text"]
    
    theme = THEME_COLORS[idx % len(THEME_COLORS)]
    
    # 기본 카드 템플릿 PIL 생성
    m_s = int(sc["start"]) // 60
    s_s = int(sc["start"]) % 60
    m_e = int(sc["end"]) // 60
    s_e = int(sc["end"]) % 60
    time_tag = f"[{m_s:02d}:{s_s:02d} ~ {m_e:02d}:{s_e:02d}]"

    for f in range(total_frames):
        # 1. OpenCV 캔버스 생성
        frame_cv = np.zeros((height, width, 3), dtype=np.uint8)
        frame_cv[:] = theme

        progress = f / max(1, total_frames)
        zoom = 1.0 + (0.035 * progress)
        
        # 중앙 카드 프레임
        pad_x = int(60 * zoom)
        pad_y = int(45 * zoom)
        cv2.rectangle(frame_cv, (pad_x, pad_y), (width - pad_x, height - 160), (16, 20, 26), -1)
        cv2.rectangle(frame_cv, (pad_x, pad_y), (width - pad_x, height - 160), (70, 110, 150), 2)

        # 시네마틱 레이더 그리드
        center_x, center_y = width // 2, (height - 160) // 2 + 30
        cv2.circle(frame_cv, (center_x, center_y), int(120 * zoom), (30, 45, 60), 1)
        cv2.circle(frame_cv, (center_x, center_y), int(60 * zoom), (30, 45, 60), 1)
        cv2.line(frame_cv, (center_x - 140, center_y), (center_x + 140, center_y), (30, 45, 60), 1)
        cv2.line(frame_cv, (center_x, center_y - 140), (center_x, center_y + 140), (30, 45, 60), 1)

        # 하단 자막 바
        cv2.rectangle(frame_cv, (0, height - 140), (width, height), (8, 8, 12), -1)
        cv2.line(frame_cv, (0, height - 140), (width, height - 140), (220, 160, 0), 2)

        # 배역 뱃지 배경
        cv2.rectangle(frame_cv, (60, height - 128), (240, height - 90), (0, 100, 180), -1)

        # 2. PIL로 변환하여 맑은고딕 한글 텍스트 완벽 각인
        img_pil = Image.fromarray(cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # 상단 메타데이터 한글
        draw.text((pad_x + 30, pad_y + 25), "FULL-SCENE VIDEO REMAKER : FLIGHT ACE CRISIS", font=font_meta, fill=(160, 170, 185))
        draw.text((pad_x + 30, pad_y + 65), f"SCENE #{idx:03d}   {time_tag}   (지속: {dur}초)", font=font_title, fill=(0, 220, 255))
        draw.text((pad_x + 30, pad_y + 115), f"배역: [{char_name}]", font=font_meta, fill=(255, 190, 0))

        # 하단 배역 뱃지 텍스트
        draw.text((75, height - 122), char_name, font=font_badge, fill=(255, 255, 255))

        # 하단 대사 자막 한글 (그림자 효과 포함)
        sub_text = text[:45] + ("..." if len(text) > 45 else "")
        draw.text((62, height - 58), sub_text, font=font_sub, fill=(0, 0, 0)) # 그림자
        draw.text((60, height - 60), sub_text, font=font_sub, fill=(255, 255, 255)) # 본문

        # 다시 OpenCV 형식으로 변환하여 프레임 기록
        frame_out = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        video_writer.write(frame_out)

video_writer.release()
print(f"[SUCCESS] 무음 비디오 트랙 렌더링 완료 ({silent_video})")

# 오디오 트랙 결합
audio_path = os.path.join(vf08_dir, "result", "[017]_episode_01_scene_3287s_speed_matched_voice.mp3")
final_mp4 = os.path.join(result_dir, "[206]_episode_01_scene_3287s_remake_master.mp4")

cmd = [
    ffmpeg_exe, "-y",
    "-i", silent_video,
    "-i", audio_path,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_mp4
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if res.returncode == 0:
    mp4_mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print("\n" + "="*70)
    print("★ [206] 맑은고딕 한글 자막 시네마틱 완제 MP4 비디오 렌더링 성공!")
    print(f"  - 출력 경로 : {final_mp4}")
    print(f"  - 비디오 크기 : {mp4_mb:.2f} MB")
    print(f"  - 해상도 : 1280x720 (HD 720p 30fps)")
    print("="*70 + "\n")
    try: os.remove(silent_video)
    except: pass
else:
    print(f"[ERROR] ffmpeg 결합 실패: {res.stderr.decode('utf-8', errors='ignore')}")
