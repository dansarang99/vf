import http.server
import socketserver
import threading
import urllib.request
import time
import os

PORT = 8089
Handler = http.server.SimpleHTTPRequestHandler
os.chdir(r"C:\Users\note\vf\vf01_webclone\src")

try:
    httpd = socketserver.TCPServer(("", PORT), Handler)
    t = threading.Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()
    print(f"Server started at http://localhost:{PORT}")

    time.sleep(1)
    with urllib.request.urlopen(f"http://localhost:{PORT}/index.html") as resp:
        print("HTTP Status:", resp.status)
        content = resp.read().decode("utf-8")
        print("Content length:", len(content))
        print("Title tag present:", "<title>" in content)
        print("Data.js linked:", "js/data.js" in content)
        print("Main.js linked:", "js/main.js" in content)
        
    # Check data.js
    with urllib.request.urlopen(f"http://localhost:{PORT}/js/data.js") as resp:
        print("data.js status:", resp.status)
    # Check style.css
    with urllib.request.urlopen(f"http://localhost:{PORT}/css/style.css") as resp:
        print("style.css status:", resp.status)
    # Check artwork image
    with urllib.request.urlopen(f"http://localhost:{PORT}/assets/images/artwork_moments_26_001.png") as resp:
        print("artwork image status:", resp.status)
finally:
    httpd.shutdown()
    print("Server cleanly shutdown.")
