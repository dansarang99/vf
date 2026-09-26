# HWP to DOCX 100% Zero-Loss Conversion Architecture Guide
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

---

## 1. 아키텍처 개요
HWP(아래아한글) 문서를 DOCX(워드)로 토씨 하나 다르지 않고 페이지 수까지 완벽히 일치(Zero-Drift)시키기 위한 핵심 파이프라인:

```
[HWP 파일]
   │
   ▼ (Hancom HwpObject OLE Automation)
[초고해상도 PDF 변환]
   │
   ▼ (pdf2docx Advanced Reflow Engine)
[네이티브 DOCX 구조체 생성]
   │
   ▼ (OOXML Surgical In-Place Transfusion Engine)
[사명/문서번호 네이티브 텍스트 치환 & 여백/줄간격 캘리브레이션]
   │
   ▼ (MS Word COM Automation & PyMuPDF Dual-Engine Audit)
[100% 무손실 복제본 완성 & 페이지 편차 0% 기계적 검증]
```

## 2. 한컴 COM 자동화 핵심 규칙
- ProgID: `HWPFrame.HwpObject`
- 보안 승인 모듈 등록 또는 `hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")` 적용
- PDF 변환 API: `hwp.SaveAs(pdf_path, "PDF", "pdf")`
- 직접 DOCX 저장 시 발생하는 표 깨짐 현상을 PDF 무손실 중간 매개체를 통해 100% 방지

## 3. 네이티브 TEXT 치환 원칙
- 비트맵 이미지 치환 금지: 워드 상단 머리글 표의 회사명 로고 셀에서 `<w:drawing>` 태그를 제거하고 `<w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>(AX)창업기술</w:t>`를 주입하여 100% 자연스러운 네이티브 텍스트로 치환.
- 문서번호 동기화: 원본 접두어(`NX-`)를 새 사명 접두어(`AX-`)로 일괄 치환.
