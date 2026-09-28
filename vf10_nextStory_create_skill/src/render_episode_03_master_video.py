#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_episode_03_master_video.py :
에피소드 03 '목성 위성 유로파 오디세이'
대화 100% 일치 고화질 I2V + 다역 TTS + 16:9 자막 완제 마스터 동영상 렌더러.
"""

import os
import sys
import json
import subprocess
import imageio_ffmpeg
from immutable_versioning import resolve_immutable_path
import i2v_cinematic_motion_engine as i2v

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")
SCRATCH_DIR = os.path.join(VF10_DIR, "scratch")
KEYFRAMES_DIR = os.path.join(SCRATCH_DIR, "ep03_keyframes")
EP03_CLIPS_DIR = os.path.join(SCRATCH_DIR, "ep03_i2v_clips")
os.makedirs(EP03_CLIPS_DIR, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 키프레임 에셋
KEYFRAME_ASSETS = {
    "mars_biosphere": os.path.join(KEYFRAMES_DIR, "ep03_scene01_mars_biosphere.jpg"),
    "cheonmyeong_ii": os.path.join(KEYFRAMES_DIR, "ep03_scene14_cheonmyeong_ii.jpg"),
    "jupiter_red_spot": os.path.join(KEYFRAMES_DIR, "ep03_scene17_jupiter_red_spot.jpg"),
    "europa_ice": os.path.join(KEYFRAMES_DIR, "ep03_scene22_europa_ice_geyser.jpg"),
    "haetae_sub": os.path.join(KEYFRAMES_DIR, "ep03_scene27_haetae_sub.jpg"),
    "alien_life": os.path.join(KEYFRAMES_DIR, "ep03_scene31_alien_life.jpg"),
}

MOTION_SEQUENCE = ["zoom_in", "pan_left", "zoom_out", "tilt_up", "pan_right", "orbit_cw"]

def select_asset_for_ep03_scene(sc):
    sid = sc["scene_id"]
    if sid <= 3 or (10 <= sid <= 12):
        return KEYFRAME_ASSETS["mars_biosphere"]
    elif (4 <= sid <= 7) or (13 <= sid <= 16) or (19 <= sid <= 20):
        return KEYFRAME_ASSETS["cheonmyeong_ii"]
    elif (17 <= sid <= 18) or sid == 21:
        return KEYFRAME_ASSETS["jupiter_red_spot"]
    elif sid == 8 or (22 <= sid <= 24):
        return KEYFRAME_ASSETS["europa_ice"]
    elif 25 <= sid <= 30:
        return KEYFRAME_ASSETS["haetae_sub"]
    else:  # 31 <= sid <= 38
        return KEYFRAME_ASSETS["alien_life"]

def render_ep03_master():
    meta_path = os.path.join(RESULT_DIR, "[102]_episode_03_calibrated_scenes.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    master_audio = os.path.join(RESULT_DIR, "[104]_episode_03_master_audio.mp3")
    target_name = "[105]_episode_03_europa_odyssey_master.mp4"
    out_file = resolve_immutable_path(target_name)

    print("=" * 80)
    print(f"  🎬 [에피소드 03] 목성 위성 유로파 오디세이 완제 마스터 렌더링 시작")
    print(f"  - 총 씬 수: {len(scenes)}개 씬")
    print(f"  - 출력 대상: {os.path.basename(out_file)}")
    print("=" * 80)

    concat_lines = []

    # 1. 초기 1.0초 앰비언트 클립
    first_img = select_asset_for_ep03_scene(scenes[0])
    init_clip = os.path.join(EP03_CLIPS_DIR, "ep03_init_pause_100s.mp4")
    if not os.path.exists(init_clip) or os.path.getsize(init_clip) < 1000:
        i2v.generate_i2v_clip(first_img, init_clip, 1.0, motion_type="zoom_in", fps=30, width=1280, height=720)
    concat_lines.append(f"file '{init_clip.replace('\\', '/')}'\n")
    concat_lines.append("inpoint 0.00\noutpoint 1.00\n")

    # 2. 씬별 I2V 클립 렌더링
    for idx, sc in enumerate(scenes):
        sid = sc["scene_id"]
        char = sc["character"]
        dur = sc["duration"]

        img_path = select_asset_for_ep03_scene(sc)
        motion_type = MOTION_SEQUENCE[idx % len(MOTION_SEQUENCE)]
        clip_name = f"ep03_clip_{sid:03d}_{char}_{dur:.2f}s.mp4"
        clip_path = os.path.join(EP03_CLIPS_DIR, clip_name)

        if not os.path.exists(clip_path) or os.path.getsize(clip_path) < 1000:
            i2v.generate_i2v_clip(img_path, clip_path, dur, motion_type=motion_type, fps=30, width=1280, height=720)

        norm_p = clip_path.replace("\\", "/")
        concat_lines.append(f"file '{norm_p}'\n")
        concat_lines.append("inpoint 0.00\n")
        concat_lines.append(f"outpoint {dur:.2f}\n")

        if (idx + 1) % 5 == 0 or idx == len(scenes) - 1:
            print(f"    ✔ [{idx + 1:>2}/{len(scenes)}] 씬 I2V 클립 완료: Scene {sid:02d} ({char}, {dur}s, {motion_type})")

    concat_txt = os.path.join(SCRATCH_DIR, "ep03_video_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.writelines(concat_lines)

    ass_path = os.path.join(SCRATCH_DIR, "subtitles_ep03_true_sync.ass")
    rel_ass = os.path.relpath(ass_path, VF10_DIR).replace("\\", "/")

    print(f"\n[*] 에피소드 03 전체 스트림 결합 (I2V 영상 + 마스터 오디오 + ASS 자막) 렌더링 중...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", master_audio,
        "-map", "0:v", "-map", "1:a",
        "-vf", f"fps=30,scale=1280:720,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, cwd=VF10_DIR, check=True)
    size_mb = round(os.path.getsize(out_file) / (1024*1024), 2)
    print(f"\n[SUCCESS] 에피소드 03 '목성 위성 유로파 오디세이' 완제 마스터 비디오 완성!")
    print(f"    -> 파일: {out_file} ({size_mb} MB)")
    return out_file

if __name__ == "__main__":
    render_ep03_master()
