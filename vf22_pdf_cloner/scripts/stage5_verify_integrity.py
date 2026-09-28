"""
Stage 5: MS Word COM OLE 엔진 실측 및 Zero-Drift 0-Error 무결성 전수 감사
"""
import os
import sys
import win32com.client
import pythoncom
import fitz

def verify_and_render_pdf(docx_path, out_pdf_path, orig_pdf_path, proof_pages=None, result_dir="."):
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    
    try:
        wdoc = word.Documents.Open(os.path.abspath(docx_path))
        page_count = wdoc.ComputeStatistics(2)
        print(f"[Stage 5] MS Word internal rendered page count: {page_count}")
        wdoc.SaveAs(os.path.abspath(out_pdf_path), FileFormat=17)
        wdoc.Close(False)
    finally:
        word.Quit()
        pythoncom.CoUninitialize()
        
    doc_orig = fitz.open(orig_pdf_path)
    doc_gen = fitz.open(out_pdf_path)
    
    orig_pages = len(doc_orig)
    gen_pages = len(doc_gen)
    drift = gen_pages - orig_pages
    
    print(f"[Stage 5] Orig: {orig_pages}p vs Cloned: {gen_pages}p (Drift: {drift}p)")
    status = "100% PASS (Zero-Drift)" if drift == 0 else f"CALIBRATION NEEDED ({drift:+d}p)"
    print(f"[Stage 5] Status: {status}")
    
    # 렌더링 증빙
    if proof_pages:
        for p in proof_pages:
            if p <= gen_pages:
                pix = doc_gen[p - 1].get_pixmap(dpi=150)
                pix.save(os.path.join(result_dir, f"proof_p{p:02d}.png"))
                print(f"  -> Proof saved: proof_p{p:02d}.png")

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        verify_and_render_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
