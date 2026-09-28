import docx
import re
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"result\[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx")

footer_re = re.compile(r'^(?:\d+\s*\|\s*제\d+장|\d+\.\s+[가-힣]+\s*\|\s*\d+|\d+\s*\|\s*2024\s*농업전망|부록\s*\|\s*\d+)')

found_footers = []
for idx, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if footer_re.match(t):
        found_footers.append({
            'idx': idx,
            'text': t
        })

print(f"Total footers detected: {len(found_footers)}")
for f in found_footers:
    print(f"P{f['idx']:03d}: {f['text']}")

with open(r"process/docx_footers_mapping.json", "w", encoding="utf-8") as out:
    json.dump(found_footers, out, ensure_ascii=False, indent=2)
