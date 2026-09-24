# 01. 웹 복제 및 마지영 작가 전시 통합 실행 로그 (Execution Log)

**프로젝트명:** ARTN Edition 클론 및 마지영 개인전 《Moments》 자연스러운 웹 통합  
**작업 일시:** 2026-09-24  
**작업자:** Antigravity AI Engineering & Curation Pair  

---

## 1. 단계별 실행 마일스톤

### Milestone 1: 아트앤에디션(ARTN Edition) 원본 사이트 정밀 역공학 분석
* 대상 URL: `https://artnedition.com/artist/detail/park-seo-bo/`
* 페이지 레이아웃, DOM 구조, CSS(`common.css`, `style.css`), SVG 로고(`logo_eng.svg`, `logo_eng_w.svg`), 아이콘(`btn_more.svg`, `icon_heart.svg`) 전수 추출 및 분석.
* 폰트 시스템(`Albert Sans`, `Pretendard`, `Noto Sans KR`), 컬러 팔레트(#111, #fff, #f7f7f7, #FA5A50), 여백 체계 완벽 추출.

### Milestone 2: `Web_마지영전시회.pptx` 데이터 및 멀티미디어 전수 추출
* 대상 파일: `C:\Users\note\Downloads\Web_마지영전시회.pptx` (총 24개 슬라이드)
* XML 파싱 및 인코딩 복원(UTF-8 한국어/영어 평론문, 시적 서정문 완벽 디코딩).
* 총 40여 종의 고해상도 작품 사진 및 청목미술관 개인전 공식 포스터 이미지 추출.
* 작품별 메타데이터 추출:
  - Moments 26-001 ~ Moments 26-042 (총 42점 전수)
  - 작품 제목, 국문/영문 부제, 시적 텍스트, 치수(cm), 재료(`mixed media on wooden Blocks`), 가격 책정 및 에디션/원화 뱃지.

### Milestone 3: 반응형 웹 아키텍처 및 데이터베이스(data.js) 구축
* `src/js/data.js`: 박서보 화백 및 마지영 작가 2인의 전체 프로필, 국영문 서문, 작품 갤러리, 전시 이력, 스토리 아티클 완벽 구조화.
* `src/css/common.css` & `src/css/style.css`: 아트앤에디션의 정통 미니멀 갤러리 디자인 시스템을 상속하여 1:1 완벽 구현.
* `src/js/main.js`:
  - 원클릭 아티스트 스위처 (마지영 <-> 박서보)
  - 국문/영문 서문 `Read More` 아코디언 애니메이션
  - 카테고리 필터 탭 (전체 / 대표작 26-001~010 / 4연작 모듈 세트 / 2연작 듀오 블록)
  - 시적 큐레이션 노트가 포함된 고해상도 작품 상세 라이트박스 모달
  - 청목미술관 개인전 상세 모달 및 전시 안내
  - 실시간 검색어 및 추천 작가 드롭다운 레이어
  - 위시리스트 토글 및 장바구니 카운터, 플로팅 토스트 피드백 알림

### Milestone 4: 브라우저 자동화(Playwright) 및 전수 검증
* Python Playwright 헤드리스 브라우저 테스트 슈트 작성(`command/test_ui_playwright.py`).
* 전체 상호작용(스크롤, 모달 오픈, 탭 필터링, 작가 전환, 검색어 팝업, 장바구니 담기) 테스트 수행.
* **콘솔 오류 및 네트워크 404: 0건 (100% 정상 로드)**.
* 결과물 고해상도 스크린샷 5종(`result/01~05.png`) 캡처 완료.
