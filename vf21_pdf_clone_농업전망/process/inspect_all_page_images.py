# -*- coding: utf-8 -*-
import fitz

doc = fitz.open(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\upload\3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
for i in range(len(doc)):
    p = doc[i]
    imgs = p.get_images()
    print(f"Page {i+1:02d} ({len(imgs)} images):")
    for img in imgs:
        xref = img[0]
        bimg = doc.extract_image(xref)
        w = bimg["width"]
        h = bimg["height"]
        print(f"   xref={xref:4d} | {w:4d}x{h:4d} | ext={bimg['ext']}")
doc.close()
