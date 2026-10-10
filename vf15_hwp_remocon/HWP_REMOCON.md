# 🎮 [HWP_REMOCON.md] 살아있는 한글(HWP) 문서 원격 제어 & 자동화 엔진

> **핵심 전제**: "죽어있는 PDF를 100% 무손실로 깨워낸 [살아있는 골격 문서]가 존재할 때, 비로소 원격 제어(리모콘) 엔진이 그 진가를 발휘한다."

---

## 1. HWP_REMOCON의 역할과 포지셔닝

1. **복제(Cloner)와의 관계**:
   - `Cloner (복제)`: 원본 PDF의 판형(196×266mm), 미러 마진, 표, 차트, 각주, 장평(95%), 자간(-0.5pt)을 100% 동일하게 살아있는 HWP로 되살리는 **골격 창조자**.
   - `Remocon (원격제어)`: 그렇게 살아난 문서 위에서 특정 표의 셀 주소(`B2`, `A6`), 체크박스, 서명 날짜, 본문 단락을 외과수술적으로 찾아서 데이터를 주입·수정·삭제하는 **지능형 조종사**.

---

## 2. 7대 핵심 원격 제어 기술 (Core APIs)

### ① COM 헤드리스 바인딩 & 보안 모듈 승인
```python
import win32com.client
from pyhwpx import Hwp

hwp = Hwp(visible=False)
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
```

### ② 용지 판형 및 미러 마진 강제 주입 (`set_pagedef`)
A4 기본 설정을 깨부수고 원본 고유 판형을 주입:
```python
pagedef = {
    'PaperWidth': 196.14,  # 가로 (mm)
    'PaperHeight': 265.99, # 세로 (mm)
    'LeftMargin': 31.0,    # 안쪽 (mm)
    'RightMargin': 26.0,   # 바깥쪽 (mm)
    'TopMargin': 33.0,     # 위쪽 (mm)
    'BottomMargin': 25.0,  # 아래쪽 (mm)
    'HeaderLen': 15.0,     # 머리글 (mm)
    'FooterLen': 12.0      # 바닥글 (mm)
}
hwp.set_pagedef(pagedef, apply='all')
```

### ③ 표(Table) 셀 내비게이션 & 외과수술적 텍스트 주입
기존 셀의 서식(글꼴, 크기, 테두리, 배경색)을 100% 보존하면서 내용만 치환:
```python
def surgical_cell_write(hwp, addr: str, text: str, align_center: bool = True):
    hwp.goto_addr(addr)
    hwp.HAction.Run("SelectAll")
    hwp.HAction.Run("Delete")
    if text:
        hwp.insert_text(text)
    if align_center:
        hwp.HAction.Run("ParagraphShapeAlignCenter")
```

### ④ 특수 체크박스 외과수술적 치환
```python
hwp.MoveDocBegin()
if hwp.find("□ 예", direction="AllDoc"):
    hwp.insert_text("■ 예")
```

### ⑤ 서명일자 역방향 탐색 치환
```python
hwp.MoveDocEnd()
if hwp.find("2026", direction="Backward"):
    hwp.MoveLineBegin()
    hwp.MoveSelLineEnd()
    hwp.insert_text("2026. 10. 10.")
    hwp.HAction.Run("ParagraphShapeAlignCenter")
```

### ⑥ 대화형 모달 연동 브리지 (`ask_question`)
원천 서류에 누락된 항목이 있을 경우 사용자에게 실시간 입력창을 제공하고 그 값을 받아 즉시 주입.

### ⑦ 한컴 네이티브 PDF 컴파일러
외부 도구 없이 한글 자체의 PDF 인쇄 엔진을 직접 호출:
```python
hwp.save_as("완성문서.hwp")
hwp.save_as("완성문서.hwpx")
hwp.save_as("완성문서.pdf", "PDF")
```
