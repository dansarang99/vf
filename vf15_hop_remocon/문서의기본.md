# 🛡️ [VERIFY.md] 멀티모달 시각 검증(VisionCheck) & 0-Error 무결성 감사 프로토콜

> **검증 철학**: "코드가 성공했다고 문서를 믿지 마라. 인간의 눈과 AI의 시각 모델이 직접 보고 검증한 것만 공인한다."  
> **핵심 엔진**: PyMuPDF (fitz) · Hancom Native PDF Engine · Multimodal Vision Inspection (`VisionCheck`) · Zero-Drift 캘리브레이션

---

## 1. VisionCheck 3단계 다차원 검증 체계

```
[한글 HWP 원본 서식] ───┐
                       ├─▶ [비교 대조 (Diff & Eye)] ──▶ [무결성 공인 합격증]
[컴파일된 완성 PDF]    ───┘
         │
         ▼
[Step 1: PyMuPDF 300 DPI 래스터라이징 (고해상도 이미지화)]
         │
         ▼
[Step 2: 5대 무결성 정밀 계측 (Zero-Drift Metric)]
  1) 페이지 일탈률: 0% (원본 1p == 결과물 1p)
  2) 표 레이아웃: 셀 병합/너비/여백 100% 보존
  3) 텍스트 주입: 대상 셀 내 위치 및 중앙 정렬 완비
  4) 체크박스 상태: 유니코드 사각형 마킹 ('■') 식별
  5) 서명 일자: 연/월/일 포맷 완제 배치
         │
         ▼
[Step 3: 멀티모달 AI 시각 판독 (view_file / Vision OCR)]
  - 글자 겹침(Overlap), 행 삐져나옴(Overflow), 줄바꿈 왜곡 여부 전수 검사
```

---

## 2. 5대 무결성 검증 지표 (Zero-Drift 100%)

| 검증 항목 | 검증 방식 | 허용 오차 | 판정 기준 |
| :--- | :--- | :---: | :--- |
| **1. 페이지 수 (Page Count)** | PDF 및 HWP 총 페이지 수 계측 | **0%** | 원본 페이지 수와 1:1 일치해야 함 (예: 1페이지 서식은 정확히 1페이지) |
| **2. 표 레이아웃 (Table Grid)** | 바운딩 박스(Bounding Box) 오차 측정 | **0.05pt 이하** | 표의 높이, 너비, 셀 구분선이 찌그러지거나 밀려나지 않아야 함 |
| **3. 글꼴 및 스타일 (Typography)** | 폰트 패밀리 및 포인트 크기 계측 | **0%** | 원본 지정 폰트(휴먼명조 13pt 등) 및 행간 그대로 유지 |
| **4. 체크박스 마킹 (Checkbox)** | 텍스트 스트림 및 시각 이미지 판독 | **0-Error** | `□`가 남아있지 않고 `■` 또는 `☑`로 확실히 변환되었는지 검증 |
| **5. 필수 필드 충족도 (Completeness)**| 정규표현식 및 키워드 추출 검사 | **100% 충족** | 회사명, 대표자명, 연락처, 이메일, 신청일자 등 필수 빈칸 누락 0건 |

---

## 3. PyMuPDF 기반 자동 렌더링 & 시각 검증 스크립트

```python
import fitz  # PyMuPDF
import os

def generate_verification_preview(pdf_path: str, output_image_path: str, dpi: int = 200):
    """
    완성된 PDF 문서를 고해상도 PNG 이미지로 렌더링하여 AI 시각 모델이 검증할 수 있도록 변환합니다.
    """
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    print(f"[검증] 총 페이지 수: {page_count}p")
    
    # 1페이지 서식 검증
    if page_count != 1:
        print(f"[경고] 페이지 일탈 발생! 원본(1p) != 현재({page_count}p)")
        return False
        
    page = doc[0]
    pix = page.get_pixmap(dpi=dpi)
    pix.save(output_image_path)
    print(f"[검증] 시각 검증용 고해상도 이미지 저장 완료: {output_image_path}")
    return True
```

---

## 4. 시각 감사(Vision Feedback) 자동 보정 절차
1. **시각 이미지 생성**: 한글 엔진이 컴파일한 PDF를 `PyMuPDF`로 고해상도 PNG로 변환.
2. **시각 모델 감사**: `view_file` 도구를 통해 AI가 렌더링 이미지를 직접 육안 검사.
3. **이상 감지 시 자동 롤백 및 재캘리브레이션**:
   - 체크박스가 비어있는 경우: 문자열 매칭 재탐색 후 직접 주입.
   - 글자가 셀을 벗어나는 경우: 자간 또는 글자 크기 미세 조정(0.5pt 축소 등).
   - 줄바꿈이 일어난 경우: 문단 여백 및 셀 여백 캘리브레이션.
4. **최종 승인**: 모든 항목이 100% 충족될 때만 사용자에게 최종 완료 파일 인계.
