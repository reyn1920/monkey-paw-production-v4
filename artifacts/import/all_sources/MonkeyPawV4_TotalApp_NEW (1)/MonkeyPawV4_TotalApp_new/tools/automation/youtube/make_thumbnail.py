import sys;from pathlib import Path
try:
 from PIL import Image,ImageDraw
except Exception:
 print('Thumbnail requires pillow; skipping');sys.exit(0)
p=Path(sys.argv[1] if len(sys.argv)>1 else 'artifacts/staging/draft_youtube.txt');img=Image.new('RGB',(1280,720));d=ImageDraw.Draw(img);d.text((40,40),p.stem[:64],fill=(255,255,255));out=p.with_suffix('.png');img.save(out);print(out)