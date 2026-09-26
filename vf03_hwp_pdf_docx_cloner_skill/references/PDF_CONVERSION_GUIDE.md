# PDF to DOCX 100% Zero-Loss Conversion Architecture Guide
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

---

## 1. 아키텍처 개요
PDF 문서를 DOCX(워드)로 변환할 때 가장 큰 문제는 **단락 줄간격 및 여백 누적으로 인한 페이지 편차(Page Drift)**입니다.
본 가이드는 이를 0%로 완벽 제어하는 외과수술적 캘리브레이션 기술을 규정합니다.

## 2. Zero-Drift 캘리브레이션 핵심 원리
1. **단락 여백 압축**:
   - `pdf2docx`로 변환 시 각 셀과 단락에 기본 상하 마진(`w:before`, `w:after`)이 누적되어 페이지가 밀리는 현상 방지
   - `document.xml` 내의 `w:before="0"`, `w:after="0"`으로 0.1초 내 전수 압축
2. **상하 여백(w:pgMar) 미세 최적화**:
   - 상단 여백(`w:top`)을 200(약 3.5mm), 하단 여백(`w:bottom`)을 350 이하로 보정하여 표의 마지막 행이 다음 페이지로 밀리는 현상 원천 차단
3. **듀얼 엔진 검증 (Word COM + PyMuPDF)**:
   - MS Word OLE 엔진(`doc.ExportAsFixedFormat`)으로 실제 렌더링된 PDF 생성
   - PyMuPDF(`fitz.open`)를 통해 150 DPI 비주얼 Diff 및 페이지 수 100% 일치 판정
