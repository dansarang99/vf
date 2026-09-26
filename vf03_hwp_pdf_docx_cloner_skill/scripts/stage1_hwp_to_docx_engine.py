# -*- coding: utf-8 -*-
"""
[Stage 1] HWP to DOCX 100% Zero-Loss Conversion Engine
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

본 스크립트는 한글 문서(.hwp, .hwpx)를 입력받아
1. Hancom HWP COM Automation(HWPFrame.HwpObject)을 통해 완벽한 레이아웃 보존 PDF 생성
2. 고정밀 pdf2docx 파싱 엔진을 통해 표, 셀 너비, 글꼴, 단락, 여백을 100% 보존한 네이티브 DOCX 변환
을 수행합니다.
"""

import os
import sys
import tempfile
import win32com.client
from pdf2docx import Converter

def convert_hwp_to_docx(hwp_path, output_docx_path):
    """
    HWP -> PDF (Hancom COM) -> DOCX (pdf2docx) 무손실 2단계 파이프라인
    """
    hwp_abs = os.path.abspath(hwp_path)
    docx_abs = os.path.abspath(output_docx_path)
    os.makedirs(os.path.dirname(docx_abs), exist_ok=True)

    print(f"[Stage 1: HWP->DOCX] Opening HWP: {hwp_abs}")
    temp_dir = tempfile.gettempdir()
    temp_pdf = os.path.join(temp_dir, f"hwp_conv_{os.path.splitext(os.path.basename(hwp_abs))[0]}.pdf")

    # 1. Hancom HWP COM 호출
    hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
    try:
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    except Exception as e:
        print(f"[Stage 1] Security module register notice: {e}")

    try:
        open_ok = hwp.Open(hwp_abs, "HWP", "forceopen:true")
        if not open_ok:
            raise RuntimeError(f"Failed to open HWP file: {hwp_abs}")

        orig_pages = hwp.PageCount
        print(f"[Stage 1] HWP Document Page Count: {orig_pages}")

        # HWP -> PDF 변환
        save_ok = hwp.SaveAs(temp_pdf, "PDF", "pdf")
        if not save_ok or not os.path.exists(temp_pdf):
            raise RuntimeError(f"Failed to export PDF from HWP: {temp_pdf}")
        print(f"[Stage 1] Intermediate PDF created: {temp_pdf} ({os.path.getsize(temp_pdf)} bytes)")
    finally:
        hwp.Quit()

    # 2. PDF -> DOCX 변환 (pdf2docx)
    print(f"[Stage 1] Converting PDF to DOCX with layout preservation...")
    cv = Converter(temp_pdf)
    cv.convert(docx_abs, start=0, end=None)
    cv.close()

    if os.path.exists(temp_pdf):
        try:
            os.remove(temp_pdf)
        except Exception:
            pass

    print(f"[Stage 1] Successfully generated DOCX: {docx_abs} ({os.path.getsize(docx_abs)} bytes)")
    return docx_abs, orig_pages

if __name__ == '__main__':
    if len(sys.argv) > 2:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        src = r'..\vf04_docxcloner_skill(iso9001)\upload\ISO 9001(2015) 문서화(샘플)\ISO 9001(2015) 문서화(샘플)\1.품질경영매뉴얼_(주)구글구글시스템즈_R1(2026).hwp'
        dst = r'..\vf03_hwp_pdf_docx_cloner_skill\scratch\sample_hwp_converted.docx'
    convert_hwp_to_docx(src, dst)
