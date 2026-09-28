import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdoc = fitz.open(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[037]_농업전망_제1원본_템플릿_골격_레이아웃.pdf")
p26 = pdoc[25]
print("=== Page 26 Blocks in [037] PDF ===")
for b in p26.get_text("blocks"):
    t = b[4].replace('\n', ' ').strip()
    print(f"y=({b[1]:.1f}~{b[3]:.1f}): '{t}'")
