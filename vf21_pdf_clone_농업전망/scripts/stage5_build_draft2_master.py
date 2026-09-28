# Stage 5: 제2원본(Draft 2) 7,065개 순수 본문 텍스트 런 100% 흑색 복원 및 PDF 컴파일
# Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

import os
import docx
from docx.oxml.ns import qn
import win32com.client
import pythoncom

def build_draft2_master(src_docx, out_docx, out_pdf):
    doc = docx.Document(src_docx)
    restored_runs = 0

    for p in doc.paragraphs:
        for r in p.runs:
            rPr = r._element.find(qn('w:rPr'))
            if rPr is not None:
                color = rPr.find(qn('w:color'))
                if color is not None:
                    val = color.get(qn('w:val'))
                    if val and val.upper() == 'FFFFFF':
                        color.set(qn('w:val'), '000000') # 순수 흑색 복원
                        restored_runs += 1

    doc.save(out_docx)
    print(f"제2원본 본문 텍스트 {restored_runs}개 런 100% 흑색 복원 완료: {out_docx}")

    # Word COM OLE 엔진 무인 기동
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        wdoc = word.Documents.Open(os.path.abspath(out_docx))
        wdoc.SaveAs(os.path.abspath(out_pdf), FileFormat=17) # 17 = wdFormatPDF
        wdoc.Close(False)
    finally:
        word.Quit()
        pythoncom.CoUninitialize()
    print(f"Word COM OLE PDF 컴파일 완료: {out_pdf}")

if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "result/[043]_농업전망_제1원본_전페이지_헤더풋터_각주_완전복원_레이아웃.docx"
    out_d = sys.argv[2] if len(sys.argv) > 2 else "result/[047]_농업전망_제2원본_본문텍스트_100%_완제복원.docx"
    out_p = sys.argv[3] if len(sys.argv) > 3 else "result/[048]_농업전망_제2원본_본문텍스트_100%_완제복원.pdf"
    build_draft2_master(src, out_d, out_p)
