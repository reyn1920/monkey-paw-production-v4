from pathlib import Path
import sys
try:
    from PIL import Image, ImageDraw
except Exception as e:
    print("Thumbnail step requires pillow; skipping. Install with: python3 -m pip install pillow")
    sys.exit(0)

def make_thumb(src_text: str):
    p = Path(src_text)
    img = Image.new("RGB", (1280, 720))
    d = ImageDraw.Draw(img)
    d.text((40, 40), p.stem[:64], fill=(255, 255, 255))
    out = p.with_suffix(".png")
    img.save(out)
    print(out)

if __name__ == "__main__":
    make_thumb(sys.argv[1] if len(sys.argv) > 1 else "artifacts/staging/draft_youtube.txt")
