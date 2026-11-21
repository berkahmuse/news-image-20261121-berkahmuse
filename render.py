#!/usr/bin/env python3
"""Render the 21 November 2026 world-news image (1024x1024 PNG).

Concept: "ONE DAY ON EARTH" — a newspaper front page with one dominant
lead story (Bitcoin's crash below $60,000) and four illustrated story
cards, plus an "also today" ticker.

FIX NOTE (21 Nov 2026): the first build of this entry FAILED independent
verification because 5 of its 8 stories were events of 20 November, not
the 21st (Russia-strikes lead, S&P 500 rout, UK-EU deals, pancreatic-
cancer pill ticker, Gen Z protests ticker). Those 5 were replaced with
the stories below; the COP31, Houthi and Peru stories were kept (the
verifier confirmed them as 21 November). Every story in this version,
with the date evidence checked before rendering:

- LEAD (Markets): Bitcoin crashes below $60,000 — CoinGecko 06:06 UTC
  Sat 21 Nov: $55,684, -9.96% in 24h, lowest since Sept 2024; 24h
  liquidations $1.76B (BeInCrypto) to nearly $2.4B (CryptoPotato /
  The Defiant). Sources: bitcoinfoundation.org, trustscrypto.com.
- SPORT: F1 Las Vegas GP — race night Sat 21 Nov (20:00 PST, 50 laps,
  Las Vegas Strip Circuit); Verstappen on pole after fastest qualifier
  Antonelli took a 5-place grid penalty. Sources: Reuters 21 Nov,
  formula1.com. (Preview only — the race had not run at build time.)
- UNITED NATIONS: CCW "killer robot" talks in Geneva end Sat 21 Nov
  (~03:00 GMT) in a weak, non-binding deal: a two-year mandate to
  elaborate rules by 2028; ~100 states backed binding rules, the US,
  Russia and Israel opposed. Source: Reuters 21 Nov.
- CLIMATE: COP31 (Antalya) talks run past their Friday deadline —
  closing plenary suspended 22:29 Fri, third draft and plenary continue
  Sat 21 Nov. Sources: AP / TBS News, The Climate Watch.
- MIDDLE EAST: Saudi-led coalition intercepts 3 Houthi ballistic
  missiles aimed at Riyadh in the early hours of Sat 21 Nov, the third
  night running. Source: Reuters 21 Nov.
- TICKER: M6.7 quake in central Peru — 19:09 Peru time Fri 20 Nov =
  00:09 GMT Sat 21 Nov (AP; China Daily). Fire at the Hartha power
  station, Basra, Sat 21 Nov kills at least 4, injures 30 (Reuters,
  dateline Basra, Nov 21).

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


def draw_bitcoin(d, x0, y0, w, h):
    """Lead art: dark navy panel, a big gold coin with a bold B and two
    vertical strokes (no bitcoin glyph in DejaVu), a red falling line
    and a -10% label. Contained in the (x0, y0, w, h) box."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(13, 20, 38))
    # faint chart gridlines
    for gy in (52, 104, 156, 208):
        d.line([x0 + 196, y0 + gy, x0 + w - 14, y0 + gy],
               fill=(38, 52, 82), width=2)
    # gold coin
    cx, cy, r = x0 + 100, y0 + h // 2, 76
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 181, 36),
              outline=(184, 128, 20), width=5)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10],
              outline=(184, 128, 20), width=3)
    # the two vertical strokes of the bitcoin B, peeking above/below
    for bx in (cx - 13, cx + 13):
        d.line([bx, cy - 56, bx, cy + 56], fill=(13, 20, 38), width=8)
    d.text((cx, cy), "B", font=font(FONT_B, 96), fill=(13, 20, 38),
           anchor="mm")
    # red falling line + arrowhead
    pts = [(x0 + 210, y0 + 48), (x0 + 268, y0 + 84), (x0 + 318, y0 + 76),
           (x0 + 368, y0 + 132), (x0 + 408, y0 + 168)]
    d.line(pts, fill=RED, width=6, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex + 6, ey + 8), (ex - 14, ey + 4), (ex + 2, ey - 12)],
              fill=RED)
    d.text((x0 + 282, y0 + 196), "-10%", font=font(FONT_B, 40), fill=RED)


def draw_f1(d, x0, y0, w, h):
    """Chequered flag (8x4) on a pole, speed lines, '50 LAPS' in gold."""
    # pole
    d.line([x0 + 8, y0 + 4, x0 + 8, y0 + 84], fill=INK, width=4)
    # chequered flag
    fx, fy, cell = x0 + 12, y0 + 6, 16
    for row in range(4):
        for col in range(8):
            if (row + col) % 2 == 0:
                d.rectangle([fx + col * cell, fy + row * cell,
                             fx + (col + 1) * cell, fy + (row + 1) * cell],
                            fill=INK)
    d.rectangle([fx, fy, fx + 8 * cell, fy + 4 * cell], outline=INK, width=2)
    # speed lines
    for i, (off, ln) in enumerate([(94, 118), (106, 88), (118, 104)]):
        d.line([x0 + 14, y0 + off, x0 + 14 + ln, y0 + off],
               fill=(156, 163, 175), width=5)
    d.text((x0 + 12, y0 + h - 28), "50 LAPS", font=font(FONT_B, 24),
           fill=GOLD)


def draw_un(d, x0, y0, w, h):
    """Simple robot in blue outline: round head, antenna, two eyes, body."""
    # antenna
    d.line([x0 + 75, y0 + 34, x0 + 75, y0 + 16], fill=BLUE, width=4)
    d.ellipse([x0 + 69, y0 + 4, x0 + 81, y0 + 16], outline=BLUE, width=4)
    # ears
    d.rectangle([x0 + 28, y0 + 58, x0 + 38, y0 + 82], outline=BLUE, width=4)
    d.rectangle([x0 + 112, y0 + 58, x0 + 122, y0 + 82], outline=BLUE, width=4)
    # head
    d.rounded_rectangle([x0 + 36, y0 + 32, x0 + 114, y0 + 98], radius=18,
                        outline=BLUE, width=4)
    # eyes
    for ex in (x0 + 60, x0 + 90):
        d.ellipse([ex - 6, y0 + 58, ex + 6, y0 + 70], fill=BLUE)
    # mouth
    d.line([x0 + 62, y0 + 84, x0 + 88, y0 + 84], fill=BLUE, width=4)
    # neck + body
    d.line([x0 + 75, y0 + 98, x0 + 75, y0 + 106], fill=BLUE, width=4)
    d.rounded_rectangle([x0 + 46, y0 + 106, x0 + 104, y0 + 144], radius=10,
                        outline=BLUE, width=4)
    d.ellipse([x0 + 69, y0 + 118, x0 + 81, y0 + 130], fill=BLUE)


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
    draw_bitcoin(d, lx + 14, ly + 22, 430, 272)
    tx = lx + 470
    d.text((tx, ly + 22), "LEAD STORY  —  MARKETS",
           font=font(FONT_B, 22), fill=RED)
    head = wrap(d, "BITCOIN CRASHES BELOW $60,000",
                font(FONT_B, 36), lw - 496)
    y = text_block(d, tx, ly + 54, head, font(FONT_B, 36), INK, 42)
    y = text_block(d, tx, y + 6,
                   wrap(d, "Down 10% in a day, lowest since Sept 2024.",
                        font(FONT_B, 22), lw - 496),
                   font(FONT_B, 22), (60, 60, 60), 27)
    text_block(d, tx, y + 8,
               wrap(d, "Nearly $2.4B in leveraged bets wiped out as the "
                       "crypto sell-off deepens.",
                    font(FONT_R, 19), lw - 496),
               font(FONT_R, 19), (70, 70, 70), 24)

    # ---------- four story cards ----------
    cards = [
        ("SPORT", RED, draw_f1,
         "F1 UNDER THE LIGHTS IN VEGAS",
         "Verstappen on pole for tonight's 50-lap race on the Strip."),
        ("UNITED NATIONS", BLUE, draw_un,
         "UN DELAYS 'KILLER ROBOT' RULES TO 2028",
         "Geneva talks end in weak deal; no binding ban on autonomous weapons."),
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
    ticker = ("6.7 quake shakes central Peru   •   "
              "Fire at Basra power station kills at least 4")
    text_block(d, 24, 962, wrap(d, ticker, font(FONT_R, 20), W - 48),
               font(FONT_R, 20), (235, 235, 235), 24)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
