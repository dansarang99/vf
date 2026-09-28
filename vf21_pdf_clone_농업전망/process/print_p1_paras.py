# -*- coding: utf-8 -*-
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

base_docx = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[014]_농업전망_제2장_국내곡물수급동향과전망_20대청사진_완벽복제.docx"
doc = docx.Document(base_docx)

for i in range(16):
    p = doc.paragraphs[i]
    drawings = len(p._element.xpath('.//*[local-name()="drawing"]'))
    # replace special space with standard space for safe printing
    t = p.text.replace('\u2005', ' ').strip()
    print(f"P{i:02d}: drawings={drawings} | text='{t}'")
