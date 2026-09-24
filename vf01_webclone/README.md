# vf01_webclone: 웹사이트 복제 (Web Cloner) 마스터 파이프라인
> **기획 및 지식재산권자**: (AX)창업기술 이한규 대표  
> **공식 Vercel 라이브 배포**: [https://src-topaz-nu.vercel.app](https://src-topaz-nu.vercel.app)  
> **공식 GitHub 아카이브**: [https://github.com/dansarang99/vf/tree/main/vf01_webclone](https://github.com/dansarang99/vf/tree/main/vf01_webclone)

---

## 1. 프로젝트 개요

본 프로젝트는 임의의 프리미엄 레퍼런스 웹사이트(URL)와 기획/콘텐츠 소스(PPTX, PDF 등)를 입력받아:
1. 레퍼런스의 **하이엔드 디자인 시스템, 레이아웃, 인터랙션 UX를 100% 역공학**하고
2. 입력 콘텐츠(42점 전 작품 수장고, 국/영문 작가노트, 시적 서정문, 청목미술관 개인전)를 **100% 디지털화**하며
3. 레퍼런스 브랜드(박서보 화백, ARTN Edition 등)의 모든 흔적을 **0%로 완전 박멸(Surgical Zero-Trace Rebranding)**한 후
4. 독자적인 **《MA JI YOUNG EDITION | 마지영 에디션 & 아틀리에》** 브랜드로 재탄생시켜
5. Playwright E2E 0-Error 자동화 검증 및 **Vercel 글로벌 CDN 배포**까지 엔드투엔드로 완결한 실전 웹 클로너 프로젝트입니다.

---

## 2. 7대 핵심 기능 및 구현 스펙

1. **독자적 브랜드 아이덴티티**:
   - 상단 헤더: `assets/images/logo_mjy.svg` (다크 벡터 로고)
   - 하단 푸터: `assets/images/logo_mjy_w.svg` (라이트 벡터 로고)
   - 전북박물관·미술관협회 청목미술관 공식 안내 웹페이지 직통 연동
2. **원클릭 시리즈 퀵 셀렉터**:
   - `[전체 컬렉션]`, `[대표작 (26-001~010)]`, `[4연작 모듈 세트]`, `[2연작 듀오 블록]`
3. **고해상도 작품 라이트박스(Modal)**:
   - 42점 전 작품 확대 뷰, 국/영문 시적 서정문 해설, 치수, 소장 가격, 장바구니 담기 지원
4. **청목미술관 초대전 모달**:
   - 《Moments: 흔들리던 순간조차 찬란했던, 기억의 유닛》 전시 상세 및 공식 안내 페이지 연동
5. **실시간 검색어 레이어**:
   - 키워드 추천 및 컬렉션별 바로가기 드롭다운
6. **장바구니 & 위시리스트**:
   - 실시간 카운트 배지 및 토스트 알림 연동
7. **Playwright 0-Error 무결성 보증**:
   - 1440px 뷰포트 풀페이지 렌더링, 콘솔 및 페이지 런타임 에러 0건

---

## 3. 디렉토리 구조

```
vf01_webclone/
├── command/                          # 자동화 및 파이프라인 스크립트
│   ├── extract_pptx.py               # PPTX 텍스트 및 미디어 파서
│   ├── zero_trace_verifier.py        # 잔여 레퍼런스 흔적 0건 전수 검사기
│   └── test_ui_playwright.py         # Playwright 자동화 테스트 슈트
├── i-plan/                           # 사전 분석 및 아키텍처 기획 문서
│   ├── 01_analysis_artnedition.md    # 레퍼런스 사이트 정밀 분석서
│   └── 02_integration_plan_ma_ji_young.md # 마지영 작가 통합 설계서
├── process/                          # 실행 및 히스토리 로그
│   └── 01_execution_log.md           # 단계별 마일스톤 실행 일지
├── result/                           # 테스트 검증 산출물 및 스크린샷
│   ├── 01_ma_ji_young_page.png       # 전체 메인 뷰 스크린샷
│   ├── 02_artwork_lightbox_modal.png # 작품 상세 라이트박스 모달
│   ├── 03_exhibition_modal.png       # 청목미술관 개인전 모달
│   ├── 05_search_suggest_layer.png   # 실시간 검색 및 추천 레이어
│   └── FINAL_REPORT.md               # 엔드투엔드 최종 보고서
└── src/                              # 최종 서비스 웹 소스 (Vercel 배포 루트)
    ├── index.html                    # 마지영 에디션 공식 웹사이트
    ├── vercel.json                   # Vercel 글로벌 CDN 캐싱 설정
    ├── css/
    │   ├── common.css                # GNB, 글로벌 배너, 검색창, 푸터 공통 스타일
    │   └── style.css                 # 갤러리 그리드, 모달, 아티스트 상세 스타일
    ├── js/
    │   ├── data.js                   # 전 작품(42점) 및 전시 메타데이터
    │   └── main.js                   # 동적 렌더링, 필터링, 모달, 검색 컨트롤러
    └── assets/images/                # 전용 벡터 로고 및 42점 원본 고해상도 이미지
```

---

## 4. 로컬 실행 및 클라우드 배포

* **로컬 웹 서버**:
  ```powershell
  cd src
  python -m http.server 8080
  # http://localhost:8080/ 접속
  ```
* **Vercel 프로덕션 배포**:
  ```powershell
  cd src
  vercel deploy --prod --yes --scope leehankyus-projects
  ```
* **공식 라이브 웹사이트**:
  👉 **[https://src-topaz-nu.vercel.app](https://src-topaz-nu.vercel.app)**
