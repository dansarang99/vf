# -*- coding: utf-8 -*-
"""
Rebuild Page 1 with exact 1:1 layout:
- Left: Title block (제2장, 국내곡물 수급 동향과 전망, 저자)
- Right: Top banner + TOC + Author footnotes
- Behind: Single full-page canvas background
- Strip all junk sliced drawings from P00 and P10
"""
import os
import sys
import docx
from docx.shared import Pt, RGBColor, Inches, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import fitz
import win32com.client as win32

sys.stdout.reconfigure(encoding='utf-8')

vf21_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망"
res_dir = os.path.join(vf21_dir, "result")
proc_dir = os.path.join(vf21_dir, "process")

# 1. First, create a single clean high-res image of Page 1 background (or full page 1 canvas)
orig_pdf = os.path.join(vf21_dir, "upload", "3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
doc_orig = fitz.open(orig_pdf)
p1_orig = doc_orig[0]

# Render Page 1 at 300 DPI
p1_img_path = os.path.join(proc_dir, "page1_canvas_300dpi.png")
pix = p1_orig.get_pixmap(dpi=300)
pix.save(p1_img_path)
print(f"Rendered Page 1 master canvas: {p1_img_path} ({pix.width}x{pix.height})")
doc_orig.close()

# 2. Open [014] base docx
base_docx = os.path.join(res_dir, "[014]_농업전망_제2장_국내곡물수급동향과전망_20대청사진_완벽복제.docx")
doc = docx.Document(base_docx)

# Remove paragraphs 0 to 13 (all the messed up Page 1 paragraphs including junk sliced images)
# Note: we need to find where Page 2 begins ('요 약')
p_start_idx = 0
p_end_idx = None
for i, p in enumerate(doc.paragraphs):
    if "요 약" in p.text:
        p_end_idx = i
        break

print(f"Page 1 paragraphs range: 0 to {p_end_idx} ('{doc.paragraphs[p_end_idx].text}')")

# Delete paragraphs from 0 up to p_end_idx (exclusive, keeping '요 약' and its preceding bar)
# But wait, p_end_idx - 1 was P14 (drawing of dark bar for 요 약). So we delete up to p_end_idx - 1!
target_del = p_end_idx - 1
for _ in range(target_del):
    p_elem = doc.paragraphs[0]._element
    p_elem.getparent().remove(p_elem)

print(f"Remaining paragraphs after removing Page 1: {len(doc.paragraphs)}, First is now: '{doc.paragraphs[0].text}'")

# 3. Now insert the newly reconstructed, 100% 1:1 Page 1 BEFORE the first remaining paragraph!
first_p = doc.paragraphs[0]

# Create a 2-column transparent table for Page 1
p1_table = doc.add_table(rows=1, cols=2)
# Move p1_table before first_p
first_p._element.addprevious(p1_table._element)

p1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
# Remove borders
tblPr = p1_table._element.xpath('w:tblPr')
if tblPr:
    borders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr[0].append(borders)

# Set widths
cell_left = p1_table.cell(0, 0)
cell_right = p1_table.cell(0, 1)
cell_left.width = Mm(85)
cell_right.width = Mm(90)

# --- LEFT CELL (Title block) ---
# Space at top
p_ltop = cell_left.paragraphs[0]
p_ltop.paragraph_format.space_before = Pt(80)
p_ltop.paragraph_format.space_after = Pt(14)
r_ch = p_ltop.add_run("| 제2장 |")
r_ch.font.name = "맑은 고딕"
r_ch.font.size = Pt(22)
r_ch.font.bold = True
r_ch.font.color.rgb = RGBColor(0, 0, 0)

p_ltitle = cell_left.add_paragraph()
p_ltitle.paragraph_format.space_before = Pt(0)
p_ltitle.paragraph_format.space_after = Pt(36)
p_ltitle.paragraph_format.line_spacing = 1.15
r_tit = p_ltitle.add_run("국내곡물 수급 동향과 전망")
r_tit.font.name = "맑은 고딕"
r_tit.font.size = Pt(25)
r_tit.font.bold = True
r_tit.font.color.rgb = RGBColor(0, 0, 0)

p_lauth = cell_left.add_paragraph()
p_lauth.paragraph_format.space_before = Pt(0)
p_lauth.paragraph_format.space_after = Pt(0)
r_auth = p_lauth.add_run("박한울¹ · 김다정² · 최준혁³ · 김지훈⁴")
r_auth.font.name = "맑은 고딕"
r_auth.font.size = Pt(10.5)
r_auth.font.bold = True
r_auth.font.color.rgb = RGBColor(0, 0, 0)

# --- RIGHT CELL (Top banner + TOC + Footnotes) ---
p_rtop = cell_right.paragraphs[0]
p_rtop.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_rtop.paragraph_format.space_before = Pt(10)
p_rtop.paragraph_format.space_after = Pt(90)
r_ban = p_rtop.add_run("AGRICULTURAL OUTLOOK CONFERENCE 2026")
r_ban.font.name = "Segoe UI"
r_ban.font.size = Pt(8.5)
r_ban.font.color.rgb = RGBColor(0x71, 0x71, 0x71)

# TOC items
toc_data = [
    ("1. 쌀", True, 0),
    ("1.1. 수급 동향", False, 12),
    ("1.2. 2026년 전망", False, 12),
    ("1.3. 중장기 전망", False, 12),
    ("2. 콩", True, 0),
    ("2.1. 수급 동향", False, 12),
    ("2.2. 2026년 전망", False, 12),
    ("2.3. 중장기 전망", False, 12),
    ("3. 감자", True, 0),
    ("3.1. 수급 동향", False, 12),
    ("3.2. 2026년 전망", False, 12),
    ("3.3. 중장기 전망", False, 12),
]

for t_text, is_bold, indent_pt in toc_data:
    p_t = cell_right.add_paragraph()
    p_t.paragraph_format.space_before = Pt(4 if is_bold else 1)
    p_t.paragraph_format.space_after = Pt(2 if is_bold else 1)
    p_t.paragraph_format.left_indent = Pt(indent_pt)
    r = p_t.add_run(t_text)
    r.font.name = "맑은 고딕"
    r.font.size = Pt(10 if is_bold else 9)
    r.font.bold = is_bold
    r.font.color.rgb = RGBColor(0, 0, 0)

# Footnotes
fn_data = [
    "1 | 한국농촌경제연구원 전문연구원, phu87@krei.re.kr",
    "2 | 한국농촌경제연구원 전문연구원, swetmug@krei.re.kr",
    "3 | 한국농촌경제연구원 연구원, wnsgur3385@krei.re.kr",
    "4 | 한국농촌경제연구원 연구원, jhkim4209@krei.re.kr",
]

p_fn_space = cell_right.add_paragraph()
p_fn_space.paragraph_format.space_before = Pt(80)
p_fn_space.paragraph_format.space_after = Pt(0)

for idx, fn_text in enumerate(fn_data):
    p_f = cell_right.add_paragraph()
    p_f.paragraph_format.space_before = Pt(1)
    p_f.paragraph_format.space_after = Pt(1)
    r = p_f.add_run(fn_text)
    r.font.name = "맑은 고딕"
    r.font.size = Pt(7.5)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

# Insert Page Break right after p1_table
p_pb = doc.add_paragraph()
p_pb.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
p1_table._element.addnext(p_pb._element)

# Save test docx
out_test = os.path.join(proc_dir, "test_p1_rebuilt.docx")
doc.save(out_test)
print(f"Saved rebuilt Page 1 DOCX: {out_test}")

# Export PDF and verify
print("Exporting rebuilt PDF in Word COM...")
word = win32.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

out_pdf = os.path.join(proc_dir, "test_p1_rebuilt.pdf")
try:
    wdoc = word.Documents.Open(os.path.abspath(out_test), ReadOnly=True)
    if os.path.exists(out_pdf):
        os.remove(out_pdf)
    wdoc.ExportAsFixedFormat(os.path.abspath(out_pdf), ExportFormat=17)
    wdoc.Close(False)
    print(f"Exported rebuilt test PDF: {out_pdf}")
finally:
    word.Quit()

pdoc = fitz.open(out_pdf)
print(f"Total Pages of rebuilt document: {len(pdoc)} (Target: 37)")
# Render Page 1 to compare
pix1 = pdoc[0].get_pixmap(dpi=200)
pix1.save(os.path.join(proc_dir, "page1_rebuilt_200dpi.png"))
pdoc.close()
print("Saved page1_rebuilt_200dpi.png!")
