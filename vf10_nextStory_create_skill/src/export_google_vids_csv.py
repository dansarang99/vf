# -*- coding: utf-8 -*-
"""
export_google_vids_csv.py :
Google Vids(vids.google.com)에 원클릭 임포트할 수 있는 91씬 전체 CSV 스토리보드 생성기
- 컬럼: Scene, Start_Time, End_Time, Speaker, Script, Stock_Video_Search_Keyword, Visual_Prompt
- 토큰 소모량: 0
"""

import os
import sys
import json
import csv

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")

json_file = os.path.join(RESULT_DIR, "[022]_episode_02_k_space_scenes_metadata.json")
if not os.path.exists(json_file):
    json_file = os.path.join(RESULT_DIR, "[020]_episode_02_k_space_scenes.json")

with open(json_file, "r", encoding="utf-8") as f:
    scenes = json.load(f)

csv_path = os.path.join(RESULT_DIR, "[065]_GOOGLE_VIDS_STORYBOARD_IMPORT.csv")

def get_stock_keyword(sc):
    char = sc["character"]
    scene_id = sc["scene_id"]

    if char in ["강수연", "최영목", "빅터"]:
        if scene_id >= 70:
            return "mission control engineers celebration applause success"
        return "flight controllers mission control room discussion monitors wide"
    elif char in ["윤선아"]:
        return "launch control firing room engineers computer console working"
    elif char in ["박준서"]:
        if scene_id <= 25:
            return "astronaut in cockpit space shuttle helmet visor operating controls"
        elif scene_id <= 45:
            return "astronaut spacewalk earth background iss floating exterior"
        elif scene_id <= 70:
            return "astronaut walking on moon surface apollo lunar lander"
        else:
            return "astronaut helmet gold visor reflection looking at mars planet"
    elif char in ["김태훈"]:
        if scene_id <= 45:
            return "astronaut flight deck copilot communicating headset"
        elif scene_id <= 65:
            return "astronaut looking out window earth moon cupola"
        else:
            return "astronaut driving lunar rover vehicle on moon dust"
    elif char in ["어머니", "민재"]:
        return "crowd watching rocket launch family looking at sky hopeful"

    # 해설 및 세종 AI
    if scene_id <= 13:
        return "massive rocket on launch pad coastal fog sunrise slow motion"
    elif scene_id <= 20:
        return "rocket launch liftoff fiery flame smoke high speed camera 4k"
    elif scene_id <= 25:
        return "earth orbit view blue planet horizon satellite separation"
    elif scene_id <= 40:
        return "deep space spaceship moving stars nebula galaxy"
    elif scene_id <= 60:
        return "orbiting moon craters flyover lunar surface space probe"
    elif scene_id <= 70:
        return "lunar lander descent engine dust blowing touchdown moon"
    elif scene_id <= 80:
        return "solar flare coronal mass ejection space radiation sun satellite"
    else:
        return "mars planet red dunes dust horizon perseverance rover moving"

fieldnames = ["Scene_ID", "Start_Sec", "End_Sec", "Speaker", "Script_KR", "Google_Vids_Stock_Video_Keyword"]

with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for sc in scenes:
        writer.writerow({
            "Scene_ID": sc["scene_id"],
            "Start_Sec": sc["start"],
            "End_Sec": sc["end"],
            "Speaker": sc["character"],
            "Script_KR": sc["text"].replace("\n", " ").strip(),
            "Google_Vids_Stock_Video_Keyword": get_stock_keyword(sc)
        })

print(f"[SUCCESS] Google Vids 91씬 전체 CSV 스토리보드 생성 완료: {csv_path} ({len(scenes)}개 씬)")
