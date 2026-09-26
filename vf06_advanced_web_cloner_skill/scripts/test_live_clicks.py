import sys
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto('https://src-topaz-nu.vercel.app')
    page.wait_for_load_state("networkidle")
    
    print("Header login HTML:", page.locator("#header-auth-section").inner_html())
    
    # Click 로그인
    page.click("text=로그인")
    page.wait_for_timeout(500)
    print("Auth modal visible after click:", page.locator("#auth-modal").is_visible())
    
    # Close auth modal
    page.click("#auth-modal-close-btn")
    page.wait_for_timeout(300)
    
    # Click Cart
    page.click(".cart")
    page.wait_for_timeout(500)
    print("Cart modal visible after click:", page.locator("#cart-modal").is_visible())
    
    b.close()
