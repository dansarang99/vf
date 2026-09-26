# vf02_new_web_cloner_skill
## (AX)창업기술 이한규 대표 고유 실무 지식재산권 기반 차세대 웹·슬라이드 클로너 마스터 파이프라인

> **리포지토리**: `github.com/dansarang99/vf/vf02_new_web_cloner_skill`  
> **핵심 기능**: PPTX 1:1 역공학 복제, 5대 TEXT 청사진 추출, 1:N(2배~5배) 무손실 분량 확장, 제미나이 딥리서치 연동, 공공데이터 20년차 EDA 시각화(300 DPI), 법적·통계적 인용표준화, 파워포인트 네이티브 벡터 덱 합성 및 전 슬라이드 발표자 대본 탑재.

---

## 1. 개요 (Overview)

본 시스템은 단순한 PPT 복제나 디자인 템플릿 복사를 넘어, **임의의 레퍼런스 프레젠테이션의 비즈니스 본질(businessDNA), 레이아웃(DESIGN), 색채 및 질감(STYLE), 인터랙션 미학(UIUX), 정량 지표 구조(DATA&EDA)를 100% 텍스트로 역공학 보관**하고, 사용자의 필요에 따라 **1:N(2x~5x)으로 분량을 확장**하며, **새로운 비즈니스 주제에 대한 딥리서치 및 공공데이터 통계 분석(EDA)**을 결합하여 **C-레벨 보고용 초고급 프레젠테이션을 네이티브 벡터 파워포인트로 자동 편찬**하는 엔드투엔드 파이프라인입니다.

---

## 2. 5대 마스터 단계 (5-Stage Architecture)

```
┌────────────────────────────────────────────────────────────────────────┐
│ [제1단계] 1:1 역공학 복제 및 5대 TEXT 청사진 추출 (Extraction Phase)     │
│  - 레퍼런스 PPTX 업로드 (upload/)                                      │
│  - businessDNA.md, DESIGN.md, STYLE.md, UIUX.md, DATA&EDA.md 자동 추출 │
│  - 100% 1:1 네이티브 벡터 도형 복제본 생성                            │
└────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ [제2단계] 원문 보존 기반 1:N(2~5배) 분량증가 및 서사 확장 (Scaling Phase)│
│  - 원문 1:1 내용 토씨 하나도 틀리지 않고 100% 보존                     │
│  - 2배(80쪽), 3배(120쪽), 5배(200쪽) 단계별 심층 서사 분기           │
│  - 전체 맥락 및 거시적 서사 연결성(Cohesion) 엄수                     │
└────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ [제3단계] 신규 주제 선정 및 제미나이 딥리서치 업로드 표준화 (Research) │
│  - Gemini Advanced / Notebook 기반 심층 분석 수행                      │
│  - upload/ 폴더 표준 규격: 딥리서치 PDF, 40p Master Script MD         │
│  - 자동 정형 데이터 파싱 (parsed_slides.json)                          │
└────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ [제4단계] 공공데이터 크롤링, EDA 시각화 및 출처·인용 표준화 (EDA Phase)│
│  - 공공데이터포털, KEPCO, KMI, 한국은행, IFR 공인 1차 데이터 수집      │
│  - 20년차 데이터 사이언티스트 EDA (기술통계, 상관, 교차분석, 인사이트)│
│  - 300 DPI 초고화질 차트 생성 (화이트테크 / 다크테크 템플릿 매핑)      │
│  - 3대 인용규정 준수: [공식 1차 출처], [분석 모형], [법적·통계적 근거] │
└────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ [제5단계] 최종 슬라이드 템플릿 통합 완성 및 납품 (Synthesis Phase)     │
│  - 템플릿(1:1 ~ 1:5) 선택                                              │
│  - 딥리서치 서사 + EDA 시각화 차트 적재적소 1:1 주입                   │
│  - 100% 파워포인트 네이티브 벡터 도형 (이미지 통캡처 0% 배제)          │
│  - 전 슬라이드 발표자 상세 대본(Notes Slide) 100% 완벽 탑재            │
│  - [001]~[999] 단일 정수 연속 관리 및 마스터 인덱스 영구 보존         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 디렉토리 구조 (Directory Tree)

```
vf02_new_web_cloner_skill/
├── SKILL.md                          # 마스터 스킬 명세서 (Gemini/Antigravity 연동)
├── README.md                         # 리포지토리 총괄 설명서 (본 파일)
├── scripts/                          # 단계별 자동화 파이프라인 엔진
│   ├── stage1_extract_blueprints.py  # 1:1 역공학 및 5대 텍스트 청사진 추출기
│   ├── stage2_expand_narrative.py    # 1:N (2x~5x) 서사 분량 확장기
│   ├── stage3_ingest_research.py     # 제미나이 딥리서치 파서
│   ├── stage4_eda_and_citations.py   # 공공데이터 EDA 및 300 DPI 시각화/출처 생성기
│   ├── stage5_synthesize_presentation.py # 최종 파워포인트 네이티브 빌더
│   └── verify_integrity.py           # 슬라이드, 대본, 차트, 번호 0-에러 무결성 검증기
├── templates/                        # 분량별 템플릿 아키텍처 청사진
│   ├── template_1x_40p.json          # 1:1 원본 40쪽 템플릿 구조
│   ├── template_2x_80p.json          # 1:2 확장 80쪽 템플릿 구조
│   └── template_master_archetypes.py # 7대 슬라이드 아키타입 렌더러
├── references/                       # 5대 청사진 템플릿 및 인용 규정
│   ├── businessDNA_template.md       # 비즈니스 본질 추출 표준
│   ├── DESIGN_template.md            # 레이아웃/판형/타이포그래피 표준
│   ├── STYLE_template.md             # 컬러 토큰/테마 표준
│   ├── UIUX_template.md              # UI/UX 인터랙션 표준
│   ├── DATA_EDA_template.md          # EDA 및 차트 구조 표준
│   └── citation_standards.md         # 공인 1차 문헌 인용표시 규정
└── examples/                         # 실전 검증 레퍼런스 케이스 (새만금 현대차 40쪽)
    ├── sample_parsed_data.json       # 40쪽 슬라이드 및 대본 실증 데이터
    └── sample_master_index.md        # [001]~[042] 무결성 색인표 실증 사례
```

---

## 4. 설치 및 실행 방법 (Quick Start)

### 1) 환경 요구사항
- Python 3.10 이상
- 필수 라이브러리: `python-pptx`, `matplotlib`, `koreanize-matplotlib`, `pandas`, `numpy`, `scipy`

```bash
pip install python-pptx matplotlib koreanize-matplotlib pandas numpy scipy
```

### 2) 5대 단계 실행 명령어

```bash
# [1단계] 레퍼런스 PPTX 업로드 후 5대 텍스트 청사진 추출
python scripts/stage1_extract_blueprints.py --input upload/농촌재생_통합본(40쪽).pptx

# [2단계] 원문 보존 기반 1:N 분량 확장
python scripts/stage2_expand_narrative.py --scale 2x --input result/[009]_40p_data.json

# [3단계] 제미나이 딥리서치 원문 업로드 및 데이터 파싱
python scripts/stage3_ingest_research.py --source upload/

# [4단계] 공공데이터 EDA 분석 및 300 DPI 화이트테크 차트(공식 출처 포함) 생성
python scripts/stage4_eda_and_citations.py --theme white-tech --dpi 300

# [5단계] 최종 파워포인트 슬라이드 덱 합성 및 발표자 대본 100% 임베딩
python scripts/stage5_synthesize_presentation.py --output result/[041]_최종완성본.pptx

# [검증] 슬라이드 40장, 대본 40개, 차트, 인덱스 0-에러 무결성 감사
python scripts/verify_integrity.py
```

---

## 5. 지식재산권 및 라이선스 (Intellectual Property)

- **원작자 및 기획자**: (AX)창업기술 이한규 대표
- **라이선스**: Proprietary Enterprise License. 무단 복제 및 전재를 금하며, 엔터프라이즈 컨설팅 및 학술 연구 목적으로 승인 후 활용 가능합니다.
