"""Render a README preview image of a cut (no Word needed)."""
import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

cut = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]

def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()

serif = ["times.ttf", "DejaVuSerif.ttf"]
serif_b = ["timesbd.ttf", "DejaVuSerif-Bold.ttf"]
serif_i = ["timesi.ttf", "DejaVuSerif-Italic.ttf"]
serif_bi = ["timesbi.ttf", "DejaVuSerif-BoldItalic.ttf"]
F = {"t": font(serif_b, 40), "a": font(serif_i, 24), "h": font(serif_b, 26),
     "cue": font(serif_i, 22), "tag": font(serif_bi, 22), "txt": font(serif, 25)}
W, M = 1400, 70
img = Image.new("RGB", (W, 4000), "white")
d = ImageDraw.Draw(img)
y = 50

def center(text, f, fill="black"):
    global y
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    y += f.size + 14

def para(parts, wrap=95):
    """parts = [(text, fontkey, color)] rendered inline then wrapped word by word."""
    global y
    x = M
    for text, fk, col in parts:
        f = F[fk]
        for word in text.split(" "):
            ww = d.textlength(word + " ", font=f)
            if x + ww > W - M:
                x = M; y += 34
            d.text((x, y), word + " ", font=f, fill=col)
            x += ww
    y += 46

center(cut["title"], F["t"])
center(cut["author"], F["a"], "#444")
y += 10
for s in cut["segments"]:
    k = s["kind"]
    if k == "head":
        para([(s["text"], "h", "black")])
    elif k == "cue":
        para([(s["text"], "cue", "#7a5c00")])
    else:
        parts = []
        if s.get("tag"):
            parts.append((s["tag"], "tag", "#1a56db"))
        parts.append((s["text"], "txt", "black"))
        para(parts)
img = img.crop((0, 0, W, y + 30))
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W - 1, img.height - 1], outline="#d0d7de", width=3)
img.save(out, optimize=True)
print("wrote", out, img.size)
