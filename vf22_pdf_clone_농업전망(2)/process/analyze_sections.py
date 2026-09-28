import os
import sys
import fitz

pdf_path = r"C:\Users\note\vf\vf22_pdf_clone_농업전망(2)\upload\62dd6efda1924f2e9f91cc136f4835b3.pdf"
doc = fitz.open(pdf_path)

print(f"=== PDF Total Pages: {len(doc)} ===")

sections = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text("text")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_3 = lines[:3] if len(lines) >= 3 else lines
    last_3 = lines[-3:] if len(lines) >= 3 else lines
    
    # Check for chapter/section titles
    for line in lines[:10]:
        if any(keyword in line for keyword in ["제8장", "배추", "무", "당근", "양배추", "부록", "요 약"]):
            # look for section headers
            pass
            
    header_candidate = lines[0] if lines else ""
    footer_candidate = lines[-1] if lines else ""
    
    if pno < 10 or pno % 5 == 0 or pno >= len(doc) - 5:
        print(f"P.{pno+1:02d} | Header: {header_candidate[:40]} | Footer: {footer_candidate[:40]}")

print("\n--- Key Section Headers Found ---")
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text("text")
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("1. 배추") or line.startswith("2. 무") or line.startswith("3. 당근") or line.startswith("4. 양배추") or "부록" in line or line == "요 약":
            print(f"Page {pno+1:02d}: {line}")
