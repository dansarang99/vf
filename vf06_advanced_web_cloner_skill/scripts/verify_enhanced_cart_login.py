import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

LIVE_URL = "https://src-topaz-nu.vercel.app"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    print(f"[1] Navigating to {LIVE_URL}...")
    page.goto(LIVE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # 1. Verify Header Cart Label and Login
    header_login = page.locator("#btn-header-login").text_content()
    header_cart_label = page.locator("#btn-header-cart .cart-label").text_content()
    print(f"[2] Header Login text: '{header_login}', Cart Label: '{header_cart_label}'")
    assert "로그인" in header_login
    assert "장바구니" in header_cart_label

    # 2. Check Floating Cart Button at bottom right
    float_cart = page.locator("#floating-cart-btn")
    print(f"[3] Floating cart widget visible: {float_cart.is_visible()}")
    assert float_cart.is_visible(), "Floating cart button not visible!"
    page.screenshot(path="result/[042]_floating_cart_widget_live.png")
    print("[4] Saved floating cart screenshot to result/[042]_floating_cart_widget_live.png")

    # 3. Check Artwork Card Direct Cart Buttons
    page.evaluate("document.getElementById('artworks-section').scrollIntoView()")
    time.sleep(1)
    card_cart_btns = page.locator(".btn-card-cart")
    print(f"[5] Artwork card direct cart buttons found: {card_cart_btns.count()}")
    assert card_cart_btns.count() >= 10, "Card cart buttons missing from grid!"
    page.screenshot(path="result/[041]_enhanced_card_cart_buttons.png")
    print("[6] Saved card cart buttons screenshot to result/[041]_enhanced_card_cart_buttons.png")

    # 4. Click direct cart button on first card
    print("[7] Clicking direct [🛒 장바구니] button on first artwork card...")
    card_cart_btns.first.click()
    time.sleep(0.8)

    float_count = page.locator("#floating-cart-count").text_content()
    header_count = page.locator("#cart-count-badge").text_content()
    print(f"[8] Cart Count updated: Floating={float_count}, Header={header_count}")
    assert int(float_count) >= 1
    assert int(header_count) >= 1

    # 5. Click Floating Cart Button to open Cart Modal
    print("[9] Clicking floating cart button to open Cart Modal...")
    float_cart.click()
    time.sleep(0.8)
    cart_modal = page.locator("#cart-modal")
    print(f"[10] Cart Modal opened: {cart_modal.is_visible()}")
    assert cart_modal.is_visible()
    page.screenshot(path="result/[044]_cart_drawer_live.png")
    print("[11] Saved cart drawer screenshot to result/[044]_cart_drawer_live.png")

    # Close Cart Modal
    page.click("#cart-modal-close-btn")
    time.sleep(0.5)

    # 6. Click Header Login to open Auth Modal
    print("[12] Clicking header [로그인] button...")
    page.click("#btn-header-login")
    time.sleep(0.8)
    auth_modal = page.locator("#auth-modal")
    print(f"[13] Auth Modal opened: {auth_modal.is_visible()}")
    assert auth_modal.is_visible()
    page.screenshot(path="result/[043]_login_modal_live.png")
    print("[14] Saved login modal screenshot to result/[043]_login_modal_live.png")

    browser.close()
    print("\n[SUCCESS] Enhanced Login & Cart verification PASSED on live Vercel production!")
