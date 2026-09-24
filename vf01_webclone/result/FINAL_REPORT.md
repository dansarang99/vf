# 마지영 작가 단독 에디션 & 아틀리에 (MA JI YOUNG EDITION) 공식 웹사이트 구축 최종 보고서

---

## 1. 프로젝트 개요

* **목표:** 
  1. 하이엔드 온라인 에디션 갤러리의 미니멀하고 세련된 레이아웃 및 UX 시스템을 계승하되, **박서보 작가 및 외부 플랫폼(ARTN Edition 등)을 참조했다는 흔적을 100% 완전히 제거**.
  2. 독자적인 브랜드 아이덴티티인 **《MA JI YOUNG EDITION | 마지영 에디션 & 아틀리에》**로 자연스럽게 차별화 및 독립 브랜드화.
  3. `Web_마지영전시회.pptx`의 전 24슬라이드 콘텐츠(작가 소개, 국/영문 작가노트, 42점 전 작품, 시적 서정문, 청목미술관 개인전)를 완벽하게 통합.
* **작업 디렉토리:** `C:\Users\note\vf\vf01_webclone`
* **접속 주소:** `http://localhost:8080/` (배경 웹 서버 구동 중)
* **품질 검증:** 잔여 참조 흔적 정밀 검색(0건) 및 Playwright UI 자동화 테스트(0 Error) 통과.

---

## 2. 독자적 브랜드 차별화 및 흔적 완전 제거 내역

### ① 브랜드 아이덴티티 완전 독립 (MA JI YOUNG EDITION)
* **전용 로고 제작 및 적용:**
  * 헤더 다크 로고: `assets/images/logo_mjy.svg` (`MA JI YOUNG EDITION | 아틀리에`)
  * 푸터 라이트 로고: `assets/images/logo_mjy_w.svg` (`MA JI YOUNG EDITION | 아틀리에`)
* **메타데이터 & 파비콘:**
  * Title: `<title>마지영 MA JI YOUNG | MA JI YOUNG EDITION</title>`
  * Author & OG Tag: `MA JI YOUNG Edition & Atelier`, 마지영 개인전 《Moments》 공식 아카이브
  * Favicon: `logo_mjy.svg`
* **푸터 및 주소 정보 현행화:**
  * 마지영 아틀리에 & 청목미술관 학예실 공식 협력 체계 구축 (전북특별자치도 전주시 완산구 유연로 87 청목빌딩)
  * 프라이빗 뷰잉룸 및 소장 문의 창구(`contact@majiyoung-edition.art`, `063-228-8422`) 일원화

### ② 이전 작가 및 플랫폼 참조 흔적 100% 영구 삭제
* 기존 임시 파일(`artist_park_seo_bo.html`, `artist_ma_ji_young.html`, `assets/images/park_seo_bo/`) 영구 삭제.
* 상단 스위처를 기존 작가 스위처에서 **마지영 컬렉션 시리즈 퀵 셀렉터**로 전면 전환:
  * `[전체 컬렉션]`
  * `[대표작 (26-001~010)]`
  * `[4연작 모듈 세트]`
  * `[2연작 듀오 블록]`
* 소스 코드 전체 전수 검사(`Get-ChildItem -Recurse | Select-String`) 결과: **잔여 키워드 0건 완벽 달성**.

---

## 3. PPTX 콘텐츠 100% 디지털 아카이빙 성과

* **전시 타이틀:** 《Moments: 흔들리던 순간조차 찬란했던, 기억의 유닛(Unit)》
* **전시 정보:** 2026. 10. 13. ~ 10. 18. @ 청목 미술관 (Cheongmok Museum of Art)
* **전시 포스터:** `image1.png` → `assets/images/exhibition_moments_poster.png`
* **작가 초상 및 아틀리에:** `image2.png`, `image3.png`
* **국/영문 공식 작가노트:**
  * 국문: *"기억은 시간을 견디며 스스로를 증명한다... 42개의 기억의 파편들이 마침내 하나의 견고한 연대기가 되었다."*
  * 영문: *"Memory endures through time to prove itself... 42 fragments of memory have finally become a solid chronicle."*
* **수장고 전 작품 42점 디지털화:**
  * `Moments 26-001` "바람이 머무는 곳 (Where the Wind Lingers)" (W 67.5 x H 40.0 cm)
  * `Moments 26-002` "바로 지금, 여기 (Right Here, Right Now)" (W 17.5 x H 27.5 cm)
  * `Moments 26-003` ~ `26-004` "중심을 지키는 것 (Finding the Center)"
  * `Moments 26-005` "흐름에 맡기는 힘 (The Power of Yielding to the Flow)"
  * `Moments 26-006` ~ `26-010` "무제 (Untitled)"
  * `Moments 26-011` ~ `26-034` (4연작 모듈 세트 A~F)
  * `Moments 26-035` ~ `26-042` (2연작 듀오 블록 A~D)
* **작품별 국/영문 시구 라이트박스 연동:**
  * 각 작품 클릭 시 고해상도 이미지 확대, 큐레이토리얼 시적 텍스트, 규격, 소장 가격, 장바구니 담기 지원.

---

## 4. 디렉토리 구조

```
C:\Users\note\vf\vf01_webclone\
├── command/                          # 자동화 스크립트
│   ├── extract_pptx.py               # PPTX 텍스트 및 미디어 파서
│   └── test_ui_playwright.py         # Playwright 자동화 테스트 슈트
├── i-plan/                           # 설계 문서
│   ├── 01_analysis_artnedition.md    # 레이아웃 분석서
│   └── 02_integration_plan_ma_ji_young.md # 마지영 작가 통합 설계서
├── process/                          # 실행 로그
│   └── 01_execution_log.md           # 단계별 마일스톤 로그
├── result/                           # 테스트 검증 및 스크린샷
│   ├── 01_ma_ji_young_page.png       # 마지영 에디션 전체 메인 화면
│   ├── 02_artwork_lightbox_modal.png # 작품 상세 라이트박스 모달
│   ├── 03_exhibition_modal.png       # 청목미술관 개인전 모달
│   ├── 05_search_suggest_layer.png   # 실시간 검색 및 컬렉션 추천
│   └── FINAL_REPORT.md               # 본 최종 보고서
└── src/                              # 최종 서비스 웹 소스
    ├── index.html                    # 마지영 에디션 공식 웹사이트
    ├── css/
    │   ├── common.css                # GNB, 글로벌 배너, 검색창, 푸터 스타일
    │   └── style.css                 # 갤러리 그리드, 라이트박스 모달, 반응형 스타일
    ├── js/
    │   ├── data.js                   # 마지영 전 작품(42점) 및 전시 메타데이터
    │   └── main.js                   # 동적 렌더링, 필터링, 모달, 검색 컨트롤러
    └── assets/images/                # 전용 에셋 및 42점 원본 고해상도 이미지
        ├── logo_mjy.svg / logo_mjy_w.svg # 마지영 에디션 전용 신규 벡터 로고
        ├── exhibition_moments_poster.png # 청목미술관 공식 포스터
        ├── artist_ma_ji_young.png        # 작가 프로필
        └── artwork_moments_26_001.png ~ 26_042.png (42점 전 작품)
```

---

## 5. 실행 및 배포 URL

### ① Vercel 공식 라이브 배포 URL
* **운영 배포 도메인 (Production):**
  👉 **https://src-topaz-nu.vercel.app**
* **배포 상세 (Vercel Console):**
  - Project: `leehankyus-projects/src`
  - Deployment ID: `dpl_7MsZefgPJ1cK3pK4WJzADgtvLCvC`
  - 상태: `READY (HTTP 200 OK)`

### ② 로컬 프리뷰 서버
* **로컬 웹 서버:**
  👉 **`http://localhost:8080/`**
