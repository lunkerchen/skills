---
name: static-site-seo-build-verification
description: Verify SEO/GEO/AEO in built static sites (Astro).
author: Hermes Agent
license: MIT
version: 1.0.0
metadata:
  hermes:
    tags: [seo, geo, astro, verification, ssg]
    related_skills:
      - static-site-geo: implementation patterns for the same class (user-owned, may need `hermes curator adopt`)
      - site-seo-geo-audit: audit workflow (user-owned)
read_when:
  - User asks to verify SEO/GEO/AEO output after building an Astro or other static site
  - Adding GA4/analytics, JSON-LD, llms.txt, robots.txt, or hreflang to an Astro static site
  - Writing a re-runnable post-build SEO verification script
  - Debugging why gtag/analytics or JSON-LD is missing or broken in built Astro HTML
related_skills:
  - static-site-geo: implementation patterns for the same class (user-owned, may need `hermes curator adopt`)
  - site-seo-geo-audit: audit workflow (user-owned)
---# Static Site SEO/GEO Build Verification

Verify **built output** (`dist/`), never source — source has template logic;
the static HTML is what crawlers see. Astro emits single-line minified HTML:
use targeted regex/python3/node, not `read_file`.

## Extended References & Guides

- [Astro inline-script pitfalls (empirically verified on Astro 6)](references/astro-inline-script-pitfalls-empirically-verified-on-astro-6.md)
- [llms.txt: generate from source, never hand-maintain](references/llms-txt-generate-from-source-never-hand-maintain.md)
- [AEO description extraction: one filter rule for ALL surfaces](references/aeo-description-extraction-one-filter-rule-for-all-surfaces.md)
- [Verification checklist (run, don't eyeball)](references/verification-checklist-run-don-t-eyeball.md)
- [New content entry audit (read-only acceptance check)](references/new-content-entry-audit-read-only-acceptance-check.md)
- [Post-deploy live verification (deployed site, not just dist)](references/post-deploy-live-verification-deployed-site-not-just-dist.md)
- [Scripts](references/scripts.md)
- [Trigger Evals](evals/eval_triggers.json): Automated evaluation test fixtures.
