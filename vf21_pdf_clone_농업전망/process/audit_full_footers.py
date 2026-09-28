import fitz
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc_orig = fitz.open(r'upload/3f3b07ee6df942cdb31b1822aa0c1cae.pdf')
doc_gen = fitz.open(r'result\[037]_농업전망_제1원본_템플릿_골격_레이아웃.pdf')

full_audit = []
for pno in range(1, 38):
    po = doc_orig[pno-1]
    pg = doc_gen[pno-1]
    
    f_orig = [b for b in po.get_text('blocks') if b[1] > 680 and b[4].strip()]
    f_gen = [b for b in pg.get_text('blocks') if b[1] > 680 and b[4].strip()]
    
    fo_txt = f_orig[0][4].strip() if f_orig else None
    fg_txt = f_gen[0][4].strip() if f_gen else None
    
    fo_box = f_orig[0][:4] if f_orig else None
    fg_box = f_gen[0][:4] if f_gen else None
    
    match = (fo_txt == fg_txt)
    delta_y = round((fg_box[1] - fo_box[1]) * 0.352778, 2) if fo_box and fg_box else 0
    delta_x = round((fg_box[0] - fo_box[0]) * 0.352778, 2) if fo_box and fg_box else 0
    
    full_audit.append({
        'page': pno,
        'orig': fo_txt,
        'gen': fg_txt,
        'match': match,
        'delta_x_mm': delta_x,
        'delta_y_mm': delta_y,
        'gen_box': [round(x, 1) for x in fg_box] if fg_box else None
    })

print(f"Total pages audited: {len(full_audit)}")
matched_count = sum(1 for a in full_audit if a['match'])
print(f"Strict text match: {matched_count} / 37")
for a in full_audit:
    m_str = "PASS" if a['match'] else "FAIL"
    print(f"P{a['page']:02d}: [{m_str}] Orig: {a['orig']} | Gen: {a['gen']} (dy={a['delta_y_mm']}mm)")
