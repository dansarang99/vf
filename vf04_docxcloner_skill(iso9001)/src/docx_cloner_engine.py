# -*- coding: utf-8 -*-
"""
DOCX 100% Surgical Cloner Engine (v3.0 - Natural Typography Edition)
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

본 스크립트는 원본 DOCX 문서의 레이아웃, 여백(Margin), 자간/장평, 글꼴, 단락 스타일,
표 그리드 및 머리글/바닥글 구조를 100% 원본 그대로 보존(Zero-Drift)하면서,
1. 머리글 로고 영역을 강제 이미지 치환이 아닌 고품질 네이티브 일반 TEXT '(AX)창업기술'로 자연스럽게 배치
2. 표지 로고 이미지 중복을 제거하고 정갈한 텍스트 사명으로 단일화
3. 문서번호 접두어를 'NX-'에서 '(AX)창업기술'의 약칭인 'AX-'로 전수 치환
4. 생성되는 모든 결과물을 [001]~[999] 순차 번호 규격에 맞추어 result 폴더에 영구 보존
"""

import os
import sys
import zipfile
import re
import win32com.client

def clone_manual(f_in, f_out):
    """[001] 품질경영매뉴얼 네이티브 텍스트 치환 및 AX- 문서번호 적용 복제"""
    os.makedirs(os.path.dirname(f_out), exist_ok=True)
    with zipfile.ZipFile(f_in, 'r') as zin:
        with zipfile.ZipFile(f_out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == 'word/header2.xml':
                    xml = content.decode('utf-8')
                    # 머리글 좌측 로고 영역의 drawing을 일반 자연스러운 텍스트 (AX)창업기술 로 치환
                    xml = re.sub(
                        r'<w:drawing>.*?</w:drawing>',
                        '<w:rPr><w:rFonts w:ascii="맑은 고딕" w:eastAsia="맑은 고딕"/><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="000000"/></w:rPr><w:t>(AX)창업기술</w:t>',
                        xml,
                        flags=re.DOTALL
                    )
                    # 문서번호 NX- -> AX-
                    xml = xml.replace('NX-QM-100', 'AX-QM-100')
                    xml = xml.replace('NX-', 'AX-')
                    content = xml.encode('utf-8')
                elif item.filename == 'word/document.xml':
                    xml = content.decode('utf-8')
                    # 표지 중복 로고 drawing 제거 (자연스러운 텍스트 사명만 노출)
                    xml = re.sub(r'<w:r><w:drawing>.*?</w:drawing></w:r>', '', xml, count=1, flags=re.DOTALL)
                    # 사명 정밀 치환
                    xml = xml.replace('(주)구글구글시스템즈는', '(AX)창업기술은')
                    xml = xml.replace('(주)구글구글시스템즈', '(AX)창업기술')
                    xml = xml.replace('구글구글시스템즈', '창업기술')
                    # 문서번호 전수 치환 (NX- -> AX-)
                    xml = xml.replace('NX-QM-100', 'AX-QM-100')
                    xml = xml.replace('NX-QP-', 'AX-QP-')
                    xml = xml.replace('NX-', 'AX-')
                    content = xml.encode('utf-8')
                zout.writestr(item, content)
    print(f"[Engine] Cloned Manual: {f_out}")

def clone_procedure(f_in, f_out):
    """[004] 품질경영시스템절차서 네이티브 텍스트 치환 및 AX- 문서번호 적용 복제"""
    os.makedirs(os.path.dirname(f_out), exist_ok=True)
    with zipfile.ZipFile(f_in, 'r') as zin:
        with zipfile.ZipFile(f_out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if 'header' in item.filename and item.filename.endswith('.xml'):
                    xml = content.decode('utf-8')
                    # 머리글 로고 영역을 일반 텍스트 (AX)창업기술 로 치환
                    xml = re.sub(
                        r'<w:drawing>.*?</w:drawing>',
                        '<w:rPr><w:rFonts w:ascii="맑은 고딕" w:eastAsia="맑은 고딕"/><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="000000"/></w:rPr><w:t>(AX)창업기술</w:t>',
                        xml,
                        flags=re.DOTALL
                    )
                    xml = xml.replace('NX-', 'AX-')
                    content = xml.encode('utf-8')
                elif item.filename == 'word/footer1.xml':
                    xml = content.decode('utf-8')
                    xml = xml.replace('㈜구글구글시스템즈', '(AX)창업기술')
                    xml = xml.replace('(주)구글구글시스템즈', '(AX)창업기술')
                    xml = xml.replace('NX-', 'AX-')
                    content = xml.encode('utf-8')
                elif item.filename == 'word/document.xml':
                    xml = content.decode('utf-8')
                    # 표지 중복 로고 drawing 제거
                    xml = re.sub(r'<w:r><w:drawing>.*?</w:drawing></w:r>', '', xml, count=1, flags=re.DOTALL)
                    xml = xml.replace('(주)구글구글시스템즈는', '(AX)창업기술은')
                    xml = xml.replace('(주)구글구글시스템즈', '(AX)창업기술')
                    xml = xml.replace('㈜구글구글시스템즈', '(AX)창업기술')
                    xml = xml.replace('구글구글시스템즈', '창업기술')
                    xml = xml.replace('NX-', 'AX-')
                    xml = xml.replace('회사의 약자 : NX', '회사의 약자 : AX')
                    content = xml.encode('utf-8')
                zout.writestr(item, content)
    print(f"[Engine] Cloned Procedure: {f_out}")

def export_pdfs_and_verify(f1_docx, f1_pdf, f2_docx, f2_pdf):
    """MS Word OLE Automation을 통한 PDF 변환 및 페이지 전수 검증"""
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        d1 = word.Documents.Open(os.path.abspath(f1_docx))
        p1 = d1.ComputeStatistics(2)
        d1.SaveAs(os.path.abspath(f1_pdf), FileFormat=17)
        d1.Close(False)

        d2 = word.Documents.Open(os.path.abspath(f2_docx))
        p2 = d2.ComputeStatistics(2)
        d2.SaveAs(os.path.abspath(f2_pdf), FileFormat=17)
        d2.Close(False)

        print(f"[Verification] Manual Pages: {p1} (Target: 68) -> {'PASS' if p1 == 68 else 'FAIL'}")
        print(f"[Verification] Procedure Pages: {p2} (Target: 201) -> {'PASS' if p2 == 201 else 'FAIL'}")
        return p1, p2
    finally:
        word.Quit()

if __name__ == '__main__':
    f1_src = r'upload\ISO 9001(2015) 문서화(샘플)\ISO 9001(2015) 문서화(샘플)\1.품질경영매뉴얼_(주)구글구글시스템즈_R1(2026).docx'
    f2_src = r'upload\ISO 9001(2015) 문서화(샘플)\ISO 9001(2015) 문서화(샘플)\2.품질경영시스템절차서_(주)구글구글시스템즈_R1(2026).docx'

    f1_docx = r'result\[001]_1.품질경영매뉴얼_(AX)창업기술_R1(2026).docx'
    f1_pdf  = r'result\[002]_1.품질경영매뉴얼_(AX)창업기술_R1(2026).pdf'
    f2_docx = r'result\[004]_2.품질경영시스템절차서_(AX)창업기술_R1(2026).docx'
    f2_pdf  = r'result\[005]_2.품질경영시스템절차서_(AX)창업기술_R1(2026).pdf'

    clone_manual(f1_src, f1_docx)
    clone_procedure(f2_src, f2_docx)
    export_pdfs_and_verify(f1_docx, f1_pdf, f2_docx, f2_pdf)
