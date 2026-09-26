# command/test_responsive_and_security.py
# Multi-Device (PC, Tablet, Smartphone) & Security Obscurity Verification

import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8080"
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../result"))
os.makedirs(RESULT_DIR, exist_ok=True)

def run_tests():
    print("[INFO] Starting Multi-Device Responsive & Stealth Admin Verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Desktop Test (1440x900)
        print("▶ Test 1: Desktop Viewport (1440x900) - No Header Overflow...")
        page_pc = browser.new_page(viewport={"width": 1440, "height": 900})
        page_pc.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page_pc.wait_for_timeout(500)
        
        # Verify NO admin button in header
        admin_btn = page_pc.query_selector("a.admin-cms-link")
        assert admin_btn is None, "Admin CMS link is still visible in header!"
        print("  - [PASS] Header does not expose Admin CMS button.")

        # Verify stealth dot in footer
        secret_dot = page_pc.query_selector("a.secret-admin-dot")
        assert secret_dot is not None, "Secret admin dot not found in footer!"
        print("  - [PASS] Secret dot (.) successfully placed in footer.")

        p_desktop = os.path.join(RESULT_DIR, "[020]_responsive_desktop_header_clean.png")
        page_pc.screenshot(path=p_desktop)
        print(f"  - Saved [020]: {p_desktop}")

        # Click secret dot to verify it navigates to admin
        secret_dot.click()
        page_pc.wait_for_timeout(600)
        assert "admin" in page_pc.url, f"Expected admin URL, got {page_pc.url}"
        print("  - [PASS] Secret dot navigates to admin/index.html correctly.")

        # Verify NO exposed credentials on admin page
        admin_body = page_pc.content()
        assert "admin / 1234567" not in admin_body, "Exposed credentials text found in HTML!"
        assert 'value="admin"' not in admin_body, "Prefilled username found!"
        assert 'placeholder="1234567"' not in admin_body, "Prefilled password hint found!"
        print("  - [PASS] Admin page has 0 exposed credentials!")

        p_admin_sec = os.path.join(RESULT_DIR, "[021]_admin_login_stealth_secured.png")
        page_pc.screenshot(path=p_admin_sec)
        print(f"  - Saved [021]: {p_admin_sec}")

        # 2. Tablet Viewport (1024x768)
        print("▶ Test 2: Tablet Viewport (1024x768)...")
        page_tab = browser.new_page(viewport={"width": 1024, "height": 768})
        page_tab.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page_tab.wait_for_timeout(500)
        p_tablet = os.path.join(RESULT_DIR, "[022]_responsive_tablet_1024px.png")
        page_tab.screenshot(path=p_tablet)
        print(f"  - Saved [022]: {p_tablet}")

        # 3. Smartphone Viewport (iPhone 14 - 390x844)
        print("▶ Test 3: Smartphone Viewport (iPhone 14 - 390x844)...")
        page_mobile = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        page_mobile.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page_mobile.wait_for_timeout(500)
        
        # Verify mobile header does not break or horizontally overflow window width
        body_scroll_w = page_mobile.evaluate("() => document.documentElement.scrollWidth")
        inner_w = page_mobile.evaluate("() => window.innerWidth")
        assert body_scroll_w <= inner_w + 5, f"Horizontal scroll detected on mobile! {body_scroll_w} > {inner_w}"
        print(f"  - [PASS] No horizontal overflow on smartphone (scrollWidth: {body_scroll_w}, innerWidth: {inner_w})")

        p_mobile = os.path.join(RESULT_DIR, "[023]_responsive_mobile_smartphone_390px.png")
        page_mobile.screenshot(path=p_mobile)
        print(f"  - Saved [023]: {p_mobile}")

        # 4. Small Mobile (iPhone SE - 375x667)
        print("▶ Test 4: Small Smartphone Viewport (iPhone SE - 375x667)...")
        page_se = browser.new_page(viewport={"width": 375, "height": 667}, is_mobile=True)
        page_se.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        page_se.wait_for_timeout(500)
        p_se = os.path.join(RESULT_DIR, "[024]_responsive_small_smartphone_375px.png")
        page_se.screenshot(path=p_se)
        print(f"  - Saved [024]: {p_se}")

        browser.close()
        print("[SUCCESS] All Multi-Device & Security tests passed with 0 Errors!")

if __name__ == "__main__":
    run_tests()
