# -*- coding: utf-8 -*-
import os
import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

vf21_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망"
orig_pdf = os.path.join(vf21_dir, "upload", "3f3b07ee6df942cdb31b1822aa0c1cae.pdf")
conv_pdf = os.path.join(vf21_dir, "result", "[002]_농업전망_제2장_국내곡물수급동향과전망_100%무손실복제.pdf")

doc_o = fitz.open(orig_pdf)
doc_c = fitz.open(conv_pdf)

print(f"{'Page':5} | {'Orig Img':9} | {'Conv Img':9} | {'Orig Draw':10} | {'Conv Draw':10} | {'Diff Img':8}")
print("-" * 65)

total_orig_img = 0
total_conv_img = 0

for i in range(len(doc_o)):
    p_o = doc_o[i]
    p_c = doc_c[i]
    io = len(p_o.get_images())
    ic = len(p_c.get_images())
    do = len(p_o.get_drawings())
    dc = len(p_c.get_drawings())
    total_orig_img += io
    total_conv_img += ic
    diff = ic - io
    flag = " [!] LOSS" if diff < 0 else ""
    print(f"P{i+1:02d}  | {io:9d} | {ic:9d} | {do:10d} | {dc:10d} | {diff:+8d}{flag}")

print("-" * 65)
print(f"Total: Orig Imgs = {total_orig_img}, Conv Imgs = {total_conv_img}, Difference = {total_conv_img - total_orig_img}")

doc_o.close()
doc_c.close()
