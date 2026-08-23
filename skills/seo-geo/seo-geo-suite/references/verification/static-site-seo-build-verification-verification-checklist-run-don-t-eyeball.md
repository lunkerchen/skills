# Verification checklist (run, don't eyeball)

- Every page: `<title>`, meta description, canonical, hreflang zh-TW +
  x-default, ≥1 parseable JSON-LD block; site-level `@graph`
  (WebSite+Person+Photographer) on all pages.
- Meta description: assert CONTENT quality, not just presence — capture the
  `content="…"` value and fail on raw HTML tags or escaped `&lt;`/`&gt;`.
  Presence-only regexes (`/<meta name="description" content="[^"]+"/`) pass
  broken pages that leak CTA/anchor markup.
- Homepage FAQ: visible questions/answers == FAQPage `mainEntity` verbatim
  (decode HTML entities before comparing).
- Sitemap: `@astrojs/sitemap` emits `sitemap-index.xml` → `sitemap-0.xml`;
  URLs carry trailing slashes. Assert: homepage present, every non-noindex
  dist page present, `/contact` (or any noindex page) absent.
- robots.txt: explicit `User-agent: GPTBot/ChatGPT-User/OAI-SearchBot/
  Google-Extended/PerplexityBot/ClaudeBot/Claude-Web` + `Allow: /`, and the
  `Sitemap:` line points at a file that exists in dist.
- GA4: no literal `import.meta.env` in any dist HTML; `gtag('config', …)`
  resolves; no PII in event payloads (interaction type + destination only).
- OG image: real raster asset (≥1200×630) present in dist and referenced
  with an absolute URL.
- noindex redirect pages (e.g. `/contact` → `/about`) have no Base layout:
  skip their head/JSON-LD checks, but assert sitemap exclusion.
