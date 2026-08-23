# Deployed Landing-Page Hardening (P0 checklist)

Captured from a 2026-08 session hardening a deployed single-file course landing page (Vercel, GitHub-backed). These are the items that silently break sharing/SEO/tracking if skipped — applies to any deployed single-page business site. Run after Biome is clean, before/with deploy.

## The P0 list

| Check | Action |
|-------|--------|
| **All absolute URLs point at a LIVE domain** | `og:url`, `twitter:url`, JSON-LD `url`/`logo`, llms.txt 官網欄位. A vanity domain that doesn't resolve (`curl` fails) breaks og:image previews AND schema trust. Verify the domain resolves before using it. |
| **canonical / robots.txt / sitemap.xml** | Once deployed: add `<link rel="canonical" href="<deployed-url>/">`, `robots.txt` with explicit `Allow: /` for `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`, `Applebot-Extended` (don't rely on defaults for GEO), and a single-URL `sitemap.xml`. Submit to Search Console. |
| **og:image / logo files EXIST** | Meta/schema referencing files not in the repo = broken share cards. Generate 1200×630 cover + 512 logo, verify `curl -s -o /dev/null -w "%{http_code}"` → 200. Add `apple-touch-icon`. |
| **llms.txt freshness** | Keep in sync with page content (class dates, prices, URLs). Stale llms.txt = AI assistants quote outdated facts. |
| **Tracking placeholders** | GA4 (`G-XXXXXXXXXX`), Meta Pixel (`000000000000000`), Turnstile sitekey, form `SHEET_URL` placeholders → conditional-load pattern below. Placeholder IDs fire 404s and pollute analytics with fake data. |
| **FAQ schema ↔ visible FAQ** | FAQPage JSON-LD questions must appear as a visible `<details>` accordion with byte-identical answers. Invisible schema = GEO grounding miss + conversion miss. |

## Conditional tracking loading (inline script)

Replaces hardcoded `<script src>` tags — external scripts only load when a real ID is present:

```js
(()=> {
  var GA_ID = 'G-XXXXXXXXXX';            // real ID goes here
  var PIXEL_ID = '000000000000000';
  var gaReal = GA_ID.indexOf('G-XXXXXXXXXX') === -1;
  var pxReal = PIXEL_ID.indexOf('000000000000000') === -1;
  var gs, ns, img;
  window.dataLayer = window.dataLayer || [];
  window.gtag = (...args)=>{ window.dataLayer.push(args); };
  if(gaReal){ /* createElement script + gtag('js')/config */ }
  window.trackEvent = (action, params)=> {
    if(gaReal && typeof window.gtag === 'function'){ window.gtag('event', action, params||{}); }
  };
  if(pxReal){ /* inject fbevents.js + init/track + noscript img */ }
})();
```

Biome note: this pattern triggers `useTemplate` (string concat → template literal), `useArrowFunction` on the IIFE and `window.gtag`, and `noInnerDeclarations` (hoist `var gs, ns, img` to function root) — write it arrow/template/hoisted from the start to avoid a second lint pass.

Turnstile: remove unconditional `<script src="...turnstile/v0/api.js">` from `<head>`; inject dynamically only when `data-sitekey` is real, else hide widget.

## Click-to-load YouTube iframe

`<iframe data-src="...embed/ID...">` with no `src`; set `src` from `data-src` in the play handler. `.video-wrap` keeps padding-top ratio → no CLS.

**⚠️ Critical pitfall — the empty iframe eats clicks.** A no-`src` iframe is transparent but still occupies its full box, and if its DOM order comes AFTER the placeholder button (same stacking context, no z-index), it sits ON TOP and swallows every click — the button never fires. Symptom: `playVideo()` works when called directly from the console but not from a real click. Fix (both lines):
```css
.video-wrap iframe:not([src]){pointer-events:none}  /* empty iframe doesn't block the button */
.video-placeholder{z-index:2}                        /* button guaranteed on top */
```
Verify with a real browser click (Playwright), not `element.click()` via evaluate — evaluate bypasses hit-testing and masks the bug.

**YouTube thumbnail placeholder (better than a flat color block):** use `https://i.ytimg.com/vi/{ID}/maxresdefault.jpg` (1280×720) as `background-image` on the placeholder, plus a dark gradient overlay div so the play button/label stay legible. All size variants exist: `maxresdefault`/`hqdefault`/`sddefault`/`mqdefault` — curl each to confirm before relying on it.

**Embeddability verification (oembed ≠ embeddable):** `youtube.com/oembed` returning 200 only proves the video EXISTS — not that embedding is enabled. Check the watch page's playabilityStatus: `curl -s ".../watch?v=ID" -H "User-Agent: Mozilla/5.0" | grep -o '"playabilityStatus":{[^}]*}'` → `"status":"OK","playableInEmbed":true` means embeddable. The embed URL may contain `unavailable` strings even when playable (initial HTML fallback) — don't judge by grepping the embed page.

## Generating og-cover/logo with Pillow (no design tools)

Use the host's system python (see python-venv-management for the PYTHONPATH trap) drawing dark bg + gold accent + CJK text with `Songti.ttc`/`STHeiti` from `/System/Library/Fonts`. When no vision provider is configured, verify text rendered by sampling pixel colors (count gold/text pixels via a Python loop) rather than eyeballing.
