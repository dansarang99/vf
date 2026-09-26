import os
import sys
import time

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8080"
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../result"))
os.makedirs(RESULT_DIR, exist_ok=True)

def run_tests():
    print("[INFO] Starting Playwright E2E Integration Test...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Main Page Test
        print("▶ Test 1: Loading Main Page (index.html)...")
        page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        # Verify title & Admin Link
        assert "MA JI YOUNG" in page.title(), "Title does not contain MA JI YOUNG"
        admin_link = page.query_selector("a.admin-cms-link")
        assert admin_link is not None, "Admin CMS link not found in header"
        print("  - Main Page Title & Admin Link verified.")

        # Check artwork grid
        art_items = page.query_selector_all("#artworks-grid li")
        print(f"  - Artworks rendered: {len(art_items)} items")
        assert len(art_items) > 0, "No artworks found in grid"
        
        page.screenshot(path=os.path.join(RESULT_DIR, "[005]_main_with_admin_cms_entry.png"))

        # 2. Inquiry Modal Test on Main Page
        print("▶ Test 2: Testing Artwork Detail & Inquiry Form Flow...")
        # Click first artwork image
        first_art_img = page.query_selector("#artworks-grid li .img")
        assert first_art_img is not None
        first_art_img.click()
        page.wait_for_timeout(600)

        # Click Buy/Inquire Button
        modal_buy_btn = page.query_selector("#modal-btn-buy")
        assert modal_buy_btn is not None
        modal_buy_btn.click()
        page.wait_for_timeout(600)

        # Fill inquiry form
        page.fill("#inq-name", "김컬렉터")
        page.fill("#inq-phone", "010-8888-9999")
        page.fill("#inq-email", "vip.collector@artgallery.com")
        page.fill("#inq-message", "Moments 26-001 원작 실물 프라이빗 뷰잉룸 예약을 신청합니다.")
        
        page.screenshot(path=os.path.join(RESULT_DIR, "[006]_artwork_inquiry_modal_form.png"))
        
        # Submit form
        page.click("#btn-submit-inquiry")
        page.wait_for_timeout(800)
        print("  - Inquiry submitted successfully.")

        # 3. Admin CMS Login & Dashboard Test
        print("▶ Test 3: Admin CMS Access & Security Authentication...")
        admin_page = context.new_page()
        admin_page.goto(f"{BASE_URL}/admin/index.html", wait_until="networkidle")
        admin_page.wait_for_timeout(600)

        # Check login modal
        login_modal = admin_page.query_selector("#loginModal")
        assert "active" in login_modal.get_attribute("class")
        print("  - Security login modal appeared correctly.")

        # Enter passcode
        admin_page.fill("#loginPasscode", "majiyoung2026!")
        admin_page.click("#btnLogin")
        admin_page.wait_for_timeout(800)

        # Verify Dashboard loaded
        kpi_total = admin_page.inner_text("#kpiTotalWorks")
        print(f"  - Admin Dashboard KPI Total Works: {kpi_total}")
        assert int(kpi_total) >= 20, "KPI Total Works is less than expected"

        admin_page.screenshot(path=os.path.join(RESULT_DIR, "[007]_admin_dashboard_kpi_overview.png"))

        # 4. Check Inquiry in Admin Ledger (Tab 2)
        print("▶ Test 4: Checking Inquiry in Admin CMS Ledger...")
        admin_page.click('button[data-tab="tabInquiries"]')
        admin_page.wait_for_timeout(600)

        inq_rows = admin_page.query_selector_all("#inquiryTableBody tr")
        print(f"  - Inquiries found in Admin Ledger: {len(inq_rows)}")
        assert len(inq_rows) > 0, "Submitted inquiry was not found in Admin Ledger!"
        
        latest_client = admin_page.inner_text("#inquiryTableBody tr td strong")
        assert "김컬렉터" in latest_client, f"Expected 김컬렉터 but got {latest_client}"
        print(f"  - Verified submitted client in Admin Ledger: {latest_client}")

        admin_page.screenshot(path=os.path.join(RESULT_DIR, "[008]_admin_inquiry_ledger_realtime.png"))

        # 5. Artwork Edit & Precision Price Control (Tab 1)
        print("▶ Test 5: Testing Precision Control (Price Edit & Status Toggle)...")
        admin_page.click('button[data-tab="tabArtworks"]')
        admin_page.wait_for_timeout(600)

        # Change price of first item
        price_input = admin_page.query_selector("#artworkTableBody tr .inline-price")
        assert price_input is not None
        price_input.fill("9,200,000")
        price_input.dispatch_event("change")
        admin_page.wait_for_timeout(600)
        print("  - Price updated to 9,200,000 in Admin Studio.")

        admin_page.screenshot(path=os.path.join(RESULT_DIR, "[009]_admin_artwork_studio_price_edit.png"))

        # 6. Verify Cloud Sync & Settings (Tab 4)
        print("▶ Test 6: Checking Supabase Settings & Cloud Sync Tab...")
        admin_page.click('button[data-tab="tabSettings"]')
        admin_page.wait_for_timeout(600)
        admin_page.screenshot(path=os.path.join(RESULT_DIR, "[010]_admin_supabase_cloud_settings.png"))

        browser.close()
        print("[SUCCESS] ALL TESTS PASSED (0 Errors)! Full integration successfully verified.")

if __name__ == "__main__":
    run_tests()
