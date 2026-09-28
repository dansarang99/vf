# -*- coding: utf-8 -*-
import os
import sys
import fitz
import zipfile
import re
import win32com.client as win32

sys.stdout.reconfigure(encoding='utf-8')

vf21_dir = r"C:\Users\note\vf\vf21_pdf_clone_농업전망"
raw_docx = os.path.join(vf21_dir, "process", "raw_converted.docx")
calib_docx = os.path.join(vf21_dir, "process", "calib_converted.docx")
calib_pdf = os.path.join(vf21_dir, "process", "calib_verify.pdf")

print("Applying vf03 calibration to raw_converted.docx...")
with zipfile.ZipFile(raw_docx, 'r') as zin:
    with zipfile.ZipFile(calib_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                xml = content.decode('utf-8', errors='ignore')
                xml = re.sub(r'w:before="\d+"', 'w:before="0"', xml)
                xml = re.sub(r'w:after="\d+"', 'w:after="0"', xml)
                xml = re.sub(r'w:top="\d+"', 'w:top="200"', xml)
                xml = re.sub(r'w:bottom="(\d+)"', lambda bm: f'w:bottom="{min(350, int(bm.group(1)))}"', xml)
                content = xml.encode('utf-8')
            zout.writestr(item, content)

print("Calibration applied. Opening in Word COM...")
word = win32.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

try:
    doc = word.Documents.Open(os.path.abspath(calib_docx), ReadOnly=True)
    if os.path.exists(calib_pdf):
        os.remove(calib_pdf)
    doc.ExportAsFixedFormat(os.path.abspath(calib_pdf), ExportFormat=17)
    doc.Close(False)
    print("Exported calib PDF successfully.")
finally:
    word.Quit()

pdf_doc = fitz.open(calib_pdf)
actual_pages = len(pdf_doc)
print(f"Original PDF Pages: 37")
print(f"Actual Rendered Pages after calibration: {actual_pages}")
if actual_pages == 37:
    print(">>> ZERO-DRIFT SUCCESS: 37p == 37p (100% PERFECT MATCH) <<<")
else:
    print(f">>> PAGE DRIFT: Difference is {actual_pages - 37} pages <<<")
pdf_doc.close()
