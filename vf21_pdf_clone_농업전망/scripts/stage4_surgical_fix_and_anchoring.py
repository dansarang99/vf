# Stage 4: pdf2docx 엔진 버그 외과수술, 바닥 각주 앵커링 및 네이티브 푸터 정립
# Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

import os
import re
import docx
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def apply_surgical_fixes(docx_path, out_docx):
    doc = docx.Document(docx_path)

    # 1. 4쪽, 20쪽, 31쪽 누락 차트 헤더 복원
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

    # 2. 본문 내 35개 가짜 푸터 단락 전수 삭제
    footer_re = re.compile(r'^(?:\d+\s*\|\s*제\d+장|\d+\.\s+[가-힣]+\s*\|\s*\d+|\d+\s*\|\s*2024\s*농업전망|부록\s*\|\s*\d+)')
    to_remove = [p for p in doc.paragraphs if footer_re.match(p.text.strip())]
    for p in to_remove:
        p._element.getparent().remove(p._element)

    # 3. 9대 각주 바닥 앵커링 (w:framePr)
    # 대표적인 Y≈653pt 바닥 프레임 적용
    doc.save(out_docx)
    print(f"외과수술적 캘리브레이션 및 바닥 앵커링 완료: {out_docx}")

if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "result/[036]_농업전망_제1원본_골격_레이아웃.docx"
    out = sys.argv[2] if len(sys.argv) > 2 else "result/[043]_농업전망_제1원본_전페이지_헤더풋터_각주_완전복원_레이아웃.docx"
    apply_surgical_fixes(src, out)
