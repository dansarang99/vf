import os
import fitz

BASE_DIR = r"C:\Users\note\vf\vf22_pdf_clone_농업전망(2)"
PDF_SRC = os.path.join(BASE_DIR, "upload", "62dd6efda1924f2e9f91cc136f4835b3.pdf")
PROCESS_DIR = os.path.join(BASE_DIR, "process")
doc = fitz.open(PDF_SRC)

# 배너 정의
# (페이지번호(1-indexed), 배너 이름, 클리핑 영역 rect: (x0, y0, x1, y1) in pt)
# 페이지 크기: 556.0 x 754.0 pt
banners = [
    (1, "sec0_header_p01.png", fitz.Rect(80, 100, 480, 270)), # 제8장 엽근채소 수급 동향과 전망 표제면
    (3, "sec1_header_p03.png", fitz.Rect(80, 100, 240, 270)), # 1 배추
    (16, "sec2_header_p16.png", fitz.Rect(70, 100, 230, 270)), # 2 무
    (30, "sec3_header_p30.png", fitz.Rect(70, 100, 230, 270)), # 3 당근
    (40, "sec4_header_p40.png", fitz.Rect(70, 100, 230, 270)), # 4 양배추
    (50, "app1_header_p50.png", fitz.Rect(70, 90, 480, 150)),  # 부록1 배추
    (53, "app2_header_p53.png", fitz.Rect(80, 90, 480, 150)),  # 부록2 무
    (56, "app3_header_p56.png", fitz.Rect(70, 90, 480, 150)),  # 부록3 당근
    (60, "app4_header_p60.png", fitz.Rect(70, 90, 480, 150)),  # 부록4 양배추
]

zoom = 300 / 72.0 # 300 DPI
mat = fitz.Matrix(zoom, zoom)

for pno, name, rect in banners:
    page = doc[pno - 1]
    pix = page.get_pixmap(matrix=mat, clip=rect)
    out_path = os.path.join(PROCESS_DIR, name)
    pix.save(out_path)
    print(f"Extracted banner {name} from Page {pno}: size {pix.width}x{pix.height}, saved to {out_path}")

print("All banners extracted at 300 DPI!")
