import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\upload\3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
p3 = doc[2]
print("=== Original PDF Page 3 Blocks (y < 400 pt) ===")
for b in p3.get_text("blocks"):
    if b[1] < 400:
        txt = b[4].replace('\n', ' ').strip()
        print(f"y=({b[1]:.1f} ~ {b[3]:.1f}), x=({b[0]:.1f} ~ {b[2]:.1f}): '{txt}'")
