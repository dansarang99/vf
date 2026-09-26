import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('http://localhost:8080/index.html')
    
    hotspot = page.locator("a.header-atelier-stealth-link")
    print("hotspot tag:", hotspot.evaluate("el => el.outerHTML"))
    
    # Listen to navigation
    with page.expect_navigation() as nav:
        hotspot.click()
    print("Navigated to:", page.url)
    
    b.close()
