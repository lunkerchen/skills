# SPA / Server-Side SEO Injection Audit — your-app (2026-08-16)

Applies to CF Pages SPA + Functions server-side SEO injection (React/Vite
SPA where `functions/_middleware.js` + `functions/seo.js` inject metadata
per request), as distinct from Astro static builds. The same live-verification
discipline applies; these are the SPA-specific traps found.

## Trap 1: JSON-LD regex must tolerate extra attributes

Server-injected JSON-LD tags carry marker attributes:

```html
<script type="application/ld+json" data-seo-managed="server">…</script>
```

A strict regex `<script type="application/ld+json">` returns **0 blocks** on a
fully-schema'd page. Always extract with:

```python
re.findall(r'<script type="application/ld+json"[^>]*>(.*?)</script>', h, re.S)
```

Then `json.loads` each block and collect `@type`. Parse failure = real bug;
zero matches with a strict regex = **regex bug, not missing schema**.

## Trap 2: llms.txt template URLs 404 for real crawlers — and curl globbing hides it

llms.txt / llms-full.txt listed API URLs with brace templates:

```
GET https://your-app.example.com/api/listings/{listing_id}
GET https://your-app.example.com/api/listings/search?q={keyword}&category={category}&listing_type={sell|seek}
```

- Real crawlers fetch the literal braces → 404 (one entry flagged in audit).
- `curl` brace-globs `{a|b}` into multiple fetches; the last one can return
  200, so a naive `curl -w '%{http_code}'` loop reports all-green.
- Fix: verify with `curl -g` (`-g` disables globbing) so templates genuinely
  rome 404, then replace templates with REAL example URLs + a params note:
  `GET https://your-app.example.com/api/listings/bd989cda-…` — "(replace the id
  with any listing id)". Both llms.txt and llms-full.txt need the same fix.

## Trap 3: hreflang is missing by default on single-language sites

`injectSeo`-style builders emit canonical/OG/twitter but often no hreflang.
The verification checklist demands hreflang zh-TW + x-default on every page —
for a single-language (zh-TW-only) site these are SELF-REFERENCING:

```html
<link rel="alternate" hreflang="zh-TW" href="https://your-app.example.com/help" />
<link rel="alternate" hreflang="x-default" href="https://your-app.example.com/help" />
```

Add to the injection template once; every public route inherits it.

## Trap 4: every public route needs ≥1 JSON-LD block

Per-route schema tables (PUBLIC_ROUTES) drift: /contact and /changelog had
title+description but no schema. Audit ALL routes for `jsonld_types == []` —
not just the flagship pages. Cheap completion: ContactPage for /contact,
WebPage for /changelog.

## Full audit recipe (worked, your-app.example.com)

1. `source $HERMES_HOME/scripts/cf-token-refresh.sh` FIRST, then
   `npx wrangler pages deployment list --project-name your-app` — running
   the refresh script as `bash script.sh` does NOT export the token into the
   current shell; wrangler then fails with auth error [code: 9109].
2. Fetch every public route with browser UA (`-A 'Mozilla/5.0 … Chrome/…'`),
   cache-bust with `?cb=$RANDOM`.
3. Per page: title, meta description, canonical, hreflang zh-TW + x-default,
   OG image, noindex, JSON-LD parse (trap 1 regex).
4. `/robots.txt`: GEO bots listed. `/llms.txt` + `/llms-full.txt`: extract
   all `https://…` URLs, verify each with `curl -g` → all 200 (trap 2).
5. `/sitemap.xml`: extract all `<loc>`, verify each 200 — 44/44 green.
6. Dynamic routes: one `/listings/<id>` (expect Product + BreadcrumbList),
   one `/trends/<brand>/<model>` (expect Dataset), one `/guides/<slug>`
   (expect Article + BreadcrumbList); missing/invalid listing → noindex.
7. Markdown twins: `/<path>.md` → 200 `text/markdown`; homepage twin has
   frontmatter (title/canonical/last_updated).
8. After fixes: `node --test functions/*.test.js` (32 pass), build, deploy,
   re-verify production with cache-bust (edge may serve stale).
