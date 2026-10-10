import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import olefile
import zipfile

src_dir = r'C:\Users\note\vf\gonggong_hwp_skill\upload\9종_공문서_원천'

for fname in sorted(os.listdir(src_dir)):
    fpath = os.path.join(src_dir, fname)
    print(f'=== File: {fname} ===')
    if fname.endswith('.hwp'):
        try:
            ole = olefile.OleFileIO(fpath)
            txt = ole.openstream('PrvText').read().decode('utf-16le', errors='ignore')
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            sample = ' | '.join(lines[:3])
            print(f'  Streams: {len(ole.listdir())} | Sample: {sample[:70]}')
            ole.close()
        except Exception as e:
            print('  HWP read error:', e)
    elif fname.endswith('.hwpx'):
        try:
            with zipfile.ZipFile(fpath, 'r') as z:
                print(f'  HWPX archive ({len(z.namelist())} files)')
        except Exception as e:
            print('  HWPX read error:', e)
