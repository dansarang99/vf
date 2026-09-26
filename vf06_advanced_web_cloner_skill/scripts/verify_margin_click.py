import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://localhost:8080/index.html')
    
    logo = page.locator("#header .logo")
    hotspot = page.locator("a.header-atelier-stealth-link")
    
    l_box = logo.bounding_box()
    h_box = hotspot.bounding_box()
    print("Logo box:", l_box)
    print("Hotspot box:", h_box)
    
    # Coordinate right in the bottom margin below (아틀리에)
    margin_x = h_box['x'] + h_box['width'] / 2
    # The logo text ends at y = 83.35, header bottom is ~112. Let's click at y = 92
    margin_y = l_box['y'] + l_box['height'] + 8
    print(f"Targeting bottom margin below (아틀리에): ({margin_x}, {margin_y})")
    
    with page.expect_navigation() as nav:
        page.mouse.click(margin_x, margin_y)
    
    print("URL after clicking bottom margin:", page.url)
    assert "admin" in page.url, f"Expected admin in URL, got {page.url}"
    
    page.screenshot(path="result/[030]_admin_opened_via_top_atelier_margin.png")
    print("Saved screenshot to result/[030]_admin_opened_via_top_atelier_margin.png")
    
    b.close()
    print("[SUCCESS] Verified clicking bottom margin below (아틀리에) navigates to admin!")
