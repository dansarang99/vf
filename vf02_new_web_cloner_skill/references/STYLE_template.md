# STYLE.md 추출 및 작성 표준 규격
## (Color Palette Tokens, Surface Elevation & Dark/Light Themes)

> **목적**: 레퍼런스 프레젠테이션의 배경, 카드 표면, 테두리, 액센트 색상 토큰을 RGB/HEX로 추출하여 무결점의 일관된 시각적 미학(Aesthetics)을 유지하기 위함.

---

## 1. 표준 디자인 토큰 체계 (Design Tokens)

### 1) 캔버스 및 서피스 토큰 (Canvas & Surface)
- `COLOR_BG`: 슬라이드 전체 바탕 캔버스 색상
  - Light (농촌재생 템플릿): Soft Pale Mint (`#E4F8EC`, RGB 228, 248, 236)
  - Dark (딥스페이스 테크): Deep Navy Slate (`#0B1120`, RGB 11, 17, 32)
- `COLOR_CARD`: 플로팅 카드 컨테이너 표면 색상
  - Light: Pure Snow White (`#FFFFFF`, RGB 255, 255, 255)
  - Dark: Dark Glass Surface (`#1E293B`, RGB 30, 41, 59, 85% 투명도)
- `COLOR_CARD_SUB`: 서브 컨테이너 / 내부 강조 박스 색상
  - Light: Pale Mint Tint (`#F1F9F4`, RGB 241, 249, 244)
  - Dark: Deep Navy Sub-box (`#0F172A`, RGB 15, 23, 42)
- `COLOR_CARD_BORDER`: 카드 외곽선 테두리 색상
  - Light: Delicate Mint Border (`#D1E7DD`, RGB 209, 231, 221, 두께 1.0~1.5pt)
  - Dark: Electric Cyan Line (`#38BDF8`, RGB 56, 189, 248, 두께 1.0~1.5pt)

### 2) 3대 액센트 컬러 토큰 (3-Pillar Accent Palette)
- `COLOR_ACCENT_PRIMARY`: 메인 강조 / 액션 / 기술적 신뢰
  - Cerulean Blue (`#0785C0`, RGB 7, 133, 192)
- `COLOR_ACCENT_SECONDARY`: 친환경 / 지속가능성 / 우위 성과
  - Emerald Jade (`#0D7C5B`, RGB 13, 124, 91)
- `COLOR_ACCENT_HIGHLIGHT`: 핵심 차별점 / 긴급 지표 / 경고
  - Amber Gold (`#D97706`, RGB 217, 119, 6)

### 3) 타이포그래피 컬러 토큰 (Typography Palette)
- `COLOR_TEXT_TITLE`: 헤드라인 및 주요 타이틀
  - Midnight Navy (`#0F172A`, RGB 15, 23, 42)
- `COLOR_TEXT_BOLD`: 리드문 및 핵심 불릿 헤드
  - Dark Slate (`#1E293B`, RGB 30, 41, 59)
- `COLOR_TEXT_BODY`: 본문 설명 텍스트
  - Slate Charcoal (`#334155`, RGB 51, 65, 85)
- `COLOR_TEXT_MUTED`: 출처, 각주, 풋노트, 부가 메타데이터
  - Slate Gray (`#64748B`, RGB 100, 116, 139)

---

## 2. 텍스트 추출 가이드 및 자동 스캔 규칙

```python
# 파워포인트 색상 토큰 추출 알고리즘 예시
from pptx import Presentation
prs = Presentation('upload/reference.pptx')
slide = prs.slides[0]
bg_color = slide.background.fill.fore_color.rgb # 캔버스 배경 RGB 감지
shape = slide.shapes[0]
card_color = shape.fill.fore_color.rgb         # 카드 서피스 RGB 감지
border_color = shape.line.color.rgb            # 테두리 RGB 감지
```
