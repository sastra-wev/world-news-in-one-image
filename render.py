#!/usr/bin/env python3
"""Render the 'World in One Page' front page for Wednesday 18 November 2026.

Draws a 1024x1024 newspaper front page with PIL and saves it as entry.png
next to this script. Deterministic: pure shape/text drawing, no randomness,
no network.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype"
SERIF_BLACK = f"{FD}/noto/NotoSerifDisplay-Black.ttf"
SERIF_XBOLD = f"{FD}/noto/NotoSerifDisplay-ExtraBold.ttf"
SERIF_BOLD = f"{FD}/liberation/LiberationSerif-Bold.ttf"
SERIF = f"{FD}/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = f"{FD}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FD}/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = f"{FD}/liberation/LiberationSans-Bold.ttf"
SANS_BLACK = f"{FD}/noto/NotoSans-Black.ttf"

PAPER = (248, 243, 230)
PANEL = (253, 250, 241)
INK = (22, 24, 30)
MUTED = (92, 90, 80)
RED = (168, 32, 22)
NAVY = (23, 52, 79)
NAVY_D = (15, 38, 60)
GOLD = (198, 152, 62)
CHIP = (239, 231, 211)
SKY = (216, 228, 234)
SEA = (29, 66, 94)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def spaced(d, xy, s, f, fill, spacing=2):
    """Draw text with manual letter spacing; returns total width."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing
    return x - xy[0] - spacing


def spaced_width(d, s, f, spacing=2):
    return sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)


def centered_spaced(d, cx, y, s, f, fill, spacing=2):
    w = spaced_width(d, s, f, spacing)
    spaced(d, (cx - w / 2, y), s, f, fill, spacing)
    return w


def centered(d, cx, y, s, f, fill):
    d.text((cx - tw(d, s, f) / 2, y), s, font=f, fill=fill)


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, path, size, maxw, min_size=10):
    while size > min_size and tw(d, s, F(path, size)) > maxw:
        size -= 2
    return F(path, size)


# ---------------------------------------------------------------- illustrations
def hero_art(d, x0, y0, x1, y1):
    """Flat illustration: Qeshm Island, the strait, a jet and a drone."""
    d.rectangle([x0, y0, x1, y1], fill=(203, 219, 226))
    # sky bands
    d.rectangle([x0, y0, x1, y0 + 46], fill=(188, 208, 219))
    # sun
    sx, sy = x1 - 58, y0 + 40
    d.ellipse([sx - 24, sy - 24, sx + 24, sy + 24], fill=(233, 197, 110))
    d.ellipse([sx - 31, sy - 31, sx + 31, sy + 31], outline=(233, 197, 110), width=3)
    # sea
    sea_y = y0 + int((y1 - y0) * 0.58)
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(7):  # wave strokes
        wy = sea_y + 14 + i * 15
        off = (i % 2) * 26
        for wx in range(x0 + 14 + off, x1 - 30, 74):
            d.arc([wx, wy, wx + 34, wy + 9], 180, 330, fill=(120, 165, 190), width=2)
    # far shore (Bahrain side), right
    d.polygon([(x1 - 96, sea_y), (x1 - 40, sea_y - 13), (x1, sea_y - 6),
               (x1, sea_y + 4), (x1 - 96, sea_y + 4)], fill=(112, 96, 74))
    d.text((x1 - 92, sea_y + 12), "BAHRAIN", font=F(SANS_BOLD, 10), fill=(190, 214, 228))
    # Qeshm island silhouette
    iy = sea_y - 6
    d.polygon([(x0 + 28, iy), (x0 + 92, iy - 26), (x0 + 168, iy - 33),
               (x0 + 252, iy - 20), (x0 + 300, iy - 4), (x0 + 300, iy + 6),
               (x0 + 28, iy + 6)], fill=(58, 52, 44))
    d.text((x0 + 62, iy - 21), "QESHM ISLAND", font=F(SANS_BOLD, 11), fill=(243, 234, 205))
    d.text((x0 + 120, y1 - 22), "STRAIT OF HORMUZ", font=F(SANS_BOLD, 10),
           fill=(150, 188, 208))
    # missile site marker + blast
    bx, by = x0 + 196, iy - 34
    d.rectangle([bx - 12, by + 8, bx + 12, by + 16], fill=(30, 28, 26))
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((bx + r * math.cos(ang), by - r * math.sin(ang) - 2))
    d.polygon(pts, fill=(226, 92, 40))
    d.ellipse([bx - 7, by - 9, bx + 7, by + 5], fill=(245, 178, 66))
    # smoke plume
    for i, (dx, r) in enumerate([(16, 9), (30, 13), (47, 17)]):
        d.ellipse([bx + dx - r, by - 26 - i * 13 - r, bx + dx + r, by - 26 - i * 13 + r],
                  fill=(150, 148, 142))
    # fighter jet silhouette (top-left, flying right)
    jx, jy = x0 + 58, y0 + 34
    d.polygon([(jx, jy + 8), (jx + 26, jy + 2), (jx + 58, jy), (jx + 86, jy + 5),
               (jx + 58, jy + 9), (jx + 30, jy + 12), (jx + 8, jy + 13)], fill=INK)
    d.polygon([(jx + 34, jy + 2), (jx + 48, jy - 9), (jx + 56, jy + 1)], fill=INK)
    d.polygon([(jx + 10, jy + 10), (jx + 2, jy + 20), (jx + 16, jy + 12)], fill=INK)
    for i in range(5):  # contrail dashes
        d.line([jx - 8 - i * 13, jy + 9 + i, jx - 15 - i * 13, jy + 10 + i],
               fill=(240, 244, 246), width=2)
    # drone silhouette (top-right)
    dx_, dy_ = x1 - 158, y0 + 52
    d.rectangle([dx_ - 9, dy_ - 4, dx_ + 9, dy_ + 4], fill=INK)
    d.polygon([(dx_, dy_ + 3), (dx_ - 4, dy_ + 13), (dx_ + 4, dy_ + 13)], fill=INK)
    for a, b in [(-26, -12), (26, -12), (-26, 10), (26, 10)]:
        d.line([dx_, dy_, dx_ + a, dy_ + b], fill=INK, width=2)
        d.ellipse([dx_ + a - 5, dy_ + b - 2, dx_ + a + 5, dy_ + b + 2], outline=INK, width=2)
    # dashed attack arc from drone toward Bahrain shore
    for t in range(0, 8):
        a = math.pi * (0.08 + 0.05 * t)
        px = dx_ + 62 * math.sin(a) + t * 4
        py = dy_ + 58 * (1 - math.cos(a)) + t * 5
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)


def bridge_art(d, x0, y0, x1, y1):
    """Kerch bridge: one span dropped into the strait."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    wy = y1 - 15
    d.rectangle([x0, wy, x1, y1], fill=SEA)
    for wx in range(x0 + 8, x1 - 26, 52):
        d.arc([wx, wy + 4, wx + 26, wy + 11], 180, 330, fill=(120, 165, 190), width=2)
    deck = y0 + 24
    # towers
    for tx in (x0 + 92, x0 + 268):
        d.rectangle([tx, deck - 16, tx + 9, wy], fill=NAVY_D)
    # arch between towers
    d.arc([x0 + 92, deck - 30, x0 + 277, deck + 24], 180, 360, fill=NAVY_D, width=4)
    # intact deck left + right stubs
    d.rectangle([x0, deck, x0 + 196, deck + 6], fill=NAVY_D)
    d.rectangle([x0 + 300, deck, x1, deck + 6], fill=NAVY_D)
    # broken ends
    d.polygon([(x0 + 196, deck), (x0 + 210, deck + 3), (x0 + 196, deck + 7)], fill=RED)
    d.polygon([(x0 + 300, deck), (x0 + 288, deck + 4), (x0 + 300, deck + 7)], fill=RED)
    # fallen span, tilted in the water
    cx, cy = x0 + 248, wy - 8
    seg = [(-52, -5), (52, -12), (52, -5), (-52, 2)]
    d.polygon([(cx + px, cy + py) for px, py in seg], fill=(38, 44, 54))
    for sx_ in (-30, 0, 30):  # splash
        d.line([cx + sx_, cy - 4, cx + sx_ - 5, cy - 15], fill=(225, 238, 244), width=2)
        d.line([cx + sx_, cy - 4, cx + sx_ + 5, cy - 15], fill=(225, 238, 244), width=2)
    d.text((x0 + 10, y0 + 6), "KERCH STRAIT", font=F(SANS_BOLD, 10), fill=NAVY)


def flag(d, x, y, w, h, kind):
    if kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=(176, 42, 42) if i % 2 == 0 else (240, 238, 232))
        d.rectangle([x, y, x + w * 0.44, y + h * 4 / 7], fill=NAVY)
        for r in range(3):
            for c in range(4):
                d.ellipse([x + 3 + c * 7, y + 3 + r * 5, x + 5 + c * 7, y + 5 + r * 5],
                          fill=(255, 255, 255))
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(206, 32, 32))
        d.polygon([(x + 6, y + 9), (x + 9, y + 3), (x + 12, y + 9), (x + 7, y + 7),
                   (x + 11, y + 7)], fill=(250, 210, 60))
        for dx_, dy_ in [(15, 4), (18, 8), (18, 13), (15, 16)]:
            d.ellipse([x + dx_, y + dy_, x + dx_ + 3, y + dy_ + 3], fill=(250, 210, 60))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h / 3], fill=(240, 240, 240))
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(30, 70, 160))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 32, 32))
    d.rectangle([x, y, x + w, y + h], outline=(20, 20, 20), width=1)


def city_art(d, x0, y0, x1, y1):
    """Shenzhen skyline at dusk with the US, China and Russia flags."""
    d.rectangle([x0, y0, x1, y1], fill=(38, 54, 84))
    d.rectangle([x0, y0, x1, y0 + 14], fill=(52, 70, 104))
    base = y1
    towers = [(6, 30, 34), (44, 20, 48), (86, 38, 28), (122, 24, 54), (164, 34, 38),
              (204, 22, 46), (240, 36, 30), (282, 26, 50), (322, 32, 36), (362, 24, 44),
              (398, 30, 32)]
    for tx, twd, th in towers:
        d.rectangle([x0 + tx, base - th, x0 + tx + twd, base], fill=(16, 24, 38))
        for wy_ in range(base - th + 5, base - 5, 8):
            for wx_ in range(x0 + tx + 4, x0 + tx + twd - 4, 8):
                if (wx_ * 7 + wy_ * 13) % 5 == 0:
                    d.rectangle([wx_, wy_, wx_ + 3, wy_ + 4], fill=(250, 205, 100))
    # flags on poles, upper area
    for i, kind in enumerate(("us", "cn", "ru")):
        fx = x1 - 148 + i * 48
        d.line([fx, y0 + 8, fx, y0 + 34], fill=(220, 220, 220), width=2)
        flag(d, fx + 2, y0 + 8, 34, 22, kind)
    d.text((x0 + 10, y0 + 6), "SHENZHEN", font=F(SANS_BOLD, 10), fill=(200, 216, 235))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX, RX = 36, 988  # margins

    # dateline bar
    f_date = F(SANS_BOLD, 15)
    d.text((MX, 24), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date, fill=INK)
    r = "ONE IMAGE · THE WHOLE WORLD"
    d.text((RX - tw(d, r, f_date), 24), r, font=f_date, fill=INK)
    d.rectangle([MX, 50, RX, 53], fill=INK)
    d.line([MX, 58, RX, 58], fill=INK, width=1)

    # masthead
    mast = "THE WORLD IN ONE PAGE"
    f_mast = fit(d, mast, SERIF_BLACK, 96, RX - MX)
    centered(d, 512, 66, mast, f_mast, INK)
    d.line([MX, 158, RX, 158], fill=INK, width=1)
    centered_spaced(d, 512, 166, "SIXTEEN STORIES · SIX REGIONS · ONE IMAGE",
                    F(SANS_BLACK, 16), RED, spacing=3)
    d.rectangle([MX, 192, RX, 195], fill=INK)

    # ---------------- hero panel
    hy0, hy1 = 203, 499
    d.rectangle([MX, hy0, RX, hy1], fill=PANEL)
    d.rectangle([MX, hy0, RX, hy1], outline=INK, width=2)
    hero_art(d, MX + 14, hy0 + 14, MX + 424, hy1 - 14)
    tx = MX + 446
    tw_max = RX - tx - 16
    spaced(d, (tx, hy0 + 16), "1 · MIDDLE EAST — CONFLICT", F(SANS_BLACK, 15), RED, 2)
    f_h = F(SERIF_BOLD, 40)
    y = hy0 + 44
    for ln in wrap(d, "US and Iran Trade Fire Over the Gulf", f_h, tw_max):
        d.text((tx, y), ln, font=f_h, fill=INK)
        y += 48
    f_b = F(SANS, 18)
    body = ("US jets struck an IRGC missile site on Qeshm Island after Iranian "
            "drones hit US radar sites in Bahrain — the third attack in a week. "
            "Kuwait's Ali Al Salem base was targeted, a missile bound for Riyadh "
            "was destroyed, and Trump says a reported Iranian 'dirty bomb' plot "
            "is being taken seriously.")
    y += 4
    for ln in wrap(d, body, f_b, tw_max):
        d.text((tx, y), ln, font=f_b, fill=(40, 42, 48))
        y += 24

    # ---------------- two panels
    py0, py1 = 511, 703
    pw = (RX - MX - 12) // 2
    panels = [
        ("2 · EUROPE — WAR IN UKRAINE", bridge_art,
         "Crimea Bridge Span Falls Into the Sea",
         "Ukraine hit the Kerch Bridge for a second day amid its biggest drone "
         "attack of the war; Russia pounded bridges in Kyiv."),
        ("3 · ASIA — DIPLOMACY", city_art,
         "Three Leaders, One City: Shenzhen",
         "APEC opens as Xi warns on protectionism and meets Putin. Trump, fresh "
         "from the QUAD summit in Manila, flies in for tomorrow's first "
         "US–China–Russia summit."),
    ]
    for i, (tag, art, head, body) in enumerate(panels):
        px0 = MX + i * (pw + 12)
        px1 = px0 + pw
        d.rectangle([px0, py0, px1, py1], fill=PANEL)
        d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
        art(d, px0 + 12, py0 + 10, px1 - 12, py0 + 66)
        spaced(d, (px0 + 14, py0 + 76), tag, F(SANS_BLACK, 13), RED, 1)
        f_ph = F(SERIF_BOLD, 26)
        y = py0 + 97
        for ln in wrap(d, head, f_ph, pw - 28):
            d.text((px0 + 14, y), ln, font=f_ph, fill=INK)
            y += 30
        f_pb = F(SANS, 14)
        for ln in wrap(d, body, f_pb, pw - 28):
            d.text((px0 + 14, y), ln, font=f_pb, fill=(40, 42, 48))
            y += 19

    # ---------------- more of the day
    my = 713
    d.line([MX, my + 8, MX + 300, my + 8], fill=INK, width=1)
    spaced(d, (MX + 312, my), "MORE OF THE DAY", F(SANS_BLACK, 16), INK, 2)
    d.line([MX + 520, my + 8, RX, my + 8], fill=INK, width=1)

    chips = [
        ("4", "AMERICAS", "Peltola wins Alaska; Democrats take 56 Senate seats"),
        ("5", "AFRICA", "Ebola in DR Congo more than doubles: 11,000 cases"),
        ("6", "PACIFIC", "Cyclone Xavier, Cat 5, hits the northern Cook Islands"),
        ("7", "EUROPE", "Russian military plane crashes in Siberia: 19 dead"),
        ("8", "ASIA", "North Korea fires missile toward the Sea of Japan"),
        ("9", "MIDDLE EAST", "New Knesset sworn in amid coalition deadlock"),
        ("10", "JUSTICE", "World Court to rule on Myanmar's genocide case"),
        ("11", "EUROPE", "2,331 migrants reach El Hierro in record weekend"),
        ("12", "MARKETS", "China's AI bubble bursts; STAR 50 nearly halves"),
        ("13", "TECH", "Microsoft unveils seven in-house AI models"),
    ]
    gy = 742
    rh = 41
    colw = (RX - MX - 24) // 2
    d.line([512, gy - 4, 512, gy + 5 * rh - 2], fill=(196, 188, 168), width=1)
    for idx, (num, region, head) in enumerate(chips):
        cx0 = MX + (idx % 2) * (colw + 24)
        cy = gy + (idx // 2) * rh
        if idx // 2 > 0:
            d.line([cx0, cy - 6, cx0 + colw, cy - 6], fill=(216, 208, 188), width=1)
        # number disc
        d.ellipse([cx0, cy + 2, cx0 + 25, cy + 27], fill=RED)
        f_n = F(SANS_BLACK, 13 if len(num) == 1 else 11)
        centered(d, cx0 + 12.5, cy + 6, num, f_n, (255, 255, 255))
        spaced(d, (cx0 + 36, cy), region, F(SANS_BLACK, 11), NAVY, 1)
        d.text((cx0 + 36, cy + 15), head, font=F(SANS_BOLD, 15), fill=INK)

    # ---------------- also today + numbers band + footer
    ay = gy + 5 * rh + 6
    centered(d, 512, ay,
             "Also today: US measles cases hit a 40-year high · MS Dhoni retires "
             "from the IPL · Cyclone Akvan bears down on India's Andhra coast",
             F(SERIF_IT, 15), MUTED)
    by0 = ay + 26
    d.rectangle([MX, by0, RX, by0 + 42], fill=NAVY)
    centered_spaced(d, 512, by0 + 6,
                    "THE DAY IN NUMBERS — 11,000 EBOLA CASES · 19 DEAD IN SIBERIA · "
                    "$92.76 BRENT · 2,331 ARRIVALS AT EL HIERRO",
                    F(SANS_BOLD, 13), (255, 255, 255), spacing=1)
    centered_spaced(d, 512, by0 + 25,
                    "EVERY STORY AS REPORTED ON WEDNESDAY 18 NOVEMBER 2026",
                    F(SANS, 10), (178, 198, 216), spacing=2)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
