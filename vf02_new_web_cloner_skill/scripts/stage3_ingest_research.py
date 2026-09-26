# -*- coding: utf-8 -*-
"""
[Stage 3] Gemini Deep Research Asset Ingestion Engine
Standardizes and parses uploaded Gemini research files from upload/ folder:
- (딥리서치)_새만금 현대차 로봇단지 분석.pdf
- [012]_Saemangeum_Robotics_40p_Master_Script.md
- [013]_Saemangeum_Robotics_Part1_Render_Prompt.md
- [014]_Saemangeum_Robotics_Part2_Render_Prompt.md
Outputs clean structured parsed_slides.json
"""
import os
import re
import json
import argparse

def ingest_research(upload_dir, out_file='parsed_slides.json'):
    print(f"[STAGE 3] Scanning Gemini Deep Research files in: {upload_dir}")
    md_files = [f for f in os.listdir(upload_dir) if f.endswith('Master_Script.md') or 'Master_Script' in f]

    if not md_files:
        # Fallback to any markdown in upload/
        md_files = [f for f in os.listdir(upload_dir) if f.endswith('.md')]

    if not md_files:
        print(f"[WARNING] No Master_Script.md found in {upload_dir}. Looking for existing parsed data...")
        return

    target_md = os.path.join(upload_dir, md_files[0])
    print(f"  -> Ingesting Master Script: {target_md}")

    with open(target_md, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split slides by Slide header patterns
    slide_chunks = re.split(r'###\s*\[(?:Slide|슬라이드)\s*(\d+)\]', text, flags=re.IGNORECASE)
    slides = []

    if len(slide_chunks) > 1:
        for i in range(1, len(slide_chunks), 2):
            s_num = int(slide_chunks[i])
            content = slide_chunks[i+1]

            # Extract Title
            title_m = re.search(r'\*\*슬라이드 제목\*\*:\s*(.+)', content)
            title = title_m.group(1).strip() if title_m else f"슬라이드 {s_num:02d}"

            # Extract Bullets
            bullets = []
            bullet_section = re.search(r'\*\*화면 구성 및 핵심 요점\*\*:(.*?)(?=\*\*발표자 상세 대본|\Z)', content, re.DOTALL)
            if bullet_section:
                for line in bullet_section.group(1).strip().split('\n'):
                    line = line.strip()
                    if line.startswith(('-', '*', '•', '1.', '2.', '3.')):
                        clean_b = re.sub(r'^[-*•\d.]\s*', '', line).strip()
                        if clean_b:
                            bullets.append(clean_b)

            # Extract Script
            script_m = re.search(r'\*\*발표자 상세 대본\*\*:\s*(.+)', content, re.DOTALL)
            script = script_m.group(1).strip() if script_m else title

            # Detect chapter
            chapter = "STRATEGIC MASTERPLAN"
            if s_num in [4, 5, 6]: chapter = "01. 서론: 피지컬 AI 시대와 새만금"
            elif s_num in [7, 8, 9, 10]: chapter = "02. 하드웨어 플랫폼: 아틀라스"
            elif s_num in [11, 12, 13, 14, 15]: chapter = "03. 초거대 전력망: 10GW RE100"
            elif s_num in [16, 17, 18, 19, 20]: chapter = "04. 지능의 설계: VLA & 디지털 트윈"
            elif s_num in [21, 22, 23, 24, 25, 26]: chapter = "05. 지능의 실체화: SDF 메타플랜트"
            elif s_num >= 27: chapter = "06. 트라이포트 물류 및 거시 파급효과"

            slides.append({
                'num': s_num,
                'chapter': chapter,
                'title': title,
                'bullets': bullets if bullets else ["추진 세부 전략 수립 및 이행"],
                'script': script
            })

    slides = sorted(slides, key=lambda x: x['num'])
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(slides, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Ingested and parsed {len(slides)} slides into '{out_file}'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='upload', help='Upload folder containing research files')
    parser.add_argument('--output', default='parsed_slides.json', help='Output JSON file')
    args = parser.parse_args()
    ingest_research(args.source, args.output)
