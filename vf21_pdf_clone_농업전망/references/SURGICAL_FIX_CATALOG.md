# pdf2docx 5대 고질적 엔진 버그 외과수술적 해결 카탈로그 (Surgical Fix Catalog)
> **지식재산권자**: (AX)창업기술 이한규 대표  
> **프로젝트**: 한국농촌경제연구원 농업전망 제2장 곡물 수급 동향과 전망 (37p)  

---

## 1. 개요
오픈소스 `pdf2docx` 엔진은 대형 학술/통계 문서를 변환할 때 5대 치명적 엔진 결함이 발생합니다. 본 문서는 각 결함의 원인과 파이썬 OOXML 직접 조작을 통한 외과수술적 해결 코드를 제공합니다.

---

## 2. 5대 엔진 버그별 원인 및 외과수술 코드

### [버그 1] 차트 상단 캡션 헤더 클리핑 증발 (4쪽, 20쪽, 31쪽)
- **원인**: 표/그림 경계면에서 `pdf2docx`가 상단 캡션 텍스트(`| 그림 2-1 | ...`)를 그래픽 내부 요소로 오인하여 삭제하거나 이전 페이지로 밀어내 삭제함.
- **해결 코드**:
```python
# 4쪽 상단 헤더 복원 주입
for p in doc.paragraphs:
    if '| 표 2-1 |' in p.text:
        new_p = p.insert_paragraph_before('| 그림 2-1 | 최근 10년(2016∼2025년) 쌀 생산 추이(연산 기준)')
        new_p.paragraph_format.space_before = Pt(12)
        new_p.paragraph_format.space_after = Pt(6)
        r = new_p.runs[0]
        r.font.name = 'Batang'
        r.font.size = Pt(9.5)
        r.font.bold = True
        break

# 20쪽 차트 헤더 복원
for p in doc.paragraphs:
    if '고 있었다. 이는 간편식' in p.text or '가성비를 중시하는' in p.text:
        new_p = p.insert_paragraph_before('| 그림 2-10 | 연령대별 콩 가공 신제품에서 기대하는 점')
        new_p.paragraph_format.space_before = Pt(12)
        new_p.paragraph_format.space_after = Pt(6)
        r = new_p.runs[0]
        r.font.name = 'Batang'
        r.font.size = Pt(9.5)
        r.font.bold = True
        break

# 31쪽 상단 헤더 복원
for p in doc.paragraphs:
    if '3.2. 2026년 전망' in p.text or '3.2.' in p.text:
        new_p = p.insert_paragraph_before('| 그림 2-13 | 감자 월별 출하량 및 가격 추이')
        new_p.paragraph_format.space_before = Pt(12)
        new_p.paragraph_format.space_after = Pt(6)
        r = new_p.runs[0]
        r.font.name = 'Batang'
        r.font.size = Pt(9.5)
        r.font.bold = True
        break
```

---

### [버그 2] 본문 내 가짜 푸터 35개 침투 현상
- **원인**: 바닥글을 워드의 섹션 바닥글(`sec.Footers`)로 분류하지 못하고 일반 문단(`w:body`)으로 파싱하여 화면 중앙에 둥둥 떠다님.
- **해결 코드**:
```python
import re
footer_re = re.compile(r'^(?:\d+\s*\|\s*제\d+장|\d+\.\s+[가-힣]+\s*\|\s*\d+|\d+\s*\|\s*2024\s*농업전망|부록\s*\|\s*\d+)')
to_remove_footers = [p for p in doc.paragraphs if footer_re.match(p.text.strip())]
print(f"가짜 푸터 {len(to_remove_footers)}개 전수 삭제")
for p in to_remove_footers:
    p._element.getparent().remove(p._element)
```

---

### [버그 3] 진짜 네이티브 바닥글 이관
- **해결**: 본문에서 삭제된 푸터를 실제 Word 섹션의 바닥글로 옮겨, 회색 여백 영역에만 안정적으로 표시되도록 조판.

---

### [버그 4] 9대 각주 바닥 앵커링 ($Y \approx 653\text{ pt}$)
- **원인**: 하단 각주가 일반 본문과 섞여 줄바꿈 및 페이지 넘침 발생.
- **해결 코드**: Word 절대 좌표 프레임(`w:framePr`)을 주입하여 페이지 맨 바닥에 물리적으로 앵커링 고정.
```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

footnote_configs = {
    41: {'page': 3, 'x_pt': 87.90, 'text_y_pt': 653.48, 'texts': ['1) 김준환(2025)...']},
    57: {'page': 5, 'x_pt': 87.90, 'text_y_pt': 643.64, 'texts': ['2) 이강산...', '3) 운송 일정...']},
    # ... 9대 각주 설정
}

pPr = p._element.get_or_add_pPr()
for fr in pPr.findall(qn('w:framePr')):
    pPr.remove(fr)

framePr = OxmlElement('w:framePr')
framePr.set(qn('w:w'), '7800')
framePr.set(qn('w:hAnchor'), 'page')
framePr.set(qn('w:vAnchor'), 'page')
framePr.set(qn('w:x'), str(int(matched_cfg['x_pt'] * 20)))
framePr.set(qn('w:y'), str(int(matched_cfg['text_y_pt'] * 20)))
framePr.set(qn('w:wrap'), 'around')
pPr.append(framePr)
```

---

### [버그 5] 중복 유령 표(Ghost Table 18) 외과수술적 제거
- **원인**: Page 26 등에서 불필요한 미니 표가 중복 생성되어 레이아웃 왜곡.
- **해결 코드**:
```python
for table in list(doc.tables):
    txt = " ".join(c.text.strip() for row in table.rows for c in row.cells)
    if '3' in txt and '감자' in txt and '수급' in txt and len(txt) < 30:
        table._element.getparent().remove(table._element)
        print("Table 18 (감자 중복 표) 외과수술적 제거 완료")
        break
```
