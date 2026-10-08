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

tables = root_sec.findall(f".//{HP}tbl")
print(f"Total tables: {len(tables)}")

for idx in [0, 1, 2, 3]:
    tbl = tables[idx]
    print(f"\n================ TABLE {idx} XML ================")
    print(ET.tostring(tbl, encoding="utf-8")[:1500].decode("utf-8"))
