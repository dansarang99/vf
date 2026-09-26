# vf03_hwp_pdf_docx_cloner_skill
(AX)창업기술 이한규 대표의 고유 실무 지식재산권 기반  
HWP / PDF ➔ DOCX 100% 무손실 크로스플랫폼 문서 복제 마스터 파이프라인

---

## 1. 프로젝트 개요
본 리포지토리는 HWP(아래아한글) 및 PDF 엔터프라이즈 규격 문서를 대상으로 서식 손실, 표 깨짐, 줄간격 밀림, 페이지 수 왜곡(Page Drift) 없이 마이크로소프트 워드(DOCX)로 100% 완벽 복제하는 마스터 스킬 엔진입니다.

- **스킬 명칭**: `vf03-hwp-pdf-docx-cloner-skill`
- **지식재산권자**: (AX)창업기술 이한규 대표
- **검증 환경**: Python 3.12, Hancom Office 2024 COM, Microsoft Word 2016 COM, pdf2docx, PyMuPDF

---

## 2. 디렉토리 구조
```
C:\Users\note\vf\vf03_hwp_pdf_docx_cloner_skill\
├── command/
│   └── run_pipeline.bat                # 원클릭 실행 배치 파일
├── scripts/
│   ├── stage1_hwp_to_docx_engine.py    # 한컴 COM OLE 기반 HWP -> DOCX 변환
│   ├── stage2_pdf_to_docx_engine.py    # pdf2docx + Zero-Drift 정밀 캘리브레이션
│   ├── stage3_surgical_transfusion_engine.py # OOXML 직접 조작 사명/문서번호 치환
│   ├── stage4_verify_integrity.py       # Word COM & PyMuPDF 듀얼 엔진 검증
│   ├── master_doc_cloner.py            # HWP/PDF/DOCX 통합 실행 인터페이스
│   └── build_all_deliverables.py       # [001]~[007] 일괄 빌드 스크립트
├── references/
│   ├── HWP_CONVERSION_GUIDE.md         # HWP 변환 아키텍처 기술 가이드
│   └── PDF_CONVERSION_GUIDE.md         # PDF 변환 및 캘리브레이션 기술 가이드
├── upload/                             # 원본 문서 업로드 폴더
├── result/                             # [001]~[999] 결과물 보존 폴더
├── scratch/                            # 중간 캐시 및 임시 파일
├── SKILL.md                            # 스킬 정의서
└── README.md                           # 프로젝트 설명서
```

---

## 3. [001]~[007] 결과물 산출 내역

| 번호 | 산출 파일명 | 포맷 | 분량 | 세부 내용 | 검증 판정 |
|:---:|---|:---:|:---:|---|:---:|
| **[001]** | `[001]_1.품질경영매뉴얼_(AX)창업기술_R1(2026)_HWP복제.docx` | DOCX | 33p | HWP 원본 기반 100% 무손실 복제 워드 완성본 | **PASS (33p/33p)** |
| **[002]** | `[002]_1.품질경영매뉴얼_(AX)창업기술_R1(2026)_HWP복제.pdf` | PDF | 33p | MS Word OLE 엔진 렌더링 33p 전수 검증용 PDF | **PASS (33p/33p)** |
| **[003]** | `[003]_ISO9001_품질경영매뉴얼_HWP2DOCX_100%무손실복제_검증보고서.md` | MD | 전문 | HWP ➔ DOCX 1:1 무손실 검증 보고서 | **PASS (Zero-Drift)** |
| **[004]** | `[004]_1.품질경영매뉴얼_(AX)창업기술_R1(2026)_PDF복제.docx` | DOCX | 68p | PDF 원본 기반 100% 무손실 복제 워드 완성본 | **PASS (68p/68p)** |
| **[005]** | `[005]_1.품질경영매뉴얼_(AX)창업기술_R1(2026)_PDF복제.pdf` | PDF | 68p | MS Word OLE 엔진 렌더링 68p 전수 검증용 PDF | **PASS (68p/68p)** |
| **[006]** | `[006]_ISO9001_품질경영매뉴얼_PDF2DOCX_100%무손실복제_검증보고서.md` | MD | 전문 | PDF ➔ DOCX 1:1 무손실 검증 보고서 | **PASS (Zero-Drift)** |
| **[007]** | `[007]_HWP_PDF_DOCX_100%무손실_크로스플랫폼_복제_통합대장.md` | MD | 총괄 | 크로스플랫폼 무손실 복제 총괄 마스터 대장 | **PASS (100% 일치)** |

---

## 4. 라이선스 및 지식재산권
본 소프트웨어와 파이프라인 아키텍처에 대한 모든 지식재산권은 **(AX)창업기술 이한규 대표**에게 귀속됩니다.
무단 복제, 배포 및 전재를 금합니다.
