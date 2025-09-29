
#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys, os, json

def load_font(size):
    # Try to load a user-provided font or fallback to default
    font_paths = [
        "assets/fonts/Inter-Bold.ttf",
        "assets/fonts/Montserrat-Bold.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

def outline_text(draw, xy, text, font, fill, outline=(0,0,0), width=4):
    x,y = xy
    for dx in range(-width,width+1):
        for dy in range(-width,width+1):
            draw.text((x+dx,y+dy), text, font=font, fill=outline)
    draw.text((x,y), text, font=font, fill=fill)

def main():
    if len(sys.argv)<6:
        print("Usage: generate_thumb.py <out.png> <aspect:16x9|9x16|1x1> <title.json> <bg.png> <avatar.png> [palette_json]")
        sys.exit(1)
    out, aspect, title_json, bg_img, avatar_img = sys.argv[1:6]
    pal = ["#0a1c4a","#2aa7ff"]
    if len(sys.argv)>6 and os.path.exists(sys.argv[6]):
        pal = json.loads(open(sys.argv[6]).read())

    W,H = (1280,720) if aspect=="16x9" else (1080,1920) if aspect=="9x16" else (1080,1080)
    img = Image.new("RGBA", (W,H), (0,0,0,0))
    # background
    bg = Image.open(bg_img).convert("RGBA").resize((W,H))
    img.paste(bg, (0,0), bg)

    # avatar with alpha (optional)
    if os.path.exists(avatar_img):
        av = Image.open(avatar_img).convert("RGBA")
        # scale to 70% height for 9:16, 60% for 16:9
        scale = 0.7 if aspect=="9x16" else 0.6
        new_h = int(H*scale); new_w = int(av.width * (new_h/av.height))
        av = av.resize((new_w,new_h), Image.LANCZOS)
        # position: right for 16:9, bottom for 9:16
        if aspect=="9x16":
            x = (W-new_w)//2; y = H - new_h
        else:
            x = W - new_w - 20; y = H - new_h
        img.alpha_composite(av, (x,y))

    # title box
    data = json.loads(open(title_json).read())
    title = data.get("title","")
    kicker = data.get("kicker","")
    font_big = load_font(size=int(H*0.12 if aspect=='9x16' else H*0.13))
    font_small = load_font(size=int(H*0.06))

    draw = ImageDraw.Draw(img)
    pad = int(H*0.04)
    # gradient bar
    bar = Image.new("RGBA", (W, int(H*0.28)), (0,0,0,0))
    bar_draw = ImageDraw.Draw(bar)
    bar_draw.rectangle((0,0,W,bar.height), fill=pal[0])
    # add top stripe
    bar_draw.rectangle((0,0,W,int(bar.height*0.18)), fill=pal[1])
    img.alpha_composite(bar, (0,0))

    # text
    outline_text(draw, (pad, pad + int(H*0.03)), kicker.upper(), font_small, fill="white", outline=(0,0,0), width=3)
    outline_text(draw, (pad, pad + int(H*0.09)), title, font_big, fill="white", outline=(0,0,0), width=5)

    # save
    img = img.convert("RGB")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "JPEG", quality=92)
    print("Wrote", out)

if __name__ == "__main__":
    main()
