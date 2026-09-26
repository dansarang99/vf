# [040] 마지영 에디션 & 아틀리에 Vercel 클라우드 프로덕션 배포 보고서

**프로젝트**: vf06_advanced_web_cloner_skill (마지영 에디션 & 아틀리에 고급화 웹 아카이브)  
**배포 플랫폼**: Vercel Cloud Production (Edge Network Global CDN)  
**발행일시**: 2026-09-26  
**배포 상태**: **100% READY (Production Live)**

---

## 1. 공식 Vercel 배포 URL

- **🌐 메인 갤러리 공식 프로덕션 URL**:  
  **`https://src-topaz-nu.vercel.app`**  
  *(예비 고유 URL: `https://src-pb3s5mtsl-leehankyus-projects.vercel.app`)*

- **🔐 관리자 CMS 스텔스 진입 URL**:  
  **`https://src-topaz-nu.vercel.app/admin`**  
  *(또는 상단 헤더 로고 `MA JI YOUNG | 아틀리에` 중 우측 `( 아틀리에 )` 바로 아랫쪽 여백 클릭 시 진입)*

---

## 2. 정식 연동 완료된 4대 E-Commerce & Firebase DB 모듈

1. **정식 회원가입 및 인증 시스템 (Collector Sign Up & Auth)**
   - 성함, 이메일, 비밀번호(6자 이상), 연락처, 배송지 주소, 회원 등급(VIP 파트론 / 일반 컬렉터 / 갤러리 기관) 입력
   - 가입 즉시 세션 연동 및 헤더 동적 갱신 (`👑 OOO 컬렉터님` | `주문내역` | `로그아웃`)
   - Firebase Firestore `users` 컬렉션에 실시간 암호화 저장

2. **반응형 장바구니 시스템 (Art Shopping Cart)**
   - 작품 상세 모달에서 "장바구니 담기" 원클릭 실시간 연동
   - 헤더 카트 뱃지 실시간 수량 동기화
   - 장바구니 모달 내 수량 증감(+ / -), 작품 개별 삭제, 전액 무료 특수 미술품 전문 배송료 지원
   - **모든 작품 금액 10,000원 단위 자동 정렬 (`Math.round(price / 10000) * 10000`) 완벽 보장**

3. **작품 소장 구매 및 주문 결제 시스템 (Checkout & Purchase)**
   - 로그인된 컬렉터의 수령인 성함, 연락처, 배송지 주소 자동 사전 입력
   - 결제 수단 선택:
     - 💳 신용카드 간편결제
     - 🏦 실시간 계좌이체 (은행권 에스크로)
     - 📄 가상계좌 안전결제
     - 🏛 갤러리 프라이빗 인보이스 / 법인 세금계산서
   - 결제 승인 시 정식 주문 번호(`ORD-2026-XXXXX`) 및 정품 보증서 발급 번호(`MJY-CERT-2026-XXXXX`) 자동 생성
   - Firebase Firestore `orders` 컬렉션에 실시간 영구 기록

4. **컬렉터 마이페이지 주문 내역 조회 (My Acquisitions & History)**
   - 컬렉터가 소장한 작품 목록 및 결제 총액 실시간 확인
   - 실시간 배송 및 소장 처리 상태 추적 (`결제완료` ➔ `작품검수중` ➔ `프라이빗배송준비` ➔ `배송중` ➔ `소장인도완료`)

5. **관리자 CMS (`admin/`) 실시간 동기화**
   - **주문 및 결제 관리대장 (`tabOrders`)**: 실시간 주문 내역 조회, 배송 상태 원클릭 변경, 누적 매출액 통계 산출
   - **등록 컬렉터 관리대장 (`tabUsers`)**: 신규 가입 컬렉터 목록, 멤버십 등급, 연락처 및 기본 배송지 확인

---

## 3. Playwright 0-Error 전체 자동화 검증 내역

| 번호 | 증빙 파일명 | 검증 내용 |
|:---:|:---|:---|
| `[032]` | `[032]_collector_signup_success.png` | '이한규 대표' 컬렉터 회원가입 및 헤더 자동 로그인 동기화 검증 |
| `[033]` | `[033]_shopping_cart_modal_active.png` | 장바구니 2점 담기, 10,000원 단위 합계(₩12,300,000) 산출 모달 |
| `[034]` | `[034]_order_purchase_completed_receipt.png` | `ORD-2026-00102` 정식 주문 및 `MJY-CERT` 보증서 발급 영수증 |
| `[035]` | `[035]_my_orders_history_modal.png` | 컬렉터 마이페이지 소장 주문 내역 실시간 조회 검증 |
| `[036]` | `[036]_admin_orders_ledger_realtime.png` | 관리자 CMS 주문관리대장에서 신규 주문 확인 및 '작품검수중' 상태 갱신 |
| `[037]` | `[037]_admin_registered_collectors_ledger.png` | 관리자 CMS 컬렉터관리대장에서 '이한규 대표' VIP 회원 등록 확인 |
| `[038]` | `[038]_vercel_live_production_main.png` | Vercel 라이브 도메인(`https://src-topaz-nu.vercel.app`) 실시간 렌더링 |
| `[039]` | `[039]_vercel_live_production_admin_stealth.png` | Vercel 프로덕션 상단 로고 여백 클릭 시 관리자 스텔스 진입 검증 |

---

## 4. 보안 및 스텔스 진입 정보

- **관리자 계정**: `admin` / `1234567` (화면 일체 미노출)
- **VIP 테스트 계정**: `collector@majiyoung.art` / `1234567` (1초 퀵 로그인 지원)
- **신규 생성 계정**: `ceo@ax-startup.com` / `1234567` (이한규 대표)
