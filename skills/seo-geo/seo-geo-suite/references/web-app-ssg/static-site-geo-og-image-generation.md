# OG Image Generation — Static Sites

Generate a 1200×630 OG share image from a dedicated HTML template using headless Chrome screenshot. This pattern works for any static site (SSG or single HTML), requires no image editor, and keeps the design in source control as markup.

## The Pattern

1. Create a standalone `og.html` in the project root — a self-contained page at exactly 1200×630.
2. Design it with the same brand colors and typography as the main page.
3. Screenshot it with headless Chrome.
4. Reference the resulting PNG in the site's OG meta tags.

## og.html Template Structure

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500;700;900&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    width:1200px; height:630px; overflow:hidden;
    background:#0a0e14;
    font-family:'Noto Sans TC',sans-serif;
    display:flex; align-items:center; padding:0 80px;
    position:relative;
  }
  /* Gradient glow behind the SVG mascot */
  body::before {
    content:''; position:absolute; right:-180px; top:-180px;
    width:640px; height:640px; border-radius:50%;
    background:radial-gradient(circle, rgba(255,122,26,.22) 0%, transparent 65%);
  }
  .left { position:relative; z-index:1; max-width:720px; }
  .brand { /* logo + brand name row */ }
  h1 { font-size:64px; font-weight:900; }
  .sub { font-size:26px; color:#8b98ab; }
  .tags { display:flex; gap:14px; }
  .tag {
    background:rgba(255,122,26,.14);
    border:1px solid rgba(255,122,26,.35);
    color:#ffb25e; font-size:20px; font-weight:700;
    padding:8px 22px; border-radius:999px;
  }
  /* SVG mascot positioned on right, extending below frame */
  .octo { position:absolute; right:60px; bottom:-40px; width:380px; z-index:0; opacity:.95; }
</style>
</head>
<body>
  <div class="left">
    <div class="brand">[SVG logo] 品牌名稱</div>
    <h1>你的標題<br><span class="accent">關鍵詞</span>強調句</h1>
    <p class="sub">副標描述 · 三項重點 · 用間隔號隔開</p>
    <div class="tags">
      <span class="tag">NT$80,000 起</span>
      <span class="tag">LINE / FB / IG / 官網</span>
      <span class="tag">2–4 週上線</span>
    </div>
  </div>
  <!-- SVG mascot on the right -->
  <svg class="octo" viewBox="0 0 480 420" fill="none">
    ...arms, head, eyes...
  </svg>
</body>
</html>
```

## Screenshot Command (macOS)

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars \
  --window-size=1200,630 \
  --virtual-time-budget=4000 \
  --screenshot=og.png "file://$PWD/og.html"
```

- `--virtual-time-budget=4000` — waits up to 4s for fonts/network. Google Fonts render reliably with this.
- `--hide-scrollbars` — prevents scrollbars in screenshot.
- Outputs `og.png` at 1200×630. Verify with `sips -g pixelWidth -g pixelHeight og.png`.

## Design Tips

### Fonts
- If using Google Fonts, load them in `<head>` via the standard link. Headless Chrome will render them within the virtual-time-budget.
- Prefer web-safe fallbacks or self-hosted fonts to avoid network dependency. If a font fails to load, Chrome will use the fallback and you might not notice until reviewing the PNG.

### Dark Background Pattern
The gradient radial glow behind the mascot:
```css
body::before {
  content:'';
  position:absolute; right:-180px; top:-180px;
  width:640px; height:640px; border-radius:50%;
  background:radial-gradient(circle, rgba(BRAND_COLOR_R, BRAND_COLOR_G, BRAND_COLOR_B, .22) 0%, transparent 65%);
}
```
The glow is cropped by `overflow:hidden` on the body, creating a soft halo effect without adding an SVG element.

### SVG Mascot Positioning
Position the SVG mascot partly outside the viewport (e.g. `right:60px; bottom:-40px; width:380px`) so it feels like it's popping out of or behind the frame. Increase `right:` to shift it right/left within the visible area.

### Price Tags as Visual Weight
The `.tag` pills in the bottom-left add visual balance to the mascot on the right. Three tags works well for a service page (price range, channels, delivery time).

## Post-Generation

### Verify
```bash
sips -g pixelWidth -g pixelHeight og.png
```
Must return `1200` and `630`.

### Reference in OG meta tags
```html
<meta property="og:image" content="https://domain.tld/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://domain.tld/og.png">
```

### Deploy og.html or not?
- `og.html` is a build tool — it doesn't affect the production site.
- If deploying via CF Pages, it will be publicly accessible at `domain.tld/og.html`. This is harmless, but you can delete it or add it to a deployment exclude list if desired.
- When you change branding, keep `og.html` in version control and re-screenshot. Do NOT try to edit `og.png` manually.

## Pitfalls

- **Missing fonts** — if Google Fonts are unreachable, the fallback renders in sans-serif. To avoid this, wait for the font in the headless browser: `--virtual-time-budget=4000` helps. Alternatively, self-host the font files.
- **No `overflow:hidden`** — the gradient glow and mascot will leak outside the 1200×630 frame, resulting in a wrong-sized or scrollable PNG.
- **Approximate pixel sizes** — fractional `font-size` values or `gap`s using `calc()` can cause sub-pixel rendering that looks slightly blurry at 1× scale. Use round values (64, 26, 20, 14).
- **SVG `opacity` aggregation** — layered translucent SVG arms as the mascot (e.g., `.85`, `.7`, `.55`, `.45`) create depth but can wash out against the background if cumulative opacity drops too low. Test by screenshotting.
- **Text-shadow** — the header text should use visible contrast against the dark background. `text-shadow:0 2px 16px rgba(0,0,0,.5)` helps.
- **Chrome not at standard path** — on machines where Chrome is in a non-standard location (Homebrew Cask, JetBrains, etc.), find it with `mdfind kMDItemKind == "Application" | grep -i chrome`.
