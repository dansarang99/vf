#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[003] 마크다운 문서 -> HWPX 고정밀 변환 엔진 (Markdown to HWPX Converter)
- 기반 라이브러리: @masteroflearning/hwpxcore (hwpx-cli-main Python 엔진)
- 주요 기능:
  1. 마크다운 제목(#, ##, ###), 메타데이터, 불릿 리스트, 일반 본문 감지 및 전용 서식 적용
  2. 마크다운 테이블(| col | col |) 감지 및 HWPX 네이티브 테이블(<hp:tbl>) 고품질 자동 렌더링
  3. 표 헤더 음영 배경(#EDF2F8) 및 테두리(Solid 0.12mm) 적용
  4. 제목(18pt Navy), H1(14pt Blue), H2(12pt Dark Slate), 본문(10pt) 등 공공기관 보고서 서식 자동 매핑
  5. [001]~[999] 순차 시리얼 체계 호환
"""

import os
import sys
import re
import argparse
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

# hwpx 엔진 경로 등록
HWPX_SRC_DIR = r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)\upload\hwpx-cli-main\hwpx-cli-main\src"
if HWPX_SRC_DIR not in sys.path:
    sys.path.insert(0, HWPX_SRC_DIR)

from hwpx.document import HwpxDocument

# 한컴 HWPX 네임스페이스 정의
HH_NS = "http://www.hancom.co.kr/hwpml/2011/head"
HH = f"{{{HH_NS}}}"
HP_NS = "http://www.hancom.co.kr/hwpml/2011/paragraph"
HP = f"{{{HP_NS}}}"
HC_NS = "http://www.hancom.co.kr/hwpml/2011/core"
HC = f"{{{HC_NS}}}"


class MarkdownToHwpxConverter:
    """마크다운 텍스트를 파싱하여 HWPX 문서로 조립 및 변환하는 전문 컨버터 클래스"""

    def __init__(self):
        self.doc = HwpxDocument.new()
        self.header = self.doc.headers[0]
        self._init_custom_styles()

    def _init_custom_styles(self):
        """보고서 전용 글자 모양(charPr) 및 문단 모양(paraPr), 테두리/배경(borderFill) 초기화"""
        # 1. 문단 정렬 (가운데 정렬 추가: id="30")
        pp_list = self.header.element.find(f".//{HH}paraProperties")
        if pp_list is not None and pp_list.find(f"{HH}paraPr[@id='30']") is None:
            base_pp = pp_list.find(f"{HH}paraPr[@id='0']")
            center_pp = deepcopy(base_pp)
            center_pp.set("id", "30")
            align_el = center_pp.find(f"{HH}align")
            if align_el is not None:
                align_el.set("horizontal", "CENTER")
            pp_list.append(center_pp)
            pp_list.set("itemCnt", str(len(list(pp_list))))

        # 2. 글자 서식 정의 (id="50"~"58")
        style_defs = {
            "50": {"height": 1800, "color": "#1F4E79", "bold": True},   # 메인 타이틀 (18pt 네이비 볼드)
            "51": {"height": 950,  "color": "#595959", "bold": False},  # 문서 메타 정보 (9.5pt 그레이)
            "52": {"height": 1400, "color": "#2E74B5", "bold": True},   # 대제목 H1 (14pt 블루 볼드)
            "53": {"height": 1200, "color": "#1F3864", "bold": True},   # 중제목 H2 (12pt 다크슬레이트 볼드)
            "54": {"height": 1050, "color": "#262626", "bold": True},   # 소제목 H3 (10.5pt 볼드)
            "55": {"height": 1000, "color": "#000000", "bold": False},  # 본문 기본 (10pt 일반)
            "56": {"height": 1000, "color": "#1F3864", "bold": True},   # 불릿 레이블 볼드 (10pt)
            "57": {"height": 950,  "color": "#1F4E79", "bold": True},   # 표 헤더 (9.5pt 네이비 볼드)
            "58": {"height": 900,  "color": "#333333", "bold": False},  # 표 데이터 (9pt 일반)
        }

        cp_list = self.header.element.find(f".//{HH}charProperties")
        base_cp = cp_list.find(f"{HH}charPr[@id='0']") if cp_list is not None else None

        if cp_list is not None and base_cp is not None:
            for cid, sdef in style_defs.items():
                if cp_list.find(f"{HH}charPr[@id='{cid}']") is None:
                    new_cp = deepcopy(base_cp)
                    new_cp.set("id", cid)
                    new_cp.set("height", str(sdef["height"]))
                    new_cp.set("textColor", sdef["color"])
                    if sdef["bold"]:
                        if new_cp.find(f"{HH}bold") is None:
                            ET.SubElement(new_cp, f"{HH}bold")
                    else:
                        b_el = new_cp.find(f"{HH}bold")
                        if b_el is not None:
                            new_cp.remove(b_el)
                    cp_list.append(new_cp)
            cp_list.set("itemCnt", str(len(list(cp_list))))

        # 3. 표 헤더 전용 음영 테두리/배경 (id="4": #EDF2F8 배경색)
        bf_list = self.header.element.find(f".//{HH}borderFills")
        basic_id = self.doc.oxml.ensure_basic_border_fill()
        basic_bf = self.header.element.find(f".//{HH}borderFill[@id='{basic_id}']")
        if bf_list is not None and basic_bf is not None:
            if bf_list.find(f"{HH}borderFill[@id='4']") is None:
                header_bf = deepcopy(basic_bf)
                header_bf.set("id", "4")
                fill_brush = ET.SubElement(header_bf, f"{HC}fillBrush")
                ET.SubElement(fill_brush, f"{HC}winBrush", {
                    "faceColor": "#EDF2F8",
                    "hatchColor": "#999999",
                    "alpha": "0"
                })
                bf_list.append(header_bf)
                bf_list.set("itemCnt", str(len(list(bf_list))))

        self.header.mark_dirty()
        self.doc.oxml.invalidate_char_property_cache()

    def _strip_markdown_inline(self, text: str) -> str:
        """볼드, 이탤릭 등 마크다운 인라인 태그 제거"""
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"`(.*?)`", r"\1", text)
        return text.strip()

    def parse_markdown(self, md_content: str):
        """마크다운 텍스트를 구조화된 블록 리스트로 분해"""
        lines = md_content.splitlines()
        blocks = []
        i = 0
        n = len(lines)

        while i < n:
            line = lines[i].strip()

            # 빈 줄
            if not line:
                i += 1
                continue

            # 구분선
            if line in ("---", "***", "___"):
                blocks.append({"type": "hr"})
                i += 1
                continue

            # 테이블 감지
            if line.startswith("|") and line.endswith("|"):
                table_lines = []
                while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                    table_lines.append(lines[i].strip())
                    i += 1
                
                # 테이블 파싱
                parsed_table = self._parse_table_block(table_lines)
                if parsed_table:
                    blocks.append({"type": "table", "data": parsed_table})
                continue

            # 제목(Heading)
            if line.startswith("#"):
                m = re.match(r"^(#{1,6})\s+(.*)$", line)
                if m:
                    level = len(m.group(1))
                    text = m.group(2).strip()
                    blocks.append({"type": "heading", "level": level, "text": text})
                    i += 1
                    continue

            # 메타데이터/리스트
            if line.startswith("- ") or line.startswith("* "):
                content = line[2:].strip()
                # 불릿 레이블 분리 (- **레이블**: 내용)
                bullet_match = re.match(r"^\*\*(.*?)\*\*:\s*(.*)$", content)
                if bullet_match:
                    blocks.append({
                        "type": "bullet_label",
                        "label": bullet_match.group(1).strip(),
                        "content": bullet_match.group(2).strip()
                    })
                else:
                    blocks.append({"type": "bullet", "text": self._strip_markdown_inline(content)})
                i += 1
                continue

            # 일반 본문 문단
            blocks.append({"type": "paragraph", "text": self._strip_markdown_inline(line)})
            i += 1

        return blocks

    def _parse_table_block(self, table_lines):
        """마크다운 테이블 라인들을 2차원 셀 배열로 변환"""
        if len(table_lines) < 2:
            return None

        rows = []
        for line in table_lines:
            # 앞뒤 | 제거 후 분할
            raw_cells = line.strip()[1:-1].split("|")
            cells = [self._strip_markdown_inline(c.strip()) for c in raw_cells]
            
            # 구분선 행 제외 (| :--- | :--- | 등)
            if all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cells if c):
                continue
            rows.append(cells)

        return rows if len(rows) >= 2 else None

    def render_blocks(self, blocks):
        """구조화된 블록들을 HWPX 문서로 렌더링"""
        # 첫 번째 기본 문단 제거 (빈 뼈대 청소)
        if len(self.doc.sections) > 0 and len(self.doc.sections[0].paragraphs) > 0:
            first_p = self.doc.sections[0].paragraphs[0]
            if not first_p.text:
                self.doc.sections[0].element.remove(first_p.element)
                self.doc.sections[0].mark_dirty()

        for block in blocks:
            btype = block["type"]

            if btype == "heading":
                level = block["level"]
                text = block["text"]
                if level == 1:
                    # 메인 문서 타이틀
                    self.doc.add_paragraph(text, char_pr_id_ref="50", para_pr_id_ref="30")
                    self.doc.add_paragraph("", char_pr_id_ref="55")  # 간격용 빈줄
                elif level == 2:
                    # 대제목 (Ⅰ, Ⅱ 등)
                    self.doc.add_paragraph("", char_pr_id_ref="55")  # 상단 여백
                    self.doc.add_paragraph(text, char_pr_id_ref="52", para_pr_id_ref="0")
                elif level == 3:
                    # 중제목 (1., 2. 등)
                    self.doc.add_paragraph(text, char_pr_id_ref="53", para_pr_id_ref="0")
                else:
                    # 소제목
                    self.doc.add_paragraph(text, char_pr_id_ref="54", para_pr_id_ref="0")

            elif btype == "bullet_label":
                label = block["label"]
                content = block["content"]
                # 단일 문단에 레이블(볼드)과 본문(일반) 결합
                p = self.doc.add_paragraph(f"  • {label}: {content}", char_pr_id_ref="55")

            elif btype == "bullet":
                text = block["text"]
                self.doc.add_paragraph(f"  - {text}", char_pr_id_ref="55")

            elif btype == "hr":
                # 구분선 대신 깔끔한 단락 구분 빈줄 삽입
                self.doc.add_paragraph("", char_pr_id_ref="55")

            elif btype == "paragraph":
                text = block["text"]
                # 메타데이터 감지
                if text.startswith("발행일자:") or text.startswith("작성부서:") or text.startswith("보고대상:") or text.startswith("문서등급:"):
                    self.doc.add_paragraph(f"  {text}", char_pr_id_ref="51")
                else:
                    self.doc.add_paragraph(text, char_pr_id_ref="55")

            elif btype == "table":
                rows = block["data"]
                self._render_table(rows)

    def _render_table(self, rows):
        """HWPX 고정밀 네이티브 테이블 렌더링"""
        num_rows = len(rows)
        num_cols = max(len(r) for r in rows)

        # A4 기준 본문 인쇄 너비 (약 15,500 hwpUnits)
        total_width = 15500
        # 컬럼 가중치 계산 (컬럼별 평균 텍스트 길이에 기반)
        col_lens = [0] * num_cols
        for r in rows:
            for c_idx in range(num_cols):
                cell_text = r[c_idx] if c_idx < len(r) else ""
                col_lens[c_idx] = max(col_lens[c_idx], len(cell_text.encode("utf-8")))

        sum_lens = sum(col_lens) or num_cols
        col_widths = [max(int(total_width * (l / sum_lens)), 1200) for l in col_lens]
        # 전체 합 보정
        diff = total_width - sum(col_widths)
        col_widths[-1] += diff

        # 테이블 생성
        tbl = self.doc.add_table(
            num_rows,
            num_cols,
            width=total_width,
            height=num_rows * 1200,
            border_fill_id_ref="3"
        )

        for r_idx, r in enumerate(rows):
            is_header = (r_idx == 0)
            for c_idx in range(num_cols):
                cell_text = r[c_idx] if c_idx < len(r) else ""
                cell = tbl.cell(r_idx, c_idx)
                
                # 너비 지정
                cell.set_size(width=col_widths[c_idx])
                cell.text = cell_text

                # 헤더 셀 스타일 적용 (배경 음영 borderFill id="4", 볼드 글씨 charPr id="57")
                tc_el = cell.element
                if is_header:
                    tc_el.set("borderFillIDRef", "4")
                    run_el = tc_el.find(f".//{HP}run")
                    if run_el is not None:
                        run_el.set("charPrIDRef", "57")
                    p_el = tc_el.find(f".//{HP}p")
                    if p_el is not None:
                        p_el.set("paraPrIDRef", "30")  # 가운데 정렬
                else:
                    # 데이터 셀 스타일
                    run_el = tc_el.find(f".//{HP}run")
                    if run_el is not None:
                        run_el.set("charPrIDRef", "58")
                    p_el = tc_el.find(f".//{HP}p")
                    if p_el is not None:
                        # 첫 번째(번호) 열은 가운데 정렬
                        if c_idx == 0 or len(cell_text) <= 4:
                            p_el.set("paraPrIDRef", "30")

        # 표 뒤 간격 문단
        self.doc.add_paragraph("", char_pr_id_ref="55")

    def convert_file(self, md_path: str, hwpx_output_path: str):
        """마크다운 파일을 읽어 .hwpx 파일로 컴파일 및 저장"""
        md_file = Path(md_path)
        if not md_file.exists():
            raise FileNotFoundError(f"마크다운 입력 파일을 찾을 수 없습니다: {md_path}")

        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        print(f"[*] 마크다운 문서 파싱 시작: {md_file.name}")
        blocks = self.parse_markdown(md_content)
        print(f"[*] 총 {len(blocks)}개 구조 블록 추출 완료")

        print(f"[*] HWPX 문서 렌더링 중...")
        self.render_blocks(blocks)

        out_path = Path(hwpx_output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(out_path)
        print(f"[OK] HWPX 보고서 생성 성공: {out_path.resolve()} (크기: {out_path.stat().st_size:,} bytes)")
        return out_path


def main():
    parser = argparse.ArgumentParser(description="마크다운 문서를 HWPX로 전환하는 전문 변환기")
    parser.add_argument("input_md", nargs="?", default=None, help="입력 마크다운 파일 경로")
    parser.add_argument("-o", "--output", default=None, help="출력 HWPX 파일 경로")

    args = parser.parse_args()

    default_base = r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)"
    input_md = args.input_md or os.path.join(default_base, "result", "[002]_20261008_인터넷주요뉴스_AI관련_10대동향_심층분석보고서.md")
    output_hwpx = args.output or os.path.join(default_base, "result", "[004]_20261008_인터넷주요뉴스_AI관련_10대동향_심층분석보고서.hwpx")

    converter = MarkdownToHwpxConverter()
    converter.convert_file(input_md, output_hwpx)


if __name__ == "__main__":
    main()
