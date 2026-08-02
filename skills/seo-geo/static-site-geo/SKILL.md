---
name: static-site-geo
description: >-
  SEO/GEO implementation patterns for static HTML sites — SSG-built
  (Astro, Eleventy, Hugo, Jekyll) or handcrafted single flat files deployed
  to CF Pages/Netlify/Vercel. Covers JSON-LD injection, sitemap setup,
  OG image generation (including template→screenshot workflow), llms.txt,
  and crawler files — framework-specific equivalents of
  webapp-geo-optimization for static portfolios, service landing pages,
  documentation sites, and marketing pages.
read_when:
  - User asks to optimize SEO or GEO on an Astro/Hugo/Eleventy/Jekyll site or single-file HTML landing page
  - Building or improving a portfolio site generated with an SSG
  - Adding JSON-LD structured data to a static site
  - Setting up sitemap, robots.txt, or llms.txt for a static site deployment
  - Any task that loads webapp-geo-optimization but the project is Astro or Hugo (not React SPA)
related_skills:
  - webapp-geo-optimization: React/Next.js GEO patterns (reference parent)
  - geo-article-friendly: Per-article GEO transformation for content sites
  - modern-seo-strategy: Strategic SEO/GEO framework (this skill is the tactical SSG subset)
  - content-driven-static-site: Building SSG portfolios (complements this skill's optimization)
---
# Static Site GEO / SEO Patterns

## When to Use

This skill covers the *tactical implementation* of SEO+GEO for static HTML sites —
SSG-built (Astro, Hugo, Eleventy, Jekyll) or a single flat HTML file deployed as a
static site. The core patterns (JSON-LD, robots.txt, sitemap, llms.txt, OG images)
apply identically either way.

Use when the project uses Astro, Eleventy, Hugo, Jekyll, or similar SSG,
or when building a single-file HTML landing page that needs SEO/GEO.
The patterns differ from SPAs because:

- No hydration lifecycle — JSON-LD is injected directly into the HTML
- No mount/unmount side effects to manage
- Built HTML can be directly verified — the browser is not required

## Patterns by Framework

### Astro

**JSON-LD injection:** use `set:html={JSON.stringify(schema)}` in `<script>` tags.
Centralise site-level schema (`@graph` with WebSite + Person/Organization) in the
base layout; pass page-specific schemas (CreativeWork, Article, FAQPage) as props.

```astro
---
export interface Props {
  title: string;
  description?: string;
  image?: string;
  jsonLd?: Record<string, unknown>;
}
const { title, description = 'Default desc', image, jsonLd } = Astro.props;
const pageJsonLd = jsonLd && { '@context': 'https://schema.org', ...jsonLd };
---
<script type="application/ld+json" set:html={JSON.stringify(siteJsonLd)}></script>
{pageJsonLd && <script type="application/ld+json" set:html={JSON.stringify(pageJsonLd)}></script>}
```

**hreflang (static single-locale):** For a Taiwan-based site with only
Traditional Chinese content, add hreflang tags in the base layout. Both
`zh-TW` and `x-default` point to the same URL — `x-default` tells Google
"no language preference", appropriate when there's no alternate-language
version.

```astro
---
const site = "https://domain.com";
const locales = [
  { lang: "zh-TW", href: Astro.url.href },
  { lang: "x-default", href: Astro.url.href },
];
---
{locales.map(loc => (
  <link rel="alternate" hreflang={loc.lang} href={loc.href} />
))}
```

If you add language variants later, map `locales` to actual alternate URLs.

**Canonical:** `<link rel="canonical" href={Astro.url} />` — `Astro.url` is a
native URL object that serialises to string in HTML context.

**Sitemap:** `@astrojs/sitemap` integration auto-outputs `sitemap-index.xml`.
Reference that filename in `robots.txt`, not `sitemap.xml`.

**OG image:** Use `sharp` (already an Astro dependency) not Pillow.

**No cleanup needed:** static build = one `<script>` per page, no React
unmount accumulation.

### SSG Agnostic

**Schema selection for portfolios:**

| Scope | E-commerce schema | Portfolio (dual-identity) schema | Portfolio (pure) schema |
|---|---|---|---|
| Site | WebSite + Organization | WebSite + Person + Photographer (via @graph) | WebSite + Person (via @graph) |
| Item | Product + Offer | CreativeWork | CreativeWork |
| SearchAction | Yes (if search exists) | Usually omit | Usually omit |

Dual-identity portfolio (photographer + developer/consulting) uses three
schemas in one `@graph`: `WebSite` (site metadata), `Person` (personal brand),
and `Photographer` (service-specific local business schema with address, price
range, area served). The `Person` and `Photographer` share the same name but
have different `@id` values to avoid schema conflict.

**Schema selection for documentation / marketing:**

| Scope | Recommendation |
|---|---|
| Site | WebSite + Organization (with logo) |
| Article | Article (with author reference) |
| BreadcrumbList | Auto-generated from URL structure |
| SoftwareApp | For product pages |

**Robots.txt:**
```
User-agent: *
Allow: /

Sitemap: https://domain.tld/sitemap-index.xml   (Astro convention)
Sitemap: https://domain.tld/sitemap.xml          (Hugo/Eleventy default)
```

Know which convention your SSG uses — check `dist/` after a build.

**llms.txt:** Per [llmstxt.org](llmstxt.org) spec. List key pages, a one-line
description of each, and selected projects. AI crawlers (GPTBot, Google-Extended)
look for this at the root.

**Verification:** Parse built HTML rather than inspecting source. The source may have dynamic template logic; the static output is what crawlers see.

**⚠️ Minified HTML problem:** SSG builds (Astro, Hugo, Eleventy) produce single-line
minified HTML. `read_file` shows content line-by-line, so the entire `<head>` appears as one
truncated line. **Do not rely on read_file for verification** — use targeted grep/python3
patterns instead.

```bash
# Check a specific JSON-LD type exists in the output
grep -oE '"@type":"(WebSite|Person|Photographer|CreativeWork)"' dist/index.html

# Verify title tag content (works on single-line HTML)
grep -oE '<title>[^<]+</title>' dist/index.html

# Check meta description content
grep -oE '<meta name="description" content="[^"]+"' dist/index.html

# Verify hreflang tags exist
grep -E 'rel="alternate".*hreflang=' dist/index.html

# Count how many times a schema type appears
grep -c '"@type":"Service"' dist/services/index.html

# Full JSON-LD extraction — pretty-print for structural verification
python3 -c "
import re, json, sys
with open('dist/index.html') as f:
    html = f.read()
matches = re.findall(r'<script type=\"application/ld\\+json\">(.*?)</script>', html, re.DOTALL)
for m in matches:
    print(json.dumps(json.loads(m), indent=2, ensure_ascii=False))
"

# Verify BreadcrumbList has 3 items with correct names
python3 -c "
import re, json
with open('dist/projects/wedding-2026/index.html') as f:
    html = f.read()
m = re.search(r'BreadcrumbList.*?\]', html)
if m: print(m.group())
"

# Count projects in llms.txt (structured file, grep works fine)
grep -c 'https://domain.tld/projects/' public/llms.txt
```

For structured files like `robots.txt` and `llms.txt`, `read_file` works fine — the
minified-HTML issue only affects HTML build output.

## Verification Checklist

- [ ] `pnpm run build` or equivalent passes
- [ ] Site-level JSON-LD (`WebSite` + `Person`/`Organization`) present in built HTML
- [ ] Per-page schema (if any) injected alongside site schema, not replacing it
- [ ] `robots.txt` exists in output with correct sitemap filename
- [ ] `llms.txt` exists and lists actual page URLs with full domain
- [ ] OG image is 1200×630 real raster image (not SVG), referenced with absolute URL
      — generate via `references/og-image-generation.md` (HTML+Chrome) or
      `references/og-image-svg-pipeline.md` (SVG+macOS)
- [ ] `canonical` URL matches page path
- [ ] OG/Twitter tags use absolute image URLs
- [ ] hreflang tags present on all pages (zh-TW + x-default for Taiwan sites)
- [ ] Each page's title and description checked via grep (not read_file)

## Reference Files

- `references/astro-portfolio-implementation.md` — Full walkthrough of an Astro
  portfolio GEO optimisation including schema JSON, page-level CreativeWork,
  verification commands, and pitfalls.
- `references/build-output-verification.md` — Reusable verification patterns:
  checking minified HTML output with grep/python3, structured checklist approach,
  and per-page schema inspection commands.
- `references/og-image-generation.md` — Template-based OG image generation:
  og.html → headless Chrome screenshot → 1200×630 PNG. Covers dark-background
  composition, SVG mascot positioning, Google Fonts timing, and verification.
- `references/og-image-svg-pipeline.md` — Alternative macOS-native OG image
  pipeline: SVG → qlmanage → Pillow → WebP. No browser dependency. Covers
  SVG composition, system-font usage, dimension handling, and one-shot script.

## Hard Rules

- Never add visible UI sections (FAQ, How-it-works) unless the user explicitly asks.
- GEO improvements are invisible by default: JSON-LD, meta tags, crawler files only.
- Verify built HTML, not source files — what crawlers see is what matters.
- OG images must be real raster images (PNG/WebP/JPEG), minimum 1200×630.

## Build Pipeline Pitfalls

- **Build script overwrites `public/` files**: Vite copies `public/` to `dist/` during build, but a post-build script (e.g., `generate-guide-pages.mjs`) that writes to `dist/` can overwrite critical files like `llms.txt` with a stale or empty version. Fix: check if the target already exists and has content before overwriting, or rename the build script output to a different path and merge later.
- **Verify the served HTML, not just dist**: CF Pages and other edge platforms may process (minify/strip) HTML during deployment. Use `curl | grep` on the live URL, not just `dist/`, to verify OG tags and JSON-LD are present. **`og:image:width`/`height` are commonly stripped** by CF Pages HTML processing — compare `grep og:image:width dist/index.html` vs `curl <url> 2>/dev/null | grep og:image:width` to detect. Social platforms (Facebook, X, LINE) usually execute JS and can read React-injected values, but non-JS crawlers won't see them. Fix: ① accept client-side fallback; ② disable CF HTML minification (Dashboard > Speed > Optimization or `_headers` rules); ③ skip (width/height are non-critical hints).
- **SSG minified HTML**: Build output is single-line minified. Use grep/python3 with regex to verify head tags; `read_file` shows one truncated line and should not be relied on for head content verification.
