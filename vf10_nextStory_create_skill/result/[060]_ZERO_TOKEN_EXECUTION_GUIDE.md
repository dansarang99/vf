# [060] AI 토큰 소비 완전 제로(Zero-Token) 원클릭 실행 가이드

> **무손실 누적 보존(Zero-Overwrite Immutable Versioning) 원칙 적용**:
> 본 문서는 외부 AI API/LLM 호출을 일절 배제하고, 사용자 로컬 PC의 하드웨어와 오픈 데이터만으로 전체 비디오 프로덕션을 100% 자립 구동하는 '토큰 제로화 실행 가이드'입니다.

---

## 1. 토큰 소모량 0(Zero)의 공학적 실현 원리

| 파이프라인 단계 | 기존 대화창 방식 (토큰 폭탄) | **vf10 토큰 제로화 솔루션 (토큰 0)** |
|:---|:---|:---|
| **1. 페르소나 및 세계관 구축** | 2,000씬/10인 배역을 AI에 질의 (수천만 토큰) | **로컬 파이썬 조합 알고리즘으로 0.1초 만에 JSON 자동 합성** |
| **2. 마스터 대본 생성** | 91개 씬 대사를 AI가 매번 스트리밍 (수십만 토큰) | **공학 고증 시나리오 룰베이스 엔진으로 로컬 빌드** |
| **3. 다중 배역 음성 합성** | 유료 TTS API 호출 (분당 과금/토큰) | **무료 Edge-TTS 웹소켓 엔진 + 24kHz 로컬 타임라인 조립** |
| **4. 실제 우주 촬영 실사 에셋** | 고비용 유료 이미지 생성기 결제 | **NASA Open Data API 무료 고해상도 공식 실사 자동 수집** |
| **5. 시네마틱 비디오 렌더링** | 클라우드 비디오 렌더링 GPU 과금 | **로컬 FFmpeg / OpenCV H.264 하드웨어 가속 렌더링** |
| **총합 AI 토큰 소모량** | **1억 토큰 이상 (수백만 원 과금 발생)** | **완전 0 (Zero Token, 비용 $0.00)** |

---

## 2. 사용자 로컬 PC 원클릭 실행 방법

### 방법 A: Windows 탐색기 더블클릭 (가장 간편한 방법)
- 프로젝트 폴더 `C:\Users\note\vf\vf10_nextStory_create_skill` 에 위치한 **`run_zero_token.bat`** 파일을 마우스로 더블클릭합니다.
- 토큰 소모량 0으로 전체 5대 페르소나 세계관 빌드, 음성 합성, 실제 사진 매핑, 비디오 렌더링이 순차적으로 자동 실행됩니다.

### 방법 B: PowerShell 콘솔 실행 (개발자 및 엔지니어용)
```powershell
cd C:\Users\note\vf\vf10_nextStory_create_skill

# 기본 실행 (토큰 제로화 오케스트레이터 가동)
.\run_vf10_pipeline.ps1

# 또는 명시적 제로 모드 지정
.\run_vf10_pipeline.ps1 -Mode zero

# 산출물 현황 테이블 조회
.\run_vf10_pipeline.ps1 -Mode status
```

### 방법 C: 대화형 주피터 노트북 실행 (연구 및 검증용)
- `result/[038]_VF10_K_SPACE_HYBRID_PIPELINE.ipynb` 또는
- `result/[043]_VF10_REAL_SCENE_HYBRID_PIPELINE.ipynb`
- 브라우저나 VS Code에서 열어 각 셀을 `Shift + Enter`로 실행하면, AI 모델 호출 없이 로컬 커널에서 즉시 비디오가 생성되고 인라인으로 재생됩니다.
