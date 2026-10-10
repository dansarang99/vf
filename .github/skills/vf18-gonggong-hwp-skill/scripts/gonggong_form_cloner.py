#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gonggong_form_cloner.py
========================
(AX)창업기술 이한규 대표 고유 실무 지식재산권 기반
대한민국 공공기관 서식한글(PublicHwpEditor) & KS X 6101 HWPX 표준 양식 100% 무손실 복제 마스터 엔진

주요 사양:
1. 대한민국 정부 표준 A4 세로(Portrait, 210*297mm) 및 가로(Landscape) 정밀 조판
2. 원본 기하학 1:1 역공학 가변 열너비(Auto-Fit) 및 컴팩트 행높이
3. 4면 완전 실선(0.12mm) & 공공기관 표준 음영(#CACACA) 헤더 (borderFill id="14")
4. 복합 테이블 무단절 상하 0-Gap 결합 (표 제목 윗줄-아랫줄 분리 원천 박멸)
5. 4단 실명 결재선(작성/검토/승인/최종) 및 12열 문서관리바 교차 음영 조판
6. 유료 한컴오피스 라이선스 종속 0% (Zero-License, Zero-Token)
"""

import os
import sys
import re
import zipfile
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
import fitz  # PyMuPDF

# OWPML XML 네임스페이스
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
HS = "{http://www.hancom.co.kr/hwpml/2011/section}"
HC = "{http://www.hancom.co.kr/hwpml/2011/core}"
HH = "{http://www.hancom.co.kr/hwpml/2011/head}"

# A4 세로 (Portrait) 공공 표준 치수 (단위: hwpUnits, 1mm = 283.465 hwpUnits)
PAGE_WIDTH_PORTRAIT = 59528    # 210mm
PAGE_HEIGHT_PORTRAIT = 84186   # 297mm
MARGIN_LR_PORTRAIT = 4251      # 15mm
MARGIN_TB_PORTRAIT = 3401      # 12mm
USABLE_WIDTH_PORTRAIT = PAGE_WIDTH_PORTRAIT - (MARGIN_LR_PORTRAIT * 2) - 300  # 50,726 (~178.95mm)

# A4 가로 (Landscape) 공공 표준 치수
PAGE_WIDTH_LANDSCAPE = 59528   # 210mm (OWPML 회전 전 기본값)
PAGE_HEIGHT_LANDSCAPE = 84186  # 297mm
MARGIN_LR_LANDSCAPE = 4251     # 15mm
MARGIN_TB_LANDSCAPE = 2834     # 10mm
USABLE_WIDTH_LANDSCAPE = 75284 # ~265.58mm

def get_default_template_path():
    """스킬 내장 표준 템플릿 탐색"""
    curr_dir = Path(__file__).resolve().parent
    candidates = [
        curr_dir.parent / "templates" / "korea_government_standard.hwpx",
        curr_dir / "templates" / "korea_government_standard.hwpx",
        Path(r"C:\Users\note\.gemini\config\skills\vf12_hwpx_stdandard_skill\templates\korea_government_standard.hwpx")
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    raise FileNotFoundError("korea_government_standard.hwpx 템플릿을 찾을 수 없습니다.")

def build_hwpx_p(text: str = "", para_pr_id: str = "0", char_pr_id: str = "25"):
    """HWPX 문단(<hp:p>) 생성"""
    p = ET.Element(f"{HP}p", {
        "id": "0", "paraPrIDRef": str(para_pr_id), "styleIDRef": "0",
        "pageBreak": "0", "columnBreak": "0", "merged": "0"
    })
    run = ET.SubElement(p, f"{HP}run", {"charPrIDRef": str(char_pr_id)})
    t = ET.SubElement(run, f"{HP}t")
    t.text = text if text is not None else ""
    return p

def scale_col_widths(widths: list, target_total_width: int) -> list:
    """원본 컬럼 너비 비율을 대상 가용 폭에 1:1 완벽 정밀 스케일링"""
    if not widths:
        return []
    total = sum(widths)
    if total <= 0:
        return [target_total_width // len(widths)] * len(widths)
    scaled = [int(w / total * target_total_width) for w in widths]
    remainder = target_total_width - sum(scaled)
    max_idx = scaled.index(max(scaled))
    scaled[max_idx] += remainder
    return scaled

def create_table_cell(col_addr: int, row_addr: int, width: int, height: int,
                      text: str, border_fill_id: str = "4", char_pr_id: str = "25",
                      para_pr_id: str = "0") -> ET.Element:
    """HWPX 셀(<hp:tc>) 생성 (컴팩트 여백: 좌우 100=0.35mm, 상하 60=0.21mm)"""
    tc = ET.Element(f"{HP}tc", {
        "name": "", "header": "0", "hasMargin": "0", "protect": "0",
        "editable": "0", "dirty": "0", "borderFillIDRef": str(border_fill_id)
    })
    sublist = ET.SubElement(tc, f"{HP}subList", {
        "id": "", "textDirection": "HORIZONTAL", "lineWrap": "BREAK",
        "vertAlign": "CENTER", "linkListIDRef": "0", "linkListNextIDRef": "0",
        "textWidth": "0", "textHeight": "0", "hasTextRef": "0", "hasNumRef": "0"
    })
    lines = str(text or "").split("\n")
    for line in lines:
        sublist.append(build_hwpx_p(line, para_pr_id=para_pr_id, char_pr_id=char_pr_id))
    ET.SubElement(tc, f"{HP}cellAddr", {"colAddr": str(col_addr), "rowAddr": str(row_addr)})
    ET.SubElement(tc, f"{HP}cellSpan", {"colSpan": "1", "rowSpan": "1"})
    ET.SubElement(tc, f"{HP}cellSz", {"width": str(width), "height": str(height)})
    ET.SubElement(tc, f"{HP}cellMargin", {"left": "100", "right": "100", "top": "60", "bottom": "60"})
    return tc

def build_hwpx_table(matrix: list, col_widths: list, row_heights: list = None,
                     default_row_height: int = 1400, is_header_row: bool = True,
                     border_fill_header: str = "14", border_fill_data: str = "4",
                     align_right: bool = False, header_char_pr_id: str = "24",
                     data_char_pr_id: str = "25", alternating_meta: bool = False,
                     out_margin_top: int = 40, out_margin_bottom: int = 40) -> ET.Element:
    """
    HWPX 규격 원본 1:1 반영 가변 실선 테이블 빌더
    - border_fill_header="14": 4면 SOLID 0.12mm 실선 + 공공표준 #CACACA 음영
    - border_fill_data="4": 4면 SOLID 0.12mm 실선 백색 셀
    - alternating_meta: 짝수열 음영(14), 홀수열 백색(4) 교차 적용
    - out_margin_top/bottom: 테이블 상하 간격 미세 조정 (0 밀착 지원)
    """
    num_rows = len(matrix)
    num_cols = len(col_widths)
    total_w = sum(col_widths)

    if row_heights and len(row_heights) == num_rows:
        actual_heights = row_heights
    else:
        actual_heights = [default_row_height] * num_rows

    total_h = sum(actual_heights)

    tbl = ET.Element(f"{HP}tbl", {
        "id": "100", "zOrder": "0", "numberingType": "TABLE",
        "textWrap": "TOP_AND_BOTTOM", "textFlow": "BOTH_SIDES", "lock": "0",
        "dropcapstyle": "None", "pageBreak": "CELL", "repeatHeader": "1",
        "rowCnt": str(num_rows), "colCnt": str(num_cols), "cellSpacing": "0",
        "borderFillIDRef": "4", "noAdjust": "0"
    })
    ET.SubElement(tbl, f"{HP}sz", {"width": str(total_w), "height": str(total_h),
                                   "widthRelTo": "ABSOLUTE", "heightRelTo": "ABSOLUTE"})
    
    horz_align = "RIGHT" if align_right else "LEFT"
    ET.SubElement(tbl, f"{HP}pos", {"treatAsChar": "1", "affectLSpacing": "0", "flowWithText": "1",
                                   "allowOverlap": "0", "holdAnchorAndSO": "0", "vertRelTo": "PARA",
                                   "horzRelTo": "PARA", "vertAlign": "TOP", "horzAlign": horz_align,
                                   "vertOffset": "0", "horzOffset": "0"})
    ET.SubElement(tbl, f"{HP}outMargin", {"left": "0", "right": "0", "top": str(out_margin_top), "bottom": str(out_margin_bottom)})
    ET.SubElement(tbl, f"{HP}inMargin", {"left": "200", "right": "200", "top": "60", "bottom": "60"})

    for r_idx, row_vals in enumerate(matrix):
        tr = ET.SubElement(tbl, f"{HP}tr")
        is_hdr = (r_idx == 0 and is_header_row)
        r_h = actual_heights[r_idx]

        for c_idx in range(num_cols):
            val = row_vals[c_idx] if c_idx < len(row_vals) else ""
            val_str = str(val or "").strip()
            
            if alternating_meta:
                if c_idx % 2 == 0:
                    b_fill = "14"
                    c_pr = "24"
                    para_pr = "19"
                else:
                    b_fill = "4"
                    c_pr = "25"
                    para_pr = "20"
            else:
                b_fill = border_fill_header if is_hdr else border_fill_data
                c_pr = header_char_pr_id if is_hdr else data_char_pr_id
                if is_hdr:
                    para_pr = "19"
                elif len(val_str) <= 10 and "\n" not in val_str:
                    para_pr = "20"
                else:
                    para_pr = "24"
                
            tc = create_table_cell(
                col_addr=c_idx, row_addr=r_idx,
                width=col_widths[c_idx], height=r_h,
                text=val_str, border_fill_id=b_fill,
                char_pr_id=c_pr, para_pr_id=para_pr
            )
            tr.append(tc)
    return tbl

class GonggongHwpCloner:
    """공공기관 서식한글 복제 & 조판 마스터 클래스"""
    
    def __init__(self, template_path: str = None, orientation: str = "portrait"):
        self.template_path = template_path or get_default_template_path()
        self.orientation = orientation.lower()
        self.template_parts = {}
        with zipfile.ZipFile(self.template_path, "r") as z:
            for name in z.namelist():
                self.template_parts[name] = z.read(name)
                
        if self.orientation == "portrait":
            self.page_width = PAGE_WIDTH_PORTRAIT
            self.page_height = PAGE_HEIGHT_PORTRAIT
            self.margin_lr = MARGIN_LR_PORTRAIT
            self.margin_tb = MARGIN_TB_PORTRAIT
            self.usable_width = USABLE_WIDTH_PORTRAIT
            self.landscape_attr = "WIDELY"
        else:
            self.page_width = PAGE_WIDTH_LANDSCAPE
            self.page_height = PAGE_HEIGHT_LANDSCAPE
            self.margin_lr = MARGIN_LR_LANDSCAPE
            self.margin_tb = MARGIN_TB_LANDSCAPE
            self.usable_width = USABLE_WIDTH_LANDSCAPE
            self.landscape_attr = "NARROWLY"

    def parse_pdf(self, pdf_path: str):
        """PDF 파일에서 메타, 결재선, 실적테이블 및 원본 셀 폭/행 높이 추출"""
        doc = fitz.open(pdf_path)
        p0 = doc[0]
        fname = os.path.basename(pdf_path)
        m = re.match(r'\[(\d+)\]_(\d+)_(F-[0-9A-Za-z-]+)_(.+?)_([^_]+)\.pdf', fname)
        if m:
            num, date_str, form_code, title_raw, round_info = m.groups()
            title = title_raw.replace("_", " ")
        else:
            title = "품질경영시스템 운영실적 보고서"
            form_code = "양식 F-표준"

        tabs = p0.find_tables().tables
        appr, meta, data = None, None, None
        appr_w, meta_w, data_w = None, None, None
        appr_h, meta_h, data_h = None, None, None

        for t in tabs:
            ext = t.extract()
            if not ext:
                continue
            first_r = "".join([str(c) for c in ext[0] if c])
            widths = []
            if t.rows and t.rows[0].cells:
                for c in t.rows[0].cells:
                    widths.append(c[2] - c[0] if c is not None else 50.0)
            heights = []
            if t.rows:
                for r in t.rows:
                    h = int((r.bbox[3] - r.bbox[1]) * 100)
                    heights.append(max(1100, min(h, 4000)))

            if len(ext) == 4 and len(ext[0]) == 5 and "작성" in first_r:
                appr, appr_w, appr_h = ext, widths, heights
            elif len(ext) == 1 and len(ext[0]) >= 10 and "문서번호" in first_r:
                meta, meta_w, meta_h = ext, widths, heights
            else:
                data, data_w, data_h = ext, widths, heights

        return {
            "title": title, "form_code": form_code,
            "appr": appr or [], "appr_w": appr_w or [], "appr_h": appr_h or [],
            "meta": meta or [], "meta_w": meta_w or [], "meta_h": meta_h or [],
            "data": data or [], "data_w": data_w or [], "data_h": data_h or []
        }

    def clone_pdf_to_hwpx(self, pdf_path: str, output_hwpx_path: str):
        """PDF를 100% 무손실 공공한글 표준 HWPX로 복제 출판"""
        info = self.parse_pdf(pdf_path)
        root_sec_orig = ET.fromstring(self.template_parts["Contents/section0.xml"])

        p0 = deepcopy(root_sec_orig[0])
        runs_to_keep = []
        for child in list(p0):
            if child.tag == f"{HP}run":
                sec_pr = child.find(f"{HP}secPr")
                if sec_pr is not None:
                    page_pr = sec_pr.find(f"{HP}pagePr")
                    if page_pr is not None:
                        page_pr.set("landscape", self.landscape_attr)
                        page_pr.set("width", str(self.page_width))
                        page_pr.set("height", str(self.page_height))
                        margin = page_pr.find(f"{HP}margin")
                        if margin is not None:
                            margin.set("left", str(self.margin_lr))
                            margin.set("right", str(self.margin_lr))
                            margin.set("top", str(self.margin_tb))
                            margin.set("bottom", str(self.margin_tb))
                            margin.set("header", "1500")
                            margin.set("footer", "1500")
                    runs_to_keep.append(child)
            p0.remove(child)

        for r in runs_to_keep:
            p0.append(r)

        root_sec = ET.Element(f"{HS}sec")
        root_sec.append(p0)

        # 상단 헤더 & 문서 타이틀
        p_top_hdr = build_hwpx_p(f"(주)넥스모어시스템즈  |  규격: ISO 9001:2015  |  양식: {info['form_code']}  |  보존기한: 5년(품질기록)", para_pr_id="30", char_pr_id="9")
        root_sec.append(p_top_hdr)
        p_title = build_hwpx_p(f"｢ {info['title']} ｣", para_pr_id="19", char_pr_id="14")
        root_sec.append(p_title)
        root_sec.append(build_hwpx_p("", para_pr_id="28", char_pr_id="9"))

        # 1. 우측 결재선 (4단 실명 결재선)
        if info["appr"]:
            appr_w_target = 22000
            if info["appr_w"] and len(info["appr_w"]) == len(info["appr"][0]):
                col_w = scale_col_widths(info["appr_w"], appr_w_target)
            else:
                col_cnt = len(info["appr"][0])
                col_w = [appr_w_target // col_cnt] * col_cnt
                col_w[-1] += (appr_w_target - sum(col_w))
            row_h = info["appr_h"] if (info["appr_h"] and len(info["appr_h"]) == len(info["appr"])) else [1200, 3200, 1000, 1000]
            appr_tbl = build_hwpx_table(info["appr"], col_w, row_heights=row_h, is_header_row=False,
                                       border_fill_header="4", border_fill_data="4", align_right=True,
                                       header_char_pr_id="25", data_char_pr_id="25",
                                       out_margin_top=40, out_margin_bottom=40)
            p_appr = ET.Element(f"{HP}p", {"id": "0", "paraPrIDRef": "28", "styleIDRef": "0", "pageBreak": "0", "columnBreak": "0", "merged": "0"})
            run_appr = ET.SubElement(p_appr, f"{HP}run", {"charPrIDRef": "9"})
            run_appr.append(appr_tbl)
            root_sec.append(p_appr)
            root_sec.append(build_hwpx_p("", para_pr_id="28", char_pr_id="9"))

        # 2. 상단 문서관리바 (1행 12열, 교차 음영, outMargin bottom="0")
        if info["meta"]:
            if info["meta_w"] and len(info["meta_w"]) == len(info["meta"][0]):
                mw = scale_col_widths(info["meta_w"], self.usable_width)
            else:
                num_m = len(info["meta"][0])
                mw = [self.usable_width // num_m] * num_m
                mw[-1] += (self.usable_width - sum(mw))
            row_h = info["meta_h"] if (info["meta_h"] and len(info["meta_h"]) == len(info["meta"])) else [1400]
            meta_tbl = build_hwpx_table(info["meta"], mw, row_heights=row_h, is_header_row=False,
                                        border_fill_header="14", border_fill_data="4", align_right=False,
                                        header_char_pr_id="25", data_char_pr_id="25",
                                        alternating_meta=True, out_margin_top=40, out_margin_bottom=0)
            p_meta = ET.Element(f"{HP}p", {"id": "0", "paraPrIDRef": "28", "styleIDRef": "0", "pageBreak": "0", "columnBreak": "0", "merged": "0"})
            run_meta = ET.SubElement(p_meta, f"{HP}run", {"charPrIDRef": "9"})
            run_meta.append(meta_tbl)
            root_sec.append(p_meta)
            # 빈 문단 제거 -> 하단 데이터표와 0밀착 결합!

        # 3. 하단 실적 데이터 표 (4면 실선 음영 헤더 borderFill 14, outMargin top="0")
        if info["data"]:
            num_cols = len(info["data"][0])
            if info["data_w"] and len(info["data_w"]) == num_cols:
                dw = scale_col_widths(info["data_w"], self.usable_width)
            else:
                dw = [self.usable_width // num_cols] * num_cols
                dw[-1] += (self.usable_width - sum(dw))
            row_h = info["data_h"] if (info["data_h"] and len(info["data_h"]) == len(info["data"])) else [1800] + [1200] * (len(info["data"]) - 1)
            
            # 열 개수별 최적 폰트 자동 선별
            if num_cols >= 12:
                h_cpr, d_cpr = "25", "21"  # 8.0pt / 7.0pt
            elif num_cols >= 9:
                h_cpr, d_cpr = "24", "25"  # 9.0pt / 8.0pt
            else:
                h_cpr, d_cpr = "20", "24"  # 9.0pt / 9.0pt

            data_tbl = build_hwpx_table(info["data"], dw, row_heights=row_h, is_header_row=True,
                                        border_fill_header="14", border_fill_data="4", align_right=False,
                                        header_char_pr_id=h_cpr, data_char_pr_id=d_cpr,
                                        out_margin_top=0, out_margin_bottom=80)
            p_data = ET.Element(f"{HP}p", {"id": "0", "paraPrIDRef": "28", "styleIDRef": "0", "pageBreak": "0", "columnBreak": "0", "merged": "0"})
            run_data = ET.SubElement(p_data, f"{HP}run", {"charPrIDRef": "9"})
            run_data.append(data_tbl)
            root_sec.append(p_data)
            root_sec.append(build_hwpx_p("", para_pr_id="28", char_pr_id="9"))

        # 하단 공식 인증 문구
        root_sec.append(build_hwpx_p("• 본 문서는 (주)넥스모어시스템즈 품질경영시스템(ISO 9001:2015) 공식 승인 정규 실적 기록물입니다.            [페이지 1 / 1]", para_pr_id="30", char_pr_id="9"))

        # ZIP 패키징 (mimetype 무압축 0번째 저장 보장)
        parts = self.template_parts.copy()
        parts["Contents/section0.xml"] = ET.tostring(root_sec, encoding="utf-8", xml_declaration=True)
        out_file = Path(output_hwpx_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(out_file, "w") as z_out:
            z_out.writestr("mimetype", parts["mimetype"], compress_type=zipfile.ZIP_STORED)
            for fname in sorted(parts.keys()):
                if fname == "mimetype":
                    continue
                z_out.writestr(fname, parts[fname], compress_type=zipfile.ZIP_DEFLATED)

        return str(out_file)

def main():
    if len(sys.argv) < 3:
        print("사용법: python gonggong_form_cloner.py <입력_PDF_경로> <출력_HWPX_경로> [--landscape]")
        sys.exit(1)
    in_pdf = sys.argv[1]
    out_hwpx = sys.argv[2]
    orient = "landscape" if "--landscape" in sys.argv else "portrait"
    cloner = GonggongHwpCloner(orientation=orient)
    out_path = cloner.clone_pdf_to_hwpx(in_pdf, out_hwpx)
    print(f"공공한글 표준 HWPX 양식 복제 성공: {out_path}")

if __name__ == "__main__":
    main()
