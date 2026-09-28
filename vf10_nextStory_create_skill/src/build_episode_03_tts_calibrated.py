#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_episode_03_tts_calibrated.py :
에피소드 03 10대 배역 다역 TTS 합성 및 0-Drift 절대 캘리브레이션 엔진.
- 오디오 실측 발화 시간 기반 1:1 완벽 자막 및 마스터 오디오 구축
"""

import os
import sys
import json
import asyncio
import edge_tts
import subprocess
import imageio_ffmpeg

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")
SCRATCH_DIR = os.path.join(VF10_DIR, "scratch")
EP03_SEG_DIR = os.path.join(SCRATCH_DIR, "ep03_segments")
os.makedirs(EP03_SEG_DIR, exist_ok=True)

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 10대 배역 프리셋 매핑
CHAR_PRESETS = {
    "해설": {"voice": "ko-KR-InJoonNeural", "pitch": "-1Hz", "rate": "+6%", "volume": "+0%"},
    "박준서": {"voice": "ko-KR-HyunsuNeural", "pitch": "+1Hz", "rate": "+8%", "volume": "+5%"},
    "강수연": {"voice": "ko-KR-SunHiNeural", "pitch": "+2Hz", "rate": "+5%", "volume": "+0%"},
    "최영목": {"voice": "ko-KR-InJoonNeural", "pitch": "-5Hz", "rate": "+4%", "volume": "+5%"},
    "빅터": {"voice": "ko-KR-InJoonNeural", "pitch": "-3Hz", "rate": "+6%", "volume": "-2%"},
    "어머니": {"voice": "ko-KR-SunHiNeural", "pitch": "-3Hz", "rate": "+4%", "volume": "-3%"},
    "김태훈": {"voice": "ko-KR-HyunsuNeural", "pitch": "+4Hz", "rate": "+10%", "volume": "+3%"},
    "민재": {"voice": "ko-KR-SunHiNeural", "pitch": "+5Hz", "rate": "+8%", "volume": "+4%"},
    "윤선아": {"voice": "ko-KR-SunHiNeural", "pitch": "+0Hz", "rate": "+5%", "volume": "+2%"},
    "세종": {"voice": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+5%", "volume": "+0%"}
}

def sec_to_ass(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

def get_audio_duration(file_path):
    cmd = [ffmpeg_exe, "-i", file_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            dur_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = dur_str.split(":")
            return float(h)*3600 + float(m)*60 + float(s)
    return 0.0

async def synthesize_all_scenes(scenes):
    print(f"[*] 에피소드 03 TTS 음성 세그먼트 {len(scenes)}개 합성 시작...")
    sem = asyncio.Semaphore(6)

    async def syn_one(sc):
        async with sem:
            sid = sc["scene_id"]
            char = sc["character"]
            text = sc["text"]
            out_p = os.path.join(EP03_SEG_DIR, f"ep03_seg_{sid:04d}.mp3")

            if os.path.exists(out_p) and os.path.getsize(out_p) > 500:
                return sid, out_p

            preset = CHAR_PRESETS.get(char, CHAR_PRESETS["해설"])
            comm = edge_tts.Communicate(
                text=text,
                voice=preset["voice"],
                pitch=preset["pitch"],
                rate=preset["rate"],
                volume=preset["volume"]
            )
            await comm.save(out_p)
            return sid, out_p

    tasks = [syn_one(s) for s in scenes]
    results = await asyncio.gather(*tasks)
    return {r[0]: r[1] for r in results}

def run_calibration():
    scenes_path = os.path.join(RESULT_DIR, "[101]_episode_03_europa_scenes.json")
    with open(scenes_path, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    # 1. TTS 합성
    seg_map = asyncio.run(synthesize_all_scenes(scenes))
    print("[✔] TTS 세그먼트 전수 합성 완료!")

    # 2. 실측 발화 시간 측정 및 타임라인 캘리브레이션
    calibrated_scenes = []
    curr_time = 1.0  # 시작 여유
    pause_sec = 0.4
    ass_events = []

    for sc in scenes:
        sid = sc["scene_id"]
        char = sc["character"]
        text = sc["text"]
        fpath = seg_map[sid]

        dur = round(get_audio_duration(fpath), 3)
        start_t = round(curr_time, 2)
        end_speech_t = round(start_t + dur, 2)
        total_dur = round(dur + pause_sec, 2)

        entry = {
            "scene_id": sid,
            "character": char,
            "text": text,
            "dialogue": text,
            "start": start_t,
            "speech_end": end_speech_t,
            "duration": total_dur,
            "actual_speech_duration": dur,
            "seg_file": fpath.replace("\\", "/")
        }
        calibrated_scenes.append(entry)

        # ASS 자막 (대사 발화 시점과 100% 일치)
        start_ass = sec_to_ass(start_t)
        end_ass = sec_to_ass(end_speech_t)
        clean_text = text.replace('"', '').strip()
        ass_line = f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{{\\b1\\c&H00FFFF&}}[{char}]{{\\b0\\c&HFFFFFF&}} {clean_text}"
        ass_events.append(ass_line)

        curr_time += total_dur

    total_time = round(curr_time, 2)
    print(f"[*] 에피소드 03 총 상영시간: {total_time:.2f}초 ({total_time/60:.2f}분)")

    # 메타데이터 저장
    calib_json = os.path.join(RESULT_DIR, "[102]_episode_03_calibrated_scenes.json")
    with open(calib_json, "w", encoding="utf-8") as f:
        json.dump(calibrated_scenes, f, ensure_ascii=False, indent=2)

    # ASS 자막 저장
    ass_header = """[Script Info]
Title: K-Space Odyssey Episode 03 Europa Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,맑은 고딕,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,32,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_path = os.path.join(SCRATCH_DIR, "subtitles_ep03_true_sync.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_events) + "\n")

    # 마스터 오디오 결합
    master_audio = os.path.join(RESULT_DIR, "[104]_episode_03_master_audio.mp3")
    silence_04 = os.path.join(SCRATCH_DIR, "pause_04s.mp3")
    init_silence = os.path.join(SCRATCH_DIR, "init_silence_10s.mp3")

    audio_list_txt = os.path.join(SCRATCH_DIR, "ep03_audio_concat.txt")
    lines = [f"file '{init_silence.replace('\\', '/')}'\n"]
    for sc in calibrated_scenes:
        lines.append(f"file '{sc['seg_file']}'\n")
        lines.append(f"file '{silence_04.replace('\\', '/')}'\n")

    with open(audio_list_txt, "w", encoding="utf-8") as f:
        f.writelines(lines)

    cmd_a = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", audio_list_txt,
        "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "24000", "-ac", "1",
        master_audio
    ]
    subprocess.run(cmd_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    real_aud_dur = get_audio_duration(master_audio)
    print(f"[✔] 에피소드 03 완벽 동기화 마스터 오디오 완성: {master_audio} ({real_aud_dur:.2f}s, 오차 {abs(total_time - real_aud_dur):.3f}s)")
    return calib_json, ass_path, master_audio

if __name__ == "__main__":
    run_calibration()
