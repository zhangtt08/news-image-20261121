#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 and save news.png.

A newspaper-style summary of the day's world news, drawn with PIL only.
Everything is laid out from fixed geometry, and every paragraph is wrapped
to fit its box before it is drawn, so no text can spill past a card edge.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news.png")

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (24, 24, 24)
NAVY = (20, 38, 74)
GOLD = (232, 182, 76)
GOLD_DARK = (176, 128, 34)
CARD = (255, 255, 255)
RULE = (180, 168, 140)
MUTED = (96, 90, 78)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, spacing=4):
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def chip(draw, x, y, label, bg, fg=(255, 255, 255)):
    fnt = SANS_BOLD(15)
    pad_x, pad_y = 10, 5
    w = int(draw.textlength(label, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), label, font=fnt, fill=fg)
    return w


def story_card(draw, box, story):
    """Draw one story inside box = (x0, y0, x1, y1).

    Headline and summary font sizes shrink step by step until the wrapped
    text fits the card, so nothing can ever spill past the card edge.
    """
    x0, y0, x1, y1 = box
    pad = 16
    inner = x1 - x0 - 2 * pad
    avail = (y1 - y0) - 13 - 32 - 4 - 12  # top pad, chip, gap, bottom pad

    hsize, ssize = story["hsize"], story["ssize"]
    while True:
        head_lines = wrap(draw, story["headline"], SERIF_BOLD(hsize), inner)
        sum_lines = wrap(draw, story["summary"], SANS(ssize), inner)
        need = len(head_lines) * (hsize + 2) + 4 + len(sum_lines) * (ssize + 3)
        if need <= avail or (hsize <= 20 and ssize <= 15):
            break
        if len(head_lines) * (hsize + 2) > avail * 0.45:
            hsize -= 1
        else:
            ssize -= 1

    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                           outline=RULE, width=1)
    cx = x0 + pad
    cy = y0 + 13
    chip(draw, cx, cy, story["chip"], story["color"])
    cy += 32
    cy = draw_wrapped(draw, cx, cy, story["headline"], SERIF_BOLD(hsize),
                      inner, INK, spacing=2)
    cy += 4
    draw_wrapped(draw, cx, cy, story["summary"], SANS(ssize),
                 inner, (58, 54, 46), spacing=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_BOLD(52)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=GOLD)
    date = "Saturday, 21 November 2026"
    df = SANS_BOLD(24)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 76), date, font=df, fill=(255, 255, 255))
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # ---- Lead story -----------------------------------------------------
    lead = {
        "chip": "EUROPE  •  NATO",
        "color": (148, 28, 28),
        "headline": "Poland seeks more NATO air defences after Russian missiles land on its soil",
        "summary": ("Two Russian Kh-101 cruise missiles and a suspected drone crashed in "
                    "south-east Poland during a huge overnight barrage on Ukraine — more than "
                    "400 drones and 110 missiles. Warsaw calls it a deliberate provocation and "
                    "has asked NATO for extra jets and radar; alliance chief Mark Rutte, who "
                    "called it a grave violation, is due in Warsaw on Saturday."),
        "hsize": 33,
        "ssize": 20,
    }
    story_card(d, (24, 138, 1000, 336), lead)

    # ---- 2 x 2 grid ------------------------------------------------------
    grid = [
        {
            "chip": "MARKETS",
            "color": (20, 90, 60),
            "headline": "Asian markets plunge as Wall Street rout spreads",
            "summary": ("Japan's Nikkei fell over 5% after the S&P 500 slid 3.7% and the "
                        "Dow lost 950 points on Friday, both entering correction. The Nasdaq "
                        "has erased all its 2026 gains, and Nvidia fell 14%."),
            "hsize": 25,
            "ssize": 18,
        },
        {
            "chip": "CLIMATE",
            "color": (24, 96, 120),
            "headline": "COP31 runs into overtime over fossil fuels",
            "summary": ("Climate talks in Antalya missed their Friday deadline with no deal: the "
                        "latest draft drops every mention of fossil fuels. A third draft is due "
                        "on Saturday, and Ethiopia was named host of COP32 in Addis Ababa."),
            "hsize": 25,
            "ssize": 18,
        },
        {
            "chip": "SPACE",
            "color": (58, 48, 120),
            "headline": "BepiColombo reaches Mercury after eight years",
            "summary": ("Europe and Japan's twin orbiters entered orbit around Mercury on "
                        "Saturday, only the second mission ever to do so, after a "
                        "10-billion-km journey since their 2018 launch. Science work "
                        "begins in April 2027."),
            "hsize": 25,
            "ssize": 18,
        },
        {
            "chip": "DISASTER",
            "color": (140, 82, 16),
            "headline": "Magnitude 6.7 quake shakes Peru, felt in Lima",
            "summary": ("A deep earthquake struck the Andes near Junin at 00:09 UTC on Saturday, "
                        "sending residents of the capital into the streets. No deaths were "
                        "reported at first; the navy ruled out a tsunami."),
            "hsize": 25,
            "ssize": 18,
        },
    ]
    gx, gy = 24, 352
    cw, chh, gap = 480, 196, 16
    for i, story in enumerate(grid):
        x0 = gx + (i % 2) * (cw + gap)
        y0 = gy + (i // 2) * (chh + gap)
        story_card(d, (x0, y0, x0 + cw, y0 + chh), story)

    # ---- Bottom story ---------------------------------------------------
    bottom = {
        "chip": "BRAZIL",
        "color": (120, 40, 90),
        "headline": "Bolsonaro taken to hospital with intestinal obstruction",
        "summary": ("Brazil's former president, 71, was taken to a Brasilia hospital with severe "
                    "abdominal pain and a near-complete intestinal obstruction. He is under house "
                    "arrest serving a 27-year sentence over a coup plot; doctors say he is stable "
                    "and being treated without surgery for now."),
        "hsize": 27,
        "ssize": 19,
    }
    story_card(d, (24, 776, 1000, 946), bottom)

    # ---- Footer ----------------------------------------------------------
    d.line([24, 962, 1000, 962], fill=RULE, width=1)
    foot = ("Sources: AP, Reuters, CNN, BBC, The Guardian, France 24, Al Jazeera, "
            "WSJ, ESA / JAXA, USGS  •  Saturday, 21 November 2026")
    ff = SANS(15)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 974), foot, font=ff, fill=MUTED)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
