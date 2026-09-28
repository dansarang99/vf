# -*- coding: utf-8 -*-
"""
run_zero_token_master.py :
AI 토큰 소비 완전 제로(Zero-Token) 대한민국 우주 대서사시 전편 총괄 오케스트레이터
- 외부 유료 LLM / API 호출 0회 (토큰 소모량: 0)
- 100% 로컬 CPU/GPU, Edge-TTS, NASA Open Data, FFmpeg, OpenCV 자립 구동
- 덮어쓰기 0% 무손실 불변 번호 체계([001]~[999]) 자동 연동
"""

import os
import sys
import time
import subprocess

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(VF10_DIR, "src")
RESULT_DIR = os.path.join(VF10_DIR, "result")

def print_banner():
    print("=" * 80)
    print("  🚀 [vf10] AI 토큰 소비 완전 제로(Zero-Token) 대한민국 우주 대서사시 오케스트레이터")
    print("  ★ 외부 유료 LLM API 호출: 0회 (비용 $0.00 / 토큰 소모: 0)")
    print("  ★ 100% 로컬 컴퓨팅 연산 기반 자립형 시네마틱 파이프라인")
    print("  ★ 덮어쓰기 0% 무손실 불변 번호 체계([001]~[999]) 영구 누적 보존")
    print("=" * 80)

def run_step(step_num, step_title, script_name, extra_args=None):
    script_path = os.path.join(SRC_DIR, script_name)
    cmd = [sys.executable, script_path]
    if extra_args:
        cmd.extend(extra_args)

    print(f"\n[{step_num}/5] {step_title} 시작...")
    print(f"      실행 파일: {script_name}")
    t0 = time.time()
    res = subprocess.run(cmd, cwd=VF10_DIR)
    elapsed = round(time.time() - t0, 2)
    if res.returncode != 0:
        print(f"[ERROR] {step_title} 실패! (종료 코드: {res.returncode})")
        return False
    print(f"[SUCCESS] {step_title} 완료! (소요 시간: {elapsed}초 / 토큰 소모: 0)")
    return True

def main():
    print_banner()
    total_t0 = time.time()

    # Step 1: 5대 페르소나 세계관(Worldbuilding) 및 2,000씬 매트릭스 빌드
    if not run_step(1, "5대 페르소나 세계관 및 2,000씬 타임라인 매트릭스 빌드", "build_worldbuilding_personas.py"):
        return

    # Step 2: 91개 씬 10대 배역 마스터 대본 생성
    if not run_step(2, "10대 배역 91씬 시네마틱 마스터 대본 빌드", "build_020_master_script.py"):
        return

    # Step 3: 24kHz 타임라인 정밀 동기화 오디오 합성
    if not run_step(3, "10인 배역 24kHz 타임라인 무손실 오디오 합성", "render_021_multichar_tts_timeline.py"):
        return

    # Step 4: 100% 실제 우주 촬영 실사 에셋 동기화
    if not run_step(4, "NASA 공인 실제 우주 촬영 실사 에셋 동기화", "fetch_nasa_api_photos.py"):
        return

    # Step 5: 100% 실제 우주 실사 시네마틱 비디오 렌더링
    if not run_step(5, "100% 실제 우주 실사 시네마틱 비디오 렌더링", "render_real_scene_video.py", ["--mode", "full"]):
        return

    total_elapsed = round(time.time() - total_t0, 2)

    # 산출물 목록 일람
    print("\n" + "=" * 80)
    print("  ★ [001]~[999] 무손실 불변 산출물 최종 보존 현황")
    print("=" * 80)
    files = sorted(os.listdir(RESULT_DIR))
    for f in files:
        fp = os.path.join(RESULT_DIR, f)
        size_kb = round(os.path.getsize(fp) / 1024, 2)
        if size_kb > 1024:
            s_str = f"{round(size_kb/1024, 2):>7.2f} MB"
        else:
            s_str = f"{size_kb:>7.2f} KB"
        print(f" - {f:<55} : {s_str}")

    print("=" * 80)
    print(f" [ALL COMPLETE] 전체 파이프라인 완결! (총 소요 시간: {total_elapsed}초 / 총 AI 토큰 소모량: 0)")
    print("=" * 80)

if __name__ == "__main__":
    main()
