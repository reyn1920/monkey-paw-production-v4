from pathlib import Path
from PIL import Image, ImageDraw, ImageFont  # pillow optional
import sys

def make_thumb(src_text: str):
    p = Path(src_text)
    img = Image.new("RGB", (1280, 720), (30, 30, 30))
    d = ImageDraw.Draw(img)
    d.text((40, 40), p.stem[:30], fill=(230, 230, 230))
    out = p.with_suffix(".png")
    img.save(out)
    print(out)

if __name__ == "__main__":
    try:
        make_thumb(sys.argv[1] if len(sys.argv) > 1 else "artifacts/staging/draft_youtube.txt")
    except Exception as e:
        print("Thumbnail step requires pillow. Skipping. ", e)
