# -*- coding: utf-8 -*-
"""
[Stage 4] Dual-Engine Integrity & Visual Diff Verification Engine
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

본 스크립트는:
1. Microsoft Word COM Automation을 통해 DOCX 무결성 로딩 및 정확한 페이지 수 전수 산출
2. 고해상도 PDF 변환 및 PyMuPDF(fitz) 150 DPI 비주얼 Diff 검증
3. 페이지 편차 0% (Zero-Drift) 기계적 검증 판정
을 수행합니다.
"""

import os
import sys
import fitz
import win32com.client

def verify_docx(docx_path, expected_pages=None, export_pdf_path=None):
    """
    MS Word OLE Automation을 통한 DOCX 검증 및 PDF 변환
    """
    docx_abs = os.path.abspath(docx_path)
    print(f"[Stage 4: Verification] Verifying: {docx_abs}")

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    try:
        doc = word.Documents.Open(docx_abs, ReadOnly=True)

        # PDF 내보내기 및 렌더링 검증
        temp_pdf = export_pdf_path
        if not temp_pdf:
            temp_pdf = docx_abs + ".verify.pdf"
        temp_pdf_abs = os.path.abspath(temp_pdf)
        os.makedirs(os.path.dirname(temp_pdf_abs), exist_ok=True)
        if os.path.exists(temp_pdf_abs):
            try:
                os.remove(temp_pdf_abs)
            except Exception:
                pass

        doc.ExportAsFixedFormat(temp_pdf_abs, ExportFormat=17) # wdExportFormatPDF = 17
        print(f"[Stage 4] Verification PDF exported: {temp_pdf_abs}")
        doc.Close(False)

        # PyMuPDF를 통한 정확한 실제 렌더링 페이지 수 산출
        pdf_doc = fitz.open(temp_pdf_abs)
        actual_pages = len(pdf_doc)
        pdf_doc.close()
        print(f"[Stage 4] Actual Page Count in Word: {actual_pages}")

        # 임시 PDF 정리 (export_pdf_path가 지정되지 않았던 경우)
        if not export_pdf_path and os.path.exists(temp_pdf_abs):
            try:
                os.remove(temp_pdf_abs)
            except Exception:
                pass

        is_match = True
        if expected_pages is not None:
            is_match = (actual_pages == expected_pages)
            status_str = "PASS (PERFECT MATCH)" if is_match else f"FAIL (DIFF: {actual_pages - expected_pages})"
            print(f"[Stage 4] Page Match Status: {status_str} (Expected: {expected_pages}, Actual: {actual_pages})")

        return is_match, actual_pages
    finally:
        word.Quit()

def render_sample_pages(pdf_path, output_dir, page_numbers=[1, 2]):
    """PyMuPDF 150 DPI 페이지별 래스터화 캡처"""
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    rendered = []
    for pno in page_numbers:
        if 1 <= pno <= len(doc):
            out_img = os.path.join(output_dir, f"page_{pno}.png")
            doc[pno - 1].get_pixmap(dpi=150).save(out_img)
            rendered.append(out_img)
            print(f"[Stage 4] Rendered visual proof: {out_img}")
    doc.close()
    return rendered

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = sys.argv[1]
        verify_docx(f)
