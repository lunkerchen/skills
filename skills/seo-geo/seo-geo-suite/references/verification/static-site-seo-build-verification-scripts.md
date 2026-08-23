# Scripts

- `scripts/verify-seo.mjs` — generalized re-runnable post-build checker
  implementing the checklist above. Copy, set `SITE` + page-specific class
  names (e.g. FAQ classes, noindex paths), run `node scripts/verify-seo.mjs`.
  Exit 0 = all checks passed, 1 = failures listed.
