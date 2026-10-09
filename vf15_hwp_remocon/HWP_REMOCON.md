# 🎮 [HWP_REMOCON.md] 한글(HWP) 원격 제어 & 자동화 엔진 마스터 규격서

> **기술 스택**: Windows OS COM (Component Object Model) · Python 3 · `pyhwpx` · `win32com.client` · Hancom HwpObject Core  
> **핵심 원칙**: 100% 무손실 서식 보존 (Zero-Drift) · 외과수술적 텍스트 치환 · 멀티모달 시각 피드백 (`VisionCheck`) · 대화형 사용자 입력 모달 연동

---

## 1. 아키텍처 개요 (Architecture Overview)

```
========================================================================================
[사용자 요청 / 원천 데이터 (PDF·이미지·텍스트)]
       │
       ▼
[AI 에이전트 & HwpRemoconEngine] ── Headless Background 구동
       │
       ├─ Step 1: FilePathCheckDLL 보안 승인 모듈 자동 등록
       ├─ Step 2: HWPFrame.HwpObject 프로세스 바인딩 (COM IPC)
       ├─ Step 3: 표(Table) 구조 전수 스캔 및 셀 주소(goto_addr) 매핑
       ├─ Step 4: 외과수술적 텍스트 주입 (SelectAll -> Delete -> insert_text)
       ├─ Step 5: 셀/문단 중앙 정렬 (ParagraphShapeAlignCenter)
       ├─ Step 6: 특수 체크박스 치환 ('□ 예' -> '■ 예')
       ├─ Step 7: 서명 날짜 캘리브레이션 ('2026.   .    .' -> '2026. 10. 10.')
       └─ Step 8: 네이티브 PDF 렌더링 엔진 호출 (save_as(..., 'PDF'))
       │
       ▼
[VisionCheck 엔진] ── PyMuPDF 이미지 렌더링 & AI 시각 다차원 감사
========================================================================================
```

---

## 2. 핵심 기술 스택 및 API 명세

### ① COM API & 보안 승인 자동화 (`FilePathCheckDLL`)
한글과컴퓨터는 외부 프로그램이 한글 문서를 열 때 보안 경고 팝업을 발생시킵니다. 이를 완벽히 무인화(Headless)하기 위해 레지스트리 보안 모듈을 등록합니다.
```python
import win32com.client

hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
# 보안 승인 DLL 모듈 등록 (팝업 차단)
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
# 백그라운드 무인 실행 모드 (창 숨김)
hwp.XHwpWindows.Item(0).Visible = False
```

### ② `pyhwpx` 고수준 래퍼 엔진 활용
`pyhwpx`를 통해 저수준 COM 조작의 불안정성을 배제하고 강력한 셀 탐색 및 문서 제어를 수행합니다.
```python
from pyhwpx import Hwp

hwp = Hwp(visible=False)
hwp.open("문서경로.hwp")
```

### ③ 표(Table) 셀 내비게이션 & 외과수술적 텍스트 주입
기존 서식(글꼴: 휴먼명조 13pt, 자간, 장평, 셀 여백 등)을 단 1픽셀도 손상시키지 않고 내용만 완벽하게 교체합니다.
```python
def set_cell_value(hwp, addr: str, text: str, align_center: bool = True):
    """
    특정 셀 주소(예: 'B2', 'A6')로 이동하여 기존 내용을 깨끗이 비우고 신규 텍스트를 주입합니다.
    """
    # 1. 대상 셀로 정확히 커서 이동
    hwp.goto_addr(addr)
    # 2. 셀 내용 전체 선택
    hwp.HAction.Run("SelectAll")
    # 3. 기존 내용 삭제
    hwp.HAction.Run("Delete")
    # 4. 신규 내용 삽입
    if text:
        hwp.insert_text(text)
    # 5. 문단 정렬 적용
    if align_center:
        hwp.HAction.Run("ParagraphShapeAlignCenter")
```

### ④ 특수 체크박스 기호 정밀 치환
유니코드 사각 기호(`□`, U+25A1)를 마킹 기호(`■`, U+25A0 또는 `☑`, U+2611)로 치환합니다.
```python
# 체크박스 단어 검색 후 즉각 치환
hwp.MoveDocBegin()
if hwp.find("□ 예", direction="AllDoc"):
    hwp.insert_text("■ 예")
```

### ⑤ 서명일자 역방향 탐색 치환
문서 하단의 서명일자(`2026.   .    .`)를 문서 끝에서 역방향 탐색(`direction='Backward'`)하여 본문의 다른 날짜와 혼동 없이 정확히 치환합니다.
```python
hwp.MoveDocEnd()
if hwp.find("2026", direction="Backward"):
    hwp.MoveLineBegin()
    hwp.MoveSelLineEnd()
    hwp.insert_text("2026. 10. 10.")
    hwp.HAction.Run("ParagraphShapeAlignCenter")
```

### ⑥ 한컴 네이티브 PDF 렌더링 엔진 호출
별도의 외부 변환기 없이 한글 프로그램 자체의 PDF 프린터 엔진을 직접 구동하여 원본과 100% 동일한 고해상도 PDF를 컴파일합니다.
```python
hwp.save_as("완성문서.hwp")
hwp.save_as("완성문서.pdf", "PDF")
hwp.quit()
```

---

## 3. 대화형 사용자 입력 연동 (`ask_question` 브리지)
원천 데이터(사업자등록증 등)에 누락된 항목(예: 개인 휴대전화번호, 담당자 직통번호 등)이 있을 경우:
1. 시스템 레벨의 `ask_question` 모달 UI를 호출하여 사용자에게 명확한 선택지 및 직접 입력창(Other)을 제공합니다.
2. 사용자가 제출한 실시간 입력을 파이프라인 변수로 수신합니다.
3. HwpRemoconEngine을 통해 해당 빈칸에 즉시 주입하고 최종 문서를 컴파일합니다.
