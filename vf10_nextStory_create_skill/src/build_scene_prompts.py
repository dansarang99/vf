#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_scene_prompts.py :
시나리오 메타데이터와 캐릭터·세계관 페르소나를 1:1 결합하여
전체 씬(Scene 1~91)별 5대 마스터 대본 및 정밀 키프레임 프롬프트 데이터셋을 컴파일하는 엔진.
- 토큰 소모량: 0
"""

import os
import sys
import json

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")
SRC_DIR = os.path.join(VF10_DIR, "src")
PERSONAS_DIR = os.path.join(SRC_DIR, "personas")

def compile_scene_prompts():
    meta_path = os.path.join(RESULT_DIR, "[022]_episode_02_k_space_scenes_metadata.json")
    if not os.path.exists(meta_path):
        meta_path = os.path.join(RESULT_DIR, "[020]_episode_02_k_space_scenes.json")

    with open(meta_path, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    with open(os.path.join(PERSONAS_DIR, "characters.json"), "r", encoding="utf-8") as f:
        char_data = json.load(f)["characters"]

    with open(os.path.join(PERSONAS_DIR, "worldbuilding_assets.json"), "r", encoding="utf-8") as f:
        wb_data = json.load(f)["worldbuilding_locations"]

    compiled_prompts = []

    for sc in scenes:
        sid = sc["scene_id"]
        char = sc["character"]
        dialogue = sc.get("dialogue", sc.get("text", ""))
        dur = sc.get("duration", 5.0)
        start_t = sc.get("start", 0.0)

        # 1. 배경 매핑
        if sid <= 13:
            loc_key = "naro_mission_control"
            stage = "지상 관제 및 발사 카운트다운"
        elif sid <= 20:
            loc_key = "nuri_v_launchpad"
            stage = "누리호-V 발사 및 1단 분리"
        elif sid <= 30:
            loc_key = "cheonmyeong_bridge"
            stage = "지구 저궤도 안착 및 전함 시스템 점검"
        elif sid <= 65:
            loc_key = "lunar_southpole_base"
            stage = "달 남극 섀클턴 아르테미스 연구기지 강하 및 탐사"
        else:
            loc_key = "mars_utopia_orbit"
            stage = "심우주 궤도 전이 및 화성 대기 진입"

        loc_info = wb_data.get(loc_key, wb_data["cheonmyeong_bridge"])

        # 2. 인물 Visual DNA
        c_info = char_data.get(char, char_data["해설"])
        v_dna = c_info["visual_persona"].get("visual_anchor_dna", "")
        role = c_info.get("role", "")

        # 3. 카메라 앵글 및 모션 설정
        if char == "해설":
            cam_shot = "Extreme wide master establishing shot, anamorphic cinematic lens"
            motion = "Slow majestic forward dolly zoom with subtle cosmic star drift"
        elif char in ["박준서", "강수연"]:
            if any(w in dialogue for w in ["긴급", "경보", "결정", "지금", "출력", "점화"]):
                cam_shot = "Intense dynamic close-up portrait, Dutch angle, dramatic red rim light"
                motion = "Rapid camera push-in focusing sharply on character eyes"
            else:
                cam_shot = "Medium shot, 35mm cinematic lens, elegant atmospheric lighting"
                motion = "Gentle horizontal tracking pan following subject focus"
        elif char == "세종":
            cam_shot = "Macro shot of luminous holographic quantum core orb, particle refraction"
            motion = "Smooth 360-degree rotation around glowing holographic lattice"
        else:
            cam_shot = "Over-the-shoulder medium shot focusing on instrument console"
            motion = "Steady slow crane tilt-up revealing space backdrop"

        # 4. 종합 이미지 프롬프트 (Visual DNA + 무대 + 행동/대사 뉘앙스)
        img_prompt = (
            f"{v_dna}, {loc_info['prompt']}, "
            f"character acting: portraying '{dialogue[:30]}...', "
            f"{cam_shot}, 8k UHD, hyper-realistic, photorealistic sci-fi cinematography, Unreal Engine 5 render aesthetic --ar 16:9"
        )

        entry = {
            "scene_id": sid,
            "start": start_t,
            "duration": dur,
            "character": char,
            "character_role": role,
            "stage": stage,
            "location": loc_info["name"],
            "dialogue": dialogue,
            "tracks": {
                "image_prompt": img_prompt,
                "camera_motion": motion,
                "narration_script": f"[{char}] {dialogue}",
                "subtitle_text": dialogue,
                "sound_design": f"Ambience: {loc_info['mood']} | Foley: Sub-bass engine rumble & comms chatter"
            }
        }
        compiled_prompts.append(entry)

    out_json = os.path.join(RESULT_DIR, "[081]_scene_prompts_master.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(compiled_prompts, f, ensure_ascii=False, indent=2)

    print(f"[*] 총 {len(compiled_prompts)}개 씬 전체 마스터 프롬프트 컴파일 완료 -> {out_json}")
    return out_json

if __name__ == "__main__":
    compile_scene_prompts()
