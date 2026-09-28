# [010] CHARACTER VOICE MATRIX & SOUND DESIGN SPECIFICATIONS
## 제2편 10대 배역 1인 다역 음성 모델 및 시네마틱 사운드 엔지니어링 규격

> **문서 번호**: `[010]`  
> **상속 엔진**: `@vf09_FullScene_VideoRemaker_skill`  
> **음성 엔진**: Microsoft Edge Neural TTS (오차율 0.05% 이내 초단위 타임라인 동기화)

---

### 1. 10대 배역 보이스 캐스팅 및 연출 매트릭스

| 번호 | 배역명 | 음성 모델 (Voice) | 피치 (Pitch) | 속도 (Rate) | 볼륨 (Vol) | ASS 자막 뱃지 컬러 | 역할 및 연출 특징 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **해설 (나레이터)** | `ko-KR-InJoonNeural` | -1Hz | +6% | +0% | Gold (`&H00A0F0&`) | 장엄하고 웅장한 대서사 다큐멘터리 서사 |
| 2 | **박준서 사령관** | `ko-KR-HyunsuNeural` | +1Hz | +8% | +5% | Lime (`&H78CF32&`) | 냉철하고 신념에 찬 에이스 우주사령관 |
| 3 | **강수연 비행디렉터** | `ko-KR-SunHiNeural` | +2Hz | +5% | +0% | Pink (`&HB482F0&`) | 날카롭고 침착한 KASA 심우주관제센터 수석 |
| 4 | **최영목 청장/장군** | `ko-KR-InJoonNeural` | -5Hz | +4% | +5% | Red (`&H4646DC&`) | 국가의 주권을 짊어진 카리스마 최고지휘관 |
| 5 | **빅터 라이벌 국장** | `ko-KR-InJoonNeural` | -3Hz | +6% | -2% | Orange (`&H28A0E6&`) | 회의적 시선에서 경외감으로 변하는 해외 우주국장 |
| 6 | **준서 어머니** | `ko-KR-SunHiNeural` | -3Hz | +4% | -3% | Purple (`&H8C78C8&`) | 애절하고 숭고한 한국적 모정의 기도 |
| 7 | **김태훈 소령** | `ko-KR-HyunsuNeural` | +4Hz | +10% | +3% | Cyan (`&H00D2D2&`) | 유쾌한 동기이자 든든한 백업 비행사 |
| 8 | **민재 (소년)** | `ko-KR-SunHiNeural` | +5Hz | +8% | +4% | Bright Blue (`&H64E6E6&`) | 미래를 꿈꾸는 순수한 아이의 감정선 |
| 9 | **윤선아 박사** | `ko-KR-SunHiNeural` | +0Hz | +5% | +2% | Steel Blue (`&HE6964B&`) | 로켓 및 추진체 물리학의 최고권위 공학자 |
| 10 | **심우주 AI 세종** | `ko-KR-InJoonNeural` | +0Hz | +5% | +0% | Silver (`&H969696&`) | 탐사선 텔레메트리, 라이다 및 비상 경보 음성 |

---

### 2. 타임라인 동기화 및 오차율 0% 제어 알고리즘

- **슬롯 간격 무음 프레임 주입 (Silence Frame Injection)**:
  - 발화와 발화 사이의 공백 구간에 MPEG-1 Layer 3 128kbps 44.1kHz 표준 무음 프레임(`b'\xff\xfb\x90\x64' + b'\x00'*413`)을 정밀 산출하여 주입.
  - 이를 통해 1시간~2시간 장편 오디오에서도 누적 타임코드 드리프트(Drift)가 0초로 유지됨.
- **실전 한국어 자연스러운 스피드 보정**:
  - 인위적인 감속(-25%)을 전면 배제하고, 실전 비상 상황의 긴박감과 몰입도를 극대화하는 `+4% ~ +10%` 탄력 속도 적용.

---

### 3. ASS 시네마틱 한글 자막 스타일 규격

```ini
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Pretendard,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.5,1.5,2,30,30,45,1
Style: SubtitleBadge,Pretendard,30,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,2.0,2,30,30,40,1
```
- 상단 또는 하단에 `[배역명]` 뱃지가 해당 배역 전용 고유 컬러로 점등되며, 대사는 가독성 높은 백색 볼드체로 렌더링.
