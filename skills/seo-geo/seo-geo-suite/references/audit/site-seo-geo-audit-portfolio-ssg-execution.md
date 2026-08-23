# Portfolio SSG SEO+GEO Execution Trace

Date: 2026-07-21
Site: your-brand.your-app.example.com (Astro 5 static, Cloudflare Pages)
Context: First-principles SEO optimization of a photography + development portfolio.

This reference captures the concrete execution order, decisions, and command patterns
from a real session. Use alongside `site-seo-geo-audit`'s workflow for actual implementation.

## Execution Order (First-Principles)

1. **Audit existing infra** — sitemap, robots.txt, GA4, llms.txt. Don't rebuild what works.
2. **Structured data first** — JSON-LD (WebSite + Person + Photographer in `@graph`). This is the single highest-impact change for local search.
3. **Title & meta description** — every page gets a unique, location+keyword-rich title. Include city ("台北") and service keywords ("商業攝影", "人像", "獨立開發").
4. **Content depth for GEO** — expand portfolio descriptions with technical specifics (gear, lighting, location, editing). AI citation requires citeable detail.
5. **llms.txt** — once you know all pages, generate the full list including GitHub repos.
6. **Build + verify** — rebuild, check every page for expected tags.

## JSON-LD Details

### Astro implementation (Base.astro)

- Site-level schema (`@graph` with WebSite + Person + Photographer) is a single `const` object in the layout frontmatter
- Page-level schema (CreativeWork, FAQPage, BreadcrumbList) passed as `jsonLd` prop
- Both rendered via `<script type="application/ld+json" set:html={JSON.stringify(...)}>`
- The `Photographer` schema includes: `address` (PostalAddress → Taipei), `priceRange` ("NT$1,490–NT$12,800"), `areaServed` (["台北", "台灣"]), `makesOffer` (array of `Offer` → `Service` items)
- The `Person` and `Photographer` schemas share `name` but have distinct `@id` values

### BreadcrumbList

Passed as prop from `[...slug].astro` to `Base.astro`:

```astro
<Base breadcrumbs={[{ name: "作品集", href: "/projects" }, { name: title }]}>
```

In layout, render only when breadcrumbs exist:

```astro
{breadcrumbs && breadcrumbs.length > 0 && (
  <script type="application/ld+json" set:html={JSON.stringify({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": breadcrumbs.map((crumb, i) => ({
      "@type": "ListItem", "position": i + 1,
      "name": crumb.name,
      "item": crumb.href ? `${site}${crumb.href}` : undefined,
    })),
  })} />
)}
```

## GEO Description Expansion

### Batch workflow

For sites with 15+ portfolio entries:

1. Read each `.md` content file
2. Expand the body with 3+ of the 6 GEO dimensions: Gear, Lighting, Location, Technique, Post-production, Subject interaction
3. Use concrete, verifiable claims — not generic "good light" but "午後窗光搭配 110cm 白色反光板補眼神光"
4. Preserve the original images; only enrich the text body

The `content-driven-static-site` reference `references/portfolio-seo-geo.md` has the full dimension checklist and template.

## llms.txt Pattern

Include portfolio entries, services, pricing, and external project URLs (GitHub repos):

```
# Site Name — Tagline

> Description.

## Photography Portfolio
- [Title](https://domain.com/projects/slug/): One-line description

## Services
- [Services](https://domain.com/services/): Description
- [Pricing](https://domain.com/pricing/): Description
- [About](https://domain.com/about/): Description

## Development Projects
- [Project Name](https://github.com/user/repo): Description
```

## Verification via Subagent

For multi-page verification after GEO changes, delegate verification to a subagent:

```json
{
  "goal": "Verify GEO output on built site",
  "context": "Site at dist/. Built with 'npm run build'. Check:
   - 24 pages built
   - JSON-LD types present (WebSite, Person, Photographer, CreativeWork, BreadcrumbList)
   - hreflang tags on all pages
   - OG images with absolute URLs
   - llms.txt has all project entries
   - robots.txt points to sitemap-index.xml
   - No build errors"
}
```

The subagent reports per-page findings with grep commands over built HTML.

## Pitfalls

- **Second frontmatter block in Astro**: The `set:html` JSON-LD tag can look like a dashed-line if the JSON contains `---` in string values. Not actually a problem — but if you add a second `<script>` block with JavaScript after the JSON-LD, it can create a spurious `---` in the JS that Astro interprets as a frontmatter separator. Keep all JavaScript in a single `<script>` block.
- **GEO description depth tradeoff**: Expanding descriptions with 100+ characters of technical detail is valuable for AI citation, but don't fabricate specs. If the original content doesn't describe the lighting setup explicitly, describe the visible result (e.g. "窗光為主光源" not "Profoto D2 雙燈").
- **llms.txt staleness**: After adding new portfolio entries, the llms.txt list drifts. Verify the count matches on every build.
