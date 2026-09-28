# -*- coding: utf-8 -*-
"""
immutable_versioning.py :
무손실 누적 보존(Zero-Overwrite Immutable Versioning) 프로토콜 엔진
- 덮어쓰기(Overwrite) 0% 보장
- 단 한 글자/바이트라도 변경될 경우 다음 순차 번호([001]~[999]) 자동 채번
"""
import os
import re

VF10_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(VF10_DIR, "result")

def get_next_available_index():
    """result 디렉토리 내의 최대 번호를 탐색하여 다음 순차 번호 반환"""
    max_idx = 0
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR, exist_ok=True)
        return 1

    pattern = re.compile(r"^\[(\d{3})\]")
    for fname in os.listdir(RESULT_DIR):
        match = pattern.match(fname)
        if match:
            idx = int(match.group(1))
            if idx > max_idx:
                max_idx = idx
    return max_idx + 1

def resolve_immutable_path(target_filename):
    """
    기존 파일이 존재하면 절대 덮어쓰지 않고,
    신규 순차 번호([N])를 채번하여 새 경로를 반환.
    파일이 없으면 지정된 대상 경로 그대로 반환.
    """
    full_path = os.path.join(RESULT_DIR, target_filename)
    if not os.path.exists(full_path):
        return full_path

    # 이미 존재한다면 신규 번호 채번
    next_idx = get_next_available_index()
    # 기존 파일명에서 [XXX]_ 접두사 제거
    clean_name = re.sub(r"^\[\d{3}\]_", "", target_filename)
    new_filename = f"[{next_idx:03d}]_{clean_name}"
    new_path = os.path.join(RESULT_DIR, new_filename)
    print(f"[IMMUTABLE] 기존 파일 보존: {target_filename} -> 신규 불변 번호 채번: {new_filename}")
    return new_path

if __name__ == "__main__":
    next_num = get_next_available_index()
    print(f"현재 result/ 폴더 다음 채번 가능 번호: [{next_num:03d}]")
