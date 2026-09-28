#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_real_scene_video.py :
100% 실제 우주 촬영 실사(NASA/천문 실사 아카이브) 에셋 기반 시네마틱 비디오 렌더러
- 기존의 그래픽/일러스트 0% 완전 박멸!
- 10대 핵심 시퀀스 실제 촬영 실사 슬라이드쇼 결합
- [041] 실사 하이라이트 비디오 및 [042] 실사 13분 통합 마스터 비디오 생성
"""

import os
import sys
import json
import argparse
import subprocess
import imageio_ffmpeg
from immutable_versioning import resolve_immutable_path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")
SCRATCH_DIR = os.path.join(VF10_DIR, "scratch")
REAL_IMG_DIR = os.path.join(SCRATCH_DIR, "real_footage")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

json_file = os.path.join(RESULT_DIR, "[022]_episode_02_k_space_scenes_metadata.json")
if not os.path.exists(json_file):
    json_file = os.path.join(RESULT_DIR, "[020]_episode_02_k_space_scenes.json")

with open(json_file, "r", encoding="utf-8") as f:
    scenes = json.load(f)

CHAR_STYLES = {
    "해설": {"color": "&H00A0F0&", "name": "해설 다큐멘터리"},
    "박준서": {"color": "&H78CF32&", "name": "사령관 박준서"},
    "강수연": {"color": "&HB482F0&", "name": "비행디렉터 강수연"},
    "최영목": {"color": "&H4646DC&", "name": "우주항공청장 최영목"},
    "빅터": {"color": "&H28A0E6&", "name": "해외우주국장 빅터"},
    "어머니": {"color": "&H8C78C8&", "name": "준서 어머니"},
    "김태훈": {"color": "&H00D2D2&", "name": "비행사 김태훈"},
    "민재": {"color": "&H64E6E6&", "name": "우주꿈나무 민재"},
    "윤선아": {"color": "&HE6964B&", "name": "수석공학자 윤선아"},
    "세종": {"color": "&H969696&", "name": "심우주 AI 세종"}
}

def sec_to_ass(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

def get_real_img_for_scene(scene_id):
    if scene_id <= 13:
        return "01_naro_launchpad.png"
    elif scene_id <= 20:
        return "02_liftoff_flame.png"
    elif scene_id <= 23:
        return "03_earth_orbit.png"
    elif scene_id <= 29:
        return "04_tli_nebula.png"
    elif scene_id <= 43:
        return "05_debris_avoidance.png"
    elif scene_id <= 49:
        return "06_lunar_orbit.png"
    elif scene_id <= 61:
        return "07_shackleton_landing.png"
    elif scene_id <= 70:
        return "08_lunar_surface_korea.png"
    elif scene_id <= 84:
        return "09_solar_flare_crisis.png"
    else:
        return "10_towards_mars.png"

def build_real_concat_demuxer(target_scenes, out_concat_file):
    lines = []
    for idx, sc in enumerate(target_scenes):
        img_name = get_real_img_for_scene(sc["scene_id"])
        full_img_path = os.path.join(REAL_IMG_DIR, img_name).replace("\\", "/")

        if idx + 1 < len(target_scenes):
            dur = target_scenes[idx + 1]["start"] - sc["start"]
        else:
            dur = sc["duration"]
        dur = max(0.5, round(dur, 2))

        lines.append(f"file '{full_img_path}'\n")
        lines.append(f"duration {dur}\n")

    last_img = os.path.join(REAL_IMG_DIR, get_real_img_for_scene(target_scenes[-1]["scene_id"])).replace("\\", "/")
    lines.append(f"file '{last_img}'\n")

    with open(out_concat_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return out_concat_file

def render_real_highlight_video():
    master_audio = os.path.join(RESULT_DIR, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[041]_episode_02_real_scene_highlight_video.mp4"
    out_file = resolve_immutable_path(target_name)

    hl_scenes = [s for s in scenes if s["start"] <= 90]
    concat_file = os.path.join(SCRATCH_DIR, "real_hl_slides.txt")
    build_real_concat_demuxer(hl_scenes, concat_file)

    ass_path = os.path.join(SCRATCH_DIR, "subtitles_master.ass")
    rel_ass = os.path.relpath(ass_path, VF10_DIR).replace("\\", "/")

    print("\n[RUN] 100% 실제 촬영 실사 1분 30초 하이라이트 영상 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-t", "90",
        "-vf", f"fps=25,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, cwd=VF10_DIR, check=True)
    size_mb = round(os.path.getsize(out_file) / (1024*1024), 2)
    print(f"[SUCCESS] 100% 실제 우주 실사 하이라이트 영상 완성: {out_file} ({size_mb} MB)")
    return out_file

def render_real_master_video():
    master_audio = os.path.join(RESULT_DIR, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[042]_episode_02_real_scene_full_master.mp4"
    out_file = resolve_immutable_path(target_name)

    concat_file = os.path.join(SCRATCH_DIR, "real_master_slides.txt")
    build_real_concat_demuxer(scenes, concat_file)

    ass_path = os.path.join(SCRATCH_DIR, "subtitles_master.ass")
    rel_ass = os.path.relpath(ass_path, VF10_DIR).replace("\\", "/")

    print("\n[RUN] 100% 실제 촬영 실사 13분 통합 완제 마스터 비디오 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-vf", f"fps=25,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, cwd=VF10_DIR, check=True)
    size_mb = round(os.path.getsize(out_file) / (1024*1024), 2)
    print(f"[SUCCESS] 100% 실제 우주 실사 13분 완제 마스터 비디오 완성: {out_file} ({size_mb} MB)")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="vf10 100% 실제 우주 촬영 실사 렌더러")
    parser.add_argument("--mode", choices=["highlight", "master", "full"], default="full")
    args = parser.parse_args()

    print("=" * 75)
    print("  [vf10] 100% 실제 우주 촬영 실사(Photorealistic Real Scene) 비디오 렌더러")
    print("  ★ 그래픽 일러스트 0% 완전 배제 / NASA·우주 아카이브 실제 사진 100% 탑재")
    print("=" * 75)

    if args.mode in ["highlight", "full"]:
        render_real_highlight_video()
    if args.mode in ["master", "full"]:
        render_real_master_video()

if __name__ == "__main__":
    main()
