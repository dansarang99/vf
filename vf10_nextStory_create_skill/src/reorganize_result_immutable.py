# -*- coding: utf-8 -*-
"""
result 디렉토리 무손실 불변 번호 체계([020]~[036]) 마이그레이션 및 정리 도구
기존 중복 번호([020], [021], [024])를 1 파일 = 1 고유 순차 번호로 완전 개편.
단 한 자라도 수정될 시 신규 번호를 붙여 추가 저장하는 정책 준수.
"""
import os
import shutil

RESULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "result")

# 이전 파일명 -> 신규 불변 고유 번호 파일명 매핑
MAPPING = [
    # Phase 1: 대본 및 메타데이터
    ("[020]_episode_02_k_space_master_script.md", "[020]_episode_02_k_space_master_script.md"),
    ("[020]_episode_02_k_space_master_script.txt", "[021]_episode_02_k_space_master_script.txt"),
    ("[020]_episode_02_k_space_scenes.json",        "[022]_episode_02_k_space_scenes_metadata.json"),
    
    # Phase 2: 다중 배역 음성 합성 및 동기화 리포트
    ("[021]_episode_02_k_space_master_audio.mp3",  "[023]_episode_02_k_space_master_audio.mp3"),
    ("[021]_episode_02_part_1_audio.mp3",          "[024]_episode_02_part_1_launch_audio.mp3"),
    ("[021]_episode_02_part_2_audio.mp3",          "[025]_episode_02_part_2_trans_lunar_audio.mp3"),
    ("[021]_episode_02_part_3_audio.mp3",          "[026]_episode_02_part_3_lunar_landing_audio.mp3"),
    ("[021]_episode_02_part_4_audio.mp3",          "[027]_episode_02_part_4_mars_transfer_audio.mp3"),
    ("[021]_TIMELINE_SYNC_ACCURACY_REPORT.txt",    "[028]_TIMELINE_SYNC_ACCURACY_REPORT.txt"),
    
    # Phase 3: 시네마틱 스타일 자막
    ("[022]_episode_02_k_space_cinematic_subtitles.ass", "[029]_episode_02_k_space_cinematic_subtitles.ass"),
    
    # Phase 4: 시네마틱 K-우주 비디오 완제본 (100% 우주비주얼 탑재본)
    ("[023]_episode_02_k_space_highlight_video.mp4", "[030]_episode_02_k_space_highlight_video.mp4"),
    ("[024]_episode_02_full_master.mp4",            "[031]_episode_02_full_master_video.mp4"),
    ("[024]_episode_02_part_1_fullscene.mp4",        "[032]_episode_02_part_1_fullscene_video.mp4"),
    ("[024]_episode_02_part_2_fullscene.mp4",        "[033]_episode_02_part_2_fullscene_video.mp4"),
    ("[024]_episode_02_part_3_fullscene.mp4",        "[034]_episode_02_part_3_fullscene_video.mp4"),
    ("[024]_episode_02_part_4_fullscene.mp4",        "[035]_episode_02_part_4_fullscene_video.mp4"),
    
    # Phase 5: 최종 보고서
    ("[025]_K_SPACE_EXPEDITION_COMPLETION_REPORT.md", "[036]_K_SPACE_EXPEDITION_FINAL_COMPLETION_REPORT.md"),
]

def migrate_result_directory():
    print("=" * 70)
    print("  [RESULT 폴더 무손실 불변 번호 체계 재편성 시작]")
    print("=" * 70)
    
    # 임시 디렉토리 생성 후 이동 (이름 충돌 방지)
    temp_dir = os.path.join(RESULT_DIR, "_temp_reorg")
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. 원본 파일들을 임시 디렉토리로 이동
    moved_count = 0
    for old_name, new_name in MAPPING:
        old_path = os.path.join(RESULT_DIR, old_name)
        if os.path.exists(old_path):
            temp_path = os.path.join(temp_dir, old_name)
            shutil.move(old_path, temp_path)
            moved_count += 1
            
    print(f"[*] 임시 디렉토리로 {moved_count}개 파일 안전 격리 완료.")
    
    # 2. 신규 고유 번호로 result 디렉토리에 재배치
    for old_name, new_name in MAPPING:
        temp_path = os.path.join(temp_dir, old_name)
        new_path = os.path.join(RESULT_DIR, new_name)
        if os.path.exists(temp_path):
            shutil.move(temp_path, new_path)
            size_kb = os.path.getsize(new_path) / 1024
            print(f" -> {new_name:<55} ({size_kb:>9.2f} KB) 배치 완료")
        else:
            print(f" [!] 경고: {old_name} 파일이 존재하지 않습니다.")
            
    # 3. 임시 디렉토리 삭제
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)
        
    print("=" * 70)
    print(f" [성공] 총 {moved_count}개 산출물이 고유 순차 번호([020]~[036])로 재정리되었습니다.")
    print("=" * 70)

if __name__ == "__main__":
    migrate_result_directory()
