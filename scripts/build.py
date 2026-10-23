"""Build the profile SVGs.

Reads templates from src/, embeds a per-file subset of every font family the
file names in its <style> (Bangers, Comic Neue, Geist, Geist Mono; all SIL OFL,
see scripts/fonts/OFL*.txt) as base64 WOFF2, and writes to assets/.
SVGs loaded through <img> cannot fetch external fonts, so embedding is the
only way to get real typography on a GitHub README.

    python scripts/build.py
"""

import base64
import html
import io
import json
import math
import random
import re
from datetime import date
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "assets"
FONTS = ROOT / "scripts" / "fonts"

# (family, file, weight range). A face is embedded only if the SVG mentions
# the family name in quotes, so unused fonts cost nothing.
FACES = [
    ("Bangers", FONTS / "Bangers-Regular.ttf", "400"),
    ("Comic Neue", FONTS / "ComicNeue-Regular.ttf", "400"),
    ("Comic Neue", FONTS / "ComicNeue-Bold.ttf", "700"),
    ("Geist", FONTS / "Geist-Variable.ttf", "100 900"),
    ("Geist Mono", FONTS / "GeistMono-Variable.ttf", "100 900"),
]

# Code 128-B for "BOOKANTNA", start/check/stop included. A real, scannable
# barcode. Generated once with python-barcode: barcode.get("code128", ...).build()
BARCODE_MODULES = (
    "11010010000100010110001000111011010001110110101100011101010001100010111"
    "000110110111000101011100011010100011000111011000101100011101011"
)


def barcode(x, y, module, height, fill):
    """Render the module string as merged <rect> runs."""
    rects, i = [], 0
    while i < len(BARCODE_MODULES):
        if BARCODE_MODULES[i] == "1":
            j = i
            while j < len(BARCODE_MODULES) and BARCODE_MODULES[j] == "1":
                j += 1
            rects.append(
                f'<rect x="{x + i * module:.2f}" y="{y}" '
                f'width="{(j - i) * module:.2f}" height="{height}"/>'
            )
            i = j
        else:
            i += 1
    return f'<g fill="{fill}">' + "".join(rects) + "</g>"


def burst(cx, cy, r_in, r_out, points, seed):
    """Comic starburst outline. Seeded jitter so every burst is lopsided
    in its own way but stable between builds."""
    rng = random.Random(seed)
    pts = []
    for i in range(points * 2):
        a = math.pi * i / points - math.pi / 2 + rng.uniform(-.06, .06)
        r = (r_out * rng.uniform(.86, 1.08)) if i % 2 == 0 else (r_in * rng.uniform(.92, 1.05))
        pts.append(f"{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}")
    return "M" + "L".join(pts) + "Z"


def rays(cx, cy, r_in, r_out, count, seed):
    """Speed lines: thin wedges radiating from a point."""
    rng = random.Random(seed)
    out = []
    for i in range(count):
        a = 2 * math.pi * i / count + rng.uniform(-.05, .05)
        w = rng.uniform(.006, .02)
        r0 = r_in * rng.uniform(1, 1.5)
        p = lambda r, t: f"{cx + r * math.cos(t):.1f} {cy + r * math.sin(t):.1f}"
        out.append(f"M{p(r0, a)}L{p(r_out, a - w)}L{p(r_out, a + w)}Z")
    return "".join(out)


# Contribution levels as halftone dots: radius grows with the level.
LEVEL_R = [1.1, 2.4, 3.1, 3.8, 4.6]
LEVEL_FILL = ["#c9bfa6", "#e4432d", "#e4432d", "#e4432d", "#e4432d"]
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def load_activity():
    path = ROOT / "data" / "activity.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def heatmap(act, x, y, pitch, cell):
    cols = []
    for i, week in enumerate(act["weeks"]):
        c = cell / 2
        rects = "".join(
            f'<circle cx="{x + i * pitch + c:g}" cy="{y + date.fromisoformat(d["date"]).isoweekday() % 7 * pitch + c:g}" '
            f'r="{LEVEL_R[d["level"]] * cell / 10:.2f}" fill="{LEVEL_FILL[d["level"]]}"/>'
            for d in week
        )
        cols.append(f'<g class="col" style="animation-delay:{.3 + i * .018:.3f}s">{rects}</g>')
    return "".join(cols)


def month_labels(act, x, y, pitch):
    out, last = [], -99
    for i, week in enumerate(act["weeks"]):
        first = next((d for d in week if d["date"].endswith("-01")), None)
        if first and i - last >= 3:
            month = MONTHS[int(first["date"][5:7]) - 1]
            out.append(f'<text x="{x + i * pitch}" y="{y}">{month}</text>')
            last = i
    return "".join(out)


def legend(x, y):
    swatches = "".join(
        f'<circle cx="{x - 46 - (4 - i) * 13}" cy="{y - 4}" r="{LEVEL_R[i]}" fill="{f}"/>'
        for i, f in enumerate(LEVEL_FILL)
    )
    return (
        f'<text x="{x - 108}" y="{y}" text-anchor="end">LESS</text>{swatches}'
        f'<text x="{x}" y="{y}" text-anchor="end">MORE</text>'
    )


def fill_activity(svg, act):
    days = [d for w in act["weeks"] for d in w]
    peak = max(days, key=lambda d: d["count"])
    peak_date = date.fromisoformat(peak["date"])
    values = {
        "TOTAL": f"{act['total']:,}",
        "ACTIVE": str(act["active_days"]),
        "LONGEST": str(act["longest"]),
        "PEAK": str(peak["count"]),
        "PEAKDATE": f"{MONTHS[peak_date.month - 1]} {peak_date.day}",
        "UPDATED": act["updated"],
    }
    svg = re.sub(r"\{\{HEATMAP (\S+) (\S+) (\S+) (\S+)\}\}",
                 lambda m: heatmap(act, *map(float, m.groups())), svg)
    svg = re.sub(r"\{\{MONTHS (\S+) (\S+) (\S+)\}\}",
                 lambda m: month_labels(act, *map(float, m.groups())), svg)
    svg = re.sub(r"\{\{LEGEND (\S+) (\S+)\}\}",
                 lambda m: legend(*map(float, m.groups())), svg)
    for k, v in values.items():
        svg = svg.replace("{{" + k + "}}", v)
    return svg


def used_chars(svg):
    body = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    text = "".join(re.findall(r">([^<]+)<", body))
    return set(html.unescape(text)) | {" "}


def font_face(family, path, weight, chars):
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum", "case"]
    opts.name_IDs = []
    opts.notdef_outline = True
    opts.drop_tables += ["meta"]
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    )


def build(path):
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(
        r"\{\{BARCODE (\S+) (\S+) (\S+) (\S+) (\S+)\}\}",
        lambda m: barcode(float(m[1]), float(m[2]), float(m[3]), m[4], m[5]),
        svg,
    )
    svg = re.sub(r"\{\{BURST (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\}\}",
                 lambda m: burst(*map(float, m.groups()[:4]), int(m[5]), int(m[6])), svg)
    svg = re.sub(r"\{\{RAYS (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)\}\}",
                 lambda m: rays(*map(float, m.groups()[:4]), int(m[5]), int(m[6])), svg)
    if "{{HEATMAP" in svg:
        act = load_activity()
        if act is None:
            print(f"skip {path.name}: run scripts/fetch_activity.py first")
            return
        svg = fill_activity(svg, act)
    chars = used_chars(svg)
    faces = "".join(font_face(f, p, w, chars) for f, p, w in FACES if f"'{f}'" in svg)
    svg = svg.replace("/*FONTS*/", faces)
    out = OUT / path.name
    out.write_text(svg, encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in sorted(SRC.glob("*.svg")):
        build(p)
