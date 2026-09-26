# -*- coding: utf-8 -*-
import os, re, sys

FORBIDDEN_PATTERNS = [
    r"박서보", r"park_seo_bo", r"park-seo-bo",
    r"ARTN\s*Edition", r"artnedition", r"아트앤에디션", r"아트앤라이프"
]

def verify_zero_traces(src_dir):
    violations = []
    regex = re.compile("|".join(FORBIDDEN_PATTERNS), re.IGNORECASE)
    
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith(('.html', '.js', '.css', '.json', '.svg')):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line_no, line in enumerate(fp, 1):
                        match = regex.search(line)
                        if match:
                            violations.append((p, line_no, match.group(0), line.strip()[:80]))
    
    if violations:
        print(f"[FAIL] {len(violations)} 잔여 레퍼런스 흔적 발견:")
        for v in violations:
            print(f"  {v[0]}:{v[1]} - [{v[2]}] {v[3]}")
        sys.exit(1)
    else:
        print("[SUCCESS] 0 Residual Traces Verified! 완벽한 독자 브랜드 구축 완료.")
        sys.exit(0)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\note\vf\vf01_webclone\src"
    verify_zero_traces(target)
