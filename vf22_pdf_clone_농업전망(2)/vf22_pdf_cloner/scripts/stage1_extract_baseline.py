"""
Stage 1: pdf2docx 기반 1차 네이티브 워드(DOCX) 구조 추출 및 Word COM 렌더링
"""
import os
import sys
import time
from pdf2docx import Converter
import win32com.client
import pythoncom
import fitz

def run_stage1(pdf_path, out_docx, out_pdf):
    print(f"[Stage 1] Converting {pdf_path} to {out_docx}...")
    cv = Converter(pdf_path)
    cv.convert(out_docx, start=0, end=None)
    cv.close()
    
    print(f"[Stage 1] Compiling {out_docx} to {out_pdf} via Word COM...")
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        wdoc = word.Documents.Open(os.path.abspath(out_docx))
        pages = wdoc.ComputeStatistics(2)
        print(f"  -> MS Word rendered pages: {pages}")
        wdoc.SaveAs(os.path.abspath(out_pdf), FileFormat=17)
        wdoc.Close(False)
    finally:
        word.Quit()
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        run_stage1(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python stage1_extract_baseline.py <pdf_path> <out_docx> <out_pdf>")
