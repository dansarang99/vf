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

for i, p in enumerate(root_sec.findall(f".//{HP}p")):
    txt = "".join([t.text or "" for t in p.findall(f".//{HP}t")]).strip()
    para_pr = p.get("paraPrIDRef")
    style_id = p.get("styleIDRef")
    runs = p.findall(f"{HP}run")
    char_prs = [r.get("charPrIDRef") for r in runs if r.findall(f"{HP}t")]
    tbls = p.findall(f"{HP}tbl")
    tbl_info = f"[TABLE {len(tbls[0].findall(f'{HP}tr'))} rows]" if tbls else ""
    if txt or tbl_info:
        print(f"P[{i:03d}] paraPr={para_pr} style={style_id} charPrs={char_prs} {tbl_info} | {txt[:70]}")
