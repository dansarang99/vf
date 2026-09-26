import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

LIVE_URL = "https://src-topaz-nu.vercel.app"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # 1. Main Live Site
    print(f"[1] Navigating to Vercel Live Production URL: {LIVE_URL}")
    page.goto(LIVE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    title = page.title()
    print(f"[2] Live page title: {title}")
    assert "마지영" in title or "MA JI YOUNG" in title, "Live title does not match!"
    page.screenshot(path="result/[038]_vercel_live_production_main.png")
    print("[3] Saved live main screenshot to result/[038]_vercel_live_production_main.png")
    
    # 2. Live Admin Mode (via stealth margin below top atelier)
    hotspot = page.locator("a.header-atelier-stealth-link")
    hotspot_box = hotspot.bounding_box()
    click_x = hotspot_box['x'] + hotspot_box['width'] / 2
    click_y = hotspot_box['y'] + hotspot_box['height'] - 8
    print(f"[4] Clicking live stealth hotspot at ({click_x}, {click_y})...")
    with page.expect_navigation():
        page.mouse.click(click_x, click_y)
    
    print(f"[5] Live Admin URL after click: {page.url}")
    assert "admin" in page.url, "Failed to navigate to admin on live production!"
    page.screenshot(path="result/[039]_vercel_live_production_admin_stealth.png")
    print("[6] Saved live admin screenshot to result/[039]_vercel_live_production_admin_stealth.png")
    
    browser.close()
    print("[SUCCESS] Vercel Live Production site verified 100%!")
