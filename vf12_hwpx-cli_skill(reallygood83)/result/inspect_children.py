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

for i, p in enumerate(root_sec):
    tbls = p.findall(f".//{HP}tbl")
    txt = "".join([t.text or "" for t in p.findall(f".//{HP}t")]).strip()
    if tbls:
        t_id = tbls[0].get("id")
        t_rows = len(tbls[0].findall(f"{HP}tr"))
        print(f"Child {i:02d}: [TABLE id={t_id} rows={t_rows}] | {txt[:40]}")
    elif txt:
        print(f"Child {i:02d}: {txt[:60]}")
    else:
        print(f"Child {i:02d}: [EMPTY]")
