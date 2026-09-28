# -*- coding: utf-8 -*-
import fitz

doc = fitz.open(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\upload\3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
p1 = doc[0]
print("Page 1 rect:", p1.rect)
blocks = p1.get_text("dict")["blocks"]
for idx, b in enumerate(blocks):
    if "lines" in b:
        bb = [round(x, 1) for x in b["bbox"]]
        print(f"Text Block {idx}: bbox={bb}")
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if txt:
                    fn = s["font"]
                    sz = s["size"]
                    col = f"0x{s['color']:06x}"
                    print(f"   [{fn:20}] sz={sz:4.1f} col={col} | {txt}")
    elif "image" in b:
        bb = [round(x, 1) for x in b["bbox"]]
        print(f"Image Block {idx}: bbox={bb} w={b['width']} h={b['height']}")
doc.close()
