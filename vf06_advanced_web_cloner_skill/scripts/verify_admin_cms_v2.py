import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ADMIN_URL = "https://src-topaz-nu.vercel.app/admin"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})

    print(f"[1] Navigating to Admin CMS: {ADMIN_URL}...")
    page.goto(ADMIN_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # 1. Login with Fast-Pass
    print("[2] Triggering Fast-Pass Admin Login...")
    fast_pass_btn = page.locator("#btnFastPassLogin")
    if fast_pass_btn.is_visible():
        fast_pass_btn.click()
    else:
        page.fill("#loginId", "admin")
        page.fill("#loginPassword", "1234567")
        page.click("#btnLogin")
    
    time.sleep(1.5)

    # 2. Verify Tab 1: Artworks Table & KPIs
    art_count = page.locator("#kpiTotalWorks").text_content()
    sales_val = page.locator("#kpiTotalSales").text_content()
    print(f"[3] Dashboard loaded: Total Works={art_count}, Total Sales={sales_val}")
    assert int(art_count) >= 42, f"Expected 42 works, got {art_count}"

    art_rows = page.locator("#artworkTableBody tr")
    print(f"[4] Artworks rendered in table: {art_rows.count()}")
    assert art_rows.count() >= 20, "Artwork table rows missing!"
    page.screenshot(path="result/[047]_admin_cms_v2_dashboard_artworks.png")
    print("[5] Saved result/[047]_admin_cms_v2_dashboard_artworks.png")

    # 3. Tab 2: Orders & Purchases Ledger + Certificate
    print("[6] Switching to Orders & Purchases Ledger...")
    page.click("button[data-tab='tabOrders']")
    time.sleep(1)
    
    view_order_btn = page.locator(".btn-view-order").first
    if view_order_btn.is_visible():
        print("[7] Opening Official Certificate & Invoice Modal...")
        view_order_btn.click()
        time.sleep(0.8)
        assert page.locator("#orderDetailModal").is_visible()
        page.screenshot(path="result/[048]_admin_cms_v2_order_certificate_modal.png")
        print("[8] Saved result/[048]_admin_cms_v2_order_certificate_modal.png")
        page.click("#btnCloseOrderDetail")
        time.sleep(0.5)

    # 4. Tab 3: Collectors Ledger + History Modal
    print("[9] Switching to Collectors Ledger...")
    page.click("button[data-tab='tabUsers']")
    time.sleep(1)
    history_btn = page.locator(".btn-user-history").first
    if history_btn.is_visible():
        print("[10] Opening Collector History Modal...")
        history_btn.click()
        time.sleep(0.8)
        assert page.locator("#userHistoryModal").is_visible()
        page.screenshot(path="result/[049]_admin_cms_v2_collector_history_modal.png")
        print("[11] Saved result/[049]_admin_cms_v2_collector_history_modal.png")
        page.click("#btnCloseUserHistory")
        time.sleep(0.5)

    # 5. Tab 5: Statement Live Typography Split View
    print("[12] Switching to Statement & Exhibition Split View...")
    page.click("button[data-tab='tabStatement']")
    time.sleep(1)
    assert page.locator("#statementLivePreview").is_visible()
    page.screenshot(path="result/[050]_admin_cms_v2_statement_split_preview.png")
    print("[13] Saved result/[050]_admin_cms_v2_statement_split_preview.png")

    # 6. Tab 6: Settings, Backup & Restore
    print("[14] Switching to Firebase & Database Settings...")
    page.click("button[data-tab='tabSettings']")
    time.sleep(1)
    page.screenshot(path="result/[051]_admin_cms_v2_backup_restore_suite.png")
    print("[15] Saved result/[051]_admin_cms_v2_backup_restore_suite.png")

    browser.close()
    print("\n[SUCCESS] Enterprise Admin CMS Studio v2.0 verification PASSED!")
