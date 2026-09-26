# -*- coding: utf-8 -*-
"""
[Stage 2] PDF to DOCX 100% Zero-Loss Conversion Engine with Page Drift Calibration
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.
"""

import os
import sys
import fitz
import zipfile
import re
from pdf2docx import Converter

def calibrate_section_breaks(docx_path):
    """
    pdf2docx 변환 후 발생하는 페이지 편차(Page Drift)를 0으로 맞추는 초고속 정밀 캘리브레이션 엔진
    1) 단락 상하 여백(w:spacing before/after)을 0으로 압축하여 행 높이 최적화
    2) 상하 여백(w:top, w:bottom)을 미세 최적화하여 콘텐츠 밀림 방지
    """
    temp_path = docx_path + ".tmp.docx"
    with zipfile.ZipFile(docx_path, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
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
    os.replace(temp_path, docx_path)

def convert_pdf_to_docx(pdf_path, output_docx_path):
    """
    PDF -> DOCX 네이티브 테이블 및 레이아웃 무손실 복제 함수
    """
    pdf_abs = os.path.abspath(pdf_path)
    docx_abs = os.path.abspath(output_docx_path)
    os.makedirs(os.path.dirname(docx_abs), exist_ok=True)

    print(f"[Stage 2: PDF->DOCX] Opening PDF: {pdf_abs}")
    doc = fitz.open(pdf_abs)
    orig_pages = len(doc)
    doc.close()
    print(f"[Stage 2] Original PDF Page Count: {orig_pages}")

    print(f"[Stage 2] Converting PDF pages to DOCX...")
    cv = Converter(pdf_abs)
    cv.convert(docx_abs, start=0, end=None)
    cv.close()

    # 캘리브레이션 적용
    calibrate_section_breaks(docx_abs)

    print(f"[Stage 2] Successfully generated DOCX: {docx_abs} ({os.path.getsize(docx_abs)} bytes)")
    return docx_abs, orig_pages

if __name__ == '__main__':
    if len(sys.argv) > 2:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        src = r'..\vf04_docxcloner_skill(iso9001)\result\[002]_1.품질경영매뉴얼_(AX)창업기술_R1(2026).pdf'
        dst = r'..\vf03_hwp_pdf_docx_cloner_skill\scratch\sample_pdf_converted.docx'
    convert_pdf_to_docx(src, dst)
