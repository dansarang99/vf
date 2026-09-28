#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_022_cinematic_space_video.py :
제2탄 100% K-우주(달·화성·발사체·착륙선) 씬별 다이내믹 시네마틱 비디오 렌더러
- 1편(항공기) 영상 0% 완전 박멸!
- 91개 씬의 서사에 1:1로 매핑되는 10대 K-우주 시네마틱 비주얼 슬라이드쇼 비디오 엔진
- 10인 배역 컬러 뱃지 + 타임코드 ASS 자막 100% 번인
- 4부작 시네마틱 풀영상 (Part 1~4) 및 13분 통합 완제 마스터 MP4 생성
- 무손실 누적 보존(Zero-Overwrite Immutable Versioning) 지원
- 옵션: --mode [highlight / part1 / all_parts / master / full]
"""

import os
import sys
import json
import argparse
import subprocess
import imageio_ffmpeg
from immutable_versioning import resolve_immutable_path

vf10_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
result_dir = os.path.join(vf10_dir, "result")
scratch_dir = os.path.join(vf10_dir, "scratch")
img_dir = os.path.join(scratch_dir, "space_footage")
os.makedirs(result_dir, exist_ok=True)
os.makedirs(scratch_dir, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 메타데이터 JSON 탐색
json_file = os.path.join(result_dir, "[022]_episode_02_k_space_scenes_metadata.json")
if not os.path.exists(json_file):
    json_file = os.path.join(result_dir, "[020]_episode_02_k_space_scenes.json")

with open(json_file, "r", encoding="utf-8") as f:
    scenes = json.load(f)

# 10대 배역 색상 및 뱃지 매핑 (BGR HEX for ASS)
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

def get_theme_img_for_scene(scene_id):
    """씬 번호에 따라 정확한 우주 테마 비주얼 이미지 매핑"""
    if scene_id <= 13:
        return "01_naro_launchpad.png"      # 발사대 & 카운트다운
    elif scene_id <= 20:
        return "02_liftoff_flame.png"       # 엔진 점화 & 맥스큐 돌파
    elif scene_id <= 23:
        return "03_earth_orbit.png"         # 저궤도 진입 & 페어링 분리
    elif scene_id <= 29:
        return "04_tli_nebula.png"          # TLI 달 전이 궤도 항행
    elif scene_id <= 43:
        return "05_debris_avoidance.png"    # 우주 파편 회피 비상 기동
    elif scene_id <= 49:
        return "06_lunar_orbit.png"         # 달 극궤도 진입 & 크레이터
    elif scene_id <= 61:
        return "07_shackleton_landing.png"  # 섀클턴 크레이터 역추진 착륙
    elif scene_id <= 70:
        return "08_lunar_surface_korea.png" # 달 표면 기지 & 로버 해치
    elif scene_id <= 84:
        return "09_solar_flare_crisis.png"  # 태양 플레어 비상 & 레이저 펄스
    else:
        return "10_towards_mars.png"        # 화성 탐사선 천명 복구 & 피날레

def build_space_concat_demuxer(target_scenes, out_concat_file):
    """씬 목록을 기반으로 FFmpeg 슬라이드쇼 concat 파일 생성"""
    lines = []
    for idx, sc in enumerate(target_scenes):
        img_name = get_theme_img_for_scene(sc["scene_id"])
        full_img_path = os.path.join(img_dir, img_name).replace("\\", "/")
        
        if idx + 1 < len(target_scenes):
            dur = target_scenes[idx + 1]["start"] - sc["start"]
        else:
            dur = sc["duration"]
        dur = max(0.5, round(dur, 2))

        lines.append(f"file '{full_img_path}'\n")
        lines.append(f"duration {dur}\n")

    last_img = os.path.join(img_dir, get_theme_img_for_scene(target_scenes[-1]["scene_id"])).replace("\\", "/")
    lines.append(f"file '{last_img}'\n")

    with open(out_concat_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return out_concat_file

def build_master_ass():
    ass_path = os.path.join(result_dir, "[029]_episode_02_k_space_cinematic_subtitles.ass")
    scratch_master_ass = os.path.join(scratch_dir, "subtitles_master.ass")
    header = """[Script Info]
Title: 대한민국 달·화성 심우주 대서사시 전편 통합 완제
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 720
PlayResY: 1280

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Malgun Gothic,30,&H00FFFFFF,&H000000FF,&H00000000,&HB0000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,70,1

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
        tc_tag = f"{m_s:02d}:{s_s:02d} / 12:53 KASA"

        clean_text = sc["text"].replace("\n", " ").strip()
        dialogue_event = (
            f"Dialogue: 0,{st_ass},{et_ass},Default,,0,0,0,,"
            f"{{\\fs22\\c{color}}}[ {badge_name} ] {{\\c&HC8C8C8&}}({tc_tag})\\N"
            f"{{\\fs32\\c&HFFFFFF&}}{clean_text}\n"
        )
        lines.append(dialogue_event)

    for p in [ass_path, scratch_master_ass]:
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(lines)
    return scratch_master_ass

def render_master_video():
    master_audio = os.path.join(result_dir, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[031]_episode_02_full_master_video.mp4"
    master_out = resolve_immutable_path(target_name)

    concat_file = os.path.join(scratch_dir, "master_space_slides.txt")
    build_space_concat_demuxer(scenes, concat_file)

    ass_path = build_master_ass()
    rel_ass = os.path.relpath(ass_path, vf10_dir).replace("\\", "/")

    print("\n[RUN] 13분 통합 완제 마스터 K-우주(달·화성) 씬별 다이내믹 영상 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-vf", f"fps=25,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        master_out
    ]
    subprocess.run(cmd, cwd=vf10_dir, check=True)
    size_mb = round(os.path.getsize(master_out) / (1024*1024), 2)
    print(f"[SUCCESS] 13분 통합 완제 K-우주 마스터 비디오 완성: {master_out} ({size_mb} MB)")

def render_highlight_video():
    master_audio = os.path.join(result_dir, "[023]_episode_02_k_space_master_audio.mp3")
    target_name = "[030]_episode_02_k_space_highlight_video.mp4"
    highlight_out = resolve_immutable_path(target_name)

    hl_scenes = [s for s in scenes if s["start"] <= 90]
    concat_file = os.path.join(scratch_dir, "hl_space_slides.txt")
    build_space_concat_demuxer(hl_scenes, concat_file)

    ass_path = build_master_ass()
    rel_ass = os.path.relpath(ass_path, vf10_dir).replace("\\", "/")

    print("\n[RUN] 1분 30초 실전 하이라이트 K-우주 영상 렌더링...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", master_audio,
        "-t", "90",
        "-vf", f"fps=25,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        highlight_out
    ]
    subprocess.run(cmd, cwd=vf10_dir, check=True)
    size_mb = round(os.path.getsize(highlight_out) / (1024*1024), 2)
    print(f"[SUCCESS] 1분 30초 하이라이트 영상 완성: {highlight_out} ({size_mb} MB)")

def render_part_video(part_num):
    total_dur = scenes[-1]["end"]
    part_dur = total_dur / 4.0
    ss = (part_num - 1) * part_dur
    to = part_num * part_dur

    part_scenes = [s for s in scenes if ss <= s["start"] < to]
    if not part_scenes:
        return

    # 파트별 오디오 매핑
    audio_map = {
        1: "[024]_episode_02_part_1_launch_audio.mp3",
        2: "[025]_episode_02_part_2_trans_lunar_audio.mp3",
        3: "[026]_episode_02_part_3_lunar_landing_audio.mp3",
        4: "[027]_episode_02_part_4_mars_transfer_audio.mp3"
    }
    part_audio = os.path.join(result_dir, audio_map[part_num])
    
    target_names = {
        1: "[032]_episode_02_part_1_fullscene_video.mp4",
        2: "[033]_episode_02_part_2_fullscene_video.mp4",
        3: "[034]_episode_02_part_3_fullscene_video.mp4",
        4: "[035]_episode_02_part_4_fullscene_video.mp4"
    }
    part_out = resolve_immutable_path(target_names[part_num])

    concat_file = os.path.join(scratch_dir, f"part_{part_num}_slides.txt")
    build_space_concat_demuxer(part_scenes, concat_file)

    ass_path = build_master_ass()
    rel_ass = os.path.relpath(ass_path, vf10_dir).replace("\\", "/")

    print(f"\n[RUN] 제{part_num}막 K-우주 풀씬 렌더링 ({ss:.1f}s ~ {to:.1f}s)...")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", part_audio,
        "-vf", f"fps=25,format=yuv420p,ass={rel_ass}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        part_out
    ]
    subprocess.run(cmd, cwd=vf10_dir, check=True)
    size_mb = round(os.path.getsize(part_out) / (1024*1024), 2)
    print(f"[SUCCESS] 제{part_num}막 K-우주 비디오 완성: {part_out} ({size_mb} MB)")

def main():
    parser = argparse.ArgumentParser(description="vf10 100% K-우주 시네마틱 비디오 렌더러")
    parser.add_argument("--mode", choices=["highlight", "part1", "all_parts", "master", "full"], default="full")
    args = parser.parse_args()

    build_master_ass()

    if args.mode == "highlight":
        render_highlight_video()
    elif args.mode == "part1":
        render_part_video(1)
    elif args.mode == "all_parts":
        render_highlight_video()
        for p in range(1, 5):
            render_part_video(p)
    elif args.mode == "master":
        render_master_video()
    elif args.mode == "full":
        render_highlight_video()
        for p in range(1, 5):
            render_part_video(p)
        render_master_video()

if __name__ == "__main__":
    main()
