import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, Mm
import sys
sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx"
doc = docx.Document(docx_path)

print("=== Paragraphs 30 to 42 in [036] ===")
for idx in range(30, 43):
    p = doc.paragraphs[idx]
    xml = p._element.xml
    drawings = p._element.xpath('.//w:drawing')
    picts = p._element.xpath('.//w:pict')
    shds = p._element.xpath('.//w:shd')
    print(f"P{idx:03d}: text='{p.text[:30]}' | drawings={len(drawings)}, picts={len(picts)}, shds={len(shds)}")
