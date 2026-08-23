# OG Image via SVG + macOS QLManage

Alternative to the headless-Chrome approach (`og-image-generation.md`). This pipeline uses a native macOS tool (`qlmanage`) to render SVG directly, with no browser dependency.

## Trade-offs vs HTML+Chrome

| Dimension | SVG + qlmanage | HTML + Chrome |
|---|---|---|
| Dependencies | macOS only (qlmanage + Pillow) | Chrome (any OS) |
| Font support | Web-safe / system fonts only | Google Fonts, custom web fonts |
| Animation / JS | None (static SVG) | Full JS/CSS power |
| Output control | Good (sharp pixel render) | Excellent (virtual-time-budget) |
| Version-control asset | SVG (editable, text) | HTML (editable, text) + PNG (binary) |

Use SVG pipeline when your OG design is purely vector — logo, decorative shapes, brand colors, text with web-safe/system fonts. Use HTML+Chrome when you need custom web fonts, complex layout, or animated elements.

## Pipeline

### 1. Design the SVG

Create `og.svg` at OG dimensions (typically 1200×630 viewBox):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <!-- Brand accent glow -->
    <radialGradient id="glow" cx="85%" cy="20%" r="55%">
      <stop offset="0%" stop-color="#ff7a1a" stop-opacity=".22"/>
      <stop offset="100%" stop-color="#ff7a1a" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>

  <!-- Decorative LEGO brick studs (example) -->
  <g fill="none" stroke="#ff7a1a" stroke-opacity=".12" stroke-width="1.5">
    <!-- pattern loops of bricks -->
  </g>

  <!-- Brand text -->
  <text x="80" y="240" fill="#e2e8f0" font-family="system-ui,-apple-system,sans-serif" font-size="72" font-weight="800">
    主標題
  </text>
  <text x="80" y="320" fill="#ffb25e" font-family="system-ui,-apple-system,sans-serif" font-size="72" font-weight="800">
    強調關鍵詞
  </text>

  <text x="80" y="390" fill="#8b98ab" font-family="system-ui,-apple-system,sans-serif" font-size="26">
    副標描述 · 重點一 · 重點二
  </text>

  <!-- Decorative SVG element on right -->
  <g transform="translate(700, 80)">
    <!-- brand mascot / decorative vector, e.g. LEGO brick, camera, robot -->
  </g>
</svg>
```

**Design tips for SVG OG:**
- Use `font-family="system-ui,-apple-system,sans-serif"` for the best system-native rendering on macOS
- Text in SVG renders at high quality — no font-loading delay
- Decorative vectors (brick studs, geometric patterns) can be hand-coded or exported from vector editor
- Keep the composition: left text + right glow/decorative element is the standard OG layout

### 2. Render to PNG via QLManage

macOS's `qlmanage` (Quick Look manager) can render SVG files to raster images:

```bash
qlmanage -t -s 1200 -o /tmp brick-loop-og.svg
# Output: /tmp/brick-loop-og.svg.png  (at 1200×something)
```

- `-t` = thumbnail mode
- `-s 1200` = thumbnails are 1200px wide (height auto-proportional)
- `-o /tmp` = output directory

⚠️ **Known issue:** `qlmanage` respects the SVG's `viewBox` aspect ratio. If your `viewBox` is `0 0 1200 630`, the output will be 1200×630. If the SVG has a different aspect ratio, the output height will differ and you'll need to crop.

### 3. Verify and Trim Dimensions

```bash
sips -g pixelWidth -g pixelHeight /tmp/brick-loop-og.svg.png
```

If height ≠ 630, crop/trim with Pillow in the next step.

### 4. Convert to WebP

```bash
python3 -c "
from PIL import Image
img = Image.open('/tmp/brick-loop-og.svg.png')
# Ensure 1200x630
if img.size != (1200, 630):
    # Center-crop to 1200:630 ratio
    target_ratio = 1200 / 630
    w, h = img.size
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    img = img.resize((1200, 630), Image.LANCZOS)
img.save('og-image.webp', 'WEBP', quality=85, method=6)
"
```

Or use `cwebp` from the WebP library:

```bash
cwebp -q 85 -resize 1200 630 /tmp/brick-loop-og.svg.png -o og-image.webp
```

### 5. Verify Final Output

```bash
python3 -c "
from PIL import Image
img = Image.open('og-image.webp')
print(f'{img.size[0]}x{img.size[1]}, {img.format}, {len(open(\"og-image.webp\",\"rb\").read()/1024):.1f}KB')
"
```

`og-image.webp` should be 1200×630 and ideally under 50KB for fast loading in social previews.

### 6. Reference in HTML Head

```html
<meta property="og:image" content="https://domain.tld/og-image.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://domain.tld/og-image.webp">
```

## One-shot Script

Save as `scripts/ogify.sh` in the project:

```bash
#!/usr/bin/env bash
# Usage: ./ogify.sh <input.svg> [output-name.webp]
set -euo pipefail

SVG="${1:?Usage: ogify.sh <input.svg> [output-name.webp]}"
OUT="${2:-og-image.webp}"
TMP_PNG="/tmp/ogify-$$.png"

qlmanage -t -s 1200 -o /tmp "$SVG" >/dev/null 2>&1
# qlmanage appends .svg.png to the filename
mv "/tmp/$(basename "$SVG").png" "$TMP_PNG" 2>/dev/null || true

python3 -c "
from PIL import Image
img = Image.open('$TMP_PNG')
if img.size != (1200, 630):
    target = (1200, 630)
    img.thumbnail(target, Image.LANCZOS)
    bg = Image.new('RGB', target, (10, 10, 20))
    bg.paste(img, ((target[0]-img.size[0])//2, (target[1]-img.size[1])//2))
    img = bg
img.save('$OUT', 'WEBP', quality=85, method=6)
"
rm -f "$TMP_PNG"
echo "→ $OUT ($(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT") bytes)"
sips -g pixelWidth -g pixelHeight "$OUT" 2>/dev/null | tail -2
```

## Pitfalls

- **qlmanage mangles alpha background** — dark/transparent SVGs with alpha channels may render with a light background tint. If so, add an explicit dark `<rect>` as the first child in the SVG.
- **qlmanage waits for user** — `qlmanage -t` is synchronous and returns after the file is written. It does NOT open a preview window (that's `qlmanage -p`). Keep the `-t` flag.
- **font-family fallback** — SVG text uses system fonts. If the text looks wrong (e.g., serif instead of sans-serif), the SVG's `font-family` attribute needs adjustment. macOS's system sans-serif is San Francisco; `system-ui,-apple-system,sans-serif` maps to it.
- **SVG viewBox mismatch** — if the output PNG dimensions don't match expectations, check the `viewBox` attribute. `viewBox="0 0 1200 630"` produces a proper 1200×630 PNG.
