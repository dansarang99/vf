import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"upload/3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
fn_pages = [3, 5, 6, 8, 11, 12, 18, 29, 30]

for pno in fn_pages:
    page = doc[pno-1]
    drawings = page.get_drawings()
    lines = [d for d in drawings if 580 <= d['rect'].y0 <= 655 and d['rect'].height < 3]
    print(f"Page {pno:02d} lines near footnote:")
    for l in lines:
        r = l['rect']
        print(f"   rect=({r.x0:.1f}, {r.y0:.1f}, {r.x1:.1f}, {r.y1:.1f}), color={l.get('color')}, fill={l.get('fill')}")
