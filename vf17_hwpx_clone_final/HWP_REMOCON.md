# 🏛️ [HWP_REMOCON] Windows COM API 기반 원격 제어 실무 매뉴얼

본 문서는 (AX)창업기술 이한규 대표의 지식재산권을 기반으로, 무손실 복제된 한글 문서 위에서 가동되는 **헤드리스 원격 제어(Remote Control)** 핵심 API 및 자동화 파이프라인 명세서입니다.

---

## 1. 개요 및 연결 메커니즘

- **사용 엔진**: `pyhwpx` 및 `win32com.client`
- **보안 모듈**: `FilePathCheckerModule` (한글 보안 승인 팝업 100% 무인 차단)
- **작동 모드**: 헤드리스(`visible=False`) 백그라운드 고속 조작

```python
import os
from pyhwpx import Hwp

# 1. 인스턴스 초기화 및 보안 승인
hwp = Hwp(visible=False)
hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')
```

---

## 2. 핵심 원격 제어 함수 라이브러리

### (1) 문서 로드 및 상태 검증
```python
doc_path = os.path.abspath('result/[131]_ZeroDrift_62p_마스터.hwp')
hwp.open(doc_path)
print('Current Document Pages:', hwp.PageCount)
```

### (2) 표(Table) 객체 전수 속성 캘리브레이션 (TreatAsChar=1)
```python
ctrl = hwp.HeadCtrl
max_w = int(139.3 * 283.465)  # 39,486 HWP Unit (139.3mm)
tbl_cnt = 0

while ctrl:
    if ctrl.CtrlID == 'tbl':
        tbl_cnt += 1
        prop = ctrl.Properties
        prop.SetItem('TreatAsChar', 1)  # 글자처럼 취급 강제
        cur_w = prop.Item('Width')
        if cur_w and cur_w > max_w:
            ratio = max_w / cur_w
            prop.SetItem('Width', max_w)
            cur_h = prop.Item('Height')
            if cur_h:
                prop.SetItem('Height', int(cur_h * ratio))
        ctrl.Properties = prop
    ctrl = ctrl.Next

print(f'Processed {tbl_cnt} tables successfully.')
```

### (3) 특정 페이지 및 표 셀 내비게이션 & 외과수술적 데이터 주입
```python
# 특정 페이지로 이동
hwp.goto_page(6)

# 표 내부 특정 셀로 이동하여 내용 수정
# hwp.set_cell_text("수정할 텍스트")
```

### (4) 다중 포맷 무손실 동시 컴파일
```python
hwp.save_as('output.hwp', 'HWP')
hwp.save_as('output.hwpx', 'HWPX')
hwp.save_as('output.pdf', 'PDF')
hwp.quit()
```

---

## 3. 대화형 피드백 연동 (`ask_question`)

리모콘 조종석 가동 중 서식 의심 구간이나 데이터 결손 발생 시 즉시 대화형 모달을 띄워 사용자(본부장님)의 의사결정을 수렴합니다.
