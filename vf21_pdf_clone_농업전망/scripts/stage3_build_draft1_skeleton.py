# Stage 3: 제1원본(Draft 1) 골격 레이아웃 생성 및 본문 백색 마스킹
# Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

import os
import re
import docx
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def build_draft1_skeleton(src_docx, out_docx, banner_dir):
    doc = docx.Document(src_docx)

    # 1. 6대 표제면 배너 안착 (P03, P15, P26, P34, P35, P37)
    # 2. 본문 텍스트 백색 공백 슬롯 마스킹 (w:color val="FFFFFF")
    title_re = re.compile(r'^(?:\|\s*제\d+장\s*\||\d+\s+[가-힣]+|\d+\.\d+\.?\s+[가-힣]+|\d+\.\d+\.\d+\.?\s+[가-힣]+|요\s*약|목\s*차|국내곡물\s*수급|김종진|1\s*\|\s*한국농촌)')
    caption_re = re.compile(r'^(?:\|\s*표\s*[^|]+\||\|\s*그림\s*[^|]+\||단위\s*:|자료\s*:|주\s*[\d\)]*:|부록|부표)')

    masked_runs = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        has_image = any(run._element.xpath('.//a:blip') for run in p.runs)
        is_template = (title_re.search(t) or caption_re.search(t) or has_image)

        if not is_template:
            for r in p.runs:
                rPr = r._element.get_or_add_rPr()
                color = rPr.find(qn('w:color'))
                if color is None:
                    color = OxmlElement('w:color')
                    rPr.append(color)
                color.set(qn('w:val'), 'FFFFFF')
                masked_runs += 1

    doc.save(out_docx)
    print(f"제1원본(골격 레이아웃) 생성 완료: {out_docx} ({masked_runs}개 런 백색 마스킹)")

if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "process/raw_converted.docx"
    out = sys.argv[2] if len(sys.argv) > 2 else "result/[036]_농업전망_제1원본_골격_레이아웃.docx"
    b_dir = sys.argv[3] if len(sys.argv) > 3 else "process"
    build_draft1_skeleton(src, out, b_dir)
