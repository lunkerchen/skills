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

**Robots.txt（2026 主流 AI 爬蟲全面放行矩陣）：**
```
User-agent: *
Allow: /

# ── 2026 主流 AI 檢索與回答引擎放行 ──
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Diffbot
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: meta-externalagent
Allow: /

Sitemap: https://domain.tld/sitemap-index.xml   (Astro convention)
Sitemap: https://domain.tld/sitemap.xml          (Hugo/Eleventy default)
```

Know which convention your SSG uses — check `dist/` after a build.

**深度知識圖譜深構（Deep Knowledge Graph `@graph` Pattern）：**
- **全域 `Organization`**：必須宣告 `legalName`、`foundingDate`、`knowsAbout`（定義專長關鍵字陣列，強化主題權威）、`hasOfferCatalog`（關聯核心服務列表）與 `areaServed`。
- **獨立服務頁 `Service` + `FAQPage`**：每個獨立服務路由皆注入專屬 `Service` 規格，並搭配 `FAQPage` 問答，供 AEO/Google Rich Results 精準抽取。
- **案例頁 `CreativeWork`**：標註 `about`（客戶實體）、`creator`（創作團隊）與具體成果指標。
- **團隊頁 `AboutPage` + `Person`**：標註團隊成員姓名、`jobTitle`、專長並關聯回文章作者。

**MDX / SSG 封面圖自動 Fallback 防呆機制：**
當內容庫（如 `content/blog/*.mdx`）文章繁多且 frontmatter 容易漏填 `coverImage` 時，在資料讀取層（如 `lib/mdx.ts`）實作自動檢查 fallback，防止 OG / Twitter Card 與 Article Schema 缺少圖片：

```ts
export function getBlogCoverImage(slug: string, frontmatterImage?: string): string {
  if (frontmatterImage) return frontmatterImage;
  const localCover = path.join(process.cwd(), 'public/images/blog', `${slug}.png`);
  if (fs.existsSync(localCover)) {
    return `/images/blog/${slug}.png`;
  }
  return '/images/default-og.png';
}
```

**雙檔 AI 協議（llms.txt + llms-full.txt）：**
- `public/llms.txt`：輕量級 Executive Summary + 核心模組導航（依 [llmstxt.org](https://llmstxt.org) 規範）。
- `public/llms-full.txt`：單檔完整全站業務上下文（含服務規格、流程、案例數據與 FAQ），供 Agent 單次 Context 注入檢索。

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

### Single-file event landing pages

Handcrafted one-file marketing pages (event invite, seminar, workshop) deployed
to CF Pages/Netlify/Vercel. All patterns apply directly; the one schema that
matters is `Event`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "活動名稱",
  "description": "一兩句，含日期地點與免費資訊",
  "startDate": "2026-08-22T14:00:00+08:00",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "場地名稱",
    "address": { "@type": "PostalAddress", "addressRegion": "台北市", "addressLocality": "信義區", "streetAddress": "基隆路一段 200 號 B1" }
  },
  "organizer": { "@type": "Organization", "name": "主辦單位" },
  "performer": { "@type": "Person", "name": "講者" },
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "TWD", "availability": "https://schema.org/LimitedAvailability" },
  "isAccessibleForFree": true
}
</script>
```

**Pitfalls specific to this class:**
- `"@context"` must be `https://schema.org` — a bare `schema.org` (or missing)
  breaks the whole block for validators; verify with `json.loads` + assert, not
  eyeballing.
- Free events: `offers.price = "0"` string + `isAccessibleForFree: true`. Never
  invent pricing.
- Also add `<html lang="zh-Hant">`, `<time datetime="...">` around the event
  date, `<address>` around the venue address, `meta name="robots"` with
  `max-image-preview:large`, `og:locale`, `twitter:card`.
- Domain-dependent assets (canonical, og:url, sitemap.xml, llms.txt) should be
  left out when no public domain exists yet — do NOT invent a placeholder URL.
  Note them as the remaining step instead.
- EXCEPTION — user explicitly asks to add everything now ("都幫我加上這些，資料之後補"):
  scaffold with ONE consistent placeholder domain across ALL files
  (`https://example.com/<path>/`), mark each site with a `<!-- TODO: replace
  example.com with the production domain before deployment. -->` comment,
  verify URL consistency programmatically across index.html / robots.txt /
  sitemap.xml / llms.txt, then end with the one remaining step: search
  `example.com` in those four files and replace before deploy. Never invent
  the placeholder silently — only on explicit "add it all now" requests.
- Full validated example + verification script: `references/event-landing-page-geo.md`.

### GEO: rewrite existing headings as questions (no fake FAQ)

AI crawlers extract "question → answer" pairs best. Before adding FAQPage
schema (which requires visible Q&A content), try rewriting EXISTING headings
into natural questions while keeping the body text unchanged:

- `工具沒有進入流程` → `為什麼 AI 工具沒有進入工作流程？`
- `老闆的 AI 學習法` → `老闆應該怎麼學 AI？`

Same layout, zero new content, better GEO extraction. Verification: count
`<h3>` ending in `？`/`?` via regex. This respects the hard rule below (no
visible UI sections added).

### Visible FAQ + FAQPage JSON-LD (when thorough GEO is explicitly requested)

The hard rule against visible sections yields when the user explicitly asks to
"把 GEO/SEO 做好" / "do GEO thoroughly". FAQPage schema REQUIRES visible Q&A
content — invisible or mismatched FAQ schema fails rich results and is a
Google violation — so a visible FAQ is the only way to complete that request.
It is also the strongest GEO move: AI crawlers get clean question→answer
pairs (not just heading rewrites) while traditional SEO gets the FAQ baseline.

Recipe:
- Add `<section id="faq">` before `#register`: a `.faq-grid` of
  `<article class="faq-item"><h3>問題？</h3><p>答案…</p></article>`, mirroring
  the page's existing card-grid + section-head styles so it looks native.
- Link it from the nav (`<a href="#faq">常見問題</a>`).
- Mobile: append `.faq-grid` to the page's existing single-column rule
  (`.pain-grid,.info-grid,.faq-grid{grid-template-columns:1fr}`).
- FAQPage JSON-LD: `mainEntity` array, one `Question` per visible item,
  `inLanguage: "zh-Hant"`. Answer text must match the visible paragraphs.

Verification (run, don't eyeball):
- `json.loads` every `application/ld+json` block — all must parse.
- **Visible == schema**: extract visible questions via
  `re.findall(r'<article class="faq-item"><h3>(.*?)</h3>', html)` and assert
  list equality with `mainEntity[].name`. Mismatch = FAQ fails rich results.
- In-browser: no horizontal overflow, no console errors, required form fields
  still present after the section insert.
- Only confirmed event facts (date/venue/fee) go in answers. The "how to
  register" answer must stay honest when the form endpoint isn't wired
  (demo mode → say so, don't invent a working signup path).
- **Grid card count**: keep the card count a multiple of the desktop grid
  columns. A 2-column `.faq-grid` with 5 cards leaves one empty slot the user
  WILL flag as broken ("六張卡片不要有空的"). Fix by adding an honest 6th
  Q&A that bridges to the event's core (e.g. 「這場活動只是教人操作 AI 工具嗎？」
  → 不是，從公司如何運作出發…), never by inventing commitments. The
  visible==schema assertion above catches schema drift automatically.

### GA4 / analytics events on static landing pages (blank-ID no-op)

Add conversion events to a single-file page without blocking the client on
wiring GA4 up front — same deferral philosophy as FORM_ENDPOINT:

- `const GA4_MEASUREMENT_ID = '';` — every event is guarded behind it. When
  blank, NO `gtag.js` script loads and `dataLayer` stays empty. Verify this in
  the console: clicking CTAs / focusing the form must push nothing
  (`window.dataLayer.length` stays 0, `querySelector('script[src*="googletagmanager"]')` is null).
- Inject gtag.js + `gtag('config', id, { anonymize_ip: true })` only when the
  ID is non-empty (use `encodeURIComponent` on the id in the script src).
- Event set proven on registration landing pages:
  - `select_content` — any CTA link click (`content_type: 'registration_cta'`)
  - `form_start` — first `focusin` inside the form (fire once)
  - `faq_view` — per `.faq-item` IntersectionObserver, fire once per card
  - `generate_lead` — successful submit (`method: FORM_ENDPOINT ? 'endpoint' : 'demo'`)
- Never send PII: names, phones, emails, and form values stay out of GA4.
- End by telling the client the one remaining step: paste the `G-…` ID, then
  test in GA4 DebugView (Admin → Data display → DebugView).

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
- `references/event-landing-page-geo.md` — Single-file event page patterns:
  validated Event JSON-LD, free-event Offer, question-heading GEO rewrite,
  AI-crawler robots.txt, domain deferral + placeholder scaffold, minified-HTML
  patch workaround.

## Hard Rules

- Never add visible UI sections (FAQ, How-it-works) unless the user explicitly asks.
- GEO improvements are invisible by default: JSON-LD, meta tags, crawler files only.
- Verify built HTML, not source files — what crawlers see is what matters.
- OG images must be real raster images (PNG/WebP/JPEG), minimum 1200×630.

## Build Pipeline Pitfalls

- **Build script overwrites `public/` files**: Vite copies `public/` to `dist/` during build, but a post-build script (e.g., `generate-guide-pages.mjs`) that writes to `dist/` can overwrite critical files like `llms.txt` with a stale or empty version. Fix: check if the target already exists and has content before overwriting, or rename the build script output to a different path and merge later.
- **Verify the served HTML, not just dist**: CF Pages and other edge platforms may process (minify/strip) HTML during deployment. Use `curl | grep` on the live URL, not just `dist/`, to verify OG tags and JSON-LD are present. **`og:image:width`/`height` are commonly stripped** by CF Pages HTML processing — compare `grep og:image:width dist/index.html` vs `curl <url> 2>/dev/null | grep og:image:width` to detect. Social platforms (Facebook, X, LINE) usually execute JS and can read React-injected values, but non-JS crawlers won't see them. Fix: ① accept client-side fallback; ② disable CF HTML minification (Dashboard > Speed > Optimization or `_headers` rules); ③ skip (width/height are non-critical hints).
- **SSG minified HTML**: Build output is single-line minified. Use grep/python3 with regex to verify head tags; `read_file` shows one truncated line and should not be relied on for head content verification.
- **Patch tool refuses single-line minified HTML**: the V4A multi-file patch form
  fails with `Binary file — cannot display as text` on single-line HTML. Workaround:
  replace-mode `patch` with a short unique old_string works fine — batch several
  replacements via a python loop over `hermes_tools.patch` pairs (one round-trip,
  ~1s for 7 pairs). See `references/event-landing-page-geo.md`.
- **Stale handoff ZIPs**: after any content edit, rebuild the archive from
  scratch (`rm -f ../proj.zip && zip -r ../proj.zip index.html robots.txt fonts`)
  and re-verify (`unzip -l` shows the file list, `shasum -a 256` + byte size to
  confirm it changed). A rebuilt ZIP is the only way to guarantee the colleague
  gets the new content. macOS: `rm .DS_Store` first — Finder-generated
  `.DS_Store` junk leaks into archives otherwise; verify with `unzip -l` that
  it's absent.
