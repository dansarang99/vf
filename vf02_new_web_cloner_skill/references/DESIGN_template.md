# DESIGN.md 추출 및 작성 표준 규격
## (Slide Layout, Aspect Ratio, Grid System & Typography Scale)

> **목적**: 레퍼런스 발표 자료의 판형 규격, 여백 그리드, 7대 슬라이드 아키타입, 폰트 계층(L1~L7)을 역공학하여 정량적 수치로 보관함으로써 100% 동일한 레이아웃을 네이티브 코드로 재현하기 위함.

---

## 1. 슬라이드 판형 및 기본 규격

- **종횡비**: 16:9 와이드스크린 (Widescreen Presentation)
- **너비 및 높이**: 13.333 인치 × 7.500 인치 (33.867 cm × 19.050 cm)
- **외부 마진 (Margins)**:
  - 좌측(Left Margin): 0.80 인치 (2.03 cm)
  - 우측(Right Margin): 0.80 인치 (2.03 cm)
  - 상단(Top Margin): 0.40 인치 (1.02 cm)
  - 하단(Bottom Margin): 0.50 인치 (1.27 cm)
- **콘텐츠 유효 너비(Content Width)**: 11.733 인치 (29.80 cm)
- **콘텐츠 유효 높이(Content Height)**: 6.600 인치 (16.76 cm)

---

## 2. 7대 슬라이드 아키타입 (Slide Archetypes)

1. **Archetype 01: Cover Slide (표지)**
   - 대형 화이트 플로팅 카드 (`0.8" L, 0.8" T, 11.733" W, 5.9" H`)
   - 상단 카테고리 필 태그 (`1.2" L, 1.2" T, 4.5" W, 0.38" H`)
   - 메인 타이틀 (`30pt Bold`) + 서브타이틀 (`16pt Bold`)
   - 3대 전략 기둥 서브 카드 그리드 (`1.2" T, 3.45" W, 1.6" H`)
2. **Archetype 02: Executive Summary (총괄 요약)**
   - 3열 독립 카드 그리드 (`3.72" W, 4.5" H, 0.28" Gap`)
   - 각 카드별 상단 소제목, 대형 헤드라인, 구분선, 본문 불릿 3개
3. **Archetype 03: Table of Contents (목차)**
   - 2열 3행 6대 챕터 카드 그리드 (`5.72" W, 1.35" H, 0.29" Gap X, 0.18" Gap Y`)
4. **Archetype 04: Chapter Divider (챕터 간지)**
   - 좌측 볼드 히어로 카드 (`0.8" L, 4.5" W, 4.9" H`) + 우측 세부 아젠다 카드 (`5.6" L, 6.933" W, 4.9" H`)
5. **Archetype 05: 3-Column Strategy Pillars (3열 전략형)**
   - 3개 균등 분할 카드 (`3.72" W, 4.5" H`)
6. **Archetype 06: 2-Column Deep Dive / Flow (2열 심층/비교형)**
   - 2개 좌우 대칭 카드 (`5.72" W, 4.5" H, 0.29" Gap`)
7. **Archetype 07: Empirical EDA Chart Slide (정량 실증 차트형)**
   - 좌측: 전략 텍스트 및 실행 불릿 카드 (`5.60" W, 4.65" H`)
   - 우측: 300 DPI 시각화 차트 및 공식 출처 박스 카드 (`5.98" W, 4.65" H`)

---

## 3. 계층적 타이포그래피 스케일 (L1~L7 Typography Scale)

| 레벨 | 용도 및 위치 | 폰트 패밀리 | 폰트 크기 | 굵기 (Weight) | 추천 색상 |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **L1** | 메인 표지 타이틀 | Malgun Gothic / Pretendard | 30 pt ~ 36 pt | Bold (700) | Midnight Navy (`#0F172A`) |
| **L2** | 슬라이드 상단 메인 헤드라인 | Malgun Gothic / Pretendard | 21 pt ~ 24 pt | Bold (700) | Midnight Navy (`#0F172A`) |
| **L3** | 카드 내부 대제목 / 챕터 제목 | Malgun Gothic / Pretendard | 14 pt ~ 16 pt | Bold (700) | Midnight Navy (`#0F172A`) |
| **L4** | 브레드크럼 필 태그 / 메트릭 레이블 | Malgun Gothic / Pretendard | 10 pt ~ 11.5 pt | Bold (700) | Cerulean Blue (`#0785C0`) |
| **L5** | 본문 리드문 / 핵심 불릿 헤드 | Malgun Gothic / Pretendard | 12 pt ~ 13 pt | Bold (700) | Dark Slate (`#1E293B`) |
| **L6** | 일반 설명 본문 텍스트 | Malgun Gothic / Pretendard | 10.5 pt ~ 11.5 pt | Regular (400) | Slate Charcoal (`#334155`) |
| **L7** | 풋노트, 공식 출처, 페이지 번호 | Malgun Gothic / Pretendard | 9.0 pt ~ 9.5 pt | Regular (400) | Muted Slate (`#64748B`) |
