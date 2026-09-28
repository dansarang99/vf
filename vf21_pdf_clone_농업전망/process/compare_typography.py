# -*- coding: utf-8 -*-
import os
import sys
import fitz
import docx

sys.stdout.reconfigure(encoding='utf-8')

vf21_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망"
orig_pdf = os.path.join(vf21_dir, "upload", "3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
conv_pdf = os.path.join(vf21_dir, "result", "[002]_농업전망_제2장_국내곡물수급동향과전망_100%무손실복제.pdf")
conv_docx = os.path.join(vf21_dir, "result", "[001]_농업전망_제2장_국내곡물수급동향과전망_100%무손실복제.docx")

print("=== ORIGINAL PDF SPANS (Page 3) ===")
doc = fitz.open(orig_pdf)
p3 = doc[2]
blocks = p3.get_text("dict")["blocks"]
for b in blocks:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if txt and len(txt) > 2:
                    fn = s["font"]
                    sz = s["size"]
                    col = s["color"]
                    print(f"  [{fn:20}] sz={sz:4.1f} col=0x{col:06x} | {txt[:35]}")
                    break
doc.close()

print("\n=== CONVERTED PDF SPANS (Page 3) ===")
doc_c = fitz.open(conv_pdf)
p3_c = doc_c[2]
blocks_c = p3_c.get_text("dict")["blocks"]
for b in blocks_c:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if txt and len(txt) > 2:
                    fn = s["font"]
                    sz = s["size"]
                    col = s["color"]
                    print(f"  [{fn:20}] sz={sz:4.1f} col=0x{col:06x} | {txt[:35]}")
                    break
doc_c.close()
