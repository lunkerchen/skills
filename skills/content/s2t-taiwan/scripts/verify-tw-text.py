#!/usr/bin/env python3
"""Verify SVG image cards contain no Simplified Chinese, and optionally build a contact sheet.

Usage:
  verify-tw-text.py fde-tw-*.svg            # scan <text> nodes across the batch, s2t diff
  verify-tw-text.py fde-tw-*.png            # PIL contact sheet montage for visual QA
  verify-tw-text.py fde-tw-*.svg fde-tw-*.png

Exit code 0 = no simplified chars in any visible text; 1 = hits found.
The SVG scan is DEFINITIVE (s2t is a deterministic per-char map, so 0 diffs = all
Traditional). A positive hit is a candidate to inspect, not a sentence — 台→臺,
只→隻, 看 are known false positives.

NEVER run OpenCC over the whole SVG file — s2twp phrase rules mangle XML tags.
This script extracts only the visible <text> nodes first.

Requires: opencc (opencc-python-reimplemented); Pillow only for PNG contact sheet.
"""
import re
import sys
from pathlib import Path

from opencc import OpenCC


def svg_text_nodes(path):
    return "".join(re.findall(r">([^<>]+)</text>", path.read_text(encoding="utf-8")))


def scan(svg_files):
    cc = OpenCC("s2t")
    bad = []
    for p in sorted(svg_files):
        s = svg_text_nodes(p)
        diffs = [(a, b) for a, b in zip(s, cc.convert(s)) if a != b]
        print(f"{p.name}: {len(s)} visible chars, s2t diffs {len(diffs)} {diffs[:10]}")
        if diffs:
            bad.append(p.name)
    if bad:
        print("SIMPLIFIED CANDIDATES:", ", ".join(bad))
        sys.exit(1)
    print("PASS: no simplified chars in any visible text")


def contact_sheet(png_files, out="contact-sheet.png", cols=4, thumb=(270, 360)):
    from PIL import Image

    files = sorted(png_files)
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (thumb[0] * cols, thumb[1] * rows), "#F8F7F4")
    for i, p in enumerate(files):
        im = Image.open(p).convert("RGB")
        im.thumbnail(thumb)
        sheet.paste(im, ((i % cols) * thumb[0], (i // cols) * thumb[1]))
    sheet.save(out, quality=95)
    print("contact sheet:", out)


if __name__ == "__main__":
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        print(__doc__)
        sys.exit(2)
    svgs = [p for p in paths if p.suffix.lower() == ".svg"]
    pngs = [p for p in paths if p.suffix.lower() == ".png"]
    if svgs:
        scan(svgs)
    if pngs:
        contact_sheet(pngs)
