#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(base_dir, "youtube_full_transcript.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total snippets: {len(data)}")
print("=== [1. 오프닝 구간 (00:00 ~ 01:00)] ===")
for d in data[:8]:
    m = int(d["start"]) // 60
    s = int(d["start"]) % 60
    print(f"[{m:02d}:{s:02d}] ({d['duration']:.1f}s) {d['text']}")

print("\n=== [2. 지정 타임스탬프 3287s 구간 (54:40 ~ 55:20)] ===")
for d in data:
    if 3280 <= d["start"] <= 3320:
        m = int(d["start"]) // 60
        s = int(d["start"]) % 60
        print(f"[{m:02d}:{s:02d}] ({d['duration']:.1f}s) {d['text']}")
