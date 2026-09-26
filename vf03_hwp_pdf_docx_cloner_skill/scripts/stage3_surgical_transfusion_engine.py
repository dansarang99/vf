# -*- coding: utf-8 -*-
"""
[Stage 3] DOCX Surgical In-Place Transfusion Engine
Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

본 스크립트는 DOCX OOXML(Open Packaging Conventions) 패키지를 직접 조작하여:
1. 토씨 하나 틀리지 않는 외과수술적 텍스트 및 사명 치환
2. 머리글/바닥글 내 인위적 이미지 제거 및 네이티브 일반 TEXT 치환
3. 문서번호 접두어(NX- ➔ AX-) 일괄 동기화
4. 여백/장평/자간/줄간격 100% 무손실 보존
을 수행합니다.
"""

import os
import sys
import zipfile
import re

def surgical_transfusion(input_docx, output_docx, target_company="(AX)창업기술", prefix_old="NX-", prefix_new="AX-"):
    """
    DOCX OOXML 직접 조작을 통한 무손실 텍스트/머리글/문서번호 외과수술 치환
    """
    in_abs = os.path.abspath(input_docx)
    out_abs = os.path.abspath(output_docx)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)

    print(f"[Stage 3: Transfusion] Processing: {in_abs} -> {out_abs}")

    with zipfile.ZipFile(in_abs, 'r') as zin:
        with zipfile.ZipFile(out_abs, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)

                # 1. 머리글 파일 처리 (header*.xml)
                if 'header' in item.filename and item.filename.endswith('.xml'):
                    xml = content.decode('utf-8', errors='ignore')
                    # 머리글 좌측 로고 셀의 drawing을 자연스러운 네이티브 텍스트로 치환
                    xml = re.sub(
                        r'<w:drawing>.*?</w:drawing>',
                        f'<w:rPr><w:rFonts w:ascii="맑은 고딕" w:eastAsia="맑은 고딕"/><w:b/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="000000"/></w:rPr><w:t>{target_company}</w:t>',
                        xml,
                        flags=re.DOTALL
                    )
                    if prefix_old and prefix_new:
                        xml = xml.replace(prefix_old, prefix_new)
                    content = xml.encode('utf-8')

                # 2. 바닥글 파일 처리 (footer*.xml)
                elif 'footer' in item.filename and item.filename.endswith('.xml'):
                    xml = content.decode('utf-8', errors='ignore')
                    xml = xml.replace('㈜구글구글시스템즈', target_company)
                    xml = xml.replace('(주)구글구글시스템즈', target_company)
                    xml = xml.replace('구글구글시스템즈', target_company)
                    if prefix_old and prefix_new:
                        xml = xml.replace(prefix_old, prefix_new)
                    content = xml.encode('utf-8')

                # 3. 본문 파일 처리 (document.xml)
                elif item.filename == 'word/document.xml':
                    xml = content.decode('utf-8', errors='ignore')
                    # 표지 중복 로고 drawing 제거
                    xml = re.sub(r'<w:r><w:drawing>.*?</w:drawing></w:r>', '', xml, count=1, flags=re.DOTALL)
                    
                    # 사명 정합 치환
                    xml = xml.replace('(주)구글구글시스템즈는', f'{target_company}은')
                    xml = xml.replace('(주)구글구글시스템즈', target_company)
                    xml = xml.replace('㈜구글구글시스템즈', target_company)
                    xml = xml.replace('구글구글시스템즈', target_company)

                    # 문서번호 전수 치환
                    if prefix_old and prefix_new:
                        xml = xml.replace(prefix_old, prefix_new)
                        xml = xml.replace(f'회사의 약자 : {prefix_old.rstrip("-")}', f'회사의 약자 : {prefix_new.rstrip("-")}')
                    content = xml.encode('utf-8')

                zout.writestr(item, content)

    print(f"[Stage 3] Successfully completed transfusion: {out_abs} ({os.path.getsize(out_abs)} bytes)")
    return out_abs

if __name__ == '__main__':
    if len(sys.argv) > 2:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        src = r'..\vf04_docxcloner_skill(iso9001)\upload\ISO 9001(2015) 문서화(샘플)\ISO 9001(2015) 문서화(샘플)\1.품질경영매뉴얼_(주)구글구글시스템즈_R1(2026).docx'
        dst = r'..\vf03_hwp_pdf_docx_cloner_skill\scratch\sample_transfused.docx'
    surgical_transfusion(src, dst)
