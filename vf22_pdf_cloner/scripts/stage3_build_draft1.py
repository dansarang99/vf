"""
Stage 3: 제1원본(Draft 1) 템플릿 골격 레이아웃 구축
- 본문 텍스트 투명 슬롯화 (w:color w:val="FFFFFF")
- 머리글, 바닥글, 300 DPI 배너, 통계 표, 각주 고정
"""
import os
import sys
import docx
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def build_draft1_skeleton(src_docx, out_docx, banner_mappings=None):
    doc = docx.Document(src_docx)
    
    # 본문 런을 투명 텍스트 공백 슬롯으로 전환하여 골격 보존
    transparent_count = 0
    for p in doc.paragraphs:
        for r in p.runs:
            rPr = r._element.get_or_add_rPr()
            color = rPr.find(qn('w:color'))
            if color is None:
                color = OxmlElement('w:color')
                rPr.append(color)
            color.set(qn('w:val'), 'FFFFFF')
            transparent_count += 1
            
    doc.save(out_docx)
    print(f"[Stage 3] Draft 1 skeleton built: {out_docx} ({transparent_count} slots created)")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        build_draft1_skeleton(sys.argv[1], sys.argv[2])
