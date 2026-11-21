#!/usr/bin/env python3
"""Render the 21 November 2026 world-news summary image (1024x1024 PNG).

Newspaper front page: masthead "THE WORLD IN ONE PAGE", a large red date
line, four ruled panels with a simple icon each, and an "ALSO TODAY"
bottom strip.

Deterministic: fixed layout, fixed fonts, no randomness, no clock.
The submitted program (main.py) simply copies the PNG this script makes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

W = H = 1024
PAPER = (248, 244, 233)
PANEL_BG = (255, 253, 246)
INK = (20, 20, 20)
RED = (163, 22, 33)
GRAY = (90, 90, 90)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size)


def centered(text, y, fnt, fill=INK):
    d.text(((W - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rule(y, width=3):
    d.line([(36, y), (988, y)], fill=INK, width=width)


def rotated(points, cx, cy, deg):
    a = math.radians(deg)
    return [
        (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
        for x, y in points
    ]


# ---------------- masthead ----------------
rule(26, width=2)
centered("THE WORLD IN ONE PAGE", 40, F(SERIF_B, 60))
rule(122, width=5)
centered("SATURDAY, NOVEMBER 21, 2026", 134, F(SERIF_B, 42), fill=RED)
rule(190, width=2)

# ---------------- icons ----------------

def icon_missile(cx, cy):
    # burst behind
    for a in range(0, 360, 30):
        r = math.radians(a)
        d.line(
            [(cx + 9 * math.cos(r), cy + 9 * math.sin(r)),
             (cx + 38 * math.cos(r), cy + 38 * math.sin(r))],
            fill=RED, width=6,
        )
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
    # missile body, nose, fins, flame (local frame, scaled, rotated -45 deg)
    s = 0.78
    sc = lambda pts: [(x * s, y * s) for x, y in pts]
    d.polygon(rotated(sc([(-52, -11), (18, -11), (18, 11), (-52, 11)]), cx, cy, -45), fill=INK)
    d.polygon(rotated(sc([(18, -11), (52, 0), (18, 11)]), cx, cy, -45), fill=INK)
    d.polygon(rotated(sc([(-52, 11), (-70, 26), (-40, 11)]), cx, cy, -45), fill=INK)
    d.polygon(rotated(sc([(-52, -11), (-70, -26), (-40, -11)]), cx, cy, -45), fill=INK)
    d.polygon(rotated(sc([(-52, -6), (-78, 0), (-52, 6)]), cx, cy, -45), fill=RED)


def icon_target(cx, cy):
    for r in (44, 29, 14):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    for x0, y0, x1, y1 in ((-54, 0, -48, 0), (48, 0, 54, 0), (0, -54, 0, -48), (0, 48, 0, 54)):
        d.line([(cx + x0, cy + y0), (cx + x1, cy + y1)], fill=RED, width=7)


def icon_chart(cx, cy):
    x0, y0, x1, y1 = cx - 78, cy - 42, cx + 78, cy + 42
    d.line([(x0, y0 - 8), (x0, y1), (x1, y1)], fill=INK, width=5)
    pts = [(x0 + 6, y0 + 2), (x0 + 42, y0 + 16), (x0 + 72, y0 + 10),
           (x0 + 108, y0 + 40), (x0 + 142, y0 + 62)]
    d.line(pts, fill=RED, width=8, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx + 6, hy + 8), (hx - 18, hy + 4), (hx - 2, hy - 16)], fill=RED)


def icon_robot(cx, cy):
    d.rounded_rectangle([cx - 56, cy - 40, cx + 56, cy + 44], radius=16, outline=INK, width=8)
    d.line([(cx, cy - 40), (cx, cy - 62)], fill=INK, width=7)
    d.ellipse([cx - 8, cy - 72, cx + 8, cy - 56], fill=RED)
    d.ellipse([cx - 35, cy - 18, cx - 13, cy + 4], fill=INK)
    d.ellipse([cx + 13, cy - 18, cx + 35, cy + 4], fill=INK)
    for i in range(-2, 3):
        d.line([(cx + i * 13 - 4, cy + 20), (cx + i * 13 - 4, cy + 34)], fill=INK, width=5)


ICONS = {"missile": icon_missile, "target": icon_target, "chart": icon_chart, "robot": icon_robot}
ICON_DY = {"missile": -76, "target": -66, "chart": -52, "robot": -52}

# ---------------- panels ----------------
PANELS = [
    dict(x=36, y=208, kicker="WAR IN EUROPE", icon="missile",
         head="RUSSIAN MISSILES LAND IN POLAND",
         sub="NATO calls it a violation as Russian strikes hit Kyiv again overnight."),
    dict(x=524, y=208, kicker="MIDDLE EAST", icon="target",
         head="TRUMP WEIGHS NEW STRIKES ON IRAN",
         sub="Tehran asks for diplomacy; Washington calls its terms unacceptable."),
    dict(x=36, y=564, kicker="MARKETS", icon="chart",
         head="STOCKS SLIDE: S&P 500 FALLS 3.7%",
         sub="Anthropic's $2 trillion stock-market debut stumbles as AI shares slide."),
    dict(x=524, y=564, kicker="TECH & LAW", icon="robot",
         head="UN OPENS PATH TO 'KILLER ROBOT' PACT",
         sub="Negotiators in Geneva open the way to global rules by 2028."),
]
PW, PH = 464, 336

for p in PANELS:
    x, y = p["x"], p["y"]
    d.rectangle([x, y, x + PW, y + PH], fill=PANEL_BG, outline=INK, width=3)
    d.text((x + 22, y + 16), p["kicker"], font=F(SANS_B, 21), fill=RED)
    hy = y + 48
    for line in wrap(p["head"], F(SERIF_B, 36), PW - 44):
        d.text((x + 22, hy), line, font=F(SERIF_B, 36), fill=INK)
        hy += 42
    sy = hy + 6
    for line in wrap(p["sub"], F(SERIF, 21), PW - 44):
        d.text((x + 22, sy), line, font=F(SERIF, 21), fill=GRAY)
        sy += 27
    ICONS[p["icon"]](x + PW // 2, y + PH + ICON_DY[p["icon"]])

# ---------------- bottom strip ----------------
rule(916, width=3)
d.text((36, 928), "ALSO TODAY", font=F(SANS_B, 20), fill=RED)
ALSO = ("COP31 CLIMATE TALKS GO INTO OVERTIME OVER FOSSIL FUELS  \u2022  "
        "USDA & FBI BREACHED BY HACKERS  \u2022  "
        "HONDA & TOYOTA RECALL 1.6 MILLION CARS  \u2022  "
        "MEXICO CAPTURES CARTEL KINGPIN")
ay = 954
for line in wrap(ALSO, F(SANS_B, 19), 952):
    d.text((36, ay), line, font=F(SANS_B, 19), fill=INK)
    ay += 25

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT)
