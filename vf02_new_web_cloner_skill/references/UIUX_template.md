# UIUX.md 추출 및 작성 표준 규격
## (Interaction Aesthetics, Visual Rhythm & Component Architecture)

> **목적**: 슬라이드 및 웹 화면 내의 시각적 리듬(Visual Rhythm), 정보 탐색을 돕는 UI 컴포넌트(필 태그, 수직 바, 하단 배너, 카드 패딩), 여백 구조를 체계화하여 전문적이고 세련된 사용자 경험(UX)을 보장하기 위함.

---

## 1. 5대 핵심 UI 컴포넌트 규격 (Key UI Components)

1. **상단 브레드크럼 필 태그 (Breadcrumb Pill Tag)**:
   - 형태: 둥근 모서리 사각형 (Rounded Rectangle, Radius 0.15")
   - 크기: 너비 4.3" ~ 4.5", 높이 0.32" ~ 0.38"
   - 색상: 연한 스카이 틴트 배경 (`#E0F2FE`), 세룰리안 블루 테두리 (`#0785C0`), 폰트 10pt Bold
   - 역할: 현재 슬라이드가 속한 상위 챕터 및 세부 카테고리를 명시.
2. **우측 상단 코퍼레이트 브랜드 마크 (Corporate Branding Header)**:
   - 크기: 너비 5.0", 높이 0.32", 우측 정렬
   - 색상: 슬레이트 그레이 (`#64748B`), 폰트 10pt Bold
   - 역할: 프로젝트 주관 기업 및 기관(예: `HYUNDAI MOTOR GROUP × SAEMANGEUM`) 공식 표기.
3. **좌측 수직 액센트 바 (Vertical Accent Bar)**:
   - 형태: 세로 직사각형 (Rectangle)
   - 크기: 너비 4.5pt (약 0.06"), 높이는 카드/배너 전체 높이와 일치
   - 색상: 세룰리안 블루 (`#0785C0`) 또는 에메랄드 제이드 (`#0D7C5B`)
   - 역할: 시선의 출발점을 유도하고 카드의 중요도를 강조.
4. **하단 익스큐티브 인사이트 배너 (Bottom Executive Insight Card)**:
   - 형태: 둥근 모서리 화이트 카드 (`#FFFFFF`, 테두리 `#D1E7DD`)
   - 크기: 좌측 0.8", 상단 6.32", 너비 11.733", 높이 0.58"
   - 구성: 좌측 4.5pt 세룰리안 액센트 바 + `【EXECUTIVE INSIGHT】` 볼드 태그 + 슬라이드 핵심 결론 1문장 (11pt Dark Slate).
   - 역할: 슬라이드 전체 내용을 3초 안에 파악할 수 있는 요약문 제공.
5. **하단 풋노트 및 동적 페이지 카운터 (Footer Metadata & Counter)**:
   - 좌측: 공식 사업단 및 참여 기관명 (9.5pt Muted Slate)
   - 우측: `SLIDE {num:02d} / 40` (10pt Bold Cerulean Blue, 우측 정렬)

---

## 2. 시각적 리듬 및 여백(Whitespace) 원칙

- **내부 패딩(Inner Padding)**: 카드의 텍스트 박스는 최소 0.25" 이상의 좌우 마진을 확보하여 텍스트가 테두리에 달라붙지 않도록 방지.
- **카드 간 간격(Gutter/Gap)**:
  - 2열 분할 시: 0.29 인치 간격
  - 3열 분할 시: 0.28 인치 간격
- **구분선(Divider)**: 카드 내부 헤드라인 아래에 연한 테두리 색상(`―` × 22~34)의 보조선을 삽입하여 위계 분리.
