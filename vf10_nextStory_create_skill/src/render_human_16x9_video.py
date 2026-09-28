#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_human_16x9_video.py :
16:9 시네마틱 와이드스크린(1280x720) 실제 사람(우주비행사, 콕핏 조종사, 지상 관제센터 요원)
전면 등장 및 인물-우주 몽타주 시네마틱 비디오 렌더러
- 사람이 단 한 명도 안 나오는 치명적 문제 100% 완전 해결!
- 16:9 가로 와이드스크린으로 정보량 극대화
- 10대 배역 ASS 자막 16:9 규격 하단 와이드 번인
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
HUMAN_DIR = os.path.join(SCRATCH_DIR, "human_16x9_footage")
SPACE_DIR = os.path.join(SCRATCH_DIR, "real_footage")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 씬 메타데이터 로드
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

def get_16x9_asset_for_scene(sc):
    """
    등장인물(사람) 대사와 우주 상황을 교차 매핑:
    인물이 말할 때는 실제 우주비행사/관제실 사람 실사 컷,
    해설이나 외부 상황일 때는 실제 우주/발사 실사 컷을 16:9로 매핑!
    """
    char = sc["character"]
    scene_id = sc["scene_id"]

    # 1. 인물 우선 매핑 (사람 등장)
    if char in ["강수연", "최영목", "빅터"]:
        if scene_id >= 70:
            return os.path.join(HUMAN_DIR, "human_09_celebration.png")
        return os.path.join(HUMAN_DIR, "human_01_mission_control.png")
    elif char in ["윤선아"]:
        return os.path.join(HUMAN_DIR, "human_02_launch_engineers.png")
    elif char in ["박준서"]:
        if scene_id <= 25:
            return os.path.join(HUMAN_DIR, "human_03_commander_cockpit.png")
        elif scene_id <= 45:
            return os.path.join(HUMAN_DIR, "human_05_spacewalk_eva.png")
        elif scene_id <= 70:
            return os.path.join(HUMAN_DIR, "human_07_lunar_surface.png")
        else:
            return os.path.join(HUMAN_DIR, "human_10_visor_portrait.png")
    elif char in ["김태훈"]:
        if scene_id <= 45:
            return os.path.join(HUMAN_DIR, "human_04_copilot_operations.png")
        elif scene_id <= 65:
            return os.path.join(HUMAN_DIR, "human_06_lunar_observer.png")
        else:
            return os.path.join(HUMAN_DIR, "human_08_rover_astronaut.png")
    elif char in ["어머니", "민재"]:
        return os.path.join(HUMAN_DIR, "human_01_mission_control.png")

    # 2. 해설 및 세종 AI (우주 상황 실사 컷을 16:9 와이드로 매핑)
    if scene_id <= 13:
        return os.path.join(HUMAN_DIR, "human_02_launch_engineers.png")
    elif scene_id <= 20:
        return os.path.join(HUMAN_DIR, "human_03_commander_cockpit.png")
    elif scene_id <= 35:
        return os.path.join(HUMAN_DIR, "human_05_spacewalk_eva.png")
    elif scene_id <= 60:
        return os.path.join(HUMAN_DIR, "human_07_lunar_surface.png")
    elif scene_id <= 80:
        return os.path.join(HUMAN_DIR, "human_08_rover_astronaut.png")
    else:
        return os.path.join(HUMAN_DIR, "human_10_visor_portrait.png")

def build_16x9_ass():
    """16:9 와이드스크린 (1280x720) 전용 시네마틱 ASS 자막 빌더"""
    ass_path = os.path.join(SCRATCH_DIR, "subtitles_16x9.ass")
    header = """[Script Info]
Title: 대한민국 달·화성 심우주 대서사시 (16:9 와이드스크린 시네마틱)
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Malgun Gothic,28,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,2.5,1.5,2,60,60,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for sc in scenes:
        char = sc["character"]
        style_info = CHAR_STYLES.get(char, CHAR_STYLES["해설"])
        badge_name = style_info["name"]
        color = style_info["color"]

        st_ass = sec_to_ass(sc["start"])
        et_ass = sec_to_ass(sc["end"])

        m_s = int(sc["start"]) // 60
        s_s = int(sc["start"]) % 60
        tc_tag = f"{m_s:02d}:{s_s:02d} KASA MISSION CONTROL"

        clean_text = sc["text"].replace("\n", " ").strip()
        dialogue_event = (
            f"Dialogue: 0,{st_ass},{et_ass},Default,,0,0,0,,"
            f"{{\\fs20\\c{color}}}[ {badge_name} ] {{\\c&HC0C0C0&}}({tc_tag})\\N"
            f"{{\\fs30\\c&HFFFFFF&}}{clean_text}\n"
        )
        lines.append(dialogue_event)

    with open(ass_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return ass_path

def build_16x9_concat(target_scenes, out_concat_file):
    lines = []
    for idx, sc in enumerate(target_scenes):
        img_path = get_16x9_asset_for_scene(sc).replace("\\", "/")
        if idx + 1 < len(target_scenes):
            dur = target_scenes[idx + 1]["start"] - sc["start"]
        else:
            dur = sc["duration"]
        dur = max(0.5, round(dur, 2))

        lines.append(f"file '{img_path}'\n")
        lines.append(f"duration {dur}\n")

    last_img = get_16x9_asset_for_scene(target_scenes[-1]).replace("\\", "/")
    lines.append(f"file '{last_img}'\n")

    with open(out_concat_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return out_concat_file

def render_16x9_highlight():
    master_audio = os.path.join(RESULT_DIR, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[062]_episode_02_human_16x9_highlight.mp4"
    out_file = resolve_immutable_path(target_name)

    hl_scenes = [s for s in scenes if s["start"] <= 90]
    concat_file = os.path.join(SCRATCH_DIR, "concat_16x9_hl.txt")
    build_16x9_concat(hl_scenes, concat_file)

    ass_path = build_16x9_ass()
    rel_ass = os.path.relpath(ass_path, VF10_DIR).replace("\\", "/")

    print(f"\n[RUN] 16:9 와이드스크린 실제 사람(인물/비행사/관제사) 등장 1분 30초 하이라이트 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-t", "90",
        "-vf", f"fps=25,scale=1280:720,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, cwd=VF10_DIR, check=True)
    size_mb = round(os.path.getsize(out_file) / (1024*1024), 2)
    print(f"[SUCCESS] 16:9 사람 실사 하이라이트 완성: {out_file} ({size_mb} MB)")
    return out_file

def render_16x9_master():
    master_audio = os.path.join(RESULT_DIR, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[063]_episode_02_human_16x9_full_master.mp4"
    out_file = resolve_immutable_path(target_name)

    concat_file = os.path.join(SCRATCH_DIR, "concat_16x9_master.txt")
    build_16x9_concat(scenes, concat_file)

    ass_path = build_16x9_ass()
    rel_ass = os.path.relpath(ass_path, VF10_DIR).replace("\\", "/")

    print(f"\n[RUN] 16:9 와이드스크린 실제 사람 등장 13분 통합 완제 마스터 비디오 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-vf", f"fps=25,scale=1280:720,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, cwd=VF10_DIR, check=True)
    size_mb = round(os.path.getsize(out_file) / (1024*1024), 2)
    print(f"[SUCCESS] 16:9 사람 실사 13분 마스터 비디오 완성: {out_file} ({size_mb} MB)")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="vf10 16:9 실제 사람 시네마틱 렌더러")
    parser.add_argument("--mode", choices=["highlight", "master", "full"], default="full")
    args = parser.parse_args()

    print("=" * 75)
    print("  [vf10] 16:9 와이드스크린 실제 사람(인물/비행사/관제사) 전면 등장 렌더러")
    print("  ★ 1280 x 720 와이드 시네마틱 / 인물-우주 크로스 컷팅 몽타주")
    print("=" * 75)

    if args.mode in ["highlight", "full"]:
        render_16x9_highlight()
    if args.mode in ["master", "full"]:
        render_16x9_master()

if __name__ == "__main__":
    main()
