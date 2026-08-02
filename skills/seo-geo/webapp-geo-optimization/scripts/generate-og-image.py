#!/usr/bin/env python3
"""Generate a 1200×630 OG image for a web app.

Usage:
  python3 generate-og-image.py --name "your-marketplace" --subtitle "Camera Market" \
      --desc "台灣最專業的二手攝影器材 C2C 交易平台" \
      --accent "#EA3B4D" --output public/og-image.png

Requires: Pillow (pip install Pillow)
"""

from PIL import Image, ImageDraw, ImageFont
import os, argparse

def try_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/NotoSansTC-Regular.otf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='Site Name')
    parser.add_argument('--subtitle', default='Subtitle')
    parser.add_argument('--desc', default='Description')
    parser.add_argument('--accent', default='#2563EB')
    parser.add_argument('--bg', default='#0F172A')
    parser.add_argument('--output', default='og-image.png')
    parser.add_argument('--show-lens', action='store_true', default=True)
    args = parser.parse_args()

    w, h = 1200, 630
    bg_rgb = tuple(int(args.bg[i:i+2], 16) for i in (1, 3, 5))
    accent_rgb = tuple(int(args.accent[i:i+2], 16) for i in (1, 3, 5))

    img = Image.new('RGB', (w, h), bg_rgb)
    draw = ImageDraw.Draw(img)

    # Subtle gradient overlay
    for y in range(h):
        alpha = int(40 * (y / h))
        draw.rectangle([(0, y), (w, y)], fill=(30, 41, 59, alpha))

    # Camera lens icon (left side)
    if args.show_lens:
        cx, cy = 200, 315
        for r, w in [(80, 6), (40, 0), (25, 3)]:
            if w == 0:
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=accent_rgb)
            else:
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=accent_rgb, width=w)

    # Title
    title_font = try_font(64)
    sub_font = try_font(24)
    desc_font = try_font(20)

    text_x = 320 if args.show_lens else 100
    draw.text((text_x, 230), args.name, fill='#F1F5F9', font=title_font)
    draw.text((text_x, 310), args.subtitle, fill=accent_rgb, font=sub_font)
    draw.text((text_x, 360), args.desc, fill='#94A3B8', font=desc_font)

    # Accent line
    draw.rectangle([(text_x, 430), (text_x + 200, 434)], fill=accent_rgb)

    img.save(args.output, 'PNG')
    print(f'✅ {args.output} ({os.path.getsize(args.output)} bytes)')

if __name__ == '__main__':
    main()
