import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from DnsXMusic import app
from config import YOUTUBE_IMG_URL
import math

IMG = "F_lxudNioBA-HD.jpg"
OUT = "o.png"
W, H = 800, 450
PAD = 30
COVER = 200
PROG = 0.33
def tri(d, x, y, s, dir='r', col='white'):
    if dir == 'r':
        pts = [(x, y - s), (x, y + s), (x + s, y)]
    else:
        pts = [(x, y - s), (x, y + s), (x - s, y)]
    d.polygon(pts, fill=col)
def pause(d, x, y, s=15, col='white'):
    d.rectangle([x - s, y - s, x - s // 2, y + s], fill=col)
    d.rectangle([x + s // 2, y - s, x + s, y + s], fill=col)
def rpt(d, x, y, s=15, col='white'):
    d.arc([x - s, y - s, x + s, y + s], 30, 300, fill=col, width=2)
    tri(d, x, y - s, s // 3, dir='r', col=col)
def shuf(d, x, y, s=15, col='white'):
    d.line([x - s, y - s, x + s, y + s], fill=col, width=2)
    tri(d, x + s, y + s, s // 3, dir='r', col=col)
    d.line([x - s, y + s, x + s, y - s], fill=col, width=2)
    tri(d, x + s, y - s, s // 3, dir='r', col=col)
def run():
    src = Image.open(IMG).convert("RGB")
    bg = src.resize((1280, 720)).filter(ImageFilter.GaussianBlur(25))
    blk = Image.new("RGBA", bg.size, (0, 0, 0, 200))
    bg = Image.alpha_composite(bg.convert("RGBA"), blk)
    cv = Image.new("RGBA", bg.size)
    cv.paste(bg, (0, 0))
    card = Image.new("RGBA", (W, H), (30, 30, 30, 240))
    msk = Image.new("L", (W, H), 0)
    ImageDraw.Draw(msk).rounded_rectangle((0, 0, W, H), 15, fill=255)
    cpos = ((cv.width - W) // 2, (cv.height - H) // 2)
    cv.paste(card, cpos, msk)
    art = src.resize((COVER, COVER))
    cv.paste(art, (cpos[0] + PAD, cpos[1] + PAD))
    try:
        f1 = ImageFont.truetype("arial.ttf", 32)
        f2 = ImageFont.truetype("arial.ttf", 28)
    except:
        f1 = ImageFont.load_default()
        f2 = ImageFont.load_default()
    d = ImageDraw.Draw(cv)
    tx = cpos[0] + PAD + COVER + 25
    d.text((tx, cpos[1] + PAD + 20), "Full Part", font=f1, fill="white")
    bx, by = cpos[0] + PAD, cpos[1] + H - 120
    bw, bh = W - 2 * PAD, 4
    d.text((bx, by - 30), "01:51", font=f2, fill="#AAA")
    d.text((bx + bw - 60, by - 30), "03:03", font=f2, fill="#AAA")
    d.rectangle([bx, by, bx + bw, by + bh], fill="#444")
    cx = bx + int(bw * PROG)
    d.rectangle([bx, by, cx, by + bh], fill="#1DB954")
    d.ellipse([cx - 8, by - 6, cx + 8, by + 10], fill="#FFF")
    py = cpos[1] + H - 80
    cx = cpos[0] + W // 2
    sz = 15
    shuf(d, cx - 120, py, sz)
    tri(d, cx - 60, py, sz, dir='l')
    pause(d, cx, py, sz)
    tri(d, cx + 60, py, sz)
    rpt(d, cx + 120, py, sz)
    vx, vy = cpos[0] + PAD, cpos[1] + H - 40
    vw = 150
    d.text((vx, vy - 5), "Vol:", font=f2, fill="#AAA")
    seg = 7
    sw, sg = 10, 5
    for i in range(seg):
        sh = (i + 1) * 4
        col = "#1DB954" if i < seg - 1 else "#FFF"
        d.rectangle([
            vx + 50 + i * (sw + sg),
            vy - sh // 2,
            vx + 50 + i * (sw + sg) + sw,
            vy + sh // 2
        ], fill=col)
    d.text((vx + vw + 10, vy - 5), "100%", font=f2, fill="#AAA")
    cv.convert("RGB").save(OUT)
    print("Saved:", OUT)
    cv.show()
run()
