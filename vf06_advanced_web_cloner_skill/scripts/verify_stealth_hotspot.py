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
    
    # 2. Test Top Menu Atelier -> Must NOT navigate to admin
    atelier_menu = page.locator("ul.gnb >> text=Atelier")
    href = atelier_menu.get_attribute("href")
    print(f"[2] Top Menu Atelier href: {href} (Expected #printstudio)")
    assert href == "#printstudio", f"GNB Atelier must be #printstudio but was {href}"
    
    # 3. Scroll to Footer
    print("[3] Scrolling to footer...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    
    # 4. Check the stealth hotspot under "마지영 아틀리에"
    hotspot = page.locator("a.stealth-admin-under-space")
    assert hotspot.count() > 0, "Stealth admin hotspot under small atelier text not found!"
    hotspot_box = hotspot.bounding_box()
    print(f"[4] Found stealth hotspot box: {hotspot_box}")
    
    # Screenshot of footer with stealth indicator
    page.screenshot(path="result/[027]_footer_stealth_hotspot_location.png")
    print("[5] Saved footer screenshot to result/[027]_footer_stealth_hotspot_location.png")
    
    # 5. Click the space under 마지영 아틀리에
    print("[6] Clicking the space directly under '마지영 아틀리에 (MA JI YOUNG Atelier)'...")
    # Click 15px below the top of the hotspot
    hotspot.click()
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    curr_url = page.url
    print(f"[7] Current URL after click: {curr_url}")
    assert "admin" in curr_url, f"Failed to navigate to admin! URL was {curr_url}"
    
    # 6. Verify Admin Page Loaded
    auth_modal = page.locator("#admin-auth-modal")
    print(f"[8] Admin Auth Modal visible: {auth_modal.is_visible()}")
    page.screenshot(path="result/[028]_admin_opened_via_footer_stealth_click.png")
    print("[9] Saved admin opened screenshot to result/[028]_admin_opened_via_footer_stealth_click.png")
    
    browser.close()
    print("[SUCCESS] All stealth admin hotspot tests PASSED with 0 errors!")
