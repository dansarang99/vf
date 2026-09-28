"""
Stage 4: 제2원본(Draft 2) 본문 텍스트 100% 흑색 복원 주입
"""
import os
import sys
import docx
from docx.oxml.ns import qn

def build_draft2_master(draft1_docx, out_docx):
    doc = docx.Document(draft1_docx)
    restored = 0
    for p in doc.paragraphs:
        for r in p.runs:
            rPr = r._element.find(qn('w:rPr'))
            if rPr is not None:
                color = rPr.find(qn('w:color'))
                if color is not None and color.get(qn('w:val', '')).upper() == 'FFFFFF':
                    color.set(qn('w:val'), '000000') # 순수 흑색 복원
                    restored += 1
    doc.save(out_docx)
    print(f"[Stage 4] Draft 2 master restored: {out_docx} ({restored} runs restored)")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        build_draft2_master(sys.argv[1], sys.argv[2])
