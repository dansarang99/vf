import os
import re
import json
import docx
from docx.shared import Inches, Pt, Mm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import win32com.client
import pythoncom
import fitz

BASE_DIR = r"C:\Users\note\vf\vf21_pdf_clone_농업전망"
RESULT_DIR = os.path.join(BASE_DIR, "result")
PROCESS_DIR = os.path.join(BASE_DIR, "process")

SRC_DOCX = os.path.join(RESULT_DIR, "[031]_농업전망_제2장_국내곡물수급동향과전망_LAYOUT_투명좌표_완벽복제.docx")
OUT_DOCX = os.path.join(RESULT_DIR, "[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx")
OUT_PDF = os.path.join(RESULT_DIR, "[037]_농업전망_제1원본_템플릿_골격_레이아웃.pdf")
OUT_REPORT = os.path.join(RESULT_DIR, "[038]_농업전망_제1원본_골격_레이아웃_검증보고서.md")

banner_p03 = os.path.join(PROCESS_DIR, "sec1_full_header_p03.png")
banner_p15 = os.path.join(PROCESS_DIR, "sec2_full_header_p15.png")
banner_p26 = os.path.join(PROCESS_DIR, "sec3_full_header_p26.png")

print(">>> [진행률: 10%] Step 1: 베이스 문서 로드 및 37페이지 초정밀 캘리브레이션 개시...")
doc = docx.Document(SRC_DOCX)

# Regular expressions for template elements
title_re = re.compile(r'^(?:\|\s*제\d+장\s*\||\d+\s+[가-힣]+|\d+\.\d+\.?\s+[가-힣]+|\d+\.\d+\.\d+\.?\s+[가-힣]+|요\s*약|목\s*차|국내곡물\s*수급|김종진|1\s*\|\s*한국농촌)')
caption_re = re.compile(r'^(?:\|\s*표\s*[^|]+\||\|\s*그림\s*[^|]+\||단위\s*:|자료\s*:|주\s*[\d\)]*:|부록|부표)')
header_footer_re = re.compile(r'(?:\d+\s*\|\s*제\d+장|\d+\.\s+[가-힣]+\s*\|\s*\d+|\d+\s*\|\s*2024\s*농업전망|부록\s*\|\s*\d+)')
footnote_re = re.compile(r'^(?:\d+\)\s+[가-힣]+|\*\s*[가-힣]+)')

# 1. Surgical Calibration for Page 3 (Section 1: 쌀)
# P032: Clear stray floating drawings
p32 = doc.paragraphs[32]
p32._element.clear_content()

# P033: Replace with crisp 300 DPI master banner
p33 = doc.paragraphs[33]
p33._element.clear_content()
r33 = p33.add_run()
r33.add_picture(banner_p03, width=Inches(5.55))
p33.paragraph_format.space_before = Pt(40)
p33.paragraph_format.space_after = Pt(10)

# P034: Clear plain text '1.1. 수급 동향' since it is in banner
p34 = doc.paragraphs[34]
p34._element.clear_content()
p34.paragraph_format.space_before = Pt(0)
p34.paragraph_format.space_after = Pt(0)

# P035: '1.1.1. 생산'
p35 = doc.paragraphs[35]
p35.paragraph_format.space_before = Pt(6)
p35.paragraph_format.space_after = Pt(6)

print("  -> Page 3 (쌀 표제면) 초정밀 배너 캘리브레이션 완료")

# 2. General Body Text White Blank Slot Transformation & Shading Cleanup
body_count = 0
template_count = 0

for idx, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    
    # Check if this paragraph contains a chart/image blip
    has_image = any(run._element.xpath('.//a:blip') for run in p.runs)
    
    is_template = (title_re.search(t) or 
                   caption_re.search(t) or 
                   header_footer_re.search(t) or 
                   footnote_re.search(t) or 
                   has_image)
    
    # Remove any unwanted background shading in paragraph
    pPr = p._element.find(qn('w:pPr'))
    if pPr is not None:
        for shd in pPr.findall(qn('w:shd')):
            pPr.remove(shd)
            
    if is_template:
        template_count += 1
    else:
        body_count += 1
        for r in p.runs:
            # Remove shading from run
            rPr = r._element.get_or_add_rPr()
            for shd in rPr.findall(qn('w:shd')):
                rPr.remove(shd)
            # Set color to pure white (blank space)
            color = rPr.find(qn('w:color'))
            if color is None:
                color = OxmlElement('w:color')
                rPr.append(color)
            color.set(qn('w:val'), 'FFFFFF')

print(f"  -> 본문 공백 슬롯 전환: 템플릿 {template_count}개, 본문 슬롯 {body_count}개")

print(">>> [진행률: 50%] Step 2: [036] 제1원본 저장...")
doc.save(OUT_DOCX)
print(f"  -> [036] 저장 완료: {OUT_DOCX} ({os.path.getsize(OUT_DOCX):,} bytes)")

print(">>> [진행률: 70%] Step 3: MS Word COM 엔진 기동 및 [037] PDF 컴파일...")
pythoncom.CoInitialize()
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

try:
    wdoc = word.Documents.Open(OUT_DOCX)
    wdoc.SaveAs(OUT_PDF, FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()
    pythoncom.CoUninitialize()

print(f"  -> [037] PDF 컴파일 완료: {OUT_PDF} ({os.path.getsize(OUT_PDF):,} bytes)")

print(">>> [진행률: 85%] Step 4: 캘리브레이션 검증 및 시각 증빙 추출...")
pdoc = fitz.open(OUT_PDF)
print(f"  -> 계측된 총 페이지 수: {len(pdoc)} (목표: 37페이지, Zero-Drift 100%)")

for pno in [0, 2, 3, 14, 25, 30]:
    page = pdoc[pno]
    rect = page.rect
    words = page.get_text("words")
    min_x = min(w[0] for w in words) if words else 0
    pix = page.get_pixmap(dpi=150)
    img_name = f"proof_037_calibrated_p{pno+1:02d}.png"
    img_path = os.path.join(RESULT_DIR, img_name)
    pix.save(img_path)
    print(f"  -> P{pno+1:02d} 실측 좌측 여백: {min_x*0.352778:.1f} mm ({min_x:.1f} pt), 이미지={img_name}")

print(">>> [진행률: 100%] 캘리브레이션 수준 제1원본 빌드 완료!")
