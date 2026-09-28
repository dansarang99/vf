# Stage 2: 6대 대형 표제면 300 DPI 무손실 배너 클리핑 추출
# Copyright (c) (AX)창업기술 이한규 대표. All Rights Reserved.

import os
import fitz

def extract_section_banners(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    # 6대 표제면 좌표 정의 (페이지 번호는 0-indexed)
    banner_targets = [
        {"page": 2, "name": "sec1_full_header_p03.png", "clip": fitz.Rect(50, 70, 500, 140)},
        {"page": 14, "name": "sec2_full_header_p15.png", "clip": fitz.Rect(50, 70, 500, 140)},
        {"page": 25, "name": "sec3_full_header_p26.png", "clip": fitz.Rect(50, 70, 500, 140)},
        {"page": 33, "name": "app1_header_p34.png", "clip": fitz.Rect(50, 70, 500, 140)},
        {"page": 34, "name": "app2_header_p35.png", "clip": fitz.Rect(50, 70, 500, 140)},
        {"page": 36, "name": "app3_header_p37.png", "clip": fitz.Rect(50, 70, 500, 140)},
    ]

    for item in banner_targets:
        page = doc[item["page"]]
        pix = page.get_pixmap(dpi=300, clip=item["clip"])
        out_path = os.path.join(output_dir, item["name"])
        pix.save(out_path)
        print(f"300 DPI 배너 추출 완료: {out_path}")

if __name__ == "__main__":
    import sys
    pdf = sys.argv[1] if len(sys.argv) > 1 else "upload/3f3b07ee6df942cdb31b1822aa0c1cae.pdf"
    out = sys.argv[2] if len(sys.argv) > 2 else "process"
    extract_section_banners(pdf, out)
