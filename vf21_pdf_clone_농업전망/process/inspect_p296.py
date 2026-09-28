import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[031]_농업전망_제2장_국내곡물수급동향과전망_LAYOUT_투명좌표_완벽복제.docx")
print("=== Paragraphs 296 to 306 ===")
for i in range(296, 306):
    p = doc.paragraphs[i]
    drawings = len(p._element.xpath('.//w:drawing'))
    print(f"P{i:03d} (drawings={drawings}): '{p.text.strip()}'")
