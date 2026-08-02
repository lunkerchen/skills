# Build Output Verification — SEO/GEO Audit After Build

Session date: 2026-07-22
Project: `your-brand` — Astro static portfolio for the site owner

This file captures the exact verification approach used to confirm SEO/GEO
changes in the built output of an Astro static site. The patterns are
reusable across any SSG (Astro, Hugo, Eleventy, Jekyll, Next.js static export).

## The Core Problem: Minified Single-Line HTML

SSG builds produce minified HTML where the entire `<head>` (title + meta +
JSON-LD + links) is a single line. `read_file` shows content line-by-line,
so you see only the first ~8KB of that line — truncating JSON-LD blocks
mid-structure.

**Do not use read_file for verification of minified HTML.** Use shell
grep patterns or python3 scripts to extract specific tags from the file.

## Verification Patterns

### 1. Check title content

```bash
grep -oE '<title>[^<]+</title>' dist/index.html
# → <title>@your-brand — 台北商業攝影師與獨立開發者 | the site owner</title>
```

### 2. Check meta description

```bash
grep -oE '<meta name="description" content="[^"]+"' dist/index.html
# → content starts with the expected text
```

### 3. Check JSON-LD schema types present

```bash
grep -oE '"@type":"(WebSite|Person|Photographer|CreativeWork)"' dist/index.html
# Count occurrences
grep -c '"@type":"Service"' dist/services/index.html
```

### 4. Extract full JSON-LD for structural inspection

```bash
python3 -c "
import re, json
with open('dist/index.html') as f:
    html = f.read()
matches = re.findall(r'<script type=\"application/ld\\+json\">(.*?)</script>', html, re.DOTALL)
for m in matches:
    parsed = json.loads(m)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
"
```

### 5. Check hreflang tags

```bash
grep -E 'rel="alternate".*hreflang=' dist/index.html
# Should show zh-TW and x-default
```

### 6. Check BreadcrumbList

```bash
python3 -c "
import re, json
with open('dist/projects/wedding-2026/index.html') as f:
    html = f.read()
m = re.search(r'BreadcrumbList.*?\]', html)
if m:
    parsed = json.loads('{\"@type\":\"' + m.group() + '}')
    for item in parsed['itemListElement']:
        print(f\"  {item['position']}. {item['name']} → {item['item']}\")
"
```

### 7. Check robots.txt (read_file works fine here)

```bash
grep -E '^(Allow|Sitemap):' dist/robots.txt
```

### 8. Count projects in llms.txt

```bash
sed -n '/^## Portfolio/,/^## /p' public/llms.txt | grep -c '^- '
grep -c 'https://domain.tld/projects/' public/llms.txt
```

### 9. Verify specific description is rich content (not template)

Project detail pages should have descriptions derived from the page body,
not just "title — category". Check with:

```bash
grep -oE '<meta name="description" content="[^"]{100,}"' dist/projects/wedding-2026/index.html
# A rich description will be 100+ characters with unique body content
```

## Structured Checklist

When verifying SEO in a built static site:

| # | Check | How |
|---|-------|-----|
| 1 | Build passes | `pnpm run build` or equivalent |
| 2 | Site-level JSON-LD (WebSite + Person/Org) | grep `@type` patterns |
| 3 | Per-page schema present | grep for page-specific types (CreativeWork, Service, etc.) |
| 4 | Per-page schema not replacing site schema | Both should appear in the same page HTML |
| 5 | robots.txt with correct sitemap path | grep robots.txt |
| 6 | llms.txt listing all projects | sed + grep for count |
| 7 | OG image 1200×630 raster with absolute URL | grep OG meta tags |
| 8 | Canonical URL matches page | grep canonical |
| 9 | hreflang tags (zh-TW + x-default) | grep alternate |
| 10 | Title and description content correct | grep patterns |
| 11 | Project page descriptions are rich body content | grep for 100+ char description |

## Pitfalls

- **read_file truncates single-line HTML** — always use grep/python3 for minified output
- **Incomplete grep** — `grep 'Photographer'` finds the word anywhere (title, description, JSON-LD); use `'"@type":"Photographer"'` for schema type specificity
- **Description too short** — if the description is just "title — category" format, it's a template fallback, not rich content. Check char count ≥ 100
- **Missing hreflang** — easy to forget on subpages; check every page path (index, services, pricing, projects, about, each project detail)
- **llms.txt project count drift** — when adding new projects, the llms.txt must be updated too. Verify the count matches the expected project count
