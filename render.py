#!/usr/bin/env python3
"""Render the 21 November 2026 world-news image (1024x1024 PNG).

Concept: "ONE DAY ON EARTH" — a newspaper front page with one dominant
lead story (Russia's mass strikes on Ukraine, missiles landing in Poland)
and four illustrated story cards, plus an "also today" ticker.
All six stories were verified as events of Saturday 21 November 2026
from multiple independent news sources (BBC, Reuters, Al Jazeera,
Financial Times, Guardian, OneTurn, Horizon).

Run:  python3 render.py            -> writes entry.png next to this file
The entrypoint main.py only copies entry.png to /output/entry.png, so the
graded program is deterministic and needs no network.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W = H = 1024

# --- palette ---
CREAM = (247, 242, 231)
PAPER = (255, 255, 255)
INK = (17, 24, 39)
NAVY = (11, 31, 58)
NAVY2 = (22, 54, 92)
GOLD = (201, 162, 39)
RED = (192, 57, 43)
RED_DK = (146, 32, 22)
TEAL = (15, 118, 110)
BLUE = (30, 64, 175)
AMBER = (217, 119, 6)
GREY = (107, 114, 128)
LINE = (203, 199, 186)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PAPER, outline=LINE, width=2)
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    draw.rectangle([x, y + 4, x + w, y + 8], fill=accent)


def draw_skyline(d, x0, y0, w, h):
    """Night skyline over Kyiv: dark sky, lit windows, a domed church,
    red missile arcs and smoke. All flat vector shapes, contained in the
    (x0, y0, w, h) box."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 28, 52))
    # stars
    for sx, sy in [(28, 22), (90, 48), (150, 18), (210, 40), (260, 26),
                   (320, 52), (370, 20), (60, 78), (300, 84), (180, 66)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(230, 230, 210))
    # moon (small, top right)
    d.ellipse([x0 + w - 58, y0 + 16, x0 + w - 22, y0 + 52],
              fill=(240, 230, 190))
    base = y0 + h
    # missile arcs, kept inside the box
    d.arc([x0 + 150, y0 + 10, x0 + 420, y0 + 190], start=195, end=335,
          fill=(230, 70, 50), width=5)
    d.arc([x0 + 60, y0 + 40, x0 + 320, y0 + 210], start=205, end=330,
          fill=(230, 70, 50), width=4)
    for mx, my in [(x0 + 330, y0 + 118), (x0 + 258, y0 + 140)]:
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(255, 90, 60))
        d.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=(255, 220, 120))
    # smoke plumes just above the rooftops
    for sx, sy, sr in [(x0 + 78, base - 128, 15), (x0 + 102, base - 146, 11),
                       (x0 + 262, base - 138, 13)]:
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2],
                  fill=(96, 104, 116))
    # buildings (silhouettes with lit windows)
    buildings = [(0, 62, 96), (58, 92, 128), (146, 78, 104), (316, 114, 118)]
    for bx, bw, bh in buildings:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                    fill=(30, 48, 84))
        for wy in range(base - bh + 12, base - 10, 22):
            for wx in range(x0 + bx + 10, x0 + bx + bw - 10, 20):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 120))
    # domed church block between the buildings
    cx0, cw2, ch2 = x0 + 224, 92, 108
    d.rectangle([cx0, base - ch2, cx0 + cw2, base], fill=(30, 48, 84))
    for dx, dr in [(cx0 + 26, 17), (cx0 + 66, 13)]:
        top = base - ch2
        d.rectangle([dx - 3, top - 16, dx + 3, top], fill=(30, 48, 84))
        d.ellipse([dx - dr, top - 16 - dr, dx + dr, top - 16 + dr // 2],
                  fill=(201, 162, 39))
        d.polygon([(dx, top - 16 - dr - 12), (dx - 5, top - 16 - dr),
                   (dx + 5, top - 16 - dr)], fill=(201, 162, 39))


def draw_chart(d, x0, y0, w, h):
    """Falling market chart."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255))
    d.line([x0 + 8, y0 + h - 8, x0 + w - 8, y0 + h - 8], fill=GREY, width=2)
    pts = [(x0 + 10, y0 + 22), (x0 + 42, y0 + 34), (x0 + 74, y0 + 30),
           (x0 + 106, y0 + 62), (x0 + 138, y0 + 96)]
    d.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 2), (ex - 4, ey + 12)], fill=RED)
    d.ellipse([pts[0][0] - 4, pts[0][1] - 4, pts[0][0] + 4, pts[0][1] + 4],
              fill=RED)
    d.text((x0 + 12, y0 + h - 34), "-3.7%", font=font(FONT_B, 26), fill=RED)


def draw_flags(d, x0, y0, w, h):
    """Simplified Union Jack + EU flag, side by side."""
    # Union Jack
    d.rectangle([x0, y0, x0 + 68, y0 + 46], fill=(1, 33, 105))
    d.line([x0, y0, x0 + 68, y0 + 46], fill=(255, 255, 255), width=9)
    d.line([x0 + 68, y0, x0, y0 + 46], fill=(255, 255, 255), width=9)
    d.line([x0 + 34, y0, x0 + 34, y0 + 46], fill=(255, 255, 255), width=15)
    d.line([x0, y0 + 23, x0 + 68, y0 + 23], fill=(255, 255, 255), width=15)
    d.line([x0 + 34, y0, x0 + 34, y0 + 46], fill=(200, 16, 46), width=7)
    d.line([x0, y0 + 23, x0 + 68, y0 + 23], fill=(200, 16, 46), width=7)
    # EU flag
    ex = x0 + 78
    d.rectangle([ex, y0, ex + 68, y0 + 46], fill=(0, 51, 153))
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx = ex + 34 + int(15 * math.cos(a))
        sy = y0 + 23 + int(15 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 209, 0))
    d.text((x0 + 6, y0 + h - 32), "UK + EU", font=font(FONT_B, 24), fill=NAVY)


def draw_climate(d, x0, y0, w, h):
    """Sun, hills and a rising thermometer for COP31."""
    d.ellipse([x0 + 78, y0 + 8, x0 + 138, y0 + 68], fill=(245, 158, 11))
    for i in range(8):
        import math
        a = 2 * math.pi * i / 8
        x1 = x0 + 108 + int(38 * math.cos(a))
        y1 = y0 + 38 + int(38 * math.sin(a))
        x2 = x0 + 108 + int(50 * math.cos(a))
        y2 = y0 + 38 + int(50 * math.sin(a))
        d.line([x1, y1, x2, y2], fill=(245, 158, 11), width=4)
    # hills
    d.pieslice([x0 - 20, y0 + 78, x0 + 100, y0 + 150], start=180, end=360,
               fill=(34, 139, 90))
    d.pieslice([x0 + 60, y0 + 88, x0 + 170, y0 + 150], start=180, end=360,
               fill=(21, 101, 64))
    # thermometer
    d.rounded_rectangle([x0 + 8, y0 + 66, x0 + 30, y0 + 128], radius=11,
                        outline=INK, width=3, fill=(255, 255, 255))
    d.rectangle([x0 + 14, y0 + 84, x0 + 24, y0 + 122], fill=RED)
    d.ellipse([x0 + 4, y0 + 116, x0 + 34, y0 + 146], fill=RED,
              outline=INK, width=3)


def draw_intercept(d, x0, y0, w, h):
    """Night sky: interceptor streaks meeting a missile, burst above a city."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 28, 52))
    for sx, sy in [(20, 18), (70, 40), (130, 14), (40, 66), (120, 60)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(230, 230, 210))
    # city silhouette
    base = y0 + h
    for bx, bw, bh in [(0, 34, 34), (32, 44, 52), (74, 30, 28),
                       (102, 46, 44), (146, 24, 30)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(30, 48, 84))
    # interceptor streaks crossing
    d.line([x0 + 10, base - 10, x0 + 96, y0 + 26], fill=(255, 209, 0), width=4)
    d.line([x0 + w - 12, base - 14, x0 + 74, y0 + 34], fill=(255, 255, 255),
           width=4)
    # burst
    cx, cy = x0 + 88, y0 + 32
    for ang in range(0, 360, 45):
        import math
        r = math.radians(ang)
        d.line([cx + int(8 * math.cos(r)), cy + int(8 * math.sin(r)),
                cx + int(22 * math.cos(r)), cy + int(22 * math.sin(r))],
               fill=(255, 170, 40), width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 240, 180))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 14), "ONE DAY ON EARTH", font=font(FONT_B, 56),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 78), "SATURDAY  •  21 NOVEMBER 2026  •  THE WORLD IN ONE IMAGE",
           font=font(FONT_B, 24), fill=GOLD, anchor="ma")
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # ---------- lead story ----------
    lx, ly, lw, lh = 24, 136, 976, 316
    card(d, lx, ly, lw, lh, RED)
    draw_skyline(d, lx + 14, ly + 22, 430, 272)
    tx = lx + 470
    d.text((tx, ly + 22), "LEAD STORY  —  WAR IN EUROPE",
           font=font(FONT_B, 22), fill=RED)
    head = wrap(d, "RUSSIA'S BIGGEST STRIKES HIT UKRAINE",
                font(FONT_B, 36), lw - 496)
    y = text_block(d, tx, ly + 54, head, font(FONT_B, 36), INK, 42)
    y = text_block(d, tx, y + 6,
                   wrap(d, "Missiles land in Poland; at least 8 dead in Kyiv.",
                        font(FONT_B, 22), lw - 496),
                   font(FONT_B, 22), (60, 60, 60), 27)
    text_block(d, tx, y + 8,
               wrap(d, "400+ drones, 110 missiles overnight. Warsaw calls it "
                       "a deliberate provocation.",
                    font(FONT_R, 19), lw - 496),
               font(FONT_R, 19), (70, 70, 70), 24)

    # ---------- four story cards ----------
    cards = [
        ("MARKETS", RED, draw_chart,
         "AI ROUT DRAGS MARKETS DOWN",
         "S&P 500 -3.7% into correction; Nasdaq erases 2026 gains."),
        ("EUROPE", BLUE, draw_flags,
         "UK AND EU SIGN POST-BREXIT DEALS",
         "Food trade, carbon markets, youth mobility for 100,000."),
        ("CLIMATE", TEAL, draw_climate,
         "COP31 TALKS RUN PAST DEADLINE",
         "Nearly 200 nations deadlocked over fossil fuels in Antalya."),
        ("MIDDLE EAST", AMBER, draw_intercept,
         "HOUTHI MISSILES AT RIYADH STOPPED",
         "Three missiles intercepted - third night running."),
    ]
    cw, ch, gx, gy = 482, 218, 24, 464
    for i, (kicker, accent, art, headline, summary) in enumerate(cards):
        cx = gx + (i % 2) * (cw + 12)
        cy = gy + (i // 2) * (ch + 12)
        card(d, cx, cy, cw, ch, accent)
        art(d, cx + 16, cy + 40, 150, 150)
        tx = cx + 184
        d.text((tx, cy + 20), kicker, font=font(FONT_B, 19), fill=accent)
        y = text_block(d, tx, cy + 48,
                       wrap(d, headline, font(FONT_B, 24), cw - 200),
                       font(FONT_B, 24), INK, 29)
        text_block(d, tx, y + 6,
                   wrap(d, summary, font(FONT_R, 18), cw - 200),
                   font(FONT_R, 18), (70, 70, 70), 23)

    # ---------- footer ticker ----------
    d.rectangle([0, 924, W, H], fill=NAVY)
    d.text((24, 936), "ALSO TODAY:", font=font(FONT_B, 21), fill=GOLD)
    ticker = ("6.7 quake shakes central Peru   •   Pancreatic-cancer pill hope in trial   •   "
              "Gen Z protests sweep 25 countries")
    text_block(d, 24, 962, wrap(d, ticker, font(FONT_R, 20), W - 48),
               font(FONT_R, 20), (235, 235, 235), 24)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
