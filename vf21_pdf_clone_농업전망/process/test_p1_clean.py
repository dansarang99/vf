# -*- coding: utf-8 -*-
"""
Test reconstructing Page 1 cleanly without junk sliced images
"""
import sys
import docx
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

# Open original docx
base_docx = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[014]_농업전망_제2장_국내곡물수급동향과전망_20대청사진_완벽복제.docx"
doc = docx.Document(base_docx)

# Check first paragraph P00
p0 = doc.paragraphs[0]
drawings_in_p0 = p0._element.xpath('.//*[local-name()="drawing"]')
print(f"P0 text='{p0.text}' | drawings={len(drawings_in_p0)}")

# Check P10
p10 = doc.paragraphs[10]
drawings_in_p10 = p10._element.xpath('.//*[local-name()="drawing"]')
print(f"P10 text='{p10.text}' | drawings={len(drawings_in_p10)}")

print("Test complete.")
