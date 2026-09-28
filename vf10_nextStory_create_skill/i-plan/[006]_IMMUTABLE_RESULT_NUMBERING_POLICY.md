# [006] 무손실 누적 보존(Zero-Overwrite Immutable Versioning) 및 RESULT 번호 체계 정책

## 1. 개요 및 배경
- **요청 사항**: "생성되는 모든 결과물은 전에 있던 결과물을 수정하는 방식으로 저장하지 말고, 단 한자라도 바뀔 경우에는 신규번호를 붙여 추가로 저장하기 바람. 이미 진행된 것도 그런 원칙을 준수해서 새로 RESULT 폴더 정리해줘."
- **목적**: 
  1. 기생성된 자산의 덮어쓰기(Overwrite) 0% 완전 박멸
  2. 단 1바이트/단 1글자의 변경이 발생하더라도 고유 신규 번호(`[001]`~`[999]`)를 채번하여 신규 파일로 추가 누적 보존
  3. 1 파일 = 1 고유 순차 번호 매핑을 통해 파일 간 충돌 및 버전 혼선 원천 차단

---

## 2. RESULT 폴더 고유 순차 번호([020]~[036]) 재편성 기준

| 번호 | 파일명 | 유형 | 내용 및 사양 |
|:---:|:---|:---:|:---|
| **[020]** | `[020]_episode_02_k_space_master_script.md` | 마크다운 | 91씬 10인 배역 대서사시 완제 대본 (서사/지문/대사) |
| **[021]** | `[021]_episode_02_k_space_master_script.txt` | 텍스트 | 순수 텍스트 대본 본문 |
| **[022]** | `[022]_episode_02_k_space_scenes_metadata.json` | JSON | 91개 씬별 화자, 대사, 시간, 우주 비주얼 매핑 메타데이터 |
| **[023]** | `[023]_episode_02_k_space_master_audio.mp3` | 오디오 | 13분 01초 전편 단일 스트림 무손실 오디오 (타임라인 오차 0.0155%) |
| **[024]** | `[024]_episode_02_part_1_launch_audio.mp3` | 오디오 | 제1막 오디오 (나로우주센터 발사 및 저궤도) |
| **[025]** | `[025]_episode_02_part_2_trans_lunar_audio.mp3` | 오디오 | 제2막 오디오 (달 전이궤도 및 데브리 회피) |
| **[026]** | `[026]_episode_02_part_3_lunar_landing_audio.mp3` | 오디오 | 제3막 오디오 (달 남극 섀클턴 착륙 및 아리온 1호 탐사) |
| **[027]** | `[027]_episode_02_part_4_mars_transfer_audio.mp3` | 오디오 | 제4막 오디오 (천명 1호 화성 전이 및 2045 지평선) |
| **[028]** | `[028]_TIMELINE_SYNC_ACCURACY_REPORT.txt` | 리포트 | 타임라인 동기화 정밀도(0.0155%) 검증 리포트 |
| **[029]** | `[029]_episode_02_k_space_cinematic_subtitles.ass` | 자막 | 10대 배역 폰트/색상 규격 시네마틱 ASS 자막 |
| **[030]** | `[030]_episode_02_k_space_highlight_video.mp4` | 비디오 | 1분 30초 실전 K-우주 비주얼 하이라이트 영상 (100% 우주비주얼) |
| **[031]** | `[031]_episode_02_full_master_video.mp4` | 비디오 | 13분 01초 전편 풀씬 통합 K-우주 마스터 비디오 |
| **[032]** | `[032]_episode_02_part_1_fullscene_video.mp4` | 비디오 | 제1막 완제 풀씬 K-우주 비디오 |
| **[033]** | `[033]_episode_02_part_2_fullscene_video.mp4` | 비디오 | 제2막 완제 풀씬 K-우주 비디오 |
| **[034]** | `[034]_episode_02_part_3_fullscene_video.mp4` | 비디오 | 제3막 완제 풀씬 K-우주 비디오 |
| **[035]** | `[035]_episode_02_part_4_fullscene_video.mp4` | 비디오 | 제4막 완제 풀씬 K-우주 비디오 |
| **[036]** | `[036]_K_SPACE_EXPEDITION_FINAL_COMPLETION_REPORT.md` | 마크다운 | 제2탄 달·화성 대서사시 최종 완결 종합 보고서 |

---

## 3. 영구 불변 버전 관리 규칙 (Immutable Versioning Protocol)

1. **덮어쓰기 절대 금지 (Never Overwrite)**:
   - 파일 쓰기 도구 및 스크립트 실행 시 `overwrite=True` 또는 기존 파일 대상 덮어쓰기 연산 수행을 영구히 금지한다.
2. **신규 번호 자동 증분 채번 (Next Monotonic Numbering)**:
   - 임의의 산출물에서 단 한 글자라도 수정, 개선, 파생, 재렌더링이 발생하면, 현재 디렉토리의 최대 번호 `N`을 스캔하여 반드시 `[N+1]` 번호를 부여하여 새 파일로 생성한다.
   - 예시: 만약 제1막 비디오를 4K로 재렌더링하거나 자막 스타일을 변경할 경우 ➡️ `[037]_episode_02_part_1_fullscene_video_v2.mp4` 형태로 신규 번호를 부여하여 추가 저장.
3. **영구 이력 보존 (Historical Lineage Preservation)**:
   - 이전 버전 파일은 절대 삭제하지 않고 보존하여, 작업의 모든 진화 과정이 [001]부터 [999]까지 완벽한 시계열로 추적 가능하도록 한다.
