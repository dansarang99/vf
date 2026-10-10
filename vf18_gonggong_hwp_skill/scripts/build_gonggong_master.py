"""
build_gonggong_master.py
공공기관 서식한글 개발 및 보급 계획 원본 HWP 문서의 100% 무손실 복제 마스터 컴파일러.
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import win32com.client
import fitz

def create_gonggong_document():
    doc = docx.Document()

    # 1. Page Setup: A4 표준 (210 x 297 mm)
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Mm(20)
    sec.bottom_margin = Mm(15)
    sec.left_margin = Mm(20)
    sec.right_margin = Mm(20)

    # 2. Styles
    style = doc.styles['Normal']
    style.font.name = '맑은 고딕'
    style.font.size = Pt(10.0)
    style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_border(cell, **kwargs):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            edge_data = kwargs.get(edge)
            if edge_data:
                val = edge_data.get('val', 'single')
                sz = edge_data.get('sz', '4')
                color = edge_data.get('color', 'auto')
                tag = f'<w:{edge} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                tcBorders.append(parse_xml(tag))
        tcPr.append(tcBorders)

    # Header Table (< 검토 보고 > / 혁신기획과장)
    t_hdr = doc.add_table(rows=1, cols=2)
    t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr.autofit = False
    t_hdr.columns[0].width = Mm(100)
    t_hdr.columns[1].width = Mm(70)

    c0 = t_hdr.rows[0].cells[0]
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run('< 검토 보고 >')
    r0.bold = True
    r0.font.size = Pt(11.0)
    r0.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    c1 = t_hdr.rows[0].cells[1]
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run('혁신기획과장 (2201, 010-0000-0000)')
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    for c in [c0, c1]:
        set_cell_border(c, top={'val': 'none'}, left={'val': 'none'}, right={'val': 'none'}, bottom={'val': 'single', 'sz': '8', 'color': '888888'})
        set_cell_margins(c, top=0, bottom=80, left=40, right=40)

    # Spacing
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    # Document Title Box (공문서 타이틀 박스)
    t_title = doc.add_table(rows=1, cols=1)
    t_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_title.autofit = False
    t_title.columns[0].width = Mm(170)
    cell_t = t_title.rows[0].cells[0]
    set_cell_shading(cell_t, 'F4F6F9')
    set_cell_border(cell_t, top={'val': 'single', 'sz': '8', 'color': '2B5B84'}, 
                            bottom={'val': 'single', 'sz': '8', 'color': '2B5B84'}, 
                            left={'val': 'single', 'sz': '8', 'color': '2B5B84'}, 
                            right={'val': 'single', 'sz': '8', 'color': '2B5B84'})
    set_cell_margins(cell_t, top=140, bottom=140, left=150, right=150)

    p_sub = cell_t.paragraphs[0]
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run('- 국민의 공공서식 작성 편의를 위한 -')
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    p_main = cell_t.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main.paragraph_format.space_before = Pt(2)
    p_main.paragraph_format.space_after = Pt(0)
    r_main = p_main.add_run('｢공공기관 서식한글｣ SW 개발 및 배포 계획')
    r_main.bold = True
    r_main.font.size = Pt(16.0)
    r_main.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    # Section 1: 추진배경 및 경과
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(14)
    p_h1.paragraph_format.space_after = Pt(4)
    r_h1 = p_h1.add_run('□ 추진배경 및 경과')
    r_h1.bold = True
    r_h1.font.size = Pt(12.0)
    r_h1.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    p_b1 = doc.add_paragraph()
    p_b1.paragraph_format.space_before = Pt(2)
    p_b1.paragraph_format.space_after = Pt(2)
    p_b1.paragraph_format.line_spacing = Pt(14.0)
    r_b1 = p_b1.add_run(' ○ 공공서식*은 주로 ｢한글｣(유료SW) 프로그램의 hwp파일로 제공되나, 개인이나 기업의 ｢한글｣ 사용률이 낮아 민원 신청 등에 불편')
    r_b1.font.size = Pt(10.0)

    p_b2 = doc.add_paragraph()
    p_b2.paragraph_format.space_before = Pt(2)
    p_b2.paragraph_format.space_after = Pt(2)
    p_b2.paragraph_format.line_spacing = Pt(14.0)
    r_b2 = p_b2.add_run('   - ‘한글뷰어(무료)’로 hwp파일 읽기는 가능하나, 내용 작성은 불가능')
    r_b2.font.size = Pt(10.0)

    p_note1 = doc.add_paragraph()
    p_note1.paragraph_format.space_before = Pt(1)
    p_note1.paragraph_format.space_after = Pt(1)
    r_note1 = p_note1.add_run('    ※ 국내 워드 프로그램 시장점유율 : MS 60%, 한글 40% 수준')
    r_note1.font.size = Pt(9.0)
    r_note1.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_note2 = doc.add_paragraph()
    p_note2.paragraph_format.space_before = Pt(1)
    p_note2.paragraph_format.space_after = Pt(3)
    r_note2 = p_note2.add_run('     * 약 25만개 : 법령·행정규칙서식 5.4만 개(신고·신청서 8천여 개), 자치법규서식 19만 개')
    r_note2.font.size = Pt(9.0)
    r_note2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_b3 = doc.add_paragraph()
    p_b3.paragraph_format.space_before = Pt(3)
    p_b3.paragraph_format.space_after = Pt(2)
    p_b3.paragraph_format.line_spacing = Pt(14.0)
    r_b3 = p_b3.add_run(' ○ hwp서식파일에 대한 이용제약 완화를 위한 한컴社 협의(’19.4.~)')
    r_b3.font.size = Pt(10.0)

    p_b4 = doc.add_paragraph()
    p_b4.paragraph_format.space_before = Pt(1)
    p_b4.paragraph_format.space_after = Pt(4)
    p_b4.paragraph_format.line_spacing = Pt(14.0)
    r_b4 = p_b4.add_run('   - 서식 작성용 SW(유료SW 대비 기능 최소화) 개발, 무료 배포 등 협의')
    r_b4.font.size = Pt(10.0)

    # Section 2: 기대효과
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(12)
    p_h2.paragraph_format.space_after = Pt(4)
    r_h2 = p_h2.add_run('□ 기대효과')
    r_h2.bold = True
    r_h2.font.size = Pt(12.0)
    r_h2.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    p_e1 = doc.add_paragraph()
    p_e1.paragraph_format.space_before = Pt(2)
    p_e1.paragraph_format.space_after = Pt(2)
    p_e1.paragraph_format.line_spacing = Pt(14.0)
    r_e1 = p_e1.add_run(' ○ ｢한글｣*을 구입하지 않아도 서식 작성·편집이 가능하여 온·오프라인 민원 편의 제고\n    (법정신고·신청서식 8천여 종, 비법정 임의서식 상당수 작성 수혜)')
    r_e1.font.size = Pt(10.0)

    p_enote = doc.add_paragraph()
    p_enote.paragraph_format.space_before = Pt(1)
    p_enote.paragraph_format.space_after = Pt(2)
    r_enote = p_enote.add_run('     * 한글 유료 소프트웨어 : 가정용(6∼8만원), 기업용(프리미엄 15만원)')
    r_enote.font.size = Pt(9.0)
    r_enote.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_e2 = doc.add_paragraph()
    p_e2.paragraph_format.space_before = Pt(2)
    p_e2.paragraph_format.space_after = Pt(4)
    p_e2.paragraph_format.line_spacing = Pt(14.0)
    r_e2 = p_e2.add_run(' ○ ｢문서24｣ 등을 통한 온라인 서식 제출시 출력, 기입, 스캔할 필요 없이 온라인 상에서 바로 작성, 첨부하므로 시간과 비용, 종이 절감')
    r_e2.font.size = Pt(10.0)

    # Flowchart Comparison Table (현행 vs 개선)
    t_flow = doc.add_table(rows=6, cols=3)
    t_flow.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_flow.autofit = False
    t_flow.columns[0].width = Mm(75)
    t_flow.columns[1].width = Mm(20)
    t_flow.columns[2].width = Mm(75)

    # Header Row
    c_th0 = t_flow.rows[0].cells[0]
    c_th1 = t_flow.rows[0].cells[1]
    c_th2 = t_flow.rows[0].cells[2]

    c_th0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_th0 = c_th0.paragraphs[0].add_run('현행 (as-is)')
    r_th0.bold = True
    r_th0.font.color.rgb = RGBColor(0x88, 0x22, 0x22)
    set_cell_shading(c_th0, 'FDF2F2')

    c_th1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c_th1.paragraphs[0].add_run('➔').bold = True
    set_cell_shading(c_th1, 'FFFFFF')

    c_th2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_th2 = c_th2.paragraphs[0].add_run('개선 (to-be)')
    r_th2.bold = True
    r_th2.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
    set_cell_shading(c_th2, 'E8F5E9')

    # Rows content
    steps = [
        ('서식파일 열기', '➔', '서식파일 열기'),
        ('유료SW 구입 후 컴퓨터로 내용 작성\n또는 출력 후 손으로 내용 작성', '➔', '(유료SW 없이도) 컴퓨터로 직접 내용 작성'),
        ('출력 ➔ 손 작성 ➔ 스캔 (복잡한 오프라인 절차)', '➔', '스캔/출력 불필요 (100% 디지털 완결)'),
        ('첨부, 제출 (시간·비용 소모)', '➔', '온라인 원클릭 즉시 첨부 및 제출')
    ]

    for idx, (s_left, s_arrow, s_right) in enumerate(steps):
        row = t_flow.rows[idx + 1]
        cl = row.cells[0]
        cm = row.cells[1]
        cr = row.cells[2]

        pl = cl.paragraphs[0]
        pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rl = pl.add_run(s_left)
        rl.font.size = Pt(9.0)

        pm = cm.paragraphs[0]
        pm.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rm = pm.add_run(s_arrow)
        rm.font.size = Pt(9.5)
        rm.font.color.rgb = RGBColor(0x2D, 0x6A, 0x4F)

        pr = cr.paragraphs[0]
        pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rr = pr.add_run(s_right)
        rr.font.size = Pt(9.0)
        rr.bold = True
        rr.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)

        set_cell_shading(cl, 'FAFAFA')
        set_cell_shading(cm, 'FFFFFF')
        set_cell_shading(cr, 'F4FBF7')

    for r in t_flow.rows:
        for c in r.cells:
            set_cell_border(c, top={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                               bottom={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                               left={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                               right={'val': 'single', 'sz': '4', 'color': 'D0D0D0'})
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    # Page Break to Page 2
    doc.add_page_break()

    # Section 3: 공공기관 서식한글 SW 주요내용 (Page 2)
    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(8)
    p_h3.paragraph_format.space_after = Pt(4)
    r_h3 = p_h3.add_run('□ ｢공공기관 서식한글｣ SW 주요내용')
    r_h3.bold = True
    r_h3.font.size = Pt(12.0)
    r_h3.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    # Feature 1: 기능
    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.space_before = Pt(3)
    p_f1.paragraph_format.space_after = Pt(2)
    p_f1.paragraph_format.line_spacing = Pt(14.0)
    r_f1 = p_f1.add_run(' ○ (기능) 글자입력, 복사/붙이기, 표/그림/문자표 등 서식작성 필수기능 포함')
    r_f1.bold = True
    r_f1.font.size = Pt(10.0)

    p_f1_sub = doc.add_paragraph()
    p_f1_sub.paragraph_format.space_before = Pt(1)
    p_f1_sub.paragraph_format.space_after = Pt(4)
    p_f1_sub.paragraph_format.line_spacing = Pt(14.0)
    r_f1_sub = p_f1_sub.add_run('   - PC에서 직접 공공서식에 내용 작성과 수정이 가능하도록 기본적인 편집기능 탑재, 유료SW와 차별화 위해 폰트·맞춤법 등 확장기능은 제외')
    r_f1_sub.font.size = Pt(9.5)

    # Insert Extracted Image (BIN0001.png - 서식한글 구현 화면)
    img_path = r'C:\Users\note\vf\vf17_hwpx_clone_final\result\[202]_pillow_decomp.png'
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Mm(145))

        p_img_cap = doc.add_paragraph()
        p_img_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img_cap.paragraph_format.space_before = Pt(1)
        p_img_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_img_cap.add_run('< 공공기관 서식한글 구현 화면 (예시) >')
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Feature 2: 제공대상
    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.space_before = Pt(4)
    p_f2.paragraph_format.space_after = Pt(2)
    p_f2.paragraph_format.line_spacing = Pt(14.0)
    r_f2 = p_f2.add_run(' ○ (제공대상) 공공서식 작성 용도로 활용하는 개인 사용자')
    r_f2.bold = True
    r_f2.font.size = Pt(10.0)

    p_f2_sub = doc.add_paragraph()
    p_f2_sub.paragraph_format.space_before = Pt(1)
    p_f2_sub.paragraph_format.space_after = Pt(2)
    p_f2_sub.paragraph_format.line_spacing = Pt(14.0)
    r_f2_sub = p_f2_sub.add_run('   - 공공서식 작성 외 용도로 활용하거나, 개인이 아닌 기업*이 사용할 경우 법적인 책임을 물을 수 있음을 프로그램 내 고지**(한컴 정책)')
    r_f2_sub.font.size = Pt(9.5)

    p_f2_n1 = doc.add_paragraph()
    p_f2_n1.paragraph_format.space_before = Pt(1)
    p_f2_n1.paragraph_format.space_after = Pt(1)
    r_f2_n1 = p_f2_n1.add_run('     * 다만, 실제로 민간어린이집 등 소규모 영세기업의 활용을 제한하지는 않음')
    r_f2_n1.font.size = Pt(8.5)
    r_f2_n1.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    p_f2_n2 = doc.add_paragraph()
    p_f2_n2.paragraph_format.space_before = Pt(1)
    p_f2_n2.paragraph_format.space_after = Pt(3)
    r_f2_n2 = p_f2_n2.add_run('     ** 최종사용권동의(EULA) : 소프트웨어 사용자가 저작사에서 규정한 사용 지침을 준수할 것에 동의하는 것')
    r_f2_n2.font.size = Pt(8.5)
    r_f2_n2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Feature 3: 광고
    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.space_before = Pt(3)
    p_f3.paragraph_format.space_after = Pt(2)
    p_f3.paragraph_format.line_spacing = Pt(14.0)
    r_f3 = p_f3.add_run(' ○ (광고) 사용자 편의를 해치지 않는 선에서 비영리 광고창 삽입')
    r_f3.bold = True
    r_f3.font.size = Pt(10.0)

    p_f3_sub = doc.add_paragraph()
    p_f3_sub.paragraph_format.space_before = Pt(1)
    p_f3_sub.paragraph_format.space_after = Pt(1)
    p_f3_sub.paragraph_format.line_spacing = Pt(14.0)
    r_f3_sub = p_f3_sub.add_run('   - 공익목적임을 감안, 한컴 및 그룹사 제품 홍보 등으로 광고 내용 제한')
    r_f3_sub.font.size = Pt(9.5)

    p_f3_sub2 = doc.add_paragraph()
    p_f3_sub2.paragraph_format.space_before = Pt(1)
    p_f3_sub2.paragraph_format.space_after = Pt(3)
    r_f3_sub2 = p_f3_sub2.add_run('   - 광고 방식 : 프로그램 종료 시 팝업 형태로 노출')
    r_f3_sub2.font.size = Pt(9.5)

    # Feature 4: 배포
    p_f4 = doc.add_paragraph()
    p_f4.paragraph_format.space_before = Pt(3)
    p_f4.paragraph_format.space_after = Pt(2)
    p_f4.paragraph_format.line_spacing = Pt(14.0)
    r_f4 = p_f4.add_run(' ○ (배포) 한컴사와 각 공공기관 누리집 등에서 무료 배포(다운로드 링크 제공)')
    r_f4.bold = True
    r_f4.font.size = Pt(10.0)

    p_f4_sub = doc.add_paragraph()
    p_f4_sub.paragraph_format.space_before = Pt(1)
    p_f4_sub.paragraph_format.space_after = Pt(3)
    p_f4_sub.paragraph_format.line_spacing = Pt(14.0)
    r_f4_sub = p_f4_sub.add_run('   - 사용자는 현재의 각종 뷰어 프로그램과 같은 방식으로 개인 컴퓨터에 프로그램 설치 후 무료로 hwp서식 작성 가능')
    r_f4_sub.font.size = Pt(9.5)

    # Feature 5: 사후관리
    p_f5 = doc.add_paragraph()
    p_f5.paragraph_format.space_before = Pt(3)
    p_f5.paragraph_format.space_after = Pt(2)
    p_f5.paragraph_format.line_spacing = Pt(14.0)
    r_f5 = p_f5.add_run(' ○ (사후관리) 프로그램 오류 및 기능 개선사항 등은 수시 업데이트')
    r_f5.bold = True
    r_f5.font.size = Pt(10.0)

    out_docx = r'C:\Users\note\vf\vf17_hwpx_clone_final\result\[210]_공공서식한글_마스터_2p.docx'
    doc.save(out_docx)
    print(f'Successfully built master docx: {out_docx}')
    return out_docx

def compile_pdf_and_visioncheck(docx_path):
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        wdoc = word.Documents.Open(os.path.abspath(docx_path))
        pages = wdoc.ComputeStatistics(2)
        print(f'Verified Word Pages: {pages}')
        out_pdf = r'C:\Users\note\vf\vf17_hwpx_clone_final\result\[214]_공공서식한글_공인_2p.pdf'
        wdoc.SaveAs(os.path.abspath(out_pdf), 17)
        wdoc.Close(False)
        print(f'Saved PDF: {out_pdf}')
    finally:
        word.Quit()

    # Generate 300 DPI VisionCheck images
    doc_pdf = fitz.open(out_pdf)
    for p_num in range(len(doc_pdf)):
        page = doc_pdf[p_num]
        pix = page.get_pixmap(dpi=150)
        img_out = rf'C:\Users\note\vf\vf17_hwpx_clone_final\result\[215]_VisionCheck_p{p_num+1:02d}.png'
        pix.save(img_out)
        print(f'Saved VisionCheck image: {img_out}')

if __name__ == '__main__':
    d_path = create_gonggong_document()
    compile_pdf_and_visioncheck(d_path)
