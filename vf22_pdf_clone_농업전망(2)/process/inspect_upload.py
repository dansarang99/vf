import os
import sys
import fitz

pdf_path = r"C:\Users\note\vf\vf22_pdf_clone_농업전망(2)\upload\62dd6efda1924f2e9f91cc136f4835b3.pdf"
doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}")

meta = doc.metadata
print("Metadata:", meta)

for i in range(min(5, len(doc))):
    page = doc[i]
    rect = page.rect
    text = page.get_text("text")
    first_lines = [line.strip() for line in text.split("\n") if line.strip()][:5]
    print(f"\n--- Page {i+1} (Size: {rect.width} x {rect.height}) ---")
    print("First lines:", " | ".join(first_lines))

last_page = doc[-1]
print(f"\n--- Last Page {len(doc)} ---")
last_lines = [line.strip() for line in last_page.get_text("text").split("\n") if line.strip()][:5]
print("Last page lines:", " | ".join(last_lines))
