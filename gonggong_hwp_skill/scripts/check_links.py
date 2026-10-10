import urllib.request
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# 1. Check gongform
try:
    url1 = 'https://gongform.com/%ED%91%9C%EC%A4%80-%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D-word-%EC%84%9C%EC%8B%9D-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C-%EC%9E%91%EC%84%B1%EB%B2%95/'
    req1 = urllib.request.Request(url1, headers=headers)
    html1 = urllib.request.urlopen(req1, timeout=5).read().decode('utf-8', errors='ignore')
    soup1 = BeautifulSoup(html1, 'html.parser')
    print('=== Gongform Links ===')
    for a in soup1.find_all('a'):
        href = a.get('href', '')
        if any(ext in href.lower() for ext in ['.hwp', '.hwpx', '.doc', '.docx', '.zip']):
            print(' ', a.get_text().strip(), href)
except Exception as e:
    print('Gongform error:', e)

# 2. Check glelog
try:
    url2 = 'https://glelog.net/%ED%91%9C%EC%A4%80-%ED%98%95%EC%8B%9D%EC%9D%98-%EA%B3%B5%EB%AC%B8-%EC%84%9C%EC%8B%9D-word-hwp-%EC%97%91%EC%85%80-%EC%96%91%EC%8B%9D-6%EC%A2%85-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C/'
    req2 = urllib.request.Request(url2, headers=headers)
    html2 = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8', errors='ignore')
    soup2 = BeautifulSoup(html2, 'html.parser')
    print('=== Glelog Links ===')
    for a in soup2.find_all('a'):
        href = a.get('href', '')
        if any(ext in href.lower() for ext in ['.hwp', '.hwpx', '.doc', '.docx', '.zip']):
            print(' ', a.get_text().strip(), href)
except Exception as e:
    print('Glelog error:', e)
