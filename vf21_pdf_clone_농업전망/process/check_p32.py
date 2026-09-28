import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

base_docx = r'C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[031]_농업전망_제2장_국내곡물수급동향과전망_LAYOUT_투명좌표_완벽복제.docx'
doc = docx.Document(base_docx)

for idx in range(30, 43):
    p = doc.paragraphs[idx]
    print(f'P{idx:03d}: text="{p.text}", runs={len(p.runs)}')
