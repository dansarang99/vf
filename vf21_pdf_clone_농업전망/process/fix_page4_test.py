# -*- coding: utf-8 -*-
"""
Surgically fix Page 4 in [019] and test rendering
"""
import os
import sys
import docx
from docx.shared import Pt, Mm
import win32com.client as win32
import fitz

sys.stdout.reconfigure(encoding='utf-8')

res_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result"
proc_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\process"

f019_docx = os.path.join(res_dir, "[019]_농업전망_제2장_국내곡물수급동향과전망_1대1정밀검증_즉시개선_완벽복제.docx")
doc = docx.Document(f019_docx)

# Locate elements around Page 4
# Find paragraph with '| 그림 2-1 |'
p_chart_idx = None
for i, p in enumerate(doc.paragraphs):
    if "그림 2-1" in p.text:
        p_chart_idx = i
        break

print(f"Found '그림 2-1' at paragraph index: {p_chart_idx}")

# In doc.element.body, let's locate the corresponding element
body = doc.element.body
chart_p_elem = doc.paragraphs[p_chart_idx]._element
elem_idx = body.index(chart_p_elem)
print(f"Element index in body: {elem_idx}")

# Look at preceding element (elem_idx - 1) which has the messy drawings
elem_prev = body[elem_idx - 1]
print(f"Preceding element tag: {elem_prev.tag}, drawings: {len(elem_prev.xpath('.//w:drawing'))}")

# Look at following element after table (Table 0)
t0 = doc.tables[0]._element
t0_idx = body.index(t0)
print(f"Table 0 index: {t0_idx}")

# Let's inspect elements from elem_idx - 2 to t0_idx + 5
for k in range(elem_idx - 2, t0_idx + 6):
    el = body[k]
    tag = el.tag.split('}')[-1]
    dw = len(el.xpath('.//w:drawing'))
    text = el.text or ''
    if tag == 'p':
        p_temp = docx.text.paragraph.Paragraph(el, doc)
        text = p_temp.text
    print(f"  {k}: <{tag}> drawings={dw} text={repr(text[:30])}")

# Let's clean up Page 4:
# 1. Remove elem_prev (the messy vector drawings)
body.remove(elem_prev)

# Now update indices
t0_idx = body.index(t0)
chart_p_elem = doc.paragraphs[p_chart_idx]._element
elem_idx = body.index(chart_p_elem)

# Check if there is a ghost drawing after table
for k in range(t0_idx + 1, min(t0_idx + 5, len(body))):
    el = body[k]
    dw = len(el.xpath('.//w:drawing'))
    if dw > 0:
        print(f"Removing ghost drawing element after table at index {k} (drawings={dw})")
        body.remove(el)
        break

# Now replace the text paragraph '| 그림 2-1 |' with clean chart image!
p_chart = doc.paragraphs[p_chart_idx]
# Clear text and runs
p_chart.text = ""
p_chart.paragraph_format.space_before = Pt(8)
p_chart.paragraph_format.space_after = Pt(8)
run = p_chart.add_run()
chart_img = os.path.join(proc_dir, "charts", "chart_01_p04.png")
run.add_picture(chart_img, width=Mm(134))

# Also remove paragraph that says '자료: 국가데이터처' right below chart since it's inside the image
p_next = docx.text.paragraph.Paragraph(body[elem_idx + 1], doc)
if "자료: 국가데이터처" in p_next.text:
    print("Removing redundant '자료: 국가데이터처' below chart image")
    body.remove(body[elem_idx + 1])

# Save and test
test_p4_docx = os.path.join(proc_dir, "test_p4_fixed.docx")
doc.save(test_p4_docx)
print("Saved test_p4_fixed.docx")

word = win32.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
test_p4_pdf = os.path.join(proc_dir, "test_p4_fixed.pdf")
try:
    wdoc = word.Documents.Open(os.path.abspath(test_p4_docx), ReadOnly=True)
    if os.path.exists(test_p4_pdf):
        os.remove(test_p4_pdf)
    wdoc.ExportAsFixedFormat(os.path.abspath(test_p4_pdf), ExportFormat=17)
    wdoc.Close(False)
    print("Exported test_p4_fixed.pdf")
finally:
    word.Quit()

pdoc = fitz.open(test_p4_pdf)
print(f"Total pages: {len(pdoc)} (Target: 37)")
pix = pdoc[3].get_pixmap(dpi=200)
proof_p4_fixed = os.path.join(proc_dir, "visual_proof", "proof_p04_fixed_200dpi.png")
pix.save(proof_p4_fixed)
pdoc.close()
print(f"Saved proof_p04_fixed_200dpi.png!")
