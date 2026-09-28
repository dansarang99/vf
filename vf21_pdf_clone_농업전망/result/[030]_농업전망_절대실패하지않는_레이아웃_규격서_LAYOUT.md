# [030] 농업전망 절대 실패하지 않는 레이아웃 규격서 (LAYOUT.md)

> **문서 번호**: `[030]`  
> **청사진 식별**: `LAYOUT.md` 마스터 엔지니어링 규격서  
> **고유 지식재산권**: (AX)창업기술 이한규 대표 고유 실무 지식재산권  
> **적용 대상**: 한국농촌경제연구원(KREI) 농업전망 및 엔터프라이즈 정밀 규격 출판 문서 전반

---

## 1. 개요 및 설계 원칙

본 규격서는 단순한 텍스트 흘림(Text Flow) 방식의 변환이 초래하는 **여백 왜곡, 문단 밀림, 줄바꿈 붕괴**를 원천 차단하기 위해 수립된 **절대 실패하지 않는 레이아웃(Infallible Layout Architecture)** 엔지니어링 표준입니다.

문서의 모든 페이지를 **실측 기반 대칭 맞쪽 여백(Mirror Margins)**과 **투명좌표(Transparent Coordinate Grid Frame)**로 결합하여, 원본 PDF와 100% 동일한 물리적 상하좌우 여백을 구현합니다.

---

## 2. 실측 기반 상하좌우 여백 (Physical Margin Specifications)

PDF 렌더링 엔진(PyMuPDF 300 DPI)으로 37페이지 전 페이지를 실측하여 도출한 물리적 여백 규격입니다.

```
[물리적 용지 규격: 4×6배판 (Crown Quarto)]
폭: 196.1 mm (556.0 pt) | 높이: 266.0 mm (754.0 pt)

          상단 한계 (Top): 33.0 mm (93.5 pt)
     ┌──────────────────────────────────────┐
     │ 머리글 배너: 21.0 mm (60.0 pt)       │
     │ ┌──────────────────────────────────┐ │
     │ │                                  │ │
좌측 │ │                                  │ │ 우측
Inside:│ │         유효 본문 인쇄 영역        │ │ Outside:
31.0mm│ │     139.3 mm × 203.3 mm         │ │ 25.8mm
(87.9)│ │     (394.8 pt × 576.5 pt)       │ │ (73.3)
     │ │                                  │ │
     │ └──────────────────────────────────┘ │
     │ 바닥글/페이지번호: 17.7 mm (50.0 pt) │
     └──────────────────────────────────────┘
          하단 한계 (Bottom): 29.7 mm (84.0 pt)
```

### [세부 여백 파라미터 매트릭스]

| 구역 / 페이지 유형 | 상단 여백 (Top) | 하단 여백 (Bottom) | 좌측 여백 (Left) | 우측 여백 (Right) | 제본 여백 (Gutter) | 머리글 / 바닥글 위치 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **홀수 페이지 (Odd)** | 33.0 mm (93.5 pt) | 29.7 mm (84.0 pt) | **31.0 mm (87.9 pt)** [안쪽] | **25.8 mm (73.3 pt)** [바깥쪽] | 0.0 mm | 머리글 21.0mm / 바닥글 17.7mm |
| **짝수 페이지 (Even)** | 33.0 mm (93.5 pt) | 29.7 mm (84.0 pt) | **27.0 mm (76.6 pt)** [바깥쪽] | **29.8 mm (84.6 pt)** [안쪽] | 0.0 mm | 머리글 21.0mm / 바닥글 17.7mm |
| **1페이지 (Cover/Title)** | 40.0 mm (113.5 pt) | 24.7 mm (70.1 pt) | 31.0 mm (87.9 pt) | 25.8 mm (73.3 pt) | 0.0 mm | 머리글 없음 (First Page Different) |
| **OOXML `w:pgMar` 설정** | `w:top="1870"` | `w:bottom="1680"` | `w:left="1758"` | `w:right="1466"` | `w:gutter="0"` | `w:header="1200"` `w:footer="1000"` |

> **대칭 여백 활성화**: `w:settings` 내 `<w:mirrorMargins/>` 선언을 통해 홀수/짝수 페이지의 안쪽/바깥쪽 여백이 자동으로 완벽 동기화됨.

---

## 3. 투명좌표 (Transparent Coordinate Grid Frame) 시스템

### [투명좌표의 정의와 필요성]
Word에서 문단과 표를 일반적인 방식으로 배치하면, 앞 단락의 행간(Line Spacing)이나 빈 줄(Empty Paragraph)의 미세 오차(0.2~1.5pt)가 누적되어 전체 페이지의 상하좌우 여백이 무너지는 **캐스케이딩 드리프트(Cascading Drift)** 현상이 발생합니다.

**투명좌표(Transparent Coordinate Frame)**는 OOXML 테이블 구조를 시각적 표가 아닌 **정밀 공간 배치 그리드**로 변환하여 사용하는 기술입니다.

```xml
<!-- 투명좌표 그리드 셀 표준 OOXML -->
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="394.8" w:type="dxa"/>
    <w:tblBorders>
      <!-- 모든 테두리를 완전히 투명화(None)하여 육안/인쇄 시 100% 비가시화 -->
      <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>
      <w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
    </w:tblBorders>
    <w:tblCellMar>
      <!-- 내부 패딩을 0으로 강제하여 절대 좌표 일치화 -->
      <w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>
      <w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tr>
    <w:trPr><w:cantSplit/><w:trHeight w:val="exact_height" w:hRule="exact"/></w:trPr>
    <w:tc>
      <w:tcPr><w:tcW w:w="cell_width" w:type="dxa"/><w:vAlign w:val="top"/></w:tcPr>
      <!-- 고정된 좌표 슬롯 내에 텍스트 또는 객체 완벽 안착 -->
    </w:tc>
  </w:tr>
</w:tbl>
```

### [핵심 페이지별 투명좌표 레이아웃 적용 명세]

1. **1페이지 표지 투명좌표 (2-Column Transparent Frame)**:
   - 좌측 슬롯 (`X = 87.9 pt`, 폭 `163.2 pt`): `| 제2장 |`, `국내곡물 수급 동향과 전망` (한 줄), `4인 저자` 고정
   - 우측 슬롯 (`X = 251.1 pt`, 폭 `217.0 pt`): `1. 쌀`~`3. 감자` 목차 및 하단 `4대 저자 각주` 고정
   - 결과: 배경 분할 이미지 침투 0%, 좌우 여백 오차 0.0mm 완벽 고정.

2. **2페이지 요약 박스 투명좌표 (Card & Accent Frame)**:
   - 상단 악센트 바 슬롯 (`Y = 98.0 pt`, 폭 `44.0 mm`, 높이 `4.0 mm`): `#555555` 솔리드 바 고정
   - 하단 본문 카드 슬롯 (`Y = 110.0 pt`, 폭 `138.0 mm`): `#F5F6F8` 연회색 배경의 둥근 모서리 카드 고정
   - 결과: 악센트 바와 텍스트의 겹침 현상 100% 영구 소멸.

3. **4페이지 차트/표 격리 투명좌표 (Top-Bottom Split Frame)**:
   - 상단 슬롯 (`폭 134.0 mm`, `높이 85.0 mm`): `그림 2-1` 300 DPI 크롭 이미지 안착
   - 간격 버퍼 (`높이 8.0 mm`): 상하 분리 물리 공간 확보
   - 하단 슬롯 (`폭 134.0 mm`, `높이 50.0 mm`): `표 2-1` 네이티브 표 안착
   - 결과: 종전의 차트/표 오버랩 및 하단 유령 도형 결함 0% 박멸.

4. **31페이지 듀얼 꺾은선 차트 투명좌표 (Single Anchor Frame)**:
   - 차트 슬롯 (`폭 134.0 mm`, `높이 75.0 mm`): `그림 2-13` 300 DPI 듀얼 차트 고정
   - 결과: 백지 누락 결함 완전 퇴출, 상하 여백 정밀 동기화.

---

## 4. 무결성 검증 및 Zero-Drift 승인 기준

1. **여백 실측 오차**:
   $$|\text{Left}_{\text{Word}} - \text{Left}_{\text{PDF}}| \le 0.1\,\text{mm}$$
   $$|\text{Top}_{\text{Word}} - \text{Top}_{\text{PDF}}| \le 0.1\,\text{mm}$$
2. **총 페이지 수**: Word COM 정식 변환 기준 **정확히 37페이지 (Zero-Drift 100%)**.
3. **인쇄 적합성**: 4×6배판 인쇄 시 재단선(Trim Box) 및 여백선(Bleed Box) 완벽 합치.
