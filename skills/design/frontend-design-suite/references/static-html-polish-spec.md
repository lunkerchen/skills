---
name: static-html-polish
description: Retrofit RWD/SEO/a11y on static HTML. Audit→harden→verify.
version: 1.0.0
---

# Static HTML Polish

Strengthen RWD, SEO/GEO, and accessibility on an already-written standalone HTML page (no build step, no external deps, single `.html` file with inline `<style>` and inline `<script>`).

## When to Use

- User says "加強 RWD", "加強 GEO+SEO", "幫這頁做 RWD" on an existing static HTML file
- User asks to make an HTML article mobile-ready, search-friendly, or accessible
- Pre-deployment polish pass on a finished single-file HTML page

## Workflow

### 1. Assessment

Read the file and check:
- **Heading hierarchy**: every level must be ≤ previous+1. h2→h4 is a skip — fix by bumping intermediate headings or converting non-heading elements to `<div class="phase-title">` with `role="img"` for diagram labels
- **Viewport meta**: `width=device-width, initial-scale=1.0` is baseline; harden with `minimum-scale=1.0, maximum-scale=5.0`
- **SEO metadata**: title, description, OG/Twitter meta. If absent, add with content matching visible page
- **JSON-LD**: add `Article` + `FAQPage` when appropriate; FAQ Q&A text must appear *verbatim* in visible HTML
- **Canonical**: omit when not deployed to a real domain — never invent one
- **A11y**: skip-link present? `prefers-reduced-motion`? `@media print`? keyboard handlers on interactive elements?
- **Offline safety**: zero `<script src="...">` for a static article

### 2. RWD Hardening Patterns

| Problem | Fix |
|---------|-----|
| Nav wraps at narrow widths | `display:flex; overflow-x:auto; white-space:nowrap` on container; links get `min-height:44px` |
| Long source URLs overflow | `overflow-wrap:anywhere; word-break:break-word` |
| Touch targets too small | `min-height:44px` on nav links, cards, buttons |
| Layout breaks below 390px | Media query `≤600px` → single column |
| Tables overflow | `.table-wrap { overflow-x:auto; }` |
| Multi-column grids break | 3col → 2col → 1col as width drops |

### 3. SEO/GEO Metadata

```html
<meta name="description" content="…">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
```

No `author`/`publisher`/`rating`/`Place`/`GeoCircle` unless the page actually has that content.

### 4. JSON-LD Schema

`Article` + `FAQPage` in an `@graph` array. FAQ Q&A text must be byte-identical to visible HTML content. No invented dates — use actual creation/modification date.

### 5. Verification Pipeline

Three stages, run in order:

**A. Static Audit** — Python HTML parser checks:
- Heading hierarchy (no skips)
- No canonical on undeployed pages
- All `#fragment` anchors resolve to existing `id`s
- JSON-LD schema types match expected
- FAQ visible content parity (substring check)
- No external scripts
- A11y artifacts preserved (skip-link, reduced-motion, print)
- RWD hardening present (overflow-wrap, min-height tokens)

**B. Browser Viewport Test** — headless Chrome CDP at 320, 375, 768, 1024, 1440px:
- No horizontal overflow (`scrollWidth ≈ clientWidth`)
- Touch targets ≥44px
- Interactive elements function at all widths

**C. Blind Auditor Delegate** — spawn a separate `role='leaf'` subagent that reads the final file (no writing), sees only the result not the implementer's reasoning, returns `VERDICT: PASS|FAIL` + findings with line numbers. On FAIL, re-spawn implementer with findings.

## Verification Checklist

- [ ] Heading hierarchy ≤+1 throughout
- [ ] Viewport hardened (min/max-scale)
- [ ] No horizontal overflow at 320–1440px
- [ ] overflow-wrap:anywhere on long text
- [ ] Description written for target-language search intent
- [ ] JSON-LD Article + FAQPage present, FAQ text matches visible HTML
- [ ] No invented author/publisher/canonical
- [ ] OG + Twitter meta present
- [ ] No external scripts
- [ ] Skip-link, reduced-motion, print styles
- [ ] Blind auditor passed

## Pitfalls

- Google Fonts preconnect required before stylesheet (if external fonts added)
- For diagram labels inside `.legal-diagram` style components: replace `<h4>` with `<div class="phase-title">` and use `role="img"` on the container — avoids heading-skip violations without changing visual hierarchy
- `og:locale` = `zh_TW` for Taiwan, not `zh-CN` or generic `zh`
- Browser viewport tests need DevTools listening port; Chrome must start with `--remote-debugging-port=9222`
