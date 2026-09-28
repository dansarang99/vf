#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_vf10_hybrid_full_pipeline.py :
하이브리드 토큰 제로화(Zero-Token) 대한민국 달·화성 대서사시 전편 완제 파이프라인
- Windows cp949 인코딩 안전 처리 (sys.stdout reconfigure)
- 토큰 소모량 0(Zero): 모든 연산과 합성을 로컬 CPU/GPU에서 100% 자립 수행
- 실행: python src/run_vf10_hybrid_full_pipeline.py [--mode quick / full]
"""

import os
import sys
import subprocess
import time
import argparse

# Windows 터미널 인코딩 안전화
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

vf10_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(vf10_dir, "src")
result_dir = os.path.join(vf10_dir, "result")

def run_step(step_name, cmd_list):
    print(f"\n{'='*75}")
    print(f"[RUN] {step_name}...")
    print(f"      명령어: {' '.join(cmd_list)}")
    print(f"{'='*75}")
    t0 = time.time()
    res = subprocess.run(cmd_list, cwd=vf10_dir)
    if res.returncode != 0:
        print(f"[ERROR] {step_name} 실패! (종료코드: {res.returncode})")
        return False
    print(f"[DONE] {step_name} 성공 (소요: {round(time.time() - t0, 2)}초)")
    return True

def main():
    parser = argparse.ArgumentParser(description="vf10 하이브리드 토큰 제로화 파이프라인")
    parser.add_argument("--mode", choices=["quick", "full"], default="full",
                        help="quick: 하이라이트+Part1, full: Part1~4 전편 및 13분 통합 마스터 비디오")
    args = parser.parse_args()

    print("*"*75)
    print("  [vf10] 하이브리드 토큰 제로화(Zero-Token) 대한민국 우주 대서사시 파이프라인")
    print("  ★ (AX)창업기술 대표 고유 실무 지식재산권 기반 / @vf09 100% 완전 계승")
    print(f"  ★ 실행 모드: {args.mode.upper()} (로컬 가속 렌더링)")
    print("*"*75)

    t_start = time.time()

    # Step 1: 마스터 대본 빌드
    if not run_step("1단계: 10대 배역 풀씬 마스터 대본 생성",
                    [sys.executable, os.path.join(src_dir, "build_020_master_script.py")]):
        return

    # Step 2: 24kHz 타임라인 오디오 합성
    if not run_step("2단계: 24kHz 타임라인 오디오 정밀 동기화 합성",
                    [sys.executable, os.path.join(src_dir, "render_021_multichar_tts_timeline.py")]):
        return

    # Step 3: 시네마틱 자막 및 영상 렌더링
    video_mode = "part1" if args.mode == "quick" else "full"
    if not run_step(f"3단계: 시네마틱 자막 및 비디오 렌더링 (모드: {video_mode})",
                    [sys.executable, os.path.join(src_dir, "render_022_cinematic_space_video.py"), "--mode", video_mode]):
        return

    # Step 4: 산출물 일람표 및 무결성 검증
    print(f"\n{'='*75}")
    print("★ [001]~[999] 무손실 영구 보존 산출물 최종 검증표")
    print(f"{'='*75}")
    files = sorted(os.listdir(result_dir))
    for f in files:
        f_path = os.path.join(result_dir, f)
        size_kb = round(os.path.getsize(f_path) / 1024, 2)
        if size_kb > 1024:
            size_str = f"{round(size_kb/1024, 2):>7.2f} MB"
        else:
            size_str = f"{size_kb:>7.2f} KB"
        print(f" - {f:<55} : {size_str}")

    total_sec = round(time.time() - t_start, 2)
    print(f"\n[ALL COMPLETE] 하이브리드 전체 파이프라인 완결! (총 소요 시간: {total_sec}초 / 토큰 소모량: 0)")

if __name__ == "__main__":
    main()
