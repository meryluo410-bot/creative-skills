#!/usr/bin/env python3
"""Render a plot-driven fictional chat screenshot from JSON."""
from __future__ import annotations
import json, math, random, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H, MARGIN = 1080, 1920, 72
TIMES = ["08:21", "08:22", "08:23", "08:23", "08:24", "08:25", "08:26", "08:26", "08:27", "08:27"]
FEMALE_NAMES = ["Amelia", "Ava", "Chloe", "Claire", "Ella", "Emily", "Grace", "Hazel", "Ivy", "Lily", "Mia", "Nora", "Olivia", "Sophie", "Violet", "Zoe"]
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FALLBACK = "/System/Library/Fonts/Supplemental/Arial.ttf"

def f(size): return ImageFont.truetype(FONT if Path(FONT).exists() else FALLBACK, size)
def safe_text(value):
    """Drop unsupported pictographs; generated media can carry decorative emoji."""
    return "".join(ch for ch in str(value) if unicodedata.category(ch) not in {"So", "Cs"}).strip()
def require_english(value, field):
    text = str(value)
    if any("\u3400" <= ch <= "\u9fff" or "\u3040" <= ch <= "\u30ff" or "\uac00" <= ch <= "\ud7af" for ch in text):
        raise ValueError(f"{field} must contain English text only")
def resolve(base, value):
    p = Path(value).expanduser()
    return p if p.is_absolute() else base / p

def cover(path, size, radius):
    im = ImageOps.fit(Image.open(path).convert("RGB"), size, method=Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=radius, fill=255)
    im.putalpha(mask)
    return im

def wrap(draw, text, face, max_width):
    result = []
    for paragraph in str(text).splitlines() or [""]:
        current = ""
        for word in paragraph.split(" "):
            trial = word if not current else current + " " + word
            if draw.textbbox((0, 0), trial, font=face)[2] <= max_width: current = trial
            else:
                if current: result.append(current)
                current = word
        result.append(current)
    return result

def placeholder(size):
    im = Image.new("RGBA", (size, size), (28, 28, 31, 255)); d = ImageDraw.Draw(im)
    d.ellipse((size*.31, size*.16, size*.69, size*.55), fill=(211, 184, 158))
    d.ellipse((size*.15, size*.48, size*.85, size*1.08), fill=(66, 59, 75))
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size-1, size-1), fill=255)
    im.putalpha(mask); return im

def status(draw):
    draw.text((108, 36), "9:41", font=f(37), fill="black")
    for i, h in enumerate((12, 20, 29, 38)): draw.rounded_rectangle((820+i*14, 58-h, 830+i*14, 58), 3, fill="black")
    draw.arc((883, 24, 925, 61), 210, 330, width=6, fill="black"); draw.arc((892, 36, 916, 58), 210, 330, width=5, fill="black")
    draw.ellipse((901, 52, 907, 58), fill="black"); draw.rounded_rectangle((942, 29, 999, 58), 7, outline=(70,70,70), width=3)
    draw.rounded_rectangle((947, 34, 992, 53), 4, fill="black")

def header(canvas, draw, base, contact, show_today):
    draw.line((68,144,103,179), fill=(35,35,35), width=4); draw.line((103,144,68,179), fill=(35,35,35), width=4)
    for x in (958,979,1000): draw.ellipse((x,157,x+9,166), fill=(40,40,40))
    size = 174; value = contact.get("avatar")
    avatar = cover(resolve(base,value),(size,size),size//2) if value else placeholder(size)
    canvas.alpha_composite(avatar,(453,86))
    draw.ellipse((585,199,644,258), fill="white", outline=(230,230,230), width=2)
    badge=str(contact.get("badge","♫"))[:2]; bb=draw.textbbox((0,0),badge,font=f(34)); draw.text((614-(bb[2]-bb[0])/2,209),badge,font=f(34),fill="black")
    name=safe_text(contact.get("name","Contact")); nf=f(50); nb=draw.textbbox((0,0),name,font=nf); draw.text(((W-(nb[2]-nb[0]))/2,269),name,font=nf,fill="black")
    if show_today:
        tb=draw.textbbox((0,0),"Today",font=f(29)); draw.text(((W-(tb[2]-tb[0]))/2,337),"Today",font=f(29),fill=(125,126,134))

def render(spec_path, output_path):
    spec=json.loads(spec_path.read_text(encoding="utf-8")); base=spec_path.parent; contact=spec.get("contact",{}); messages=spec.get("messages",[])
    if not contact.get("name"): contact["name"] = random.SystemRandom().choice(FEMALE_NAMES)
    require_english(contact["name"], "contact.name")
    for idx, item in enumerate(messages):
        if "text" in item: require_english(item["text"], f"messages[{idx}].text")
        for oi, line in enumerate(item.get("overlay", [])): require_english(line, f"messages[{idx}].overlay[{oi}]")
    if not messages: raise ValueError("messages must contain at least one block")
    canvas=Image.new("RGBA",(W,H),"white"); draw=ImageDraw.Draw(canvas); status(draw); header(canvas,draw,base,contact,spec.get("output",{}).get("show_today",True))
    y=386; body=f(29); timeface=f(22)
    for idx,item in enumerate(messages):
        kind=item.get("type","text"); side=item.get("side","in"); stamp=TIMES[min(idx,len(TIMES)-1)]
        if kind=="text":
            maxw=700 if side=="in" else 610; lines=wrap(draw,safe_text(item.get("text","")),body,maxw); lh=40
            tw=max(draw.textbbox((0,0),line or " ",font=body)[2] for line in lines); bw=min(maxw+48,max(210,tw+58)); bh=len(lines)*lh+34
            x=MARGIN if side=="in" else W-MARGIN-bw; fill=(245,245,245) if side=="in" else (25,25,27); color=(25,25,27) if side=="in" else "white"
            draw.rounded_rectangle((x,y,x+bw,y+bh),23,fill=fill)
            for li,line in enumerate(lines): draw.text((x+29,y+16+li*lh),line,font=body,fill=color)
            ty=y+bh+7; label=stamp if side=="in" else stamp+"  ✓"; tb=draw.textbbox((0,0),label,font=timeface); tx=MARGIN if side=="in" else W-MARGIN-(tb[2]-tb[0])
            draw.text((tx,ty),label,font=timeface,fill=(126,128,139)); y=ty+55
        elif kind=="media":
            cw=max(360,min(764,int(item.get("width",764)))); ch=max(180,min(420,int(item.get("height",286)))); x=MARGIN if side=="in" else W-MARGIN-cw; canvas.alpha_composite(cover(resolve(base,item["image"]),(cw,ch),18),(x,y))
            for oi,line in enumerate(item.get("overlay",[])[:3]): draw.text((x+42,y+43+oi*48),safe_text(line),font=f(34 if oi==0 else 26),fill="white",stroke_width=2,stroke_fill=(0,0,0))
            label=stamp if side=="in" else stamp+"  ✓"; tb=draw.textbbox((0,0),label,font=timeface); tx=x if side=="in" else W-MARGIN-(tb[2]-tb[0]); draw.text((tx,y+ch+7),label,font=timeface,fill=(126,128,139)); y+=ch+62
        elif kind=="gallery":
            vals=item.get("images",[])
            if not vals: continue
            cols=1 if len(vals)==1 else min(3,len(vals)); rows=math.ceil(len(vals)/cols); gap=10; tw=(764-gap*(cols-1))//cols; th=270 if cols==1 else 206
            gallery_x = MARGIN if side=="in" else W-MARGIN-764
            for j,value in enumerate(vals): canvas.alpha_composite(cover(resolve(base,value),(tw,th),16),(gallery_x+(j%cols)*(tw+gap),y+(j//cols)*(th+gap)))
            block=rows*th+(rows-1)*gap; label=stamp if side=="in" else stamp+"  ✓"; tb=draw.textbbox((0,0),label,font=timeface); tx=gallery_x if side=="in" else W-MARGIN-(tb[2]-tb[0]); draw.text((tx,y+block+7),label,font=timeface,fill=(126,128,139)); y+=block+62
        else: raise ValueError("unsupported message type: "+kind)
    top=1782
    if y>top-18: raise ValueError(f"content overflows by {y-top+18}px; shorten dialogue or media")
    draw.ellipse((58,1791,140,1873),outline=(220,220,225),width=2); draw.line((99,1814,99,1850),fill="black",width=4); draw.line((81,1832,117,1832),fill="black",width=4)
    draw.rounded_rectangle((165,1791,1004,1873),41,outline=(220,220,225),width=2); draw.text((203,1811),f"Message {safe_text(contact.get('name','Contact'))}",font=f(31),fill=(155,155,165))
    draw.ellipse((918,1798,994,1866),fill=(28,28,30)); draw.rounded_rectangle((952,1817,961,1845),5,outline="white",width=3); draw.arc((945,1832,968,1854),0,180,fill="white",width=3)
    draw.rounded_rectangle((348,1900,732,1911),6,fill="black"); output_path.parent.mkdir(parents=True,exist_ok=True); canvas.convert("RGB").save(output_path)

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("Usage: render_chat.py SPEC.json OUTPUT.png")
    render(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
