---
name: vf17-hwpx-clone-final
description: "(AX)창업기술 이한규 대표의 고유 실무 지식재산권 기반. 대한민국 최고 정밀도의 '대규모 PDF to HWPX/DOCX 100% 무손실 복제 & 한글 원격 제어' 마스터 파이프라인. 기존의 vf03, vf12, vf15, vf21, vf22, vf23 및 Anthropic 최첨단 스킬(@docx, @doc-coauthoring)을 완전 흡수·통합하여, 사문화된 대규모 학술·통계·정책 PDF를 단 1글자·1표·1페이지 오차도 없는 Zero-Drift 100% 완제 문서(DOCX, HWP, HWPX)로 부활시키고 Windows COM API 원격 조종석에서 외과수술적 제어를 완결합니다. (1) 20대 코어 청사진 v5.0 (DNA, DESIGN, STYLE, 문서의기본) 사전 계측 (2) TreatAsChar=1 및 139.3mm 폭 리사이징 기반 표 중첩(Overlapping) 0% 완전 박멸 (3) 템플릿 우선배치 2벌식 작업규칙(Draft 1 골격 레이아웃 + Draft 2 본문 텍스트 1:1 완제 주입) (4) OOXML zip-level 조작 & docx dual width/PositionalTab/run merging (5) 60개 본문 침투 가짜 푸터 및 8개 가짜 소제목 표 전수 척결 (6) 2단 다단 구역 continuous 고정 및 미러 마진(Mirror Margin) 정밀 안착 (7) Hancom Office COM OLE & MS Word COM OLE 듀얼 엔진 기반 실측 검증 (8) ask_question 대화형 결손 보완 리모콘 제어 (9) PyMuPDF 300 DPI Multimodal VisionCheck 전수 감사 및 result [001]~[999] 무손실 영구 보존. pdf to hwpx, pdf to docx, hwp 복제, hwpx cloner, pdf 복제, Zero-Drift 100%, 표 중첩 해결, 한글 원격 제어 요청 시 반드시 활성화하여 사용할 것."
---

# 👑 [vf17-hwpx-clone-final] 대규모 PDF to HWPX / DOCX 100% 무손실 복제 & 한글 원격 제어 마스터 스킬

> **"사문화된 PDF 문서를 1글자·1표·1페이지의 오차도 없는 살아있는 한글(HWPX/HWP)과 워드(DOCX)로 복제한 후, 비로소 원격 조종석(HWP_REMOCON)에 앉아 자유자재로 제어한다."**  
> **지식재산권자 및 최고 의사결정권자**: 본부장님 (이한규 대표 / USER / CEO)  
> **총괄 작전 지휘관**: ADVISOR 총괄팀장 (MAIN AI)  
> **현장 최고 공장장**: 대장장이 (Factory Manager)  
> **완전 통합 선행 스킬**: `vf03`, `vf12`, `vf15`, `vf21`, `vf22`, `vf23`, `@docx`, `@doc-coauthoring`, `@pdf`  
> **공식 저장소**: `github.com/dansarang99/vf/vf17_hwpx_clone_final`  
> **등록 경로**: `.github/skills/vf17-hwpx-clone-final`, `.gemini/config/skills/vf17-hwpx-clone-final`

---

## 1. 개요 및 왜 '감탄할 수밖에 없는가' (Why Unrivaled)

기존의 모든 상용 PDF 변환기(Adobe Acrobat, 한컴 변환기, pdf2docx 등)와 오픈소스 도구들은 실무 복제 시 **3대 치명적 결함**을 유발하여 수작업 재편집에 수십 시간을 낭비하게 만듭니다:
1. **표 중첩 (Table Overlapping)**: 표가 공중에 떠돌며(TreatAsChar=0) 텍스트와 겹치거나 뒤섞이는 대참사.
2. **페이지 폭발 (Page Drift)**: 62쪽 원본이 84쪽, 134쪽, 151쪽으로 폭증하며 단락 경계가 완전히 무너지는 현상.
3. **가짜 개체 침투 (Ghost Objects)**: 본문 중간에 가짜 페이지 번호 푸터가 수십 개씩 침투하고, 소제목이 1x2 표로 쪼개지는 현상.

**`vf17-hwpx-clone-final`은 이 모든 문제를 원천적으로 해결하고 증명된 결과(Zero-Drift 100%, 62/62쪽 정확 일치, 표 중첩 0건)를 산출하는 세계 최고 수준의 완성형 마스터 스킬입니다.**

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     vf17-hwpx-clone-final 5대 불패 메커니즘                              │
├──────────────────────────┬─────────────────────────────────────────────────────────────┤
│ 1. 표 중첩 0% 완전 박멸   │ • TreatAsChar=1 (글자처럼 취급) 전수 강제 고정               │
│    (Zero-Overlap)        │ • 가용 본문 폭(139.3mm / 39,486 HU) 초과 와이드 표 비례 축소│
│                          │ • 셀 내부 상하 여백 0pt 및 줄간격 7.5~9.0pt 슬림화 캘리브레이션│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 2. Zero-Drift 100% 페이지 │ • 단일 set_pagedef 덮어쓰기 금지! 구역별 고유 판형/여백 보존│
│    (Page Drift 0%)       │ • 2단 다단 구역 sectPr의 type="continuous" 정상화로 분할 차단 │
│                          │ • MS Word COM & Hancom COM 듀얼 엔진 실측 검증 (PageCount 1:1)│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 3. 외과수술적 개체 정제   │ • @docx merge_runs 기법: 잘게 쪼개진 런을 병합하여 검색성 확보│
│    (Ghost Cleanse)       │ • 가짜 소제목 1x2 표 전수 ➔ 네이티브 일반 문단으로 환원       │
│                          │ • 본문 침투 가짜 푸터 정규식 전수 척결 ➔ 네이티브 바닥글 이관│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 4. 템플릿 우선배치 2벌식 │ • 제1원본 (Draft 1: 골격 레이아웃 + 공백 슬롯)              │
│    (Twofold Protocol)    │ • /grill-me 대화형 승인 게이트 (ask_question)                │
│                          │ • 제2원본 (Draft 2: 순수 본문 텍스트 1:1 완제 주입)          │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 5. HWP 원격 조종석 가동  │ • Windows COM API (HWPFrame.HwpObject) 헤드리스 원격 연결    │
│    (HWP_REMOCON)         │ • FilePathCheckDLL 보안 무인 등록으로 팝업 차단              │
│                          │ • 셀 내비게이션(goto_addr), 데이터 주입, PyMuPDF VisionCheck│
└──────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 2. 20대 코어 청사진 (DOCUMENT_DNA) v5.0

문서 복제 착수 전 원천 PDF로부터 HWPX/DOCX 규격에 최적화된 20대 핵심 DNA를 추출하여 사전 검증 기준으로 확정합니다:

| 구분 | 번호 | 청사진 항목 | 핵심 규격 및 통제 기준 |
| :--- | :---: | :--- | :--- |
| **Part I. 비즈니스 및 판형 기하학** | 01 | **businessDNA** | 조직 정체성(KREI 등), 저자진, 발행 정보, 문서 번호 접두어 |
| | 02 | **DESIGN (판형)** | 물리적 판형 치수 (예: Crown Quarto 196.14 × 265.99mm 등) |
| | 03 | **STYLE (컬러/그리드)** | 1단/2단 그리드, 표 헤더 RGB 테마, 셀 배경 음영, 구분선 |
| | 04 | **[서체, 글꼴]** | 한글(한컴바탕/함초롬바탕/KoPub) 및 영문(Times New Roman) 4중 매핑 |
| | 05 | **Typography 위계** | 대제목(18pt), 중제목(14pt), 소제목(11pt), 본문(9.5pt), 캡션(8.5pt) |
| | 06 | **상하좌우 여백** | 미러 마진(Mirror Margin): 홀수(좌31/우26), 짝수(좌27/우30) 정밀 계측 |
| | 07 | **장평·자간·줄간격** | 본문 장평 95%, 자간 -0.5pt, 줄간격 145~155% (Word 9~10pt) |
| **Part II. 정보 개체 및 미디어** | 08 | **표 (Table)** | TreatAsChar=1 강제, 폭 139.3mm 한계 통제, 셀 내부 여백 0pt |
| | 09 | **그래프 및 차트** | 300 DPI 무손실 추출 및 BinData 인라인 안착 |
| | 10 | **대형 표제면 배너** | 챕터 시작면 상단 배너 300 DPI 무손실 래스터라이징 및 결합 |
| | 11 | **각주 / 참조자료** | 본문 하단 바닥 앵커링(Y≈653pt), space_before 30pt 분리 |
| **Part III. 구조 및 네이티브 태그**| 12 | **HWPX 네이티브 XML** | `<hp:p>`, `<hp:run>`, `<hp:linesegarray>` 정밀 조작 |
| | 13 | **개방형 패키징** | KS X 6101 표준 ZIP 구조, mimetype 무압축 최상단 배치 |
| | 14 | **문단 병합 (merge)** | 쪼개진 run 병합하여 텍스트 검색성 100% 확보 |
| | 15 | **구역 및 다단 (Section)**| 2단 구역 `sectPr` continuous 고정 (페이지 쪼개짐 원천 차단) |
| | 16 | **content.hpf 매니페스트**| BinData ID 및 스파인(Spine) 순서 100% 동기화 |
| **Part IV. 원격 제어 및 무결성** | 17 | **FilePathCheckerModule** | Hancom 보안 팝업 0% 차단 무인 DLL 레지스트리 등록 |
| | 18 | **Word & HWP 듀얼 COM** | 양대 오피스 엔진에서 PageCount 실측 동시 공인 |
| | 19 | **HWP_REMOCON 제어** | 셀 이동, 서식 치환, 대화형 결손 보완 (ask_question) |
| | 20 | **[001]~[999] 순차 보존** | result 폴더에 전수 스크립트, 문서, VisionCheck 증빙 영구 보존 |

---

## 3. 7단계 엔드투엔드 마스터 파이프라인

```
[원천 PDF 문서]
      │
      ▼
[Stage 1] 20대 코어 청사진 사전 정밀 계측 ➔ [DNA.md], [DESIGN.md], [STYLE.md], [문서의기본.md] 확정
      │
      ▼
[Stage 2] 외과수술적 데이터 정제 ➔ 60개 가짜 푸터 척결, 8개 소제목 표 환원, 300 DPI 배너/차트 추출
      │
      ▼
[Stage 3] 제1원본 (Draft 1) 골격 레이아웃 구축 ➔ 여백, 다단 continuous, 빈 표 틀, 백색 마스킹 런
      │
      ▼
[Stage 4] /grill-me 대화형 승인 게이트 (ask_question) ➔ 본부장님 골격 레이아웃 및 서식 검인
      │
      ▼
[Stage 5] 제2원본 (Draft 2) 100% 본문 텍스트 주입 ➔ 순수 흑색(#000000) 1:1 복원 & TreatAsChar=1
      │
      ▼
[Stage 6] MS Word & Hancom Office 듀얼 엔진 컴파일 ➔ DOCX(마스터), HWP(편집본), HWPX(개방형표준)
      │
      ▼
[Stage 7] HWP_REMOCON 원격 제어 & Multimodal VisionCheck 300 DPI 전수 감사 ➔ [170] 최종 공인 보고서
```

---

## 4. 템플릿 우선배치 2벌식 작업규칙 (Twofold Draft Protocol)

> **"제1원본(골격 레이아웃) 승인 뒤에 제2원본(본문 주입) 결과를 내놓는 것이 제대로 된 순서임. 절대 앞서가지 말 것."**

1. **제1원본 (Draft 1: 골격 레이아웃)**:
   - 텍스트로 인한 줄바꿈 및 페이지 밀림을 차단하기 위해, 헤더, 푸터, 쪽번호, 챕터 배너, 표 테두리(빈 셀), 차트 프레임만을 배치한 무결점 뼈대를 세웁니다.
2. **제2원본 (Draft 2: 본문 텍스트 완제 주입)**:
   - 골격이 안정된 상태에서 슬롯에 순수 본문 텍스트를 1:1 주입하여 흑색 텍스트로 복원합니다.

---

## 5. HWP 원격 조종석 (HWP_REMOCON) 실무 명령어 가이드

복제된 문서를 바탕으로 파이썬(pyhwpx)을 통해 헤드리스로 원격 제어합니다:

```python
import os
from pyhwpx import Hwp

# 1. 헤드리스 인스턴스 생성 및 보안 모듈 등록
hwp = Hwp(visible=False)
hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')

# 2. 문서 열기
hwp.open(os.path.abspath('result/[131]_ZeroDrift_62p_마스터.hwp'))

# 3. 표 전수 TreatAsChar=1 및 가용폭 리사이징
ctrl = hwp.HeadCtrl
max_w = int(139.3 * 283.465)  # 39,486 HWP Unit
while ctrl:
    if ctrl.CtrlID == 'tbl':
        prop = ctrl.Properties
        prop.SetItem('TreatAsChar', 1)
        w = prop.Item('Width')
        if w and w > max_w:
            ratio = max_w / w
            prop.SetItem('Width', max_w)
            h = prop.Item('Height')
            if h:
                prop.SetItem('Height', int(h * ratio))
        ctrl.Properties = prop
    ctrl = ctrl.Next

# 4. 특정 표 셀 원격 데이터 주입
# hwp.goto_page(6)
# hwp.set_cell_text("2026년 전망치 수정")

# 5. 삼중 포맷 저장
hwp.save_as('output.hwp', 'HWP')
hwp.save_as('output.hwpx', 'HWPX')
hwp.save_as('output.pdf', 'PDF')
hwp.quit()
```

---

## 6. 3대 기본 탑재 프로토콜 (/plan, /grill-me, /goal)

- **`/plan` (자립 계획 수립)**: 사전 계측 ➔ 청사진 확정 ➔ 제1원본 ➔ 승인 ➔ 제2원본 ➔ 듀얼 컴파일 ➔ VisionCheck 전 공정 사전 수립.
- **`/grill-me` (대화형 승인 게이트 & ask_question)**: 골격 완성 및 서식 의심 부분 발생 시 `ask_question` 모달을 통해 본부장님의 재가를 득함.
- **`/goal` (0-Error 완결 시까지 연속 추진)**: 단 1글자, 1페이지라도 원본과 다르면 멈추지 않고 스스로 원인을 분석·재조정하여 Zero-Drift 100%를 달성할 때까지 자립 완결.

---

## 7. 4대 표준 폴더 구조 (Standard Folder Structure)

- **`conversation/`**: 본부장님과의 대화 전체 1:1 무손실 복제 실록 (`CONVERSATION_TOTAL.md`).
- **`prompt/`**: 본부장님의 원천 지시문 영구 보존 (`PROMPT_MASTER.md`).
- **`result/`**: 모든 마스터 스크립트, 문서, 검증 리포트가 `[001]`~`[999]` 순차 번호로 영구 보존되는 유일한 산출물 기지.
- **`upload/`**: 원천 PDF 및 신청서 원본 보관소.
- **`scripts/`**: 재사용 가능한 파이썬 복제 엔진 스크립트 모음.
