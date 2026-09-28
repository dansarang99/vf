#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_022_space_visual_assets.py :
제2탄 전용 10대 K-우주(달·화성·발사체·착륙선) 고해상도 시네마틱 비주얼 에셋 생성기
- 1편(항공기) 영상 0% 배제! 100% 제2탄 달·화성·우주 테마 비주얼 탑재
- 10대 핵심 씬별 고해상도(720x1280 9:16) 시네마틱 그래픽 생성
  1. 나로우주센터 발사대 & 카운트다운 (KASA Naro Space Center)
  2. KSLV-III 차세대 발사체 500톤 메탄 엔진 점화 & 화염 (Liftoff Flame)
  3. 지구 저궤도 250km 블루 오빗 & 페어링 분리 (Blue Earth Orbit)
  4. 심우주 TLI(달 전이 궤도) 은하수 & 성운 (Trans-Lunar Injection)
  5. 우주 파편군(Debris) 충돌 회피 & 펄스 RCS 기동 (Debris Avoidance)
  6. 달 극궤도 진입 & 크레이터 지형 (Lunar Polar Orbit)
  7. 달 남극 섀클턴 크레이터(Shackleton Crater) 역추진 하강 (Descent Thrusters)
  8. 달 표면 태극기 안착 & 탐사 로버 '해치' (Lunar Base & Haechi Rover)
  9. 태양 플레어 폭풍 & 양성자 방사선 비상 (Solar Flare Storm)
  10. 붉은 행성 화성(Mars) 지평선 & 천명-1호 레이저 교신 (Towards Mars)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

vf10_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scratch_dir = os.path.join(vf10_dir, "scratch", "space_footage")
os.makedirs(scratch_dir, exist_ok=True)

WIDTH, HEIGHT = 720, 1280

def create_base_canvas(color_top, color_bot):
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color_top[0] * (1 - ratio) + color_bot[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bot[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bot[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img

def draw_stars(draw, count=150, seed=42):
    import random
    random.seed(seed)
    for _ in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        brightness = random.randint(140, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])
        draw.ellipse([x, y, x + size, y + size], fill=(brightness, brightness, brightness))

def draw_hud_overlay(draw, act_title, telemetry_text, time_tag="2032.10.15 KASA"):
    # 상단 HUD
    draw.rectangle([20, 40, WIDTH - 20, 125], outline=(0, 200, 255), width=2)
    draw.text((40, 50), "KOREA AEROSPACE ADMINISTRATION // KASA DSOC", fill=(0, 220, 255))
    draw.text((40, 75), f"MISSION: {act_title}", fill=(255, 255, 255))
    draw.text((WIDTH - 240, 75), time_tag, fill=(0, 255, 180))

    # 조준선 & 레티클
    draw.line([(WIDTH // 2 - 40, HEIGHT // 2), (WIDTH // 2 + 40, HEIGHT // 2)], fill=(0, 255, 200), width=1)
    draw.line([(WIDTH // 2, HEIGHT // 2 - 40), (WIDTH // 2, HEIGHT // 2 + 40)], fill=(0, 255, 200), width=1)
    draw.ellipse([WIDTH // 2 - 70, HEIGHT // 2 - 70, WIDTH // 2 + 70, HEIGHT // 2 + 70], outline=(0, 255, 200), width=1)

    # 하단 텔레메트리 박스
    draw.rectangle([20, HEIGHT - 230, WIDTH - 20, HEIGHT - 150], outline=(0, 180, 255), width=1)
    draw.text((40, HEIGHT - 210), telemetry_text, fill=(200, 240, 255))

THEMES = [
    {
        "id": 1,
        "name": "01_naro_launchpad",
        "title": "ACT 1 // NARO SPACE CENTER // KSLV-III PAD",
        "telemetry": "SYS: KSLV-III STAGE-1 PRE-IGNITION // CH4/LOX 500tf // GO FOR LAUNCH",
        "top": (10, 15, 35), "bot": (40, 20, 10),
        "draw_func": lambda d: (
            d.rectangle([WIDTH//2 - 25, 250, WIDTH//2 + 25, 950], fill=(220, 225, 235), outline=(100, 110, 130), width=2),
            d.polygon([(WIDTH//2 - 25, 250), (WIDTH//2 + 25, 250), (WIDTH//2, 170)], fill=(240, 245, 255)),
            d.line([(WIDTH//2 + 40, 200), (WIDTH//2 + 40, 1000)], fill=(200, 70, 50), width=8),
            d.line([(WIDTH//2 + 40, 300), (WIDTH//2 + 10, 300)], fill=(200, 70, 50), width=4),
            d.line([(WIDTH//2 + 40, 500), (WIDTH//2 + 15, 500)], fill=(200, 70, 50), width=4),
            d.ellipse([WIDTH//2 - 12, 450, WIDTH//2 + 12, 474], fill=(200, 30, 30))
        )
    },
    {
        "id": 2,
        "name": "02_liftoff_flame",
        "title": "ACT 1 // LIFTOFF & MAX-Q // 500tf IGNITION",
        "telemetry": "ALT: 18.4km // VEL: MACH 2.4 // P: MAX-Q PASS // VIB: NORMAL",
        "top": (15, 20, 50), "bot": (180, 70, 10),
        "draw_func": lambda d: (
            d.rectangle([WIDTH//2 - 20, 180, WIDTH//2 + 20, 680], fill=(240, 240, 250)),
            d.polygon([(WIDTH//2 - 20, 180), (WIDTH//2 + 20, 180), (WIDTH//2, 110)], fill=(255, 255, 255)),
            d.polygon([(WIDTH//2 - 30, 680), (WIDTH//2 + 30, 680), (WIDTH//2, 1050)], fill=(255, 200, 50)),
            d.polygon([(WIDTH//2 - 18, 680), (WIDTH//2 + 18, 680), (WIDTH//2, 920)], fill=(255, 255, 200)),
            d.polygon([(WIDTH//2 - 45, 750), (WIDTH//2 + 45, 750), (WIDTH//2, 1180)], fill=(255, 90, 20))
        )
    },
    {
        "id": 3,
        "name": "03_earth_orbit",
        "title": "ACT 1 // LOW EARTH ORBIT // 250km INJECTION",
        "telemetry": "ALT: 250.2km // VEL: 7.78 km/s // FAIRING: JETTISONED // SOLAR: 100%",
        "top": (5, 8, 20), "bot": (10, 60, 140),
        "draw_func": lambda d: (
            d.ellipse([-200, 750, WIDTH + 200, 1600], fill=(20, 80, 180), outline=(100, 200, 255), width=4),
            d.ellipse([-150, 780, WIDTH + 150, 1550], fill=(15, 60, 150)),
            d.arc([-210, 740, WIDTH + 210, 1610], start=200, end=340, fill=(120, 230, 255), width=6),
            d.rectangle([WIDTH//2 - 30, 380, WIDTH//2 + 30, 500], fill=(230, 235, 245)),
            d.rectangle([WIDTH//2 - 140, 425, WIDTH//2 - 35, 455], fill=(20, 40, 120), outline=(0, 200, 255), width=2),
            d.rectangle([WIDTH//2 + 35, 425, WIDTH//2 + 140, 455], fill=(20, 40, 120), outline=(0, 200, 255), width=2)
        )
    },
    {
        "id": 4,
        "name": "04_tli_nebula",
        "title": "ACT 2 // TRANS-LUNAR INJECTION // 380,000km",
        "telemetry": "TRAJECTORY: EARTH-MOON TRANSFER // DV: +3.15 km/s // DIST: 124,000km",
        "top": (8, 5, 25), "bot": (20, 10, 45),
        "draw_func": lambda d: (
            d.ellipse([100, 300, 620, 700], fill=(50, 20, 80), outline=(120, 50, 180)),
            d.ellipse([200, 380, 520, 620], fill=(70, 30, 110)),
            d.polygon([(WIDTH//2, 420), (WIDTH//2 - 25, 490), (WIDTH//2 + 25, 490)], fill=(240, 245, 255)),
            d.line([(WIDTH//2, 490), (WIDTH//2, 540)], fill=(0, 200, 255), width=3)
        )
    },
    {
        "id": 5,
        "name": "05_debris_avoidance",
        "title": "ACT 2 // EMERGENCY // DEBRIS COLLISION AVOIDANCE",
        "telemetry": "WARN: OBJECT 1974-082B // RANGE: 820m // RCS PULSE: MANUAL ACTIVE",
        "top": (25, 10, 15), "bot": (15, 8, 20),
        "draw_func": lambda d: (
            d.rectangle([40, 220, WIDTH - 40, 300], outline=(255, 50, 50), width=3),
            d.text((WIDTH//2 - 130, 245), "COLLISION ALERT // 85 SEC", fill=(255, 70, 70)),
            d.polygon([(200, 480), (280, 450), (310, 520), (230, 560)], fill=(120, 110, 100), outline=(255, 80, 80), width=2),
            d.line([(WIDTH//2 + 20, 520), (WIDTH//2 + 70, 500)], fill=(100, 230, 255), width=3)
        )
    },
    {
        "id": 6,
        "name": "06_lunar_orbit",
        "title": "ACT 3 // LUNAR POLAR ORBIT // ALT 100km",
        "telemetry": "ORBIT: 100x100km POLAR // TARGET: SHACKLETON CRATER // GNC: LOCKED",
        "top": (4, 6, 15), "bot": (25, 30, 40),
        "draw_func": lambda d: (
            d.ellipse([50, 600, WIDTH + 300, 1400], fill=(160, 165, 175), outline=(220, 225, 230), width=3),
            d.ellipse([200, 750, 360, 850], outline=(100, 105, 115), fill=(130, 135, 145), width=2),
            d.ellipse([420, 820, 520, 890], outline=(100, 105, 115), fill=(130, 135, 145), width=2),
            d.ellipse([180, 930, 320, 1010], outline=(90, 95, 105), fill=(110, 115, 125), width=2),
            d.rectangle([WIDTH//2 - 20, 360, WIDTH//2 + 20, 430], fill=(240, 245, 255)),
            d.rectangle([WIDTH//2 - 90, 385, WIDTH//2 - 25, 405], fill=(20, 50, 140)),
            d.rectangle([WIDTH//2 + 25, 385, WIDTH//2 + 90, 405], fill=(20, 50, 140))
        )
    },
    {
        "id": 7,
        "name": "07_shackleton_landing",
        "title": "ACT 3 // SHACKLETON CRATER // DESCENT 500m",
        "telemetry": "ALT: 480m // VERT VEL: -12.4 m/s // NOZZLE 2: MANUAL TRIM ACTIVE",
        "top": (10, 12, 22), "bot": (15, 18, 25),
        "draw_func": lambda d: (
            d.polygon([(0, 800), (250, 680), (500, 720), (WIDTH, 650), (WIDTH, HEIGHT), (0, HEIGHT)], fill=(60, 65, 75)),
            d.polygon([(150, 820), (350, 750), (WIDTH, 780), (WIDTH, HEIGHT), (150, HEIGHT)], fill=(25, 28, 35)),
            d.rectangle([WIDTH//2 - 35, 400, WIDTH//2 + 35, 470], fill=(230, 235, 245)),
            d.line([(WIDTH//2 - 35, 470), (WIDTH//2 - 60, 520)], fill=(180, 185, 195), width=4),
            d.line([(WIDTH//2 + 35, 470), (WIDTH//2 + 60, 520)], fill=(180, 185, 195), width=4),
            d.polygon([(WIDTH//2 - 20, 470), (WIDTH//2 + 20, 470), (WIDTH//2, 590)], fill=(100, 200, 255))
        )
    },
    {
        "id": 8,
        "name": "08_lunar_surface_korea",
        "title": "ACT 3 // TOUCHDOWN CONFIRMED // KOREA LUNAR BASE",
        "telemetry": "STATUS: LANDED // COORD: 89.9°S 0.0°E // RESOURCE: H2O & 3He DETECTED",
        "top": (2, 4, 10), "bot": (70, 75, 85),
        "draw_func": lambda d: (
            d.rectangle([0, 700, WIDTH, HEIGHT], fill=(130, 135, 145)),
            d.rectangle([WIDTH//2 - 50, 560, WIDTH//2 + 50, 700], fill=(240, 245, 255), outline=(180, 185, 195), width=2),
            d.line([(WIDTH//2 - 50, 700), (WIDTH//2 - 80, 760)], fill=(150, 155, 165), width=5),
            d.line([(WIDTH//2 + 50, 700), (WIDTH//2 + 80, 760)], fill=(150, 155, 165), width=5),
            d.line([(WIDTH//2 - 120, 620), (WIDTH//2 - 120, 760)], fill=(220, 220, 220), width=4),
            d.rectangle([WIDTH//2 - 120, 620, WIDTH//2 - 55, 665], fill=(255, 255, 255), outline=(100, 100, 100), width=1),
            d.ellipse([WIDTH//2 - 95, 633, WIDTH//2 - 80, 652], fill=(220, 20, 20)),
            d.rectangle([WIDTH//2 + 80, 720, WIDTH//2 + 150, 760], fill=(200, 180, 50)),
            d.ellipse([WIDTH//2 + 85, 755, WIDTH//2 + 100, 770], fill=(50, 50, 50)),
            d.ellipse([WIDTH//2 + 130, 755, WIDTH//2 + 145, 770], fill=(50, 50, 50))
        )
    },
    {
        "id": 9,
        "name": "09_solar_flare_crisis",
        "title": "ACT 4 // SOLAR PROTON STORM // SPE LEVEL X-9",
        "telemetry": "ALERT: CME IMPACT // MARS PROBE COMM DOWN // EMERGENCY LASER PATCH",
        "top": (50, 15, 10), "bot": (150, 50, 10),
        "draw_func": lambda d: (
            d.ellipse([WIDTH - 150, -100, WIDTH + 300, 350], fill=(255, 200, 20), outline=(255, 80, 10), width=8),
            d.arc([WIDTH - 250, -150, WIDTH + 400, 450], start=100, end=240, fill=(255, 50, 0), width=12),
            d.line([(0, 450), (WIDTH, 520)], fill=(255, 120, 30), width=2),
            d.line([(0, 550), (WIDTH, 620)], fill=(255, 120, 30), width=2),
            d.line([(100, 750), (WIDTH - 100, 250)], fill=(0, 255, 200), width=4)
        )
    },
    {
        "id": 10,
        "name": "10_towards_mars",
        "title": "ACT 4 // TOWARDS THE RED PLANET // MARS 2045",
        "telemetry": "CHEONMYEONG-1: REBOOT OK // NEXT DESTINATION: MARS // WE WILL RETURN",
        "top": (10, 5, 15), "bot": (100, 30, 20),
        "draw_func": lambda d: (
            d.ellipse([WIDTH//2 - 220, 450, WIDTH//2 + 220, 890], fill=(190, 60, 30), outline=(230, 90, 40), width=3),
            d.ellipse([WIDTH//2 - 160, 520, WIDTH//2 - 40, 600], fill=(150, 40, 20)),
            d.ellipse([WIDTH//2 - 50, 640, WIDTH//2 + 140, 700], fill=(130, 35, 15)),
            d.line([(WIDTH//2, 180), (WIDTH//2, 380)], fill=(255, 230, 180), width=2),
            d.rectangle([WIDTH//2 - 25, 280, WIDTH//2 + 25, 330], fill=(230, 240, 255)),
            d.rectangle([WIDTH//2 - 80, 298, WIDTH//2 - 30, 312], fill=(20, 60, 160)),
            d.rectangle([WIDTH//2 + 30, 298, WIDTH//2 + 80, 312], fill=(20, 60, 160))
        )
    }
]

def generate_all_images():
    print(f"[RUN] 10대 K-우주(달·화성·나로) 고해상도 시네마틱 이미지 생성 시작...")
    generated = []
    for t in THEMES:
        img_path = os.path.join(scratch_dir, f"{t['name']}.png")
        canvas = create_base_canvas(t["top"], t["bot"])
        draw = ImageDraw.Draw(canvas)
        draw_stars(draw, count=130, seed=t["id"] * 29)
        t["draw_func"](draw)
        draw_hud_overlay(draw, t["title"], t["telemetry"])
        canvas.save(img_path)
        generated.append(img_path)
        print(f" - {t['name']}.png 생성 완료")
    print("[SUCCESS] 10대 우주 비주얼 이미지 생성 완료!")
    return generated

if __name__ == "__main__":
    generate_all_images()
