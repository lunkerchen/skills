#!/usr/bin/env python3
"""Generate routing-demo.gif — README two-stage routing demo.
Regenerate: python3 docs/assets/make_routing_gif.py (Pillow only)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 880, 520
OUT = Path(__file__).resolve().parent / "routing-demo.gif"
BG, PANEL, BORDER = (11, 18, 32), (17, 26, 46), (30, 42, 68)
TEXT, DIM, CYAN = (226, 232, 240), (124, 140, 166), (56, 189, 248)
SWEEP = (30, 58, 95)
GBG, GFILL, GLINE = (6, 78, 59), (167, 243, 208), (52, 211, 153)
MATCH = 0  # seo-geo-suite
ROUTES = [
    ("seo-geo-suite", "SEO/GEO/AEO"),
    ("fde-adoption-suite", "企業 AI 導入"),
    ("content-writing-suite", "文字內容"),
    ("multimedia-repurpose-suite", "多媒體轉製"),
    ("frontend-design-suite", "前端設計"),
    ("blueprint-concrete-design", "建築設計"),
    ("code-quality-suite", "代碼品質"),
    ("cloud-workers-suite", "Workers/MCP"),
    ("messaging-bots-suite", "企業通訊"),
    ("system-watchdog-suite", "監控/紅隊"),
    ("sync-lark-wiki", "獨立技能"),
    ("labangram-agent", "獨立技能"),
]
_MENLO = "/System/Library/Fonts/Menlo.ttc"
_CJK = ("/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc")


def mono(size, bold=False):
    if bold:
        for i in (1, 2, 3):
            try:
                return ImageFont.truetype(_MENLO, size, index=i)
            except OSError:
                continue
    return ImageFont.truetype(_MENLO, size, index=0)


def cjk(size):
    for p in _CJK:
        try:
            return ImageFont.truetype(p, size, index=0)
        except OSError:
            continue
    return mono(size)


def panel(d, box, title=None, title_fill=DIM):
    d.rounded_rectangle(box, radius=8, fill=PANEL, outline=BORDER, width=1)
    if title:
        d.text((box[0] + 16, box[1] + 12), title, font=mono(11, True), fill=title_fill)


def rtext(d, right, y, s, font, fill):
    d.text((right - d.textlength(s, font=font), y), s, font=font, fill=fill)


def build(s):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((28, 24), "lunkerchen/skills", font=mono(15, True), fill=CYAN)
    rtext(d, W - 28, 27, "two-stage routing · SKILL.md", mono(11), DIM)
    d.line([(28, 50), (W - 28, 50)], fill=BORDER, width=1)
    panel(d, (28, 62, W - 28, 136))
    d.text((44, 72), "PROMPT", font=mono(10, True), fill=DIM)
    d.text((44, 90), "> Audit our site for GEO and agent readiness",
           font=mono(14), fill=TEXT)
    d.text((44, 112), "> 幫我做全站 GEO 與代理就緒審計", font=cjk(14), fill=DIM)
    d.text((28, 494), "npx skills add https://github.com/lunkerchen/skills.git",
           font=mono(11), fill=DIM)
    if s["arrow"]:
        x = 64
        d.line([(x, 142), (x, 154)], fill=DIM, width=2)
        d.polygon([(x - 5, 152), (x + 5, 152), (x, 160)], fill=DIM)
    if s["router"]:
        panel(d, (28, 164, 528, 470), "SKILL.md · ROOT ROUTER", TEXT)
        rtext(d, 512, 176, "12 rows", mono(10), DIM)
        y = 198
        for i, (name, domain) in enumerate(ROUTES):
            if s["locked"] and i == MATCH:
                d.rounded_rectangle((40, y - 3, 516, y + 15), radius=4, fill=CYAN)
                fn, fd, fill, dfill = mono(12, True), cjk(10), BG, BG
            elif s["sweep"] == i:
                d.rounded_rectangle((40, y - 3, 516, y + 15), radius=4, fill=SWEEP)
                fn, fd, fill, dfill = mono(12), cjk(10), TEXT, TEXT
            else:
                fn, fd, fill, dfill = mono(12), cjk(10), DIM, DIM
            d.text((48, y), name, font=fn, fill=fill)
            rtext(d, 508, y + 1, domain, fd, dfill)
            y += 19
        d.text((40, 440), "stage 1 of 2 · then references/ on demand",
               font=mono(10), fill=DIM)
    if s["right"]:
        title = "MATCHING…" if not s["matched"] else "MATCHED"
        panel(d, (548, 164, W - 28, 470), title, DIM if not s["matched"] else CYAN)
        if not s["matched"]:
            for j, line in enumerate(("scoring prompt…", "12 candidates",
                                      "unique top-1 required")):
                d.text((564, 204 + j * 22), line, font=mono(12), fill=DIM)
        elif s["target"]:
            d.text((564, 204), "skills/seo-geo/", font=mono(12), fill=DIM)
            d.text((564, 224), "seo-geo-suite/", font=mono(13, True), fill=TEXT)
            d.text((564, 246), "SKILL.md", font=mono(13, True), fill=CYAN)
            d.line([(564, 274), (836, 274)], fill=BORDER, width=1)
            d.text((564, 286), "stage 2: references/ on demand",
                   font=mono(11), fill=DIM)
        if s["badge"]:
            d.rounded_rectangle((564, 384, 836, 456), radius=8,
                                fill=GBG, outline=GLINE, width=1)
            s1, s2 = "eval 24/24 PASS", "scan OK · 12 skills covered"
            d.text((564 + (272 - d.textlength(s1, font=mono(15, True))) / 2, 398),
                   s1, font=mono(15, True), fill=GFILL)
            d.text((564 + (272 - d.textlength(s2, font=mono(10))) / 2, 428),
                   s2, font=mono(10), fill=DIM)
    return img


def state(**o):
    b = dict(arrow=True, router=True, right=True, sweep=None, locked=False,
             matched=False, target=False, badge=False)
    b.update(o)
    return b


STATES = [state(right=False), state()] \
    + [state(sweep=i) for i in range(12)] \
    + [state(sweep=0, locked=True, matched=True),
       state(locked=True, matched=True, target=True),
       state(locked=True, matched=True, target=True, badge=True)]
DURATIONS = [900, 380] + [85] * 12 + [320, 520, 1700]


def main():
    assert len(STATES) == len(DURATIONS)
    rgb = [build(s) for s in STATES]
    donor = rgb[-1].quantize(colors=64)
    frames = [f.quantize(palette=donor) for f in rgb]
    frames[0].save(OUT, save_all=True, append_images=frames[1:],
                   duration=DURATIONS, loop=0, optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes,", len(frames), "frames")


if __name__ == "__main__":
    main()
