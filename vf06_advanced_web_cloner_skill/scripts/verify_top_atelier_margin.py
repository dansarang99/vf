import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Main Page Load
    print("[1] Navigating to http://localhost:8080/index.html")
    page.goto("http://localhost:8080/index.html")
    page.wait_for_load_state("networkidle")
    
    # 2. Check Logo & Stealth Hotspot
    logo = page.locator("#header .logo")
    logo_box = logo.bounding_box()
    print(f"[2] Logo bounding box: {logo_box}")
    
    hotspot = page.locator("a.header-atelier-stealth-link")
    assert hotspot.count() > 0, "Top header atelier stealth hotspot not found!"
    hotspot_box = hotspot.bounding_box()
    print(f"[3] Found top header stealth hotspot box: {hotspot_box}")
    
    # Save zoomed screenshot of header logo area
    page.screenshot(path="result/[029]_top_header_atelier_hotspot_verified.png", clip={
        "x": 0, "y": 0, "width": 600, "height": 100
    })
    print("[4] Saved zoomed header screenshot to result/[029]_top_header_atelier_hotspot_verified.png")
    
    # 3. Click the bottom margin area of (아틀리에) in the top header
    # Click near the bottom of the hotspot (hotspot_box['height'] - 10)
    click_x = hotspot_box['x'] + hotspot_box['width'] / 2
    click_y = hotspot_box['y'] + hotspot_box['height'] - 8
    print(f"[5] Clicking bottom space of (아틀리에) at ({click_x}, {click_y})...")
    page.mouse.click(click_x, click_y)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    curr_url = page.url
    print(f"[6] Current URL after click: {curr_url}")
    assert "admin" in curr_url, f"Failed to navigate to admin via top atelier margin! URL: {curr_url}"
    
    # 4. Verify Admin Page & Login Modal
    login_modal = page.locator("#loginModal")
    print(f"[7] Admin Login Modal visible: {login_modal.is_visible()}")
    page.screenshot(path="result/[030]_admin_opened_via_top_atelier_margin.png")
    print("[8] Saved admin opened screenshot to result/[030]_admin_opened_via_top_atelier_margin.png")
    
    browser.close()
    print("[SUCCESS] Top header (아틀리에) bottom space admin navigation PASSED with 0 errors!")
