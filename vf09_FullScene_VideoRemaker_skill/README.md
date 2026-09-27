# vf09_FullScene_VideoRemaker_skill : 2시간 풀씬 비디오 리메이커 마스터 파이프라인

본 디렉터리는 1~2시간 분량의 장편 영상(유튜브 등)에서 **N천 개의 전체 씬(Full-Scene)을 정밀 추출**하고, **10대 보이스 캐릭터 1인 다역 배정**, **상영시간 초단위 관리(오차율 1% 이내 달성)**, **씬별 고화질 캡처 및 비디오 조립(MP4)**을 엔드투엔드로 완결하며, `result/` 폴더에 `[202]`~`[999]` 순차 번호로 영구 보존하는 전문 영상 리메이크 마스터 파이프라인입니다.

---

## 1. 주요 구성 및 산출물 ([202]~[205])

- `SKILL.md` : Antigravity 정식 스킬 규격서
- `result/` : [202]~[999] 무손실 결과물 영구 보존소
  - `[202]_episode_01_10char_1124scenes_master_script.md` : 1,124씬 10인 배역 타임코드 전수 대본
  - `[203]_episode_01_2hour_multichar_master_voice.mp3` : 2시간 완제 10인 배역 마스터 오디오 (108.15 MB, 오차율 0.249%)
  - `[203]_episode_01_part_1~4_voice.mp3` : 30분 단위 분할본 4개
  - `[203]_TIMELINE_SYNC_ACCURACY_REPORT.txt` : 시간 동기화 정확도 측정 보고서
  - `[204]_2HOUR_RESTORATION_PROBLEM_ANALYSIS.md` : 2시간 전편 복원 심층 문제점 검토 보고서
  - `[205]_FULLSCENE_VIDEO_REMAKER_MASTER_REPORT.md` : 비디오 리메이커 스킬 종합 완제 보고서
- `src/` : 코어 파이프라인 엔진
  - `build_202_master_script.py` : 10인 배역 1인 다역 대본 빌더
  - `render_vf09_2hour_multichar_timeline.py` : 초단위 상영시간 관리 2시간 렌더러
  - `remake_video_builder.py` : 비디오 프레임 캡처 및 MP4 리메이크 조립기
