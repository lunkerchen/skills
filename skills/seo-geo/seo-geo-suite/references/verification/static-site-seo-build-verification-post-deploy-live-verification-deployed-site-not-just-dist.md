# Post-deploy live verification (deployed site, not just dist)

The checklist above validates `dist/`; after the deploy lands, re-run the
key checks against LIVE URLs to catch deployment-layer problems (stale edge
cache, wrong canonical domain, missing files):

- Check BOTH the deployment-specific URL (`https://<hash>.<project>.pages.dev`)
  and the production domain — deployment URL is ready first; production is
  what users/crawlers actually hit.
- Cache-bust every URL: append `?_cd=<commit-sha>` — CF edge cache may serve
  stale HTML/JSON after deploy otherwise.
- Use a browser UA (`-A 'Mozilla/5.0 … Chrome/…'`) — CF edge returns 403 to
  non-browser agents (urllib, bare curl).
- Verify content identity, not just HTTP 200: new `<title>` served, canonical
  points at the production domain, target JSON-LD `@type` present, no literal
  `import.meta.env`, `/robots.txt` lists the GEO bots, `/llms.txt` present
  with expected section, sitemap-index fetchable.
- Spot-check one content page's meta description for escaped HTML (`&lt;`)
  — the CTA-leak bug class survives builds that pass presence-only regexes.

Verified on your-brand (Astro 6 + CF Pages direct upload, 2026-08-11): both
URLs served the new title, production canonical, FAQPage JSON-LD, robots
GPTBot, llms.txt Portfolio section, and sitemap-index; no env leak.
