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
tbl3 = tables[3]
first_cell = tbl3.find(f".//{HP}tc")
print("Table 3 Cell XML:")
print(ET.tostring(first_cell, encoding="utf-8").decode("utf-8"))
