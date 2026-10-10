# 👑 [vf17-hwpx-clone-final] 대규모 PDF to HWPX/DOCX 100% 무손실 복제 & 한글 원격 제어 마스터 스킬

본 저장소는 (AX)창업기술 이한규 대표의 고유 지식재산권을 바탕으로, 사문화된 대규모 PDF 문서를 단 1글자·1표·1페이지의 오차도 없는 **Zero-Drift 100% 살아있는 문서(DOCX, HWP, HWPX)**로 복제하고 **Windows COM API 기반 원격 제어(HWP_REMOCON)**를 완결하는 대한민국 최고 정밀도의 엔터프라이즈급 문서 복제 마스터 시스템입니다.

---

## 1. 주요 핵심 기능 및 달성 성과

1. **Zero-Drift 100% (62 / 62 페이지 완벽 일치)**:
   - 한국농촌경제연구원(KREI) 농업전망 2026 제8장 엽근채소 대규모 리포트(62쪽)를 대상으로 **MS Word COM 실측 62쪽, Hancom Office COM 실측 62쪽**을 동시에 달성 및 공인.
2. **표 중첩 (Overlapping) 0건 완전 박멸**:
   - `TreatAsChar=1`(글자처럼 취급) 전수 강제 및 가용 본문 폭(139.3mm) 비례 리사이징을 통해 표가 텍스트와 겹치는 고질적 결함 완전 척결.
3. **가짜 푸터 60건 & 가짜 소제목 표 8건 외과수술적 정제**:
   - 본문에 침투한 유령 페이지 번호를 정규식으로 박멸하고 네이티브 바닥글(`sec.Footers`)로 이관.
   - 소제목 1x2 표를 네이티브 Heading 문단으로 복원.
4. **다단(2-Column) 구역 분할 방지**:
   - `sectPr`의 type을 `continuous`로 고정하여 1페이지가 수십 페이지로 폭발 분할되는 버그 원천 차단.
5. **HWP_REMOCON 헤드리스 원격 제어 탑재**:
   - `FilePathCheckerModule` 보안 무인 통과 및 셀 내비게이션, 데이터 주입, 다중 포맷(HWP/HWPX/PDF) 자동 컴파일 파이프라인 완비.

---

## 2. 5대 마스터 규격 헌장 문서

- [`SKILL.md`](SKILL.md): 통합 마스터 파이프라인 및 실행 지침서
- [`DNA.md`](DNA.md): 20대 코어 청사진 v5.0 명세서
- [`DESIGN.md`](DESIGN.md): 물리적 판형(Crown Quarto 196x266mm), 미러 마진(31/26mm), 그리드 시스템
- [`STYLE.md`](STYLE.md): 서체 4중 매핑(한컴바탕/Times), 위계 계단, 컬러 토큰
- [`문서의기본.md`](문서의기본.md): Zero-Drift 100% 불변의 10대 계명
- [`HWP_REMOCON.md`](HWP_REMOCON.md): Windows COM API 원격 조종석 매뉴얼
- [`VERIFY.md`](VERIFY.md): 듀얼 엔진 실측 및 Multimodal VisionCheck 검증 명세서

---

## 3. 완제 산출물 (result/)

- `[001]_ZeroDrift_62p_마스터.docx`: MS Word 62페이지 공인 마스터
- `[002]_MSWord_ZeroDrift_62p_공인.pdf`: MS Word 렌더링 62페이지 PDF
- `[003]_ZeroDrift_62p_마스터.hwp`: 한글 2024/2020 실측 62페이지 완제본
- `[004]_ZeroDrift_62p_마스터.hwpx`: 대한민국 정부 개방형 KS X 6101 표준 62페이지 완제본
- `[005]_Hancom_ZeroDrift_62p_공인.pdf`: 한글 엔진 렌더링 62페이지 PDF
- `[160]_VisionCheck_p01~p62.png`: 300 DPI 시각 감사 증빙 캡처
- `[161]_HancomVisionCheck_p01~p62.png`: 한글 엔진 시각 감사 증빙 캡처

---

## 4. 공식 등록 및 배포

- **저장소**: `github.com/dansarang99/vf/vf17_hwpx_clone_final`
- **시스템 등록 경로**:
  - `C:\Users\note\vf\.github\skills\vf17-hwpx-clone-final\SKILL.md`
  - `C:\Users\note\.gemini\config\skills\vf17-hwpx-clone-final\SKILL.md`
