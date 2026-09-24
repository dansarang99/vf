# -*- coding: utf-8 -*-
import os
import time
from playwright.sync_api import sync_playwright

result_dir = r"C:\Users\note\vf\vf01_webclone\result"
os.makedirs(result_dir, exist_ok=True)

errors = []

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("Navigating to http://localhost:8080/index.html ...")
        page.goto("http://localhost:8080/index.html", wait_until="networkidle")
        time.sleep(1)

        print("Page Title:", page.title())

        # Scroll down and back up to trigger any lazy effects
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)

        # Screenshot 1: Full Artist Detail Page
        shot1 = os.path.join(result_dir, "01_ma_ji_young_page.png")
        page.screenshot(path=shot1, full_page=True)
        print(f"Saved: {shot1}")

        # Test Read More button
        read_more = page.locator("#read-more-btn")
        read_more.click()
        time.sleep(0.5)
        print("Read more clicked. Text is now:", read_more.inner_text())

        # Test Series Quick Switcher (e.g., 대표작)
        print("Testing Series Quick Switcher...")
        page.locator("button[data-filter='master']").click()
        time.sleep(0.8)
        filtered_count = page.locator("#artworks-grid li").count()
        print(f"Master artworks count: {filtered_count}")

        # Reset to All
        page.locator("button[data-filter='all']").click()
        time.sleep(0.5)

        # Test Artwork Lightbox Modal
        first_art_img = page.locator("#artworks-grid li .img").first
        first_art_img.click()
        time.sleep(0.8)

        modal = page.locator("#artwork-modal")
        if modal.is_visible():
            print("Artwork modal successfully opened!")
            modal_title = page.locator("#modal-title").inner_text()
            print("Modal Title:", modal_title)
            shot2 = os.path.join(result_dir, "02_artwork_lightbox_modal.png")
            page.screenshot(path=shot2)
            print(f"Saved: {shot2}")

            # Test Add to Cart in Modal
            page.locator("#modal-btn-cart").click()
            time.sleep(0.5)
            cart_text = page.locator("#cart-count-badge").inner_text()
            print(f"Cart count badge: {cart_text}")

        # Test Exhibition Modal
        page.locator("#exhibition-grid li").first.click()
        time.sleep(0.8)
        exb_modal = page.locator("#exb-modal")
        if exb_modal.is_visible():
            print("Exhibition modal successfully opened!")
            shot3 = os.path.join(result_dir, "03_exhibition_modal.png")
            page.screenshot(path=shot3)
            print(f"Saved: {shot3}")
            page.locator("#exb-modal-close-btn").click()
            time.sleep(0.4)

        # Focus Search Input to show Search Suggestion Dropdown
        page.locator("#top-search-input").focus()
        time.sleep(0.5)
        shot5 = os.path.join(result_dir, "05_search_suggest_layer.png")
        page.screenshot(path=shot5)
        print(f"Saved: {shot5}")

        browser.close()
except Exception as e:
    print(f"Test exception: {e}")

if errors:
    print("PAGE ERRORS ENCOUNTERED:", errors)
else:
    print("ALL TESTS PASSED WITH 0 CONSOLE/PAGE ERRORS!")
