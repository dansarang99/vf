# DOCX Cloner Skill Architecture Specification
## (100% Surgical OOXML Clone Architecture)

> **작성자**: (AX)창업기술 이한규 대표  
> **프로젝트**: `vf04_docxcloner_skill(iso9001)`  
> **목적**: 원본 문서 대비 100% 동일한 서식/자간/장평/여백/페이지 수 보장 및 다중 페이지 브랜드 치환 기술 표준화

---

## 1. 기술적 난제와 해결 방안 (Technical Challenge & Solution)

### 기존 접근법의 한계 (Legacy python-docx limitations)
1. **서식 소실**: `python-docx`나 `docx-js`로 문서를 재생성할 경우, 한글 워드나 특수 워드 프로세서가 생성한 고유 XML 네임스페이스(`w:spacing`, `w:w`, `w:lang`, 복잡한 테이블 테두리)가 누락되어 68페이지 문서가 64페이지 또는 72페이지로 어긋나는 치명적인 페이지 드리프트(Page Drift) 발생.
2. **머리글 렌더링 붕괴**: 다중 행 머리글 표 내부의 도면(`w:drawing`) 앵커 및 릴레이션십 ID가 재할당되면서 로고가 비뚤어지거나 삭제됨.

### 외과수술적 OPC 직접 조작 기법 (Surgical OOXML Direct Manipulation)
1. **바이너리 레벨 보존**:
   - `[Content_Types].xml`, `_rels/.rels`, `word/_rels/*.rels`, `word/styles.xml`, `word/numbering.xml`, `word/settings.xml`을 100% 원본 그대로 유지.
2. **Surgical In-Place Text Transfusion**:
   - `word/document.xml` 및 `word/header*.xml`을 메모리 스트림 상에서 UTF-8 파싱.
   - 단락 서식(`w:pPr`), 런 서식(`w:rPr`), 글꼴/자간/장평 속성은 0.1 twip도 건드리지 않고, `<w:t>` 태그 내부의 지정 문자열만 핀포인트로 교체.
3. **Multi-Page Header Asset Transfusion**:
   - 머리글에 바인딩된 비트맵 에셋(`image6.bmp`)을 동일한 포맷 규격(175x67, 24-bit RGB BMP)의 고해상도 안티앨리어싱 로고로 1:1 바이너리 치환하여, 전체 68페이지 전 영역의 머리글에 신규 브랜드를 완벽하게 영구 반영.
4. **Dual Verification Pipeline**:
   - 1단계: MS Word COM 엔진(`win32com.client`)을 통한 `ComputeStatistics(wdStatisticPages)` 실행으로 68페이지 일치 검증.
   - 2단계: PyMuPDF 150 DPI 고해상도 렌더링을 통한 픽셀 단위 레이아웃 무결성 시각 검증.
