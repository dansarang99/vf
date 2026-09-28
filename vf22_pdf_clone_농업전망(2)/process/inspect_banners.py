import os
import fitz

BASE_DIR = r"C:\Users\note\vf\vf22_pdf_clone_농업전망(2)"
PDF_SRC = os.path.join(BASE_DIR, "upload", "62dd6efda1924f2e9f91cc136f4835b3.pdf")
PROCESS_DIR = os.path.join(BASE_DIR, "process")
doc = fitz.open(PDF_SRC)

# 주요 섹션 페이지 확인
key_pages = [1, 3, 16, 17, 31, 41, 50, 53, 56, 60]

for pno in key_pages:
    page = doc[pno - 1]
    print(f"=== PAGE {pno} ===")
    blocks = page.get_text("blocks")
    for b in blocks[:5]:
        print(f"  bbox: ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}) text: {b[4].strip()[:50]}")
