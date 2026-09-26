# vf06_advanced_web_cloner_skill: 홈페이지 고급화 & Supabase DB + 정밀제어 관리자모드 (Admin CMS)

본 리포지토리는 `vf01_webclone`에서 1차 복제된 마지영 에디션 웹사이트를 기반으로, **(1) Supabase Cloud & 로컬 하이브리드 DB**, **(2) 관리자 보안 인증 (`admin` / `1234567`)**, **(3) 작품 가격 일괄 가중치 조정(최소 10,000원 단위 정렬 정책)** 및 **(4) 고객 소장 문의 실시간 관리장(Inquiry Ledger)**을 구축하여 엔터프라이즈급 아트 커머스 플랫폼으로 격상시킨 **홈페이지 고급화 전용 공식 프로젝트**입니다.

---

## 1. 주요 고급화 기능 명세

1. **Supabase PostgreSQL & 하이브리드 DB 엔진:**
   * 42점 전 작품, 전시 3건, 작가 프로필, 고객 문의, 글로벌 공지 배너 DDL 스키마 및 RLS 보안 체계 완비.
   * 클라우드 키 입력 시 Supabase Cloud 즉시 연동, 오프라인 시 브라우저 내장 Local DB Engine 작동.
2. **관리자 통합 제어 센터 (Admin CMS Studio):**
   * 접속 URL: `http://localhost:8080/admin/index.html`
   * 인증 계정: 아이디 `admin` / 비밀번호 `1234567`
   * **작품 가격 일괄 가중치 조정:** 전체/시리즈별 가중치 배율(+10%, +20%, -10% 등) 일괄 계산 및 **최소 10,000원 단위 자동 반올림 정렬 (`Math.round(price / 10000) * 10000`)**
   * **소장 문의 관리대장:** 고객 문의 실시간 접수 및 상태(검토/연락/완료) 관리
   * **작가노트 & 전시 에디터:** 전시 일정 및 국/영문 작가노트 문단 실시간 편집
3. **`result` 폴더 순차 영구 보존 (`[001]` ~ `[025]`):**
   * 모든 화면 캡처, 소스코드 백업, DDL, 시드 SQL, 테스트 스크립트, 종합 마스터 보고서가 `result` 폴더에 결번 없이 100% 영구 보존되어 있습니다.

---

## 2. 실행 가이드

```bash
# 로컬 웹 서버 실행
python -m http.server 8080 --directory src

# 자동화 검증 E2E 테스트 실행
python command/test_admin_auth_and_batch_pricing.py
```
