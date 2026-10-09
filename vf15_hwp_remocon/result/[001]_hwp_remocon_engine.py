"""
[001]_hwp_remocon_engine.py - 한글(HWP) 원격 제어 & 자동화 마스터 엔진
작성자: AX-TWIN 전술 부대 (대장장이 & 프로그래머)
용도: 한컴오피스 COM API 및 pyhwpx를 이용한 헤드리스 서식 자동 채우기 및 PDF 컴파일
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional

try:
    from pyhwpx import Hwp
except ImportError:
    print("[경고] pyhwpx 모듈이 설치되어 있지 않습니다. pip install pyhwpx 필요")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("[경고] PyMuPDF 모듈이 설치되어 있지 않습니다. pip install pymupdf 필요")


class HwpRemoconEngine:
    def __init__(self, visible: bool = False):
        self.visible = visible
        self.hwp: Optional[Hwp] = None

    def start(self):
        """한글 백그라운드 프로세스 기동 및 보안 승인 모듈 등록"""
        print("[엔진] 한글 프로세스 기동 중 (visible={})...".format(self.visible))
        self.hwp = Hwp(visible=self.visible)
        # 보안 승인 등록
        try:
            self.hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        except Exception as e:
            print("[엔진] RegisterModule 안내:", e)

    def close(self):
        """한글 프로세스 안전 종료"""
        if self.hwp:
            try:
                self.hwp.quit()
                print("[엔진] 한글 프로세스 정상 종료 완료.")
            except Exception as e:
                print("[엔진] 프로세스 종료 오류:", e)
            self.hwp = None

    def fill_form(
        self,
        template_path: str,
        output_hwp: str,
        output_pdf: str,
        cell_mapping: Dict[str, str],
        checkboxes: Optional[Dict[str, str]] = None,
        date_str: Optional[str] = None
    ) -> bool:
        """
        양식 파일(.hwp)을 열어 셀 매핑, 체크박스 치환, 서명 일자 수정을 수행하고
        HWP 및 PDF로 저장합니다.
        """
        if not self.hwp:
            self.start()

        abs_template = os.path.abspath(template_path)
        print(f"[엔진] 서식 문서 오픈: {abs_template}")
        self.hwp.open(abs_template)

        # 1. 셀 주소 기반 외과수술적 텍스트 주입
        # 표의 시작점 확보를 위해 첫번째 표/제목 탐색
        self.hwp.MoveDocBegin()
        self.hwp.find("참  가  신  청  서", direction="AllDoc")

        for addr, val in cell_mapping.items():
            try:
                ok = self.hwp.goto_addr(addr)
                if ok:
                    self.hwp.HAction.Run("SelectAll")
                    self.hwp.HAction.Run("Delete")
                    if val:
                        self.hwp.insert_text(val)
                    self.hwp.HAction.Run("ParagraphShapeAlignCenter")
                    print(f"  └─ 셀 [{addr}] 주입 성공: {val!r}")
                else:
                    print(f"  └─ [주의] 셀 [{addr}] 이동 실패")
            except Exception as e:
                print(f"  └─ [에러] 셀 [{addr}] 처리 중 오류: {e}")

        # 2. 체크박스 치환
        if checkboxes:
            for src_box, dst_box in checkboxes.items():
                self.hwp.MoveDocBegin()
                if self.hwp.find(src_box, direction="AllDoc"):
                    self.hwp.insert_text(dst_box)
                    print(f"  └─ 체크박스 치환 성공: {src_box!r} -> {dst_box!r}")

        # 3. 서명 일자 치환
        if date_str:
            self.hwp.MoveDocEnd()
            if self.hwp.find("2026", direction="Backward"):
                self.hwp.MoveLineBegin()
                self.hwp.MoveSelLineEnd()
                self.hwp.insert_text(date_str)
                self.hwp.HAction.Run("ParagraphShapeAlignCenter")
                print(f"  └─ 서명 일자 치환 성공: {date_str!r}")

        # 4. 파일 저장 (HWP 및 PDF)
        abs_hwp = os.path.abspath(output_hwp)
        abs_pdf = os.path.abspath(output_pdf)
        os.makedirs(os.path.dirname(abs_hwp), exist_ok=True)

        self.hwp.save_as(abs_hwp)
        print(f"[엔진] 완제 HWP 저장 완료: {abs_hwp} (크기: {os.path.getsize(abs_hwp):,} bytes)")

        self.hwp.save_as(abs_pdf, "PDF")
        print(f"[엔진] 완제 PDF 컴파일 완료: {abs_pdf} (크기: {os.path.getsize(abs_pdf):,} bytes)")

        return True

    @staticmethod
    def render_pdf_to_image(pdf_path: str, output_png: str, dpi: int = 200) -> bool:
        """PyMuPDF(fitz)를 이용한 검증용 이미지 렌더링"""
        try:
            doc = fitz.open(pdf_path)
            if len(doc) == 0:
                return False
            page = doc[0]
            pix = page.get_pixmap(dpi=dpi)
            pix.save(output_png)
            print(f"[VisionCheck] 고해상도 검증 이미지 생성: {output_png} (해상도: {pix.width}x{pix.height})")
            return True
        except Exception as e:
            print(f"[VisionCheck] 렌더링 실패: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="HWP 원격 제어 자동화 엔진")
    parser.add_argument("--template", required=True, help="원천 서식 HWP 경로")
    parser.add_argument("--out-hwp", required=True, help="출력 HWP 파일 경로")
    parser.add_argument("--out-pdf", required=True, help="출력 PDF 파일 경로")
    parser.add_argument("--out-png", default="", help="검증용 PNG 이미지 경로 (선택)")
    parser.add_argument("--company", default="(AX)창업기술", help="회사명")
    parser.add_argument("--tel", default="010-5060-8345", help="대표 전화번호")
    parser.add_argument("--fax", default="-", help="팩스번호")
    parser.add_argument("--email", default="ceo@ax-startup.com", help="대표 이메일")
    parser.add_argument("--name", default="이한규", help="참가자 성명")
    parser.add_argument("--title", default="대표", help="참가자 부서/직위")
    parser.add_argument("--phone", default="010-5060-8345", help="참가자 휴대전화")
    parser.add_argument("--p-email", default="ceo@ax-startup.com", help="참가자 이메일")
    parser.add_argument("--date", default="2026. 10. 10.", help="신청 일자")

    args = parser.parse_args()

    engine = HwpRemoconEngine(visible=False)
    try:
        cell_mapping = {
            "B2": args.company,
            "B3": args.tel,
            "D3": args.fax,
            "B4": args.email,
            "A6": args.name,
            "B6": args.title,
            "C6": args.phone,
            "D6": getattr(args, "p_email", args.email),
            "B7": "",
            "B8": ""
        }
        checkboxes = {
            "□ 예": "■ 예"
        }
        engine.fill_form(
            template_path=args.template,
            output_hwp=args.out_hwp,
            output_pdf=args.out_pdf,
            cell_mapping=cell_mapping,
            checkboxes=checkboxes,
            date_str=args.date
        )

        if args.out_png:
            engine.render_pdf_to_image(args.out_pdf, args.out_png, dpi=200)

    finally:
        engine.close()


if __name__ == "__main__":
    main()
