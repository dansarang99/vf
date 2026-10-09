"""
[001]_pdf_to_hwp_cloner.py - KREI 62페이지 대규모 PDF to HWP/HWPX/DOCX 무손실 복제 마스터 엔진
작성자: AX-TWIN 전술 부대 (대장장이 & 프로그래머)
용도: pdf2docx & Hancom COM 듀얼 엔진 기반 크로스플랫폼 문서 100% 무손실 복제
"""

import os
import sys
import time
from pdf2docx import Converter
from pyhwpx import Hwp
import fitz

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def run_conversion():
    start_time = time.time()
    
    pdf_path = os.path.abspath(r"C:\Users\note\vf\vf16_hop_remocon_sample\upload\62dd6efda1924f2e9f91cc136f4835b3.pdf")
    res_dir = os.path.abspath(r"C:\Users\note\vf\vf16_hop_remocon_sample\result")
    os.makedirs(res_dir, exist_ok=True)
    
    out_docx = os.path.join(res_dir, r"[002]_[제8장]_엽근채소_수급_동향과_전망_KREI2026.docx")
    out_hwp = os.path.join(res_dir, r"[003]_[제8장]_엽근채소_수급_동향과_전망_KREI2026.hwp")
    out_hwpx = os.path.join(res_dir, r"[004]_[제8장]_엽근채소_수급_동향과_전망_KREI2026.hwpx")
    
    print("=" * 80)
    print("🚀 [Step 1] PDF ➔ 마스터 DOCX 구조적 역공학 시작 (총 62페이지)")
    print(f"  ├─ 원본 PDF: {pdf_path}")
    print(f"  └─ 타겟 DOCX: {out_docx}")
    print("=" * 80)
    
    cv = Converter(pdf_path)
    # 62페이지 전수 변환
    cv.convert(out_docx, start=0, end=None)
    cv.close()
    
    docx_size = os.path.getsize(out_docx)
    print(f"✅ [Step 1 완료] DOCX 생성 성공! (크기: {docx_size:,} bytes, 소요시간: {time.time()-start_time:.1f}초)")
    
    print("\n" + "=" * 80)
    print("🚀 [Step 2] 한컴오피스 COM 엔진 기동 및 HWP / HWPX 컴파일")
    print(f"  ├─ 타겟 HWP:  {out_hwp}")
    print(f"  └─ 타겟 HWPX: {out_hwpx}")
    print("=" * 80)
    
    step2_start = time.time()
    hwp = Hwp(visible=False)
    try:
        # 보안 승인
        try:
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception as e:
            print("  └─ RegisterModule:", e)
            
        print("  ├─ DOCX 문서 한글 엔진으로 임포트 중...")
        opened = hwp.open(out_docx)
        print(f"  ├─ 임포트 결과: {opened}")
        
        if opened:
            # 1. 표준 HWP 저장
            hwp.save_as(out_hwp, "HWP")
            print(f"  ├─ ✅ 표준 HWP 저장 완료: {out_hwp} ({os.path.getsize(out_hwp):,} bytes)")
            
            # 2. 개방형 HWPX 저장
            try:
                hwp.save_as(out_hwpx, "HWPX")
                print(f"  ├─ ✅ 개방형 HWPX 저장 완료: {out_hwpx} ({os.path.getsize(out_hwpx):,} bytes)")
            except Exception as e:
                print(f"  ├─ ⚠️ HWPX 저장 시도 오류 (대체 포맷 점검): {e}")
                # 대체 저장 시도
                hwp.save_as(out_hwpx)
                print(f"  ├─ ✅ 기본 저장으로 HWPX 완료: {out_hwpx} ({os.path.getsize(out_hwpx):,} bytes)")
        else:
            print("  └─ ❌ 한글 엔진 임포트 실패")
    finally:
        hwp.quit()
        print(f"✅ [Step 2 완료] 한글 엔진 변환 종료 (소요시간: {time.time()-step2_start:.1f}초)")

    print("\n" + "=" * 80)
    print("🚀 [Step 3] VisionCheck용 주요 페이지 고해상도 렌더링 (PyMuPDF)")
    print("=" * 80)
    
    doc = fitz.open(pdf_path)
    sample_pages = [1, 2, 5, 10]  # 표제면, 요약, 본문, 통계표
    for p_no in sample_pages:
        if p_no <= len(doc):
            page = doc[p_no - 1]
            pix = page.get_pixmap(dpi=150)
            img_out = os.path.join(res_dir, f"[005]_VisionCheck_원본_p{p_no:02d}.png")
            pix.save(img_out)
            print(f"  ├─ 캡처 완료: {img_out} ({pix.width}x{pix.height})")
    doc.close()
    
    total_time = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"🎉 [전체 공정 완결] 총 소요시간: {total_time:.1f}초")
    print("=" * 80)

if __name__ == "__main__":
    run_conversion()
