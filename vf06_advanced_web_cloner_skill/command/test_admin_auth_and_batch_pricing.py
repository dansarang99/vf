# command/test_admin_auth_and_batch_pricing.py
# Captures ONLY NEWLY ADDED FEATURES for vf06 with [001]~ sequential numbering

import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8080"
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../result"))
os.makedirs(RESULT_DIR, exist_ok=True)

def run_tests():
    print("[INFO] Capturing ONLY NEWLY ADDED FEATURES for vf06...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Capture Login Modal (admin / 1234567)
        page.goto(f"{BASE_URL}/admin/index.html", wait_until="networkidle")
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(600)
        
        # [001]
        p1 = os.path.join(RESULT_DIR, "[001]_admin_auth_login_admin_1234567.png")
        page.screenshot(path=p1)
        print(f"  - Saved [001]: {p1}")

        # Login
        page.fill("#loginId", "admin")
        page.fill("#loginPassword", "1234567")
        page.click("#btnLogin")
        page.wait_for_timeout(800)

        # [002] Dashboard KPI
        p2 = os.path.join(RESULT_DIR, "[002]_admin_dashboard_kpi_overview.png")
        page.screenshot(path=p2)
        print(f"  - Saved [002]: {p2}")

        # [003] Batch Price Multiplier Modal with 10,000 KRW unit
        page.click("#btnOpenBatchPrice")
        page.wait_for_timeout(500)
        page.click('.preset-btn[data-val="1.10"]')
        page.wait_for_timeout(500)
        p3 = os.path.join(RESULT_DIR, "[003]_admin_batch_price_weight_modal.png")
        page.screenshot(path=p3)
        print(f"  - Saved [003]: {p3}")

        # [004] Apply Batch Price & Verify 10,000 KRW Unit Policy
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("#btnApplyBatchPrice")
        page.wait_for_timeout(1500)
        p4 = os.path.join(RESULT_DIR, "[004]_admin_batch_price_applied_10000krw.png")
        page.screenshot(path=p4)
        print(f"  - Saved [004]: {p4}")

        # [005] Artwork Studio Precision Price Edit
        p5 = os.path.join(RESULT_DIR, "[005]_admin_artwork_studio_price_edit.png")
        page.screenshot(path=p5)
        print(f"  - Saved [005]: {p5}")

        # [006] Inquiry Ledger Tab
        page.click('button[data-tab="tabInquiries"]')
        page.wait_for_timeout(500)
        p6 = os.path.join(RESULT_DIR, "[006]_admin_inquiry_ledger_realtime.png")
        page.screenshot(path=p6)
        print(f"  - Saved [006]: {p6}")

        # [007] Supabase Cloud Settings Tab
        page.click('button[data-tab="tabSettings"]')
        page.wait_for_timeout(500)
        p7 = os.path.join(RESULT_DIR, "[007]_admin_supabase_cloud_settings.png")
        page.screenshot(path=p7)
        print(f"  - Saved [007]: {p7}")

        # [008] Main with Admin CMS Entry Link
        main_page = context.new_page()
        main_page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        main_page.wait_for_timeout(600)
        p8 = os.path.join(RESULT_DIR, "[008]_main_with_admin_cms_entry.png")
        main_page.screenshot(path=p8)
        print(f"  - Saved [008]: {p8}")

        # [009] Artwork Inquiry Form Modal on Main
        first_art_img = main_page.query_selector("#artworks-grid li .img")
        if first_art_img:
            first_art_img.click()
            main_page.wait_for_timeout(500)
            modal_buy_btn = main_page.query_selector("#modal-btn-buy")
            if modal_buy_btn:
                modal_buy_btn.click()
                main_page.wait_for_timeout(500)
                main_page.fill("#inq-name", "김컬렉터")
                main_page.fill("#inq-phone", "010-8888-9999")
                main_page.fill("#inq-email", "vip.collector@artgallery.com")
                main_page.fill("#inq-message", "Moments 26-001 원작 실물 프라이빗 뷰잉룸 예약을 신청합니다.")
                p9 = os.path.join(RESULT_DIR, "[009]_artwork_inquiry_modal_form.png")
                main_page.screenshot(path=p9)
                print(f"  - Saved [009]: {p9}")

        browser.close()
        print("[SUCCESS] All 9 new feature screenshots generated successfully!")

if __name__ == "__main__":
    run_tests()
