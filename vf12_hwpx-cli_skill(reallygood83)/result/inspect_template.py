import sys, os, glob, zipfile, io
import xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

upload_dir = r"C:\Users\note\vf\vf12_hwpx-cli_skill(reallygood83)\upload"
hwpx_files = glob.glob(os.path.join(upload_dir, "*.hwpx"))
target = hwpx_files[0]

with zipfile.ZipFile(target, "r") as z:
    sec0_bytes = z.read("Contents/section0.xml")
    root_sec = ET.fromstring(sec0_bytes)

HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"

print("=== PARAGRAPH-BY-PARAGRAPH INSPECTION (50 to end) ===")
all_p = root_sec.findall(f".//{HP}p")
for idx in range(50, len(all_p)):
    p = all_p[idx]
    txt = "".join([t.text or "" for t in p.findall(f".//{HP}t")]).strip()
    tbls = p.findall(f"{HP}tbl")
    if tbls:
        print(f"P[{idx}]: [HAS_TABLE rows={len(tbls[0].findall(f'{HP}tr'))}]")
    elif txt:
        print(f"P[{idx}]: {txt[:80]}")
