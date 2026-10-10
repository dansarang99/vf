# 🏛️ [STYLE] 타이포그래피, 서체 4중 매핑 및 색상 명세서

본 문서는 (AX)창업기술 이한규 대표의 지식재산권을 기반으로, 복제 문서의 글꼴, 위계, 자간, 장평, 줄간격 및 색상 토큰을 규정합니다.

---

## 1. 서체 4중 매핑 (Font Quad-Mapping)

서체 결손으로 인한 폰트 깨짐 및 페이지 밀림을 방지하기 위해 4중 대체 서체를 정의합니다:

| 역할 | 1순위 (Primary) | 2순위 (Secondary) | 3순위 (Fallback) | 영문/숫자 (Latin) |
| :--- | :--- | :--- | :--- | :--- |
| **본문 명조** | 한컴바탕 | 함초롬바탕 | KoPub바탕 Medium | Times New Roman |
| **제목 고딕** | 한컴고딕 | 함초롬돋움 | KoPub돋움 Bold | Arial / Helvetica |
| **표/수치** | 한컴바탕 | 함초롬바탕 | 바탕 | Times New Roman |

---

## 2. 타이포그래피 위계 (Typographic Hierarchy)

| 위계 수준 | 글자 크기 | 볼드 여부 | 장평 | 자간 | 줄간격 (Word/HWP) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **대제목 (Title)** | 18.0 pt | Bold | 100% | 0.0 pt | 130% / 18pt 고정 |
| **중제목 (Heading 1)** | 14.0 pt | Bold | 98% | -0.3 pt | 140% / 15pt 고정 |
| **소제목 (Heading 2)** | 11.0 pt | Bold | 95% | -0.5 pt | 150% / 12pt 고정 |
| **본문 (Body Text)** | 9.5 pt | Regular | 95% | -0.5 pt | 150% / 8.5~9.0pt 고정 |
| **불릿 항목 (List)** | 9.5 pt | Regular | 95% | -0.5 pt | 145% / 8.5pt 고정 |
| **표 내용 (Cell Text)** | 7.0 ~ 8.0 pt | Regular | 95% | -0.5 pt | 120% / 7.0~8.0pt 고정 |
| **표 헤더 (Table Head)** | 7.5 ~ 8.5 pt | Bold | 95% | -0.5 pt | 120% / 7.5~8.5pt 고정 |
| **각주/출처 (Footnote)** | 7.5 ~ 8.0 pt | Regular | 95% | -0.5 pt | 130% / 7.5pt 고정 |

---

## 3. 색상 토큰 (Color Palette Tokens)

```json
{
  "colors": {
    "primary_dark": "#1E4D2B",
    "primary_green": "#2D6A4F",
    "secondary_olive": "#52796F",
    "table_header_bg": "#EAF2EC",
    "table_subhead_bg": "#F4F7F5",
    "table_border_dark": "#1E4D2B",
    "table_border_light": "#D8E2DC",
    "text_main": "#111111",
    "text_muted": "#555555",
    "text_caption": "#777777",
    "background_white": "#FFFFFF"
  }
}
```

---

## 4. 단락 포맷 규칙 (Paragraph Spacing Rules)

- **본문 일반 문단**:
  - 문단 앞 간격: `0 pt`
  - 문단 뒤 간격: `1.0 ~ 1.5 pt`
- **소제목 앞 간격**:
  - 문단 앞 간격: `4.0 ~ 6.0 pt`
  - 문단 뒤 간격: `2.0 pt`
- **표 전후 간격**:
  - 표 상단 캡션 문단 앞 간격: `4.0 pt`
  - 표 하단 출처 문단 뒤 간격: `4.0 pt`
