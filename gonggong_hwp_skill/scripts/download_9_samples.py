import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import urllib.parse
import os
import shutil

# Target directory
out_dir = r'C:\Users\note\vf\gonggong_hwp_skill\upload\9종_공문서_원천'
os.makedirs(out_dir, exist_ok=True)

# 1. First file from Naver Blog (already downloaded in Downloads)
download_src = r'C:\Users\note\Downloads\1 공문 양식 한글.hwp'
if os.path.exists(download_src):
    shutil.copyfile(download_src, os.path.join(out_dir, '[01]_제안서_공문_양식_한글.hwp'))
    print('Copied [01] 1 공문 양식 한글.hwp!')

# 2. Six files from Glelog + Gongform
glelog_files = [
    ('[02]_표준_공문_양식_한글.hwp', 'https://gongform.com/wp-content/uploads/2025/09/%ED%91%9C%EC%A4%80-%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D-%ED%95%9C%EA%B8%80-%EC%9B%90%EB%B3%B8%ED%8C%8C%EC%9D%BC-1.hwp'),
    ('[03]_회사_공문_양식_한글.hwp', 'https://gongform.com/wp-content/uploads/2025/09/%ED%92%88%EC%82%AC-%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D.hwp'.replace('%ED%92%88%EC%82%AC', '%ED%9A%8C%EC%82%AC')),
    ('[04]_정부_공문_양식_한글.hwp', 'https://gongform.com/wp-content/uploads/2025/09/%EC%A0%95%EB%B6%80-%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D-%ED%95%9C%EA%B8%80.hwp'),
    ('[05]_계약해지_공문_양식_한글.hwp', 'https://kangform.com/wp-content/uploads/2025/09/%EA%B3%84%EC%95%BD%ED%95%B4%EC%A7%80-%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D-%ED%95%9C%EA%B8%80.hwp'),
    ('[06]_깔끔한_공문_서식_한글.hwp', 'https://gongform.com/wp-content/uploads/2025/09/%EA%B9%94%EB%81%94%ED%95%9C-%EA%B3%B5%EB%AC%B8-%EC%84%9C%EC%8B%9D-%ED%95%9C%EA%B8%80.hwp'),
    ('[07]_협조공문_양식_한글.hwp', 'https://gongform.com/wp-content/uploads/2025/09/%ED%98%91%EC%A1%B0%EA%B3%B5%EB%AC%B8-%EC%96%91%EC%8B%9D-%ED%95%9C%EA%B8%80.hwp')
]

headers = {'User-Agent': 'Mozilla/5.0'}

for fname, url in glelog_files:
    save_path = os.path.join(out_dir, fname)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            with open(save_path, 'wb') as f:
                f.write(resp.read())
        print(f'Downloaded {fname} ({os.path.getsize(save_path)} bytes)')
    except Exception as e:
        print(f'Error downloading {fname}: {e}')

# 3. Plus two historic public hwp files already in system
hwp_historic = r'C:\Users\note\vf\vf17_hwpx_clone_final\upload\공공기관 서식한글 개발 및 보급 계획.hwp'
if os.path.exists(hwp_historic):
    shutil.copyfile(hwp_historic, os.path.join(out_dir, '[08]_공공기관_서식한글_개발및보급계획.hwp'))
    print('Copied [08] 공공기관 서식한글 개발 및 보급 계획.hwp!')

hwp_ai = r'C:\Users\note\Downloads\260423+(4.24+보도)+국가AI전략위·행안부·문체부++AI시대+개방형+포맷+전환을+위한+‘협력·속도·실행’+박차++‘hwp+파일+첨부제한’+부터.hwpx'
if os.path.exists(hwp_ai):
    shutil.copyfile(hwp_ai, os.path.join(out_dir, '[09]_국가AI전략위_개방형HWPX전환표준.hwpx'))
    print('Copied [09] 국가AI전략위 개방형 HWPX 전환 표준!')

print('=== Current files in upload/9종_공문서_원천 ===')
for f in os.listdir(out_dir):
    p = os.path.join(out_dir, f)
    print(f'  {f} ({os.path.getsize(p)} bytes)')
