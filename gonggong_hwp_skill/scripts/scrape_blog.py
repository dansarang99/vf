import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import re
from bs4 import BeautifulSoup

url = 'https://blog.naver.com/PostView.naver?blogId=deworker&logNo=222807776198'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a')
for a in links:
    href = a.get('href', '')
    text = a.get_text().strip()
    if '.hwp' in href.lower() or 'attach' in href.lower() or 'download' in href.lower() or '양식' in text:
        print(f'Link: text="{text}" href="{href}"')

content = soup.find('div', class_='se-main-container')
if content:
    lines = [line.strip() for line in content.get_text().splitlines() if line.strip()]
    print('Total content lines:', len(lines))
    for l in lines[:50]:
        print('  ', l)
