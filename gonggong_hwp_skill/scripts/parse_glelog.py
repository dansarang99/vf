import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}

url = 'https://glelog.net/%ED%91%9C%EC%A4%80-%ED%98%95%EC%8B%9D%EC%9D%98-%EA%B3%B5%EB%AC%B8-%EC%84%9C%EC%8B%9D-word-hwp-%EC%97%91%EC%85%80-%EC%96%91%EC%8B%9D-6%EC%A2%85-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C/'
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

items = []
for p in soup.find_all(['p', 'h2', 'h3', 'div']):
    # check for links inside
    a_tags = p.find_all('a')
    for a in a_tags:
        href = a.get('href', '')
        if '.hwp' in href or '.docx' in href:
            unquoted = urllib.parse.unquote(href)
            items.append((a.get_text().strip(), unquoted))

print(f'Total link occurrences: {len(items)}')
seen = set()
for title, link in items:
    if link not in seen:
        seen.add(link)
        filename = link.split('/')[-1]
        print(f'File: {filename} -> URL: {link}')
