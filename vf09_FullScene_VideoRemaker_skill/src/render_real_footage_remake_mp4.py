#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_real_footage_remake_mp4.py
- 원본 유튜브 실제 영상(Real Captured Footage) 프레임 100% 탑재
- 슬로우모션 왜곡 없는 자연스럽고 빠른 실전 보이스 스피드 (rate +3% ~ +8%)
- 맑은고딕 볼드 자막 및 10대 배역 뱃지 오버레이
- 정확한 타임라인 동기화 (초단위 무음 간격 배치)
- 결과물: vf09_FullScene_VideoRemaker_skill/result/[206]_episode_01_scene_3287s_remake_master.mp4
"""

import os
import sys
import json
import asyncio
import cv2
import numpy as np
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import edge_tts
import time

vf09_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vf08_dir = os.path.join(os.path.dirname(vf09_dir), "vf08_VOICE.md")
result_dir = os.path.join(vf09_dir, "result")
scratch_dir = os.path.join(vf09_dir, "scratch")
temp_dir = os.path.join(scratch_dir, "footage_tmp")
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
raw_video_path = os.path.join(scratch_dir, "raw_clip_3287s.mp4")

# 1. 폰트 세팅
font_path = "C:\\Windows\\Fonts\\malgun.ttf"
font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
if not os.path.exists(font_bold_path):
    font_bold_path = font_path

font_sub = ImageFont.truetype(font_bold_path, 32)
font_badge = ImageFont.truetype(font_bold_path, 22)
font_tag = ImageFont.truetype(font_path, 20)

# 2. 54:40~56:15 구간 자막 데이터 로드
json_path = os.path.join(vf08_dir, "youtube_full_transcript.json")
with open(json_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CLIP_START_OFFSET = 3280.0
CLIP_END_OFFSET = 3375.0

# 씬 묶기
scenes = []
cur_text = ""
s_time = 0.0
e_time = 0.0

for d in raw_data:
    st = d["start"]
    dur = d["duration"]
    et = st + dur

    if CLIP_START_OFFSET <= st <= CLIP_END_OFFSET:
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
                    "clip_start": max(0.0, s_time - CLIP_START_OFFSET),
                    "clip_end": min(CLIP_END_OFFSET - CLIP_START_OFFSET, e_time - CLIP_START_OFFSET),
                    "text": cur_text
                })
                cur_text = ""

if cur_text:
    scenes.append({
        "start": s_time,
        "end": e_time,
        "clip_start": max(0.0, s_time - CLIP_START_OFFSET),
        "clip_end": min(CLIP_END_OFFSET - CLIP_START_OFFSET, e_time - CLIP_START_OFFSET),
        "text": cur_text
    })

# 배역 배정
def get_char(t):
    if any(k in t for k in ["비행", "사원", "성원"]): return ("동기 파일럿", (60, 160, 240))
    if any(k in t for k in ["실력", "조작", "절차", "멘타", "전투기"]): return ("교관 / 장군", (220, 70, 70))
    if any(k in t for k in ["오빠", "만점", "첫 수업"]): return ("여후배 조종사", (240, 130, 180))
    if any(k in t for k in ["한심", "환국", "늦지"]): return ("라이벌 경쟁자", (230, 160, 40))
    if any(k in t for k in ["전생", "에이스", "괴롭혔다"]): return ("주인공 (한성원)", (50, 205, 120))
    return ("해설 나레이터", (180, 180, 180))

# 자연스러운 보이스 세팅 (절대 느리게 끌지 않음: rate +3% ~ +8%)
CHAR_VOICE_CFG = {
    "해설 나레이터": {"voice": "ko-KR-InJoonNeural", "rate": "+6%", "pitch": "-1Hz"},
    "주인공 (한성원)": {"voice": "ko-KR-HyunsuNeural", "rate": "+8%", "pitch": "+1Hz"},
    "동기 파일럿": {"voice": "ko-KR-HyunsuNeural", "rate": "+7%", "pitch": "+4Hz"},
    "교관 / 장군": {"voice": "ko-KR-InJoonNeural", "rate": "+4%", "pitch": "-5Hz"},
    "여후배 조종사": {"voice": "ko-KR-SunHiNeural", "rate": "+5%", "pitch": "+2Hz"},
    "라이벌 경쟁자": {"voice": "ko-KR-InJoonNeural", "rate": "+6%", "pitch": "-2Hz"},
}

for sc in scenes:
    char_name, color = get_char(sc["text"])
    sc["char"] = char_name
    sc["color"] = color

print(f"[INFO] 타겟 구간 총 {len(scenes)}개 씬 구성 완료. 상영시간: {CLIP_START_OFFSET}s ~ {CLIP_END_OFFSET}s")

# 3. 보이스 합성 (자연스럽고 빠른 스피드로 사전 렌더링)
async def synthesize_all():
    print("[RUN] 자연스러운 스피드 multi-char 보이스 합성 중...")
    for idx, sc in enumerate(scenes):
        seg_file = os.path.join(temp_dir, f"voice_{idx:03d}.mp3")
        sc["audio_file"] = seg_file
        cfg = CHAR_VOICE_CFG.get(sc["char"], {"voice": "ko-KR-InJoonNeural", "rate": "+6%", "pitch": "+0Hz"})
        
        comm = edge_tts.Communicate(
            text=sc["text"],
            voice=cfg["voice"],
            rate=cfg["rate"],
            pitch=cfg["pitch"]
        )
        await comm.save(seg_file)
    print("[SUCCESS] 모든 씬 보이스 합성 완료!")

asyncio.run(synthesize_all())

# 4. ffmpeg을 통해 전체 오디오 타임라인을 원본 비디오 타임스탬프에 맞추어 정확히 믹싱
# 各 씬의 clip_start 시점에 오디오가 재생되도록 amix / adelay 필터 사용
print("[RUN] 오디오 타임라인 동기화 믹싱 생성 중...")
filter_parts = []
input_args = []
idx = 0
for sc in scenes:
    delay_ms = int(sc["clip_start"] * 1000)
    input_args.extend(["-i", sc["audio_file"]])
    filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}];")
    idx += 1

mix_inputs = "".join(f"[a{i}]" for i in range(idx))
filter_str = "".join(filter_parts) + f"{mix_inputs}amix=inputs={idx}:dropout_transition=0:normalize=0[aout]"

merged_audio_path = os.path.join(temp_dir, "synced_audio.wav")
total_duration = CLIP_END_OFFSET - CLIP_START_OFFSET
cmd_audio = [
    ffmpeg_exe, "-y",
    *input_args,
    "-filter_complex", filter_str,
    "-map", "[aout]",
    "-t", str(total_duration),
    "-ar", "44100", "-ac", "2",
    merged_audio_path
]
subprocess.run(cmd_audio, check=True)
print(f"[SUCCESS] 타임라인 정밀 동기화 오디오 생성 완료: {merged_audio_path}")

# 5. 원본 비디오 프레임 추출 및 실시간 고화질 한글 자막 오버레이
print(f"[RUN] 원본 영상({raw_video_path})에서 실제 프레임 읽어 자막 합성 시작...")
cap = cv2.VideoCapture(raw_video_path)
orig_fps = cap.get(cv2.CAP_PROP_FPS)
if orig_fps <= 0 or orig_fps > 60:
    orig_fps = 25.0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"[INFO] 원본 영상 제원: {width}x{height} @ {orig_fps:.2f}fps (총 {total_video_frames} 프레임)")

silent_video_out = os.path.join(temp_dir, "footage_with_subtitles.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_writer = cv2.VideoWriter(silent_video_out, fourcc, orig_fps, (width, height))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cur_sec = frame_idx / orig_fps
    
    # 현재 시간에 해당하는 씬 찾기
    active_sc = None
    for sc in scenes:
        if sc["clip_start"] <= cur_sec <= sc["clip_end"]:
            active_sc = sc
            break
    
    if active_sc is not None:
        # PIL 이미지로 변환하여 고화질 한글 자막 렌더링
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil, "RGBA")
        
        # 1. 하단 반투명 시네마틱 자막 바
        bar_h = 130
        draw.rectangle(
            [(0, height - bar_h), (width, height)],
            fill=(10, 10, 15, 195)
        )
        # 상단 액센트 라인 (배역 컬러)
        col = active_sc["color"]
        draw.line([(0, height - bar_h), (width, height - bar_h)], fill=(col[0], col[1], col[2], 255), width=3)
        
        # 2. 배역 뱃지
        badge_text = f" {active_sc['char']} "
        draw.rectangle(
            [(50, height - bar_h + 16), (50 + len(badge_text)*18 + 10, height - bar_h + 46)],
            fill=(col[0], col[1], col[2], 230)
        )
        draw.text((55, height - bar_h + 18), badge_text, font=font_badge, fill=(255, 255, 255, 255))
        
        # 3. 타임스탬프
        real_time_sec = CLIP_START_OFFSET + cur_sec
        m = int(real_time_sec) // 60
        s = int(real_time_sec) % 60
        time_str = f"원본 타임코드: {m:02d}:{s:02d} / 01:57:57"
        draw.text((width - 320, height - bar_h + 20), time_str, font=font_tag, fill=(180, 200, 220, 220))
        
        # 4. 메인 자막 텍스트
        sub_text = active_sc["text"]
        # 자막 그림자 효과
        draw.text((52, height - bar_h + 60), sub_text, font=font_sub, fill=(0, 0, 0, 230))
        draw.text((50, height - bar_h + 58), sub_text, font=font_sub, fill=(255, 255, 255, 255))
        
        # 다시 BGR로 변환
        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    out_writer.write(frame)
    frame_idx += 1
    if frame_idx % 300 == 0:
        print(f"  [렌더링 진행] {frame_idx}/{total_video_frames} 프레임 ({frame_idx/total_video_frames*100:.1f}%)")

cap.release()
out_writer.release()
print(f"[SUCCESS] 자막 합성 영상 렌더링 완료 ({frame_idx} 프레임)")

# 6. 최종 MP4 병합 (영상 + 무손실 AAC 동기화 오디오)
final_mp4 = os.path.join(result_dir, "[206]_episode_01_scene_3287s_remake_master.mp4")
cmd_mux = [
    ffmpeg_exe, "-y",
    "-i", silent_video_out,
    "-i", merged_audio_path,
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    final_mp4
]
print(f"[RUN] 최종 마스터 MP4 인코딩: {final_mp4}")
subprocess.run(cmd_mux, check=True)
print(f"[SUCCESS] 완벽 복원 MP4 생성 완료! 파일 크기: {os.path.getsize(final_mp4)/1024/1024:.2f} MB")
