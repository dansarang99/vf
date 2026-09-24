---
name: web-cloner
description: "(AX)창업기술 이한규 대표의 고유 실무 지식재산권 기반. 임의의 레퍼런스 웹사이트(URL)와 기획/작품 소스(PPTX, PDF, 문서, 원천 데이터)를 입력받아 (1) 레퍼런스 디자인 시스템·레이아웃·GNB·모달 역공학 (2) 입력 콘텐츠 100% 디지털화 및 미디어 에셋 파이프라인 (3) 레퍼런스 및 타사 브랜드 흔적 0% 완전 박멸 (Surgical Zero-Trace Rebranding) (4) 전용 브랜드 아이덴티티 및 신규 벡터 에셋 창출 (5) 반응형 UI/UX, 검색 필터, 라이트박스 모달, 장바구니/토스트 구현 (6) Playwright 0-Error 무결성 자동화 검증 (7) Vercel 원클릭 클라우드 프로덕션 배포까지 엔드투엔드로 완결하는 웹사이트 복제·리브랜딩 마스터 파이프라인. 웹사이트 복제, 웹 클로너, 사이트 복제, 웹클론, web cloner, webclone 요청 시 반드시 활성화하여 사용할 것."
---

# Web Cloner Master Pipeline v1.0
## (웹사이트 복제 및 정밀 리브랜딩 마스터 스킬)

> **기획 및 지식재산권자**: (AX)창업기술 이한규 대표  
> **핵심 철학 (Core Philosophy)**:  
> 레퍼런스 웹사이트의 **압도적인 디자인 시스템, 미학적 그리드 레이아웃, 세련된 인터랙션 UX를 100% 온전히 계승**하되, 원본 사이트의 브랜드·로고·메타데이터·텍스트 흔적을 0%로 완벽하게 도려내고, 새로운 도메인 콘텐츠(PPTX, PDF, 원천 데이터)를 완벽하게 주입하여 독자적인 하이엔드 전용 웹 플랫폼으로 재탄생시키는 **'정밀 수술형 웹 복제 및 리브랜딩(Surgical Zero-Trace Web Cloning & Rebranding)'** 전문 파이프라인입니다.

---

## 1. 안티패턴 및 핵심 금기사항 (What NOT to Do)

1. **단순 프레임 복제 후 타사 브랜드 방치 금지 (Anti-Residual Leaks)**:
   - 레퍼런스 사이트의 로고, 파비콘, 메타 태그, 푸터 사업자 정보, 원본 작가/기업명이 단 한 글자라도 코드나 주석에 남아있어서는 안 됩니다.
   - 전수 정규식 스캔(`zero_trace_verifier.py`)을 통해 0건 확인 전까지 배포하지 마십시오.
2. **백지 템플릿(Blank Slate)으로 조잡하게 재작성 금지 (Anti-Naive Template)**:
   - 복제 대상 사이트의 정교한 1px 보더, 여백 비율, CSS 변수 체계, 반응형 그리드를 무시하고 기본 부트스트랩/테일윈드 기본 템플릿으로 대충 때우지 마십시오.
3. **입력 콘텐츠 임의 누락 및 축약 금지 (Anti-Content Loss)**:
   - PPTX, PDF, 문서에 수록된 모든 슬라이드, 작품, 시적 서정문, 국/영문 작가노트, 치수, 가격 데이터를 누락 없이 100% 전수 디지털화하여 `data.js`로 구조화하십시오.
4. **검증 없는 배포 금지 (Anti-Unverified Deploy)**:
   - 로컬 구동 확인 및 Playwright 무결성 테스트(0 Console Errors, 0 Page Errors)를 통과하기 전에는 Vercel 프로덕션에 배포하지 마십시오.

---

## 2. 7대 마스터 파이프라인 프로토콜

```
[입력 1: 레퍼런스 사이트 URL] + [입력 2: 신규 콘텐츠 PPTX / PDF / 원천데이터]
                                   │
                                   ▼
[Phase 1] 레퍼런스 웹사이트 구조 역공학 (Deconstruction)
  - DOM 계층 구조, CSS 변수 시스템, 타이포그래피 스케일, GNB 및 푸터 아키텍처 파싱
  - 모달(Modal), 드롭다운(Dropdown), 필터(Filter) 동작 로직 분석 -> 01_analysis.md 생성
                                   │
                                   ▼
[Phase 2] 입력 소스 100% 디지털화 & 에셋 파이프라인 (Asset Pipeline)
  - PPTX/PDF 내 모든 텍스트, 국/영문 병기문, 고해상도 이미지 전수 추출
  - RDBMS 형태의 독립형 프론트엔드 데이터베이스(`src/js/data.js`) 모델링
                                   │
                                   ▼
[Phase 3] 정밀 수술형 흔적 박멸 프로토콜 (Surgical Zero-Trace Purge)
  - 레퍼런스 사이트의 로고, 파비콘, 브랜드명, 작가명, 외주사 메타데이터 전수 색출
  - 임시 파일, 레퍼런스 이미지 에셋 영구 삭제 및 0-Residual 검색 통과 검증
                                   │
                                   ▼
[Phase 4] 독자적 브랜드 아이덴티티 주입 (Brand Identity Injection)
  - 신규 브랜드 전용 다크/라이트 벡터 로고(SVG) 실시간 생성 및 헤더/푸터 적용
  - 신규 브랜드 타이틀, 메타 태그, 파비콘, 큐레이토리얼 테마 컬러 셋업
                                   │
                                   ▼
[Phase 5] 반응형 인터랙티브 기능 엔지니어링 (Interactive Engineering)
  - 원클릭 시리즈/카테고리 퀵 스위처 및 필터 탭
  - 고해상도 라이트박스 모달 (국/영문 해설, 치수, 소장 가격, 장바구니 담기)
  - 실시간 검색어 제안 레이어, 장바구니 카운터, 플로팅 토스트 알림 연동
                                   │
                                   ▼
[Phase 6] Playwright UI 무결성 자동화 검증 (Playwright QA)
  - 1440px 뷰포트 기준 풀페이지 렌더링, 모달 오픈, 필터링, 검색 동작 시뮬레이션
  - `console.error` 및 `pageerror` 0건 검증, 주요 뷰포트 증빙 스크린샷 캡처
                                   │
                                   ▼
[Phase 7] Vercel 프로덕션 원클릭 클라우드 배포 (Cloud Deployment)
  - `vercel.json` 캐싱 최적화, Vercel CLI 논인터랙티브 프로덕션 배포
  - 공식 라이브 URL 발행, 글로벌 CDN 무결성 검증 및 GitHub 리포지토리 동기화
```

---

## 3. 표준 프로젝트 폴더 아키텍처 (`vfXX_webclone`)

모든 웹 클론 프로젝트는 반드시 아래 5대 표준 디렉토리 규격을 준수합니다:

```
vf01_webclone/
├── command/                          # 자동화 및 파이프라인 스크립트
│   ├── extract_media.py              # PPTX/PDF 텍스트 및 미디어 파서
│   ├── zero_trace_verifier.py        # 잔여 레퍼런스 흔적 0건 전수 검사기
│   ├── test_ui_playwright.py         # Playwright 자동화 테스트 슈트
│   └── deploy_vercel.py              # Vercel 원클릭 배포 스크립트
├── i-plan/                           # 설계 및 기획 산출물
│   ├── 01_analysis_reference.md      # 레퍼런스 사이트 정밀 분석서
│   └── 02_integration_plan.md        # 신규 브랜드/콘텐츠 통합 설계서
├── process/                          # 실행 및 히스토리 로그
│   └── 01_execution_log.md           # 단계별 마일스톤 실행 일지
├── result/                           # 검증 산출물 및 스크린샷
│   ├── 01_main_page.png              # 전체 메인 뷰 스크린샷
│   ├── 02_lightbox_modal.png         # 작품 상세 라이트박스 모달 캡처
│   ├── 03_exhibition_modal.png       # 전시/이벤트 모달 캡처
│   ├── 05_search_suggest_layer.png   # 실시간 검색 및 추천 레이어 캡처
│   └── FINAL_REPORT.md               # 엔드투엔드 최종 보고서
└── src/                              # 최종 서비스 웹 소스
    ├── index.html                    # 공식 통합 웹사이트
    ├── vercel.json                   # Vercel 배포 및 CDN 캐싱 설정
    ├── css/
    │   ├── common.css                # GNB, 글로벌 배너, 검색창, 푸터 공통 스타일
    │   └── style.css                 # 갤러리 그리드, 모달, 아티스트/브랜드 상세 스타일
    ├── js/
    │   ├── data.js                   # 전 작품/상품/콘텐츠 RDBMS 구조체
    │   └── main.js                   # 동적 렌더링, 필터링, 모달, 장바구니 컨트롤러
    └── assets/images/                # 신규 벡터 로고 및 고해상도 디지털 에셋
```

---

## 4. 실전 표준 스크립트 툴킷

### 4.1. PPTX/PDF 고해상도 에셋 파서 (`command/extract_media.py`)
```python
# -*- coding: utf-8 -*-
import os, zipfile
from pptx import Presentation

def extract_pptx_assets(pptx_path, out_img_dir):
    os.makedirs(out_img_dir, exist_ok=True)
    prs = Presentation(pptx_path)
    
    # 1. Slide Text Extraction
    slides_data = []
    for idx, slide in enumerate(prs.slides, 1):
        texts = [shape.text.strip() for shape in slide.shapes if shape.has_text_frame and shape.text.strip()]
        slides_data.append({"slide": idx, "texts": texts})
    
    # 2. High-Res Media Extraction from OOXML
    with zipfile.ZipFile(pptx_path, 'r') as z:
        media_files = [f for f in z.namelist() if f.startswith('ppt/media/')]
        for mf in media_files:
            filename = os.path.basename(mf)
            dest = os.path.join(out_img_dir, filename)
            with open(dest, 'wb') as f:
                f.write(z.read(mf))
    return slides_data
```

### 4.2. 흔적 0건 전수 정규식 검사기 (`command/zero_trace_verifier.py`)
```python
# -*- coding: utf-8 -*-
import os, re, sys

FORBIDDEN_PATTERNS = [
    r"박서보", r"park_seo_bo", r"park-seo-bo",
    r"ARTN\s*Edition", r"artnedition", r"아트앤에디션", r"아트앤라이프"
]

def verify_zero_traces(src_dir):
    violations = []
    regex = re.compile("|".join(FORBIDDEN_PATTERNS), re.IGNORECASE)
    
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith(('.html', '.js', '.css', '.json', '.svg')):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line_no, line in enumerate(fp, 1):
                        match = regex.search(line)
                        if match:
                            violations.append((p, line_no, match.group(0), line.strip()[:80]))
    
    if violations:
        print(f"[FAIL] {len(violations)} 잔여 레퍼런스 흔적 발견:")
        for v in violations:
            print(f"  {v[0]}:{v[1]} - [{v[2]}] {v[3]}")
        sys.exit(1)
    else:
        print("[SUCCESS] 0 Residual Traces Verified! 완벽한 독자 브랜드 구축 완료.")
        sys.exit(0)

if __name__ == "__main__":
    verify_zero_traces(sys.argv[1] if len(sys.argv) > 1 else "src")
```

### 4.3. Playwright 무결성 자동화 검증 (`command/test_ui_playwright.py`)
```python
# -*- coding: utf-8 -*-
import os, time
from playwright.sync_api import sync_playwright

def run_qa_suite(target_url, result_dir):
    os.makedirs(result_dir, exist_ok=True)
    errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda err: errors.append(str(err)))
        
        page.goto(target_url, wait_until="networkidle")
        page.screenshot(path=os.path.join(result_dir, "01_main_page.png"), full_page=True)
        
        # Test Modal
        first_card = page.locator("#artworks-grid li .img").first
        if first_card.is_visible():
            first_card.click()
            time.sleep(0.5)
            page.screenshot(path=os.path.join(result_dir, "02_lightbox_modal.png"))
            page.locator("#modal-close-btn").click()
            
        browser.close()
        
    assert len(errors) == 0, f"Page errors: {errors}"
    print("[SUCCESS] All UI Tests Passed with 0 Console/Page Errors!")
```

---

## 5. Vercel 배포 자동화 규격 (`vercel.json`)

```json
{
  "version": 2,
  "cleanUrls": true,
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

배포 명령:
```powershell
vercel deploy --prod --yes --scope <team_or_user_scope>
```

---

## 6. 성공 판정 기준 (Definition of Done)

1. [x] **레퍼런스 미학 완벽 복제**: GNB, 반응형 카드 그리드, 모달 라이트박스, 장바구니/위시리스트 완비.
2. [x] **100% 콘텐츠 디지털화**: 누락된 작품, 텍스트, 시적 서정문 없이 1:1 완벽 구조화.
3. [x] **Zero Traces**: 레퍼런스 타사 브랜드/작가/플랫폼 텍스트 및 에셋 전수 색출 및 0건 검증.
4. [x] **독자 브랜드 정체성 구축**: 전용 SVG 벡터 로고 및 메타 태그 완비.
5. [x] **Playwright 0-Error**: 콘솔 및 페이지 런타임 에러 0건 증빙.
6. [x] **Vercel 프로덕션 라이브**: 글로벌 CDN 배포 완료 및 HTTP 200 정상 응답.
7. [x] **GitHub 버전 관리**: 지정된 리포지토리에 커밋 및 원격 푸시 완료.
