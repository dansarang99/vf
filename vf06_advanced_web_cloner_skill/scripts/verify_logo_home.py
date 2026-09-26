import sys
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://localhost:8080/index.html#exclusive')
    
    # Click MA JI YOUNG (left part of logo)
    logo_img = page.locator("#header-logo-img")
    box = logo_img.bounding_box()
    # click at left side of logo (x=50)
    page.mouse.click(box['x'] + 30, box['y'] + box['height'] / 2)
    page.wait_for_load_state("networkidle")
    
    print("URL after clicking MA JI YOUNG:", page.url)
    assert "admin" not in page.url, "Clicking main logo should NOT go to admin!"
    
    b.close()
    print("[SUCCESS] Clicking MA JI YOUNG safely stays on public site / navigates to home!")
