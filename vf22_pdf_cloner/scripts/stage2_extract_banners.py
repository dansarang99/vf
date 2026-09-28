"""
Stage 2: 챕터 표제면 및 부록 300 DPI 무손실 배너 추출 스크립트
"""
import os
import sys
import fitz

def extract_banners(pdf_path, output_dir, banner_defs):
    """
    banner_defs: list of tuple (page_no_1_indexed, filename, (x0, y0, x1, y1))
    """
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = 300 / 72.0
    mat = fitz.Matrix(zoom, zoom)
    
    for pno, name, (x0, y0, x1, y1) in banner_defs:
        page = doc[pno - 1]
        rect = fitz.Rect(x0, y0, x1, y1)
        pix = page.get_pixmap(matrix=mat, clip=rect)
        out_path = os.path.join(output_dir, name)
        pix.save(out_path)
        print(f"[Stage 2] Saved 300 DPI banner: {out_path} ({pix.width}x{pix.height})")

if __name__ == "__main__":
    print("Stage 2 banner extraction module ready.")
