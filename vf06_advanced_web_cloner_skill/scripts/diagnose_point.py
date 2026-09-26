import sys
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://localhost:8080/index.html')
    
    hotspot = page.locator("a.header-atelier-stealth-link")
    print("Hotspot bounding box:", hotspot.bounding_box())
    
    logo = page.locator("#header .logo")
    print("Logo bounding box:", logo.bounding_box())
    
    # Check elements at various points
    for y_offset in [0, 10, 20, 25, 30, 40]:
        pt_x = 163.5
        pt_y = hotspot.bounding_box()['y'] + y_offset
        el = page.evaluate(f"() => {{ const el = document.elementFromPoint({pt_x}, {pt_y}); return el ? el.outerHTML : 'null'; }}")
        print(f"y_offset {y_offset} (y={pt_y}):", el[:80] if el else 'null')
    
    b.close()
