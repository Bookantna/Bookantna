"""Build the profile SVGs.

Reads templates from src/, embeds a per-file subset of Geist and Geist Mono
(SIL OFL, see scripts/fonts/OFL.txt) as base64 WOFF2, and writes to assets/.
SVGs loaded through <img> cannot fetch external fonts, so embedding is the
only way to get real typography on a GitHub README.

    python scripts/build.py
"""

import base64
import html
import io
import json
import re
from datetime import date
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "assets"
FONTS = ROOT / "scripts" / "fonts"

FAMILIES = {
    "Geist": FONTS / "Geist-Variable.ttf",
    "Geist Mono": FONTS / "GeistMono-Variable.ttf",
}

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


LEVEL_FILL = ["#1d1c1a", "#5a4320", "#8a6327", "#b98232", "#e2a03f"]
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def load_activity():
    path = ROOT / "data" / "activity.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def heatmap(act, x, y, pitch, cell):
    cols = []
    for i, week in enumerate(act["weeks"]):
        rects = "".join(
            f'<rect x="{x + i * pitch}" y="{y + date.fromisoformat(d["date"]).isoweekday() % 7 * pitch}" '
            f'width="{cell}" height="{cell}" rx="1.5" fill="{LEVEL_FILL[d["level"]]}"/>'
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
        f'<rect x="{x - 40 - (4 - i) * 11}" y="{y - 8}" width="8" height="8" rx="1.5" fill="{f}"/>'
        for i, f in enumerate(LEVEL_FILL)
    )
    return (
        f'<text x="{x - 100}" y="{y}" text-anchor="end">LESS</text>{swatches}'
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


def font_face(family, path, chars):
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
        f"@font-face{{font-family:'{family}';font-weight:100 900;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    )


def build(path):
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(
        r"\{\{BARCODE (\S+) (\S+) (\S+) (\S+) (\S+)\}\}",
        lambda m: barcode(float(m[1]), float(m[2]), float(m[3]), m[4], m[5]),
        svg,
    )
    if "{{HEATMAP" in svg:
        act = load_activity()
        if act is None:
            print(f"skip {path.name}: run scripts/fetch_activity.py first")
            return
        svg = fill_activity(svg, act)
    chars = used_chars(svg)
    faces = "".join(font_face(f, p, chars) for f, p in FAMILIES.items())
    svg = svg.replace("/*FONTS*/", faces)
    out = OUT / path.name
    out.write_text(svg, encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in sorted(SRC.glob("*.svg")):
        build(p)
