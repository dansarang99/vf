# 🏛️ [DOCUMENT_DNA] 20대 코어 청사진 v5.0 Master Specification

본 문서는 (AX)창업기술 이한규 대표의 고유 지식재산권을 바탕으로, 사문화된 대규모 PDF를 100% 무손실 살아있는 문서로 복제하기 위해 사전에 반드시 계측하고 확정해야 하는 20대 핵심 매개변수 명세서입니다.

---

## 1. Part I: 비즈니스 및 판형 기하학 (Business & Geometry)

1. **`businessDNA`**:
   - 발행기관: 한국농촌경제연구원 (KREI)
   - 보고서명: 농업전망 2026 (KREI Agricultural Outlook 2026)
   - 문서 권호: 제8장 엽근채소 수급 동향과 전망
   - 저자진: 지선우, 윤성욱, 남호진, 안나영, 손호기 (5인)
   - 문서 번호 및 접두어 규칙: NX ➔ AX 동기화

2. **`DESIGN (물리적 판형)`**:
   - 용지 규격: Crown Quarto (변형 4륙판, 196.14mm × 265.99mm)
   - 뷰포트 포인트: 556.0pt × 754.0pt
   - 용지 방향: 세로 (Portrait)

3. **`STYLE (컬러 토큰 및 선 규격)`**:
   - 프라이머리 딥그린: `#1E4D2B` (표 메인 헤더 및 대제목)
   - 세컨더리 올리브: `#4A7C59` (소제목 및 불릿)
   - 표 헤더 배경: `#EAF2EC` (연한 회색-녹색)
   - 표 테두리선: 상단/하단 이중선 또는 1.0pt 실선, 내부선 0.5pt 실선
   - 캡션 회색: `#666666` (출처 및 주석)

4. **`[서체, 글꼴] 4중 매핑`**:
   - 대표 한글 명조: 한컴바탕 (보조: 함초롬바탕, KoPub바탕)
   - 대표 한글 고딕: 한컴고딕 (보조: 함초롬돋움, KoPub돋움)
   - 대표 영문/숫자: Times New Roman
   - 보조 영문: Arial

5. **`Typography 위계 계단`**:
   - 대제목 (Chapter Title): 18.0pt, Bold, 중앙 정렬
   - 중제목 (Section Title): 14.0pt, Bold, 왼쪽 정렬
   - 소제목 (Sub-section): 11.0pt, Bold
   - 본문 (Body): 9.5pt, Regular, 양쪽 정렬
   - 표 내부 (Table Cell): 7.0pt ~ 8.0pt, Regular
   - 각주 및 출처 (Footnote/Source): 7.5pt ~ 8.0pt

6. **`상하좌우 여백 (미러 마진)`**:
   - 상단 여백: 16.5mm (46.8pt)
   - 하단 여백: 8.8mm (25.0pt)
   - 홀수 페이지: 안쪽(좌) 31.0mm, 바깥쪽(우) 26.0mm
   - 짝수 페이지: 안쪽(우) 31.0mm, 바깥쪽(좌) 26.0mm
   - 본문 가용 폭: 139.3mm (39,486 HWP Unit / 394.8pt)

7. **`장평·자간·줄간격`**:
   - 장평 (Scale): 95%
   - 자간 (Letter Spacing): -0.5pt (-5%)
   - 본문 줄간격: 150% (Word 기준 8.5pt ~ 9.0pt 고정치)
   - 문단 위/아래 간격: 0pt / 1.5pt

---

## 2. Part II: 정보 개체 및 미디어 (Objects & Media)

8. **`표 (Table) 속성 통제`**:
   - 총 표 개수: 73개 (본문 60개, 부록 13개)
   - 배치 속성: `TreatAsChar=1` (글자처럼 취급) 전수 필수
   - 최대 가용 폭: 139.3mm (초과 시 비율 유지 비례 축소)
   - 셀 내부 안여백: 좌우 1.5mm, 상하 0.0mm (높이 팽창 차단)
   - 줄간격: 셀 내부 120% (Word 7.0pt ~ 8.0pt)

9. **`그래프 및 차트`**:
   - 차트 개수: 13종 (도매가격, 재배면적 추이 등)
   - 이미지 포맷: PNG 300 DPI 무손실 추출
   - HWPX 임베딩: `BinData/` 폴더 내 저장 및 `<hp:pic>` 연동

10. **`대형 표제면 배너`**:
    - 챕터 시작면(P01) 상단 타이틀 배너 300 DPI 무손실 안착
    - 배경 장식 및 일러스트 원형 보존

11. **`각주 및 참조자료 앵커링`**:
    - 1페이지 저자 소속 각주: `space_before 30pt` 적용 후 바닥 고정
    - 본문 각주: Y≈653pt 바닥 영역 정렬

---

## 3. Part III: 구조 및 네이티브 조판 (Structure & Native Layout)

12. **`HWPX 네이티브 XML 태그`**:
    - 문단: `<hp:p>`
    - 런: `<hp:run>`
    - 텍스트: `<hp:t>`
    - 줄바꿈 세그먼트: `<hp:linesegarray>`

13. **`개방형 KS X 6101 패키징`**:
    - mimetype: `application/hwp+zip` (무압축, 0번 오프셋)
    - 버전 정의: `version.xml`
    - 메타데이터: `META-INF/container.xml`, `Contents/content.hpf`

14. **`문단 그루핑 및 런 머징`**:
    - `merge_runs`: 인접한 동일 서식 런을 병합하여 텍스트 검색성 100% 확보

15. **`구역 및 다단 (Section & Column)`**:
    - 전체 구역 수: 68개 구역
    - 2단 다단 구역: `sectPr`의 type을 반드시 `continuous`로 고정 (페이지 쪼개짐 원천 차단)

16. **`content.hpf 매니페스트 동기화`**:
    - 모든 `section0.xml` ~ `section61.xml` 스파인(Spine) 등록 및 ID 순차 매핑

---

## 4. Part IV: 원격 제어 및 무결성 (Automation & Integrity)

17. **`FilePathCheckerModule`**:
    - 레지스트리 경로: `HKCU\Software\Hnc\HwpAutomation\Modules`
    - 보안 승인 팝업 0% 차단

18. **`듀얼 COM OLE 엔진 검증`**:
    - Word: `wdoc.ComputeStatistics(2) == 62`
    - Hancom: `hwp.PageCount == 62`

19. **`HWP_REMOCON 원격 제어 인터페이스`**:
    - 셀 주소 기반 내비게이션 및 정밀 데이터 치환

20. **`[001]~[999] 결과물 순차 보존 체계`**:
    - 모든 생성 파일의 고유 번호 영구 보존
