
#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import json, sys, os
def font(sz): 
    try: return ImageFont.truetype("assets/fonts/Inter-Bold.ttf", sz)
    except: return ImageFont.load_default()
if __name__=="__main__":
    out, aspect, title_json, bg_img, avatar_img, pal_json = sys.argv[1:7]
    pal = json.loads(open(pal_json).read()) if os.path.exists(pal_json) else ["#0a1c4a","#2aa7ff"]
    W,H = (1280,720) if aspect=="16x9" else (1080,1920) if aspect=="9x16" else (1080,1080)
    img = Image.new("RGBA",(W,H),(0,0,0,0)); bg = Image.open(bg_img).convert("RGBA").resize((W,H)); img.alpha_composite(bg,(0,0))
    if os.path.exists(avatar_img): av = Image.open(avatar_img).convert("RGBA"); av=av.resize((int(W*0.45),int(H*0.6))); img.alpha_composite(av,(W-av.width-10,H-av.height))
    data=json.loads(open(title_json).read()); draw=ImageDraw.Draw(img)
    draw.rectangle((0,0,W,int(H*0.25)), fill=pal[0])
    draw.text((20, 20), data.get("kicker","").upper(), font=font(int(H*0.06)), fill="white")
    draw.text((20, int(H*0.1)), data.get("title",""), font=font(int(H*0.12)), fill="white")
    img.convert("RGB").save(out, "JPEG", quality=92); print("Wrote", out)
