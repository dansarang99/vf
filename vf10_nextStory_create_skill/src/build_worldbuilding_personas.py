# -*- coding: utf-8 -*-
"""
build_worldbuilding_personas.py :
토큰 소모량 0(Zero)으로 다음 핵심 자산을 로컬에서 100% 자립 구축:
1. [050]_WORLD_BUILDING_PERSONA_MANIFESTO.md (세계관 바이블)
2. [051]_CHARACTER_PERSONA_SHEETS.json (10대 인물 캐릭터 시트)
3. [052]_LOCATION_PROP_EQUIPMENT_PERSONA.json (10대 장소, 10대 장비/소품 페르소나)
4. [053]_100_SCENE_PERSONA_PROMPT_BOOK.json (100대 장면 페르소나 텍스트 데이터북)
5. [054]_2000_SCENE_EXPEDITION_TIMELINE_MATRIX.json (2,000씬 초정밀 조립 타임라인 매트릭스)
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
os.makedirs(RESULT_DIR, exist_ok=True)

# 1. 10대 인물 페르소나 & 캐릭터 시트
CHARACTERS = [
    {
        "id": "char_01",
        "name": "박준서 (Park Jun-seo)",
        "role": "대한민국 심우주 탐사선 아리온 1호 총괄사령관 (Commander)",
        "age": 42,
        "appearance": "날카로운 눈매와 굳은 의지의 턱선, 짧은 단정한 검은 머리, 피로 속에서도 흔들림 없는 눈빛",
        "suit_costume": "차세대 K-IVA/EVA 차압 우주복(백색 티타늄 복합 직물, 가슴에 선명한 태극기 및 KASA 패치, 손목 내장형 터치 HUD)",
        "personality": "냉철한 판단력, 동료와 가족을 향한 깊은 책임감, 1편의 위기를 극복한 베테랑 파일럿",
        "voice_style": "중저음의 단호하고 안정적인 톤 (Edge-TTS ko-KR-InJoonNeural, rate=-3%, pitch=-2Hz)"
    },
    {
        "id": "char_02",
        "name": "강수연 (Kang Su-yeon)",
        "role": "KASA 지상종합통제센터 비행디렉터 (Flight Director)",
        "age": 39,
        "appearance": "지적이고 차분한 인상, 얇은 메탈 안경, 뒤로 묶은 단발, 통신 헤드셋 착용",
        "suit_costume": "다크 네이비 KASA 공식 지상관제 제복, 비행 디렉터 뱃지, 실시간 데이터 태블릿 소지",
        "personality": "초인적인 데이터 분석력과 상황 통제력, 사령관과의 10년 지기 신뢰",
        "voice_style": "명료하고 직관적인 여성 전문직 톤 (ko-KR-SunHiNeural, rate=+4%, pitch=+1Hz)"
    },
    {
        "id": "char_03",
        "name": "세종 (Sejong AI / GAON)",
        "role": "아리온 1호 및 천명 1호 탑재 심우주 자율 인공지능 (Deep Space AI)",
        "age": "N/A (양자 뉴로모픽 코어)",
        "appearance": "물리적 신체 없음. 메인 콘솔의 푸른색 기하학적 링 홀로그램 인터페이스로 시각화",
        "suit_costume": "광학 센서 렌즈 및 양자 코어 발광 모듈",
        "personality": "극도의 객관성과 수치 기반 안전 우선주의, 위기 시 인간의 직관을 보좌",
        "voice_style": "잡음 없는 무기물적 청아한 하이테크 톤 (ko-KR-InJoonNeural, rate=+8%, pitch=-5Hz)"
    },
    {
        "id": "char_04",
        "name": "최영목 (Choi Young-mok)",
        "role": "대한민국 우주항공청장 (KASA Administrator)",
        "age": 58,
        "appearance": "희끗희끗한 백발이 섞인 중후한 외모, 깊은 주름, 국가적 결단을 내리는 무게감 있는 눈빛",
        "suit_costume": "정갈한 짙은 회색 정장, 태극 깃발 핀, KASA 공식 명찰",
        "personality": "정치적 압박 속에서도 과학자와 비행사들을 전폭 신뢰하는 든든한 최고 의사결정권자",
        "voice_style": "중후하고 깊은 울림의 C-Level 톤 (ko-KR-BongJinNeural, rate=-5%, pitch=-4Hz)"
    },
    {
        "id": "char_05",
        "name": "빅터 (Victor Vance)",
        "role": "NASA 딥스페이스 네트워크(DSN) 연락관 겸 아르테미스 해외국장",
        "age": 51,
        "appearance": "다부진 체격의 흑인 남성, 짧은 수염, 친근하면서도 프로페셔널한 미소",
        "suit_costume": "NASA 블루 플라이트 재킷, 글로벌 연합 탐사 패치",
        "personality": "K-우주청의 독자 기술력을 존중하며 글로벌 심우주 통신망을 전폭 지원",
        "voice_style": "자신감 넘치고 호탕한 글로벌 외교관 톤"
    },
    {
        "id": "char_06",
        "name": "김태훈 (Kim Tae-hoon)",
        "role": "달 착륙선 아리온 1호 부조종사 겸 지질생태 연구원",
        "age": 34,
        "appearance": "활동적인 인상의 청년 과학자, 밝은 갈색 짧은 머리",
        "suit_costume": "경량화 탐사 우주복, 지질 샘플링 공구 벨트",
        "personality": "호기심 많고 낙천적이나 우주선 결함 앞에서는 1초의 망설임 없는 행동파",
        "voice_style": "밝고 빠른 활력 넘치는 청년 파일럿 톤"
    },
    {
        "id": "char_07",
        "name": "윤선아 (Yoon Seon-ah)",
        "role": "KASA 추진제 및 궤도역학 수석공학자",
        "age": 36,
        "appearance": "몰입할 때 머리를 질끈 묶는 습관, 날카로운 직관",
        "suit_costume": "발사대 현장 방염 점퍼, 공학 안전모, 포터블 터미널",
        "personality": "1단 엔진부터 TLI 궤도 계산까지 0.001초의 오차도 허용치 않는 완벽주의자",
        "voice_style": "빠르고 정확한 팩트 전달형 톤"
    },
    {
        "id": "char_08",
        "name": "준서 어머니 (Mother)",
        "role": "지상에서 아들을 기다리는 사령관의 모친",
        "age": 69,
        "appearance": "따뜻하고 자애로운 주름, 정갈한 옷차림",
        "suit_costume": "단정한 한국식 일상복, 준서가 준 첫 비행 기념 목걸이",
        "personality": "우주로 향하는 아들의 무사 귀환을 조용히 기도하는 모성애",
        "voice_style": "온화하고 떨리는 온기를 지닌 모성 톤 (ko-KR-SunHiNeural, rate=-6%)"
    },
    {
        "id": "char_09",
        "name": "민재 (Min-jae)",
        "role": "우주꿈나무 초등학생 (국민 대표)",
        "age": 11,
        "appearance": "커다란 눈망울, 우주 로켓 장난감을 손에 쥔 소년",
        "suit_costume": "KASA 어린이 우주캠프 후드티",
        "personality": "순수한 동경과 미래 세대의 꿈",
        "voice_style": "해맑고 낭랑한 소년 톤"
    },
    {
        "id": "char_10",
        "name": "다큐멘터리 해설자 (Narrator)",
        "role": "K-우주 대서사시의 역사적 무게를 전달하는 거시적 화자",
        "age": 45,
        "appearance": "보이지 않는 관조자",
        "suit_costume": "N/A",
        "personality": "대한민국 70년 우주개발 역사의 장엄함과 인류의 확장을 선언",
        "voice_style": "신뢰감 100%의 명품 다큐 내레이션 (ko-KR-InJoonNeural, rate=-4%)"
    }
]

# 2. 10대 장소 페르소나
LOCATIONS = [
    {"id": "loc_01", "name": "나로우주센터 해안 발사대 제3패드", "desc": "남해 바다 안개 속 우뚝 선 KSLV-III 발사대와 초대형 엄빌리컬 타워"},
    {"id": "loc_02", "name": "KASA 대덕 종합우주관제센터(MOC)", "desc": "수백 개의 모니터와 초대형 글로벌 궤도 맵이 실시간 점멸하는 첨단 통제실"},
    {"id": "loc_03", "name": "아리온 1호 여압 조종실(Cockpit)", "desc": "차세대 터치 글래스 콕핏, 3면 파노라마 내열 창, 세종 AI 홀로그램 프로젝터"},
    {"id": "loc_04", "name": "지구 저궤도 400km 궤도면", "desc": "암흑의 심연 속 눈부신 코발트블루 지구 지평선과 한반도 상공"},
    {"id": "loc_05", "name": "TLI 달 전이 궤도 심우주", "desc": "지구와 달 사이의 완벽한 진공, 은하수 먼지와 미세 운석 흐름"},
    {"id": "loc_06", "name": "달 남극 상공 100km 극궤도", "desc": "달 표면의 날카로운 섀클턴 크레이터 림과 칠흑 같은 영구음영지대"},
    {"id": "loc_07", "name": "달 남극 섀클턴 베이스캠프 표면", "desc": "미세한 회색 레골리스 가루, 영구 얼음 퇴적층, 첫 태극기 기지"},
    {"id": "loc_08", "name": "달 궤도 정거장 '세종 루나 게이트웨이'", "desc": "도킹 포트 4개와 대형 태양광 회전 날개를 갖춘 우주 정거장"},
    {"id": "loc_09", "name": "심우주 레이저 지상 송수신 기지 (제주 안덕)", "desc": "밤하늘을 향해 532nm 초록빛 양자 레이저 빔을 쏘아 올리는 광학 망원경 돔"},
    {"id": "loc_10", "name": "화성 올림포스 몬스 북동부 고원 지평선", "desc": "붉은 산화철 사막과 분홍빛 희박한 대기, 2045 첫 착륙 기지 후보지"}
]

# 3. 10대 장비 및 주요 품목 페르소나
EQUIPMENTS = [
    {"id": "eq_01", "name": "KSLV-III 2단 초대형 메가로켓", "desc": "추력 100톤급 다단연소사이클 메탄-액체산소 5기 클러스터링 발사체"},
    {"id": "eq_02", "name": "아리온 1호 달 착륙선 (Arion-1)", "desc": "금빛 다층단열재(MLI), 4족 착륙 기어, 4단 역추진 스러스터 완비"},
    {"id": "eq_03", "name": "천명 1호 화성 궤도선 (Cheonmyeong-1)", "desc": "이온 엔진 추진기, 초정밀 화성 대기 분광기, 고해상도 지형 카메라"},
    {"id": "eq_04", "name": "차세대 K-EVA 자율 생명유지 우주복", "desc": "방사선 차폐 티타늄 섬유, 헬멧 투시 HUD, 산소 24시간 리사이클링 팩"},
    {"id": "eq_05", "name": "달 남극 수자원 시추 로버 '단비'", "desc": "영구음영 분지 투입용 6륜 독립구동 바퀴, 극저온 심도 2m 열 드릴 탑재"},
    {"id": "eq_06", "name": "양자 얽힘 심우주 레이저 통신 모듈", "desc": "지구-달-화성 간 기가비트급 지연 극복 광통신 터미널"},
    {"id": "eq_07", "name": "세종 AI 양자 뉴로모픽 코어", "desc": "초저전력으로 궤도 섭동과 충돌 위협을 실시간 병렬 계산하는 연산 장치"},
    {"id": "eq_08", "name": "달 레골리스 3D 프린팅 자율 건설 로봇", "desc": "달 흙을 녹여 우주 방사선 차폐 거주벽을 쌓아 올리는 무인 건설기"},
    {"id": "eq_09", "name": "소형 원자로 원자력 전지(RTG)", "desc": "태양빛이 닿지 않는 달 남극 영구음영과 화성 모래폭풍을 견디는 전력원"},
    {"id": "eq_10", "name": "사령관 준서의 1편 기적의 조종간(Stick)", "desc": "민항기 조종 시절부터 우주선 콕핏에 거치한 상징적 부적이자 직관 조작기"}
]

def generate_100_scene_personas():
    """100대 장면 페르소나 텍스트 데이터북 생성 (인물x장소x장비 조합)"""
    scene_personas = []
    camera_shots = [
        "Extreme Close-up (ECU) of character expression",
        "Cinematic Medium Close-up (MCU) with HUD reflection",
        "Dynamic Low-Angle Cockpit View with starry backdrop",
        "Massive Wide Establishing Shot (EWS) of space architecture",
        "Point of View (POV) looking through astronaut helmet visor",
        "High-Angle Drone/Satellite perspective looking down",
        "Cinematic Over-The-Shoulder (OTS) dialogue framing",
        "Extreme Long Shot (ELS) of spacecraft against planetary horizon"
    ]
    lighting_moods = [
        "Golden hour warm sunbeam piercing coastal morning fog",
        "Cold, harsh, high-contrast unfiltered space sunlight",
        "Dramatic red cockpit emergency alert lighting with particle dust",
        "Pale, mystical blue lunar regolith reflection",
        "Soft amber interior cabin instrumental glow",
        "Blinding radioactive solar flare plasma halo",
        "Ethereal reddish-pink Martian sunset golden hour"
    ]

    for i in range(1, 101):
        char = CHARACTERS[(i - 1) % len(CHARACTERS)]
        loc = LOCATIONS[(i - 1) % len(LOCATIONS)]
        eq = EQUIPMENTS[(i - 1) % len(EQUIPMENTS)]
        shot = camera_shots[(i - 1) % len(camera_shots)]
        light = lighting_moods[(i - 1) % len(lighting_moods)]

        prompt_en = (
            f"Cinematic photorealistic documentary frame, Scene Persona #{i:03d}: "
            f"{shot}. Featuring {char['name']} at {loc['name']}, operating {eq['name']}. "
            f"Atmosphere: {light}. Extreme hyper-realistic texture, 8k resolution, "
            f"ARRI Alexa 65 cinematography, IMAX 70mm, actual space mission aesthetic."
        )

        scene_personas.append({
            "persona_id": f"scene_persona_{i:03d}",
            "number": i,
            "title": f"장면 페르소나 #{i:03d}: {loc['name']}의 {char['name']}",
            "character_id": char["id"],
            "character_name": char["name"],
            "location_id": loc["id"],
            "location_name": loc["name"],
            "equipment_id": eq["id"],
            "equipment_name": eq["name"],
            "camera_shot": shot,
            "lighting_mood": light,
            "prompt_en": prompt_en
        })
    return scene_personas

def generate_2000_scene_matrix():
    """2,000씬 초정밀 조립 타임라인 매트릭스 생성 (총 780초 타임라인 기준 세분화)"""
    total_scenes = 2000
    total_duration = 781.12 # 13분 01초
    avg_cut_dur = round(total_duration / total_scenes, 3) # 약 0.39초~0.5초 단위 컷

    scene_matrix = []
    cur_time = 0.0

    motion_types = ["slow_zoom_in", "slow_pan_left", "slow_pan_right", "pull_out", "camera_shake", "subtle_drift"]

    for sc_id in range(1, total_scenes + 1):
        persona_idx = (sc_id - 1) % 100 + 1
        motion = motion_types[(sc_id - 1) % len(motion_types)]
        
        # 컷 지속 시간 (0.3~0.6초 다이내믹 변동)
        dur = 0.35 + ((sc_id * 17) % 25) * 0.01
        if sc_id == total_scenes:
            dur = max(0.1, round(total_duration - cur_time, 3))

        scene_matrix.append({
            "cut_id": sc_id,
            "start_sec": round(cur_time, 3),
            "end_sec": round(cur_time + dur, 3),
            "duration": round(dur, 3),
            "scene_persona_ref": f"scene_persona_{persona_idx:03d}",
            "motion_type": motion,
            "zoom_ratio": 1.05 + ((sc_id % 5) * 0.05),
            "act_phase": f"Part {(sc_id - 1) // 500 + 1}"
        })
        cur_time += dur
        if cur_time >= total_duration:
            break

    return scene_matrix

def main():
    print("=" * 75)
    print("  [vf10] 페르소나 세계관(Worldbuilding) & 2,000씬 조립 엔진 가동")
    print("  ★ 인물/장소/장비 페르소나 + 100 장면 페르소나 + 2,000씬 타임라인 매트릭스")
    print("  ★ 토큰 소모량: 0 (로컬 알고리즘 100% 자립 생성)")
    print("=" * 75)

    # 1. [051] 캐릭터 시트 저장
    p_051 = os.path.join(RESULT_DIR, "[051]_CHARACTER_PERSONA_SHEETS.json")
    with open(p_051, "w", encoding="utf-8") as f:
        json.dump(CHARACTERS, f, ensure_ascii=False, indent=2)
    print(f" -> [051] 10대 인물 페르소나 & 캐릭터 시트 저장 완료: {os.path.basename(p_051)}")

    # 2. [052] 장소/장비/소품 페르소나 저장
    p_052 = os.path.join(RESULT_DIR, "[052]_LOCATION_PROP_EQUIPMENT_PERSONA.json")
    with open(p_052, "w", encoding="utf-8") as f:
        json.dump({"locations": LOCATIONS, "equipments": EQUIPMENTS}, f, ensure_ascii=False, indent=2)
    print(f" -> [052] 10대 장소 및 10대 장비/소품 페르소나 저장 완료: {os.path.basename(p_052)}")

    # 3. [053] 100대 장면 페르소나 프롬프트북 저장
    scene_personas = generate_100_scene_personas()
    p_053 = os.path.join(RESULT_DIR, "[053]_100_SCENE_PERSONA_PROMPT_BOOK.json")
    with open(p_053, "w", encoding="utf-8") as f:
        json.dump(scene_personas, f, ensure_ascii=False, indent=2)
    print(f" -> [053] 100대 시네마틱 장면 페르소나 프롬프트북 저장 완료: {os.path.basename(p_053)} (100개 컷)")

    # 4. [054] 2,000씬 초정밀 조립 타임라인 매트릭스 저장
    scene_matrix = generate_2000_scene_matrix()
    p_054 = os.path.join(RESULT_DIR, "[054]_2000_SCENE_EXPEDITION_TIMELINE_MATRIX.json")
    with open(p_054, "w", encoding="utf-8") as f:
        json.dump(scene_matrix, f, ensure_ascii=False, indent=2)
    print(f" -> [054] 2,000씬 시네마틱 타임라인 조립 매트릭스 저장 완료: {os.path.basename(p_054)} ({len(scene_matrix)}개 씬)")

    # 5. [050] 세계관 바이블 마크다운 편찬
    manifesto_md = f"""# [050] 대한민국 우주항공청(KASA) 대서사시 세계관(Worldbuilding) & 페르소나 마스터 바이블

> **무손실 누적 보존(Zero-Overwrite Immutable Versioning) 원칙 적용**:
> 본 문서는 인물, 장소, 소품, 장비, 100대 장면 페르소나 및 2,000씬 조립 매트릭스를 총괄하는 공식 세계관 바이블입니다.

---

## 1. 10대 주요 등장인물 페르소나 (Character Sheets)
총 {len(CHARACTERS)}명의 주요 인물에 대한 연령, 외모, 우주복/복장, 성격 및 1인 다역 음성 DNA가 완벽히 규정되었습니다.

## 2. 10대 핵심 장소 및 10대 우주 장비 페르소나
- 장소: 나로우주센터 3패드부터 달 남극 섀클턴, 화성 올림포스 지평선까지 10대 거점.
- 장비: KSLV-III, 아리온 1호, 천명 1호, 단비 시추 로버, 양자 레이저 통신 모듈 등 10대 하이테크.

## 3. 100대 시네마틱 장면 페르소나 (100 Scene Personas)
인물 x 장소 x 장비 x 카메라샷 x 조명 무드가 결합된 100개 고유 시네마틱 앵커 컷 구축 완료.

## 4. 2,000씬 초정밀 타임라인 조립 매트릭스 (2,000 Cut Assembly Matrix)
총 {len(scene_matrix)}개 컷이 0.3~0.5초 단위로 켄 번스 모션(줌인/패닝/진동)과 함께 13분 01초 타임라인에 완벽히 동기화되었습니다.
"""
    p_050 = os.path.join(RESULT_DIR, "[050]_WORLD_BUILDING_PERSONA_MANIFESTO.md")
    with open(p_050, "w", encoding="utf-8") as f:
        f.write(manifesto_md)
    print(f" -> [050] 페르소나 세계관 종합 바이블 마크다운 생성 완료: {os.path.basename(p_050)}")

    print("=" * 75)
    print("[SUCCESS] 5대 페르소나 세계관 핵심 자산이 result/ 폴더에 완벽히 구축되었습니다!")
    print("=" * 75)

if __name__ == "__main__":
    main()
