# Zero-Drift 외과수술적 캘리브레이션 기술 가이드 (Zero-Drift Guide)
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

---

## 1. Zero-Drift 개념
- **정의**: 원천 PDF 문서의 페이지 수와 복제본(DOCX/PDF)의 페이지 수가 단 1페이지의 편차도 없이 100.00% 일치하는 상태 (`Drift = 0%`).
- **목적**: 원본의 인용 페이지(예: 35쪽 표 2-1)와 복제본의 페이지가 완벽히 일치하여 학술적·법적 효력 유지.

---

## 2. 4대 외과수술적 압축 기법

### 1) 단락 상하 여백 제거 (w:before / w:after = 0)
- Word 기본 서식에 의해 모든 단락마다 6~10pt의 여백이 삽입되어 30페이지 문서 기준 3~5페이지의 불필요한 확장이 발생합니다.
- OOXML의 `<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>`를 적용하여 단락 간 불필요한 간격을 전수 제거합니다.

### 2) 표(Table) 셀 패딩 및 행 높이 캘리브레이션
- 표 내부 단락 여백을 0pt로 강제 고정하고, 셀 상하 패딩(`w:top`, `w:bottom`)을 20~40 dxa 수준으로 최적화합니다.
- 표 제목(캡션)과 표 상단 간격을 Pt(4)로 압축합니다.

### 3) 챕터 표제면 300 DPI 배너 안착
- 텍스트 타이포그래피로 구현 시 폰트 크기 및 행간 오차로 밀리는 현상을 원천 방지하기 위해, 원본 표제면 배너를 300 DPI 래스터 이미지로 추출하여 정확한 너비(`Inches(5.55)`)로 단일 단락에 배치합니다.

### 4) MS Word COM OLE 실측 검증
- 가상 PDF 렌더러가 아닌 Windows OLE COM (`win32com.client.DispatchEx("Word.Application")`)을 직접 구동하여 `wdoc.ComputeStatistics(2)`로 Word 내부 렌더링 페이지 수를 실측합니다.
