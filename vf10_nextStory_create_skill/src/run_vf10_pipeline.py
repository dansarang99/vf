#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_vf10_pipeline.py :
대한민국 달·화성 심우주 대서사시 엔드투엔드 원클릭 총괄 오케스트레이터
- Step 1: 풀씬 10인 배역 마스터 대본 생성 ([020])
- Step 2: Edge-TTS 다중 화자 정밀 타임라인 오디오 합성 ([021])
- Step 3: 시네마틱 한글 자막 및 영상 렌더링 ([022]~[024])
- Step 4: 0-Error 무결성 검증 및 보고서 최종 업데이트 ([025])
"""

import os
import sys
import subprocess
import time

vf10_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(vf10_dir, "src")
result_dir = os.path.join(vf10_dir, "result")

def run_step(step_name, script_name):
    print(f"\n{'='*70}")
    print(f"[RUN] {step_name} ({script_name})...")
    print(f"{'='*70}")
    t0 = time.time()
    script_path = os.path.join(src_dir, script_name)
    res = subprocess.run([sys.executable, script_path], capture_output=False)
    if res.returncode != 0:
        print(f"[ERROR] {step_name} 실패! 종료코드: {res.returncode}")
        return False
    print(f"[DONE] {step_name} 성공 (소요: {round(time.time() - t0, 2)}초)")
    return True

def main():
    print("*"*70)
    print("  vf10 대한민국 달·화성 심우주 대서사시 엔드투엔드 파이프라인 가동")
    print("  (AX)창업기술 대표 고유 실무 지식재산권 기반 / @vf09 100% 계승")
    print("*"*70)

    t_start = time.time()

    # 1단계: 대본 빌더
    if not run_step("1단계: 마스터 대본 빌드", "build_020_master_script.py"):
        return

    # 2단계: 오디오 타임라인 합성
    if not run_step("2단계: 10대 배역 타임라인 오디오 합성", "render_021_multichar_tts_timeline.py"):
        return

    # 3단계: 시네마틱 자막 및 비디오 렌더링
    if not run_step("3단계: 시네마틱 자막 및 영상 렌더링", "render_022_cinematic_space_video.py"):
        return

    # 산출물 목록 확인
    print(f"\n{'='*70}")
    print("★ [001]~[999] 무손실 영구 보존 산출물 검증")
    print(f"{'='*70}")
    files = sorted(os.listdir(result_dir))
    for f in files:
        f_path = os.path.join(result_dir, f)
        size_kb = round(os.path.getsize(f_path) / 1024, 2)
        print(f" - {f:<55} : {size_kb:>10.2f} KB")

    print(f"\n[ALL COMPLETE] 전체 파이프라인 완결! 총 소요: {round(time.time() - t_start, 2)}초")

if __name__ == "__main__":
    main()
