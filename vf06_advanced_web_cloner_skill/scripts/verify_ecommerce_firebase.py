import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # ==========================================
    # STEP 1: Main Page Load & User Sign Up
    # ==========================================
    print("[1] Navigating to http://localhost:8080/index.html")
    page.goto("http://localhost:8080/index.html")
    page.wait_for_load_state("networkidle")
    # Clean slate for test reproducibility
    page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
    page.reload()
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    print("[2] Opening Sign Up Modal...")
    page.click("#btn-header-signup")
    time.sleep(0.5)

    print("[3] Filling Sign Up Form for '이한규 대표'...")
    page.fill("#signup-name", "이한규 대표")
    page.fill("#signup-email", "ceo@ax-startup.com")
    page.fill("#signup-password", "1234567")
    page.fill("#signup-phone", "010-9988-7766")
    page.fill("#signup-address", "전북특별자치도 전주시 덕진구 백제대로 567 갤러리빌딩 7층")
    page.select_option("#signup-tier", "vip")

    page.click("#btn-submit-signup")
    time.sleep(1)

    # Check header has user greeting
    greeting = page.locator("#btn-header-profile").text_content()
    print(f"[4] Header greeting after Sign Up: {greeting}")
    assert "이한규 대표" in greeting, "User greeting missing from header!"
    page.screenshot(path="result/[032]_collector_signup_success.png")
    print("[5] Saved signup screenshot to result/[032]_collector_signup_success.png")

    # ==========================================
    # STEP 2: Adding Artworks to Cart
    # ==========================================
    print("[6] Opening artwork detail modal and adding to cart...")
    # Scroll to artworks section
    page.evaluate("document.getElementById('artworks-section').scrollIntoView()")
    time.sleep(1)

    # Click first artwork card
    first_art = page.locator("#artworks-grid li .img").first
    first_art.click()
    time.sleep(0.8)

    # Click '장바구니 담기'
    page.click("#modal-btn-cart")
    time.sleep(0.5)

    # Click second artwork card
    second_art = page.locator("#artworks-grid li .img").nth(1)
    second_art.click()
    time.sleep(0.8)
    page.click("#modal-btn-cart")
    time.sleep(0.5)

    badge_count = page.locator("#cart-count-badge").text_content()
    print(f"[7] Cart Badge Count after adding 2 items: {badge_count}")
    assert int(badge_count) >= 2, f"Expected at least 2 items, got {badge_count}"

    # Open Cart Modal
    print("[8] Opening Cart Modal...")
    page.click("#btn-header-cart")
    time.sleep(1)

    cart_subtotal = page.locator("#cart-summary-subtotal").text_content()
    cart_total = page.locator("#cart-summary-total").text_content()
    print(f"[9] Cart Subtotal: {cart_subtotal}, Final Total: {cart_total}")
    page.screenshot(path="result/[033]_shopping_cart_modal_active.png")
    print("[10] Saved cart screenshot to result/[033]_shopping_cart_modal_active.png")

    # ==========================================
    # STEP 3: Checkout & Order Submission
    # ==========================================
    print("[11] Proceeding to Checkout...")
    page.click("#btn-cart-proceed-checkout")
    time.sleep(1)

    # Verify pre-filled info
    chk_name = page.input_value("#chk-name")
    chk_phone = page.input_value("#chk-phone")
    chk_address = page.input_value("#chk-address")
    print(f"[12] Checkout Prefilled: Name={chk_name}, Phone={chk_phone}, Address={chk_address}")
    assert chk_name == "이한규 대표", f"Expected 이한규 대표, got {chk_name}"

    # Select payment method & submit
    page.click(".payment-method-card[data-method='credit_card']")
    page.fill("#chk-note", "갤러리 1층 로비 프라이빗 직접 수령 희망")
    time.sleep(0.5)

    print("[13] Submitting final order...")
    page.click("#btn-submit-order")
    time.sleep(1.5)

    receipt_order_id = page.locator("#receipt-order-id").text_content()
    receipt_warranty_no = page.locator("#receipt-warranty-no").text_content()
    receipt_amount = page.locator("#receipt-total-amount").text_content()
    print(f"[14] Order Created Successfully: ID={receipt_order_id}, Warranty={receipt_warranty_no}, Amount={receipt_amount}")
    assert "ORD-2026-" in receipt_order_id, f"Invalid order ID: {receipt_order_id}"
    page.screenshot(path="result/[034]_order_purchase_completed_receipt.png")
    print("[15] Saved receipt screenshot to result/[034]_order_purchase_completed_receipt.png")

    # ==========================================
    # STEP 4: My Orders Modal History Check
    # ==========================================
    print("[16] Opening My Orders History...")
    page.click("#btn-go-my-orders")
    time.sleep(1)

    orders_count = page.locator("#my-orders-list-container > div").count()
    print(f"[17] Orders count in collector history: {orders_count}")
    assert orders_count >= 1, "Expected at least 1 order in collector history!"
    page.screenshot(path="result/[035]_my_orders_history_modal.png")
    print("[18] Saved my orders history screenshot to result/[035]_my_orders_history_modal.png")

    # ==========================================
    # STEP 5: Admin CMS Verification
    # ==========================================
    print("[19] Navigating to Admin CMS: http://localhost:8080/admin/index.html")
    page.goto("http://localhost:8080/admin/index.html")
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # Login to Admin
    if page.locator("#loginModal").is_visible():
        print("[20] Logging into Admin CMS with admin / 1234567...")
        page.fill("#loginId", "admin")
        page.fill("#loginPassword", "1234567")
        page.click("#btnLogin")
        time.sleep(1)

    # Check KPI Sales & Collectors
    kpi_sales = page.locator("#kpiTotalSales").text_content()
    kpi_collectors = page.locator("#kpiTotalCollectors").text_content()
    print(f"[21] Admin KPIs: Total Sales = {kpi_sales}, Total Collectors = {kpi_collectors}")
    assert int(kpi_collectors) >= 3, f"Expected at least 3 collectors, got {kpi_collectors}"

    # Click Orders Tab
    print("[22] Switching to '주문 및 결제 관리대장' tab...")
    page.click("button[data-tab='tabOrders']")
    time.sleep(1)

    # Verify the order exists in admin table
    orders_table_text = page.locator("#orderTableBody").text_content()
    assert "이한규 대표" in orders_table_text, "Newly created order not found in Admin table!"
    assert receipt_order_id in orders_table_text, f"{receipt_order_id} not found in Admin table!"
    print(f"[23] Verified order {receipt_order_id} for '이한규 대표' in Admin CMS table!")

    # Change order status to '작품검수중'
    status_select = page.locator(f".order-status-select[data-id='{receipt_order_id}']")
    status_select.select_option("작품검수중")
    time.sleep(1)
    print(f"[24] Updated status of {receipt_order_id} to '작품검수중'")
    page.screenshot(path="result/[036]_admin_orders_ledger_realtime.png")
    print("[25] Saved admin orders ledger screenshot to result/[036]_admin_orders_ledger_realtime.png")

    # Click Users Tab
    print("[26] Switching to '등록 컬렉터 관리대장' tab...")
    page.click("button[data-tab='tabUsers']")
    time.sleep(1)

    users_table_text = page.locator("#userTableBody").text_content()
    assert "이한규 대표" in users_table_text, "User '이한규 대표' not found in Admin Users table!"
    assert "ceo@ax-startup.com" in users_table_text, "User email not found in Admin Users table!"
    print("[27] Verified user '이한규 대표 (ceo@ax-startup.com)' in Admin Collectors table!")
    page.screenshot(path="result/[037]_admin_registered_collectors_ledger.png")
    print("[28] Saved admin collectors ledger screenshot to result/[037]_admin_registered_collectors_ledger.png")

    browser.close()
    print("\n=======================================================")
    print("[SUCCESS] ALL E-COMMERCE & FIREBASE TESTS PASSED 100%!")
    print("=======================================================")
