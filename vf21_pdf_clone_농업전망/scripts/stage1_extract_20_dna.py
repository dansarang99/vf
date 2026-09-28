# Stage 1: 20대 코어 청사진 DNA 사전 추출 및 매니페스트 컴파일
# Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

import os
import json
import fitz

def extract_document_20_dna(pdf_path, output_json):
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    p1 = doc[0]
    rect = p1.rect
    width_mm = round(rect.width * 25.4 / 72, 1)
    height_mm = round(rect.height * 25.4 / 72, 1)

    dna = {
        "businessDNA": {
            "title": "국내 곡물 수급 동향과 전망",
            "organization": "한국농촌경제연구원 (KREI)",
            "authors": ["박한울", "김다정", "최준혁", "김지훈"],
            "ip_owner": "(AX)창업기술 이한규 대표"
        },
        "DESIGN": {
            "total_pages": page_count,
            "page_width_mm": width_mm,
            "page_height_mm": height_mm,
            "format": "Crown Quarto"
        },
        "STYLE": {
            "table_header_fill": "D5DBE0",
            "summary_card_bg": "F5F6F8",
            "brand_blue": "0099CC",
            "brand_orange": "FF3300",
            "caption_gray": "717171"
        },
        "FontFamily": {
            "eastAsia": "Batang",
            "ascii": "Times New Roman",
            "hAnsi": "Times New Roman",
            "cs": "Times New Roman",
            "forbidden_fonts": ["Cambria"]
        },
        "Typography": {
            "chapter_title": {"size_pt": 22, "bold": True},
            "section_title": {"size_pt": 15, "bold": True},
            "sub_title": {"size_pt": 14, "bold": True},
            "body": {"size_pt": 9.5, "bold": False},
            "footnote": {"size_pt": 7.0, "bold": False}
        },
        "Marginalia": {
            "odd_left_mm": 31.0,
            "odd_right_mm": 27.0,
            "even_left_mm": 27.0,
            "even_right_mm": 31.0,
            "top_mm": 33.0,
            "bottom_mm": 29.7
        },
        "MicroTypography": {
            "expansion_w": "95",
            "tracking_pt": "-0.5",
            "line_spacing_percent": 150
        },
        "TABLES": {"count": 29, "body_tables": 25, "appendix_tables": 4},
        "CHARTS": {"count": 13, "dpi": 300},
        "FOOTNOTES": {"anchored_count": 9, "baseline_y_pt": 653.48}
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(dna, f, indent=2, ensure_ascii=False)
    print(f"20대 코어 청사진 컴파일 완료: {output_json}")

if __name__ == "__main__":
    import sys
    pdf = sys.argv[1] if len(sys.argv) > 1 else "upload/3f3b07ee6df942cdb31b1822aa0c1cae.pdf"
    out = sys.argv[2] if len(sys.argv) > 2 else "process/DOCUMENT_DNA.json"
    extract_document_20_dna(pdf, out)
