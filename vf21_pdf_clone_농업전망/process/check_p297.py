import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx")
for i in range(297, 303):
    p = doc.paragraphs[i]
    blips = len(p._element.xpath('.//a:blip'))
    print(f"P{i:03d}: text='{p.text}', blips={blips}, xml_len={len(p._element.xml)}")
