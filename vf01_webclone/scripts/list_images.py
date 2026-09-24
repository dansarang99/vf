import os
import json
from PIL import Image

images_dir = r"C:\Users\note\vf\vf01_webclone\src\assets\images"
files = [f for f in os.listdir(images_dir) if f.startswith("image") and f.endswith(".png")]
files.sort(key=lambda x: int(x.replace("image", "").replace(".png", "")))

print(f"Total extracted PNG files: {len(files)}")
for f in files:
    fp = os.path.join(images_dir, f)
    with Image.open(fp) as im:
        print(f"{f:12}: size={im.size}, mode={im.mode}, bytes={os.path.getsize(fp):,}")
