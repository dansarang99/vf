import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx")
for i, p in enumerate(doc.paragraphs):
    if '감자' in p.text and len(p.text.strip()) < 30:
        print(f"P{i:03d}: '{p.text.strip()}'")
