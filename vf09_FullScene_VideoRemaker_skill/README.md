# vf09_FullScene_VideoRemaker_skill

(AX)창업기술 대표 고유 실무 지식재산권 기반.
1~2시간 장편 유튜브 영상에서 1,124개 전체 씬(Full-Scene)을 정밀 추출하고, 10대 보이스 캐릭터 1인 다역 매핑, 상영시간 초단위 관리(오차율 1% 이내 엄격 보정), 원본 실제 비디오 스트림(Footage) 100% 탑재, 자연스러운 실전 보이스 스피드(+3%~+10%) 및 시네마틱 한글 자막 번인을 통해 원본과 분초단위까지 완벽히 일치하는 리메이크 비디오(MP4)를 자동 조립·생산하며, `result/` 폴더에 `[202]`~`[999]` 순차 번호로 영구 보존하는 차세대 풀씬 비디오 리메이커 마스터 파이프라인.

---

## 📁 주요 디렉토리 구조

```
vf09_FullScene_VideoRemaker_skill/
├── SKILL.md                                              # 스킬 규격서 및 코어 아키텍처
├── README.md                                             # 프로젝트 개요 및 실행 가이드
├── src/                                                  # 핵심 엔진 소스코드
│   ├── render_vf09_full_2hour_remake.py                  # 2시간 1124씬 전체 자동 복원 마스터 파이프라인
│   ├── render_real_footage_remake_mp4.py                 # 실제 영상 추출 및 파일럿 MP4 생성기
│   ├── render_vf09_2hour_multichar_timeline.py           # 2시간 오디오 타임라인 동기화 엔진
│   └── build_202_master_script.py                        # 1,124씬 10인 배역 대본 추출기
├── result/                                               # [202]~[999] 영구 보존 산출물
│   ├── [202]_episode_01_10char_1124scenes_master_script.md # 10인 배역 마스터 대본
│   ├── [203]_episode_01_2hour_multichar_master_voice.mp3   # 2시간 완제 마스터 오디오 (오차율 0.048%)
│   ├── [203]_episode_01_part_1~4_voice.mp3                 # 30분 단위 분할 오디오 4부작
│   ├── [204]_2HOUR_RESTORATION_PROBLEM_ANALYSIS.md         # 심층 문제점 진단서
│   ├── [205]_FULLSCENE_VIDEO_REMAKER_MASTER_REPORT.md      # 마스터 스킬 완제 보고서
│   ├── [206]_episode_01_scene_3287s_remake_master.mp4      # 1분 35초 실전 검증 MP4
│   ├── [207]_episode_01_part_1~4_fullscene_remake.mp4      # 2시간 풀씬 4부작 시네마틱 MP4
│   ├── [207]_episode_01_2hour_full_remake_master.mp4       # 2시간 통합 완제 마스터 MP4
│   └── [208]_FULLSCENE_2HOUR_RESTORATION_COMPLETION_REPORT.md # 최종 완제 보고서
└── scratch/                                              # 임시 작업 디렉토리
```

---

## 🚀 실행 방법

```bash
# 2시간 1,124씬 전수 자동 복원 및 4부작 + 통합 마스터 MP4 생성
python src/render_vf09_full_2hour_remake.py
```
