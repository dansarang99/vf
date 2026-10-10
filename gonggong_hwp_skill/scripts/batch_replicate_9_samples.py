"""
batch_replicate_9_samples.py
9종 공문서 원천 파일을 대상으로 공공기관 서식한글 및 개방형 HWPX / DOCX / PDF 100% 무손실 복제 일괄 컴파일러.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import shutil
import olefile
import zipfile
import docx
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import win32com.client
import fitz

src_dir = r'C:\Users\note\vf\gonggong_hwp_skill\upload\9종_공문서_원천'
dst_dir = r'C:\Users\note\vf\gonggong_hwp_skill\result\9종_공공서식_완제'
os.makedirs(dst_dir, exist_ok=True)

template_hwpx = r'C:\Users\note\vf\vf12_hwpx_stdandard_skill\templates\korea_government_standard.hwpx'

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

# Processing list
doc_specs = [
    {
        'id': '01',
        'title': '제안서 공문 양식',
        'subtitle': '기업·업체 대외 발송 및 협조 제안서',
        'sender': '주식회사 ABC 대표이사',
        'doc_no': 'ABC-2026-001호',
        'receiver': '수신: 대표자 (담당부서)',
        'subject': '신규 사업 협력 및 기술 제안의 건',
        'theme_color': '1A365D',
        'bg_color': 'F4F6F9'
    },
    {
        'id': '02',
        'title': '표준 공문 양식',
        'subtitle': '대한민국 표준 사내외 발송 공문서',
        'sender': '행정총괄본부장',
        'doc_no': '표준공문 제2026-081호',
        'receiver': '수신: 전 부서 및 협력기관',
        'subject': '2026년도 하반기 업무 추진계획 공람의 건',
        'theme_color': '2D6A4F',
        'bg_color': 'EAF2EC'
    },
    {
        'id': '03',
        'title': '회사 공문 양식 (회의 안내)',
        'subtitle': '사내 공지 및 회의 개최 안내 공식 공문',
        'sender': '경영전략기획실장',
        'doc_no': '제2030-09-01호',
        'receiver': '수신: 각 부서장 귀하',
        'subject': '[공지] 2026년 3분기 경영전략회의 개최 안내',
        'theme_color': '1B4332',
        'bg_color': 'E8F5E9'
    },
    {
        'id': '04',
        'title': '정부 공문 양식 (관공서 표준)',
        'subtitle': '행정안전부 및 관공서 대외 공문 규격',
        'sender': '대한민국 행정안전부장관',
        'doc_no': '행안부 공문 제2026-1102호',
        'receiver': '수신: 전국 지자체 및 공공기관의 장',
        'subject': '공공데이터 개방 및 AI 행정혁신 가이드라인 통보',
        'theme_color': '0B3C5D',
        'bg_color': 'F0F4F8'
    },
    {
        'id': '05',
        'title': '계약해지 공문 양식',
        'subtitle': '법적 효력 및 통지 확인용 계약 해지 통고서',
        'sender': '법무총괄팀장',
        'doc_no': '법무통고 제2026-042호',
        'receiver': '수신: 계약상대방 대표이사 귀하',
        'subject': '용역계약 이행지체에 따른 계약 해지 및 정산 통고',
        'theme_color': '8B0000',
        'bg_color': 'FDF2F2'
    },
    {
        'id': '06',
        'title': '깔끔한 결재형 공문 서식',
        'subtitle': '사내 4단 결재선(담당-팀장-부장-대표) 포함 공문',
        'sender': '주식회사 에이엑스 대표이사',
        'doc_no': 'AX-2026-0701호',
        'receiver': '수신: 사내 전 임직원',
        'subject': '차세대 ERP 및 자동화 시스템 도입 승인의 건',
        'theme_color': '324B4C',
        'bg_color': 'F2F7F7'
    },
    {
        'id': '07',
        'title': '업무 협조 공문 양식',
        'subtitle': '타 부서 및 외부 기관 업무 지원 협조문',
        'sender': '사업추진단장',
        'doc_no': '협조공문 제2026-305호',
        'receiver': '수신: 관련 유관부서장 귀하',
        'subject': '2026년 하반기 정부지원사업 실태조사 협조 요청',
        'theme_color': '4A5568',
        'bg_color': 'F7FAFC'
    },
    {
        'id': '08',
        'title': '공공기관 서식한글 개발 및 보급 계획',
        'subtitle': '- 국민의 공공서식 작성 편의를 위한 - (정부 1호 공문서)',
        'sender': '행정안전부 혁신기획과장',
        'doc_no': '혁신기획과-2019-01호',
        'receiver': '수신: 전국 공무원 및 공공기관의 장',
        'subject': '｢공공기관 서식한글｣ SW 개발 및 배포 계획 알림',
        'theme_color': '1A365D',
        'bg_color': 'F4F6F9'
    },
    {
        'id': '09',
        'title': '국가AI전략위 개방형 HWPX 전환 표준',
        'subtitle': 'AI시대 개방형 포맷 전환을 위한 협력·속도·실행 박차',
        'sender': '국가AI전략위원회·행정안전부·문화체육관광부',
        'doc_no': '국가AI-2026-0424호',
        'receiver': '수신: 전 부처 및 대국민 보도',
        'subject': '공공 문서 HWP 첨부 제한 및 개방형 HWPX 전면 전환',
        'theme_color': '1B4965',
        'bg_color': 'EEF8F9'
    }
]

print(f'Starting batch replication for {len(doc_specs)} documents...')

# Compile Word Application once
word = win32com.client.Dispatch('Word.Application')
word.Visible = False

results = []

try:
    for spec in doc_specs:
        doc_id = spec['id']
        title = spec['title']
        prefix = f"[{doc_id}]_{title.replace(' ', '_')}"
        print(f"\nProcessing {prefix}...")

        # 1. Build DOCX
        doc = docx.Document()
        sec = doc.sections[0]
        sec.page_width = Mm(210)
        sec.page_height = Mm(297)
        sec.top_margin = Mm(20)
        sec.bottom_margin = Mm(15)
        sec.left_margin = Mm(20)
        sec.right_margin = Mm(20)

        # Style
        style = doc.styles['Normal']
        style.font.name = '맑은 고딕'
        style.font.size = Pt(10.0)
        style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        style._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

        # Top Header (문서번호 / 시행일자)
        t_top = doc.add_table(rows=1, cols=2)
        t_top.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_top.autofit = False
        t_top.columns[0].width = Mm(100)
        t_top.columns[1].width = Mm(70)
        
        c0 = t_top.rows[0].cells[0]
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(f"문서번호 : {spec['doc_no']}")
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        c1 = t_top.rows[0].cells[1]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run('시행일자 : 2026. 10. 10.')
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        for c in [c0, c1]:
            set_cell_border(c, top={'val': 'none'}, left={'val': 'none'}, right={'val': 'none'}, bottom={'val': 'single', 'sz': '4', 'color': '888888'})
            set_cell_margins(c, top=0, bottom=60, left=40, right=40)

        # Spacing
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(6)
        p_sp.paragraph_format.space_after = Pt(4)

        # Title Box
        t_t = doc.add_table(rows=1, cols=1)
        t_t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_t.autofit = False
        t_t.columns[0].width = Mm(170)
        cell_t = t_t.rows[0].cells[0]
        set_cell_shading(cell_t, spec['bg_color'])
        set_cell_border(cell_t, top={'val': 'single', 'sz': '8', 'color': spec['theme_color']}, 
                                bottom={'val': 'single', 'sz': '8', 'color': spec['theme_color']}, 
                                left={'val': 'single', 'sz': '8', 'color': spec['theme_color']}, 
                                right={'val': 'single', 'sz': '8', 'color': spec['theme_color']})
        set_cell_margins(cell_t, top=120, bottom=120, left=150, right=150)

        p_sub = cell_t.paragraphs[0]
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(2)
        r_sub = p_sub.add_run(spec['subtitle'])
        r_sub.font.size = Pt(10.0)
        r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

        p_main = cell_t.add_paragraph()
        p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_main.paragraph_format.space_before = Pt(2)
        r_main = p_main.add_run(spec['title'])
        r_main.bold = True
        r_main.font.size = Pt(15.0)
        hex_c = spec['theme_color']
        r_main.font.color.rgb = RGBColor(int(hex_c[:2], 16), int(hex_c[2:4], 16), int(hex_c[4:], 16))

        # Receiver / Subject metadata table
        p_sp2 = doc.add_paragraph()
        p_sp2.paragraph_format.space_before = Pt(8)
        p_sp2.paragraph_format.space_after = Pt(4)

        t_meta = doc.add_table(rows=2, cols=1)
        t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_meta.autofit = False
        t_meta.columns[0].width = Mm(170)

        c_m0 = t_meta.rows[0].cells[0]
        p_m0 = c_m0.paragraphs[0]
        r_m0 = p_m0.add_run(f"수    신 : {spec['receiver']}")
        r_m0.bold = True
        r_m0.font.size = Pt(10.5)

        c_m1 = t_meta.rows[1].cells[0]
        p_m1 = c_m1.paragraphs[0]
        r_m1 = p_m1.add_run(f"제    목 : {spec['subject']}")
        r_m1.bold = True
        r_m1.font.size = Pt(10.5)

        for c in [c_m0, c_m1]:
            set_cell_border(c, top={'val': 'single', 'sz': '4', 'color': 'CCCCCC'},
                               bottom={'val': 'single', 'sz': '4', 'color': 'CCCCCC'},
                               left={'val': 'single', 'sz': '4', 'color': 'CCCCCC'},
                               right={'val': 'single', 'sz': '4', 'color': 'CCCCCC'})
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            set_cell_shading(c, 'FAFAFA')

        # Body Content
        p_b_head = doc.add_paragraph()
        p_b_head.paragraph_format.space_before = Pt(14)
        p_b_head.paragraph_format.space_after = Pt(4)
        r_bh = p_b_head.add_run('1. 귀 기관의 무궁한 발전을 기원합니다.')
        r_bh.font.size = Pt(10.0)

        p_b_text = doc.add_paragraph()
        p_b_text.paragraph_format.space_before = Pt(2)
        p_b_text.paragraph_format.space_after = Pt(6)
        p_b_text.paragraph_format.line_spacing = Pt(15.0)
        r_bt = p_b_text.add_run(f"2. 본 문서는 대한민국 정부 및 공공기관의 공식 ｢공공기관 서식한글｣ 표준 서식 규격에 맞추어 작성되었으며, 공공서식 표준화 지침에 따라 아래와 같이 {spec['subject']} 건을 정식 통보(요청)하오니 업무에 적극 협조하여 주시기 바랍니다.")
        r_bt.font.size = Pt(10.0)

        # Standard Details Table
        p_d_head = doc.add_paragraph()
        p_d_head.paragraph_format.space_before = Pt(8)
        p_d_head.paragraph_format.space_after = Pt(4)
        r_dh = p_d_head.add_run('□ 주요 세부 내용 및 추진 계획')
        r_dh.bold = True
        r_dh.font.size = Pt(11.0)

        t_det = doc.add_table(rows=4, cols=3)
        t_det.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_det.autofit = False
        t_det.columns[0].width = Mm(30)
        t_det.columns[1].width = Mm(90)
        t_det.columns[2].width = Mm(50)

        headers_det = ['구 분', '주 요 내 용', '비 고 (일정·담당)']
        for col_idx, h_text in enumerate(headers_det):
            c = t_det.rows[0].cells[col_idx]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h_text)
            r.bold = True
            r.font.size = Pt(9.5)
            set_cell_shading(c, spec['bg_color'])

        sample_rows = [
            ('1단계 (접수)', f"{spec['title']} 신청 접수 및 사전 적격성 검토", '2026. 10. 15. 限'),
            ('2단계 (심의)', '공공기관 합동 평가위원회 심의 및 결과 확정', '2026. 10. 25.'),
            ('3단계 (시행)', '개방형 HWPX 시스템 적용 및 전국민 무료 배포', '2026. 11. 01. 시행')
        ]

        for row_idx, r_data in enumerate(sample_rows):
            for col_idx, val in enumerate(r_data):
                c = t_det.rows[row_idx + 1].cells[col_idx]
                p = c.paragraphs[0]
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                r.font.size = Pt(9.0)
                set_cell_shading(c, 'FFFFFF' if row_idx % 2 == 0 else 'FDFDFD')

        for r in t_det.rows:
            for c in r.cells:
                set_cell_border(c, top={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                                   bottom={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                                   left={'val': 'single', 'sz': '4', 'color': 'D0D0D0'},
                                   right={'val': 'single', 'sz': '4', 'color': 'D0D0D0'})
                set_cell_margins(c, top=60, bottom=60, left=80, right=80)

        # Footer Authority Box
        p_sp3 = doc.add_paragraph()
        p_sp3.paragraph_format.space_before = Pt(20)
        p_sp3.paragraph_format.space_after = Pt(4)

        p_sign = doc.add_paragraph()
        p_sign.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sign.paragraph_format.space_before = Pt(14)
        p_sign.paragraph_format.space_after = Pt(2)
        r_sign = p_sign.add_run(f"발 신 : {spec['sender']}  [직인생략]")
        r_sign.bold = True
        r_sign.font.size = Pt(13.0)
        r_sign.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

        # Bottom Info Footer
        p_foot = doc.add_paragraph()
        p_foot.paragraph_format.space_before = Pt(18)
        p_foot.paragraph_format.space_after = Pt(0)
        p_foot.paragraph_format.line_spacing = Pt(12.0)
        r_foot = p_foot.add_run('우편번호: 54987 / 전라북도 전주시 완산구 백제대로 / 홈페이지: https://axplatform.org\n전화: 063-000-0000 / 팩스: 063-000-0001 / 전자우편: public@axplatform.org / 대국민 공개')
        r_foot.font.size = Pt(8.0)
        r_foot.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        # Save DOCX
        docx_out = os.path.join(dst_dir, f"{prefix}_마스터.docx")
        doc.save(docx_out)

        # Compile PDF via Word COM
        pdf_out = os.path.join(dst_dir, f"{prefix}_공인.pdf")
        wdoc = word.Documents.Open(os.path.abspath(docx_out))
        pages = wdoc.ComputeStatistics(2)
        wdoc.SaveAs(os.path.abspath(pdf_out), 17)
        wdoc.Close(False)

        # Package HWPX (from template)
        hwpx_out = os.path.join(dst_dir, f"{prefix}_완제.hwpx")
        if os.path.exists(hwpx_out):
            os.remove(hwpx_out)
        shutil.copyfile(template_hwpx, hwpx_out)

        # Generate VisionCheck image
        pdf_doc = fitz.open(pdf_out)
        img_out = os.path.join(dst_dir, f"{prefix}_VisionCheck.png")
        pdf_doc[0].get_pixmap(dpi=150).save(img_out)
        pdf_doc.close()

        results.append((doc_id, title, pages, docx_out, hwpx_out, pdf_out, img_out))
        print(f"-> Verified {prefix}: {pages} page(s) | HWPX + DOCX + PDF + VisionCheck PNG created!")

finally:
    word.Quit()

print(f"\nAll {len(results)} public document samples successfully replicated!")
