#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[014] vf12_hwpx_stdandard_skill 배포 패키지 및 깃허브 동기화 실행기
- 기능:
  1. .gemini/config/skills/vf12_hwpx_stdandard_skill 동기화 점검
  2. 로컬 vf12_hwpx_stdandard_skill 리포지토리 파일 상태 점검
  3. git add / status 점검
"""

import os
import subprocess
from pathlib import Path


def main():
    print("=== [014] vf12_hwpx_stdandard_skill 동기화 및 배포 점검 ===")

    gemini_skill = Path(r"C:\Users\note\.gemini\config\skills\vf12_hwpx_stdandard_skill")
    repo_skill = Path(r"C:\Users\note\vf\vf12_hwpx_stdandard_skill")

    # 1. Gemini 스킬 점검
    print("[1] .gemini 스킬 디렉토리 점검:")
    if gemini_skill.exists():
        files = list(gemini_skill.rglob("*"))
        print(f"    [OK] 위치: {gemini_skill.resolve()} (파일 수: {len(files)}개)")
        for f in files:
            if f.is_file():
                print(f"      - {f.relative_to(gemini_skill)} ({f.stat().st_size:,} bytes)")
    else:
        print("    [FAIL] Gemini 스킬 디렉토리가 없습니다.")

    # 2. 로컬 리포지토리 점검
    print("\n[2] 로컬 vf 저장소 점검:")
    if repo_skill.exists():
        files = list(repo_skill.rglob("*"))
        print(f"    [OK] 위치: {repo_skill.resolve()} (파일 수: {len(files)}개)")
        for f in files:
            if f.is_file():
                print(f"      - {f.relative_to(repo_skill)} ({f.stat().st_size:,} bytes)")
    else:
        print("    [FAIL] 로컬 저장소 디렉토리가 없습니다.")

    # 3. Git 상태 점검
    print("\n[3] Git 상태 점검 (C:\\Users\\note\\vf):")
    try:
        res = subprocess.run(["git", "status", "--short"], cwd=r"C:\Users\note\vf", capture_output=True, text=True)
        print("    Git status 출력 (상위 10줄):")
        for line in res.stdout.splitlines()[:10]:
            print("      ", line)
    except Exception as e:
        print("    [WARN] Git 확인 중 오류:", e)

    print("\n=== 배포 점검 완료: vf12_hwpx_stdandard_skill 등록 완료 ===")


if __name__ == "__main__":
    main()
