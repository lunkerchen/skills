# YourBrand SEO + GEO — Astro Portfolio Walkthrough

Session date: 2026-07-21
Project: `your-brand.example.com` — Astro static portfolio for the site owner.

This file captures the exact implementation from the session, for reproduction
on similar Astro portfolio projects.

## Setup

- SSG: Astro 5 (static mode, `output: 'static'`)
- Content: Astro content collections with `cover`, `date`, `category`, `tags`, `location` frontmatter
- Sitemap: `@astrojs/sitemap` integration in `astro.config.mjs`

## Changes Made

### 1. Base.astro — centralised SEO/GEO layer

**Added to Props interface:**
```astro
jsonLd?: Record<string, unknown>;
```

**Site-level schema** (unconditional, every page):
```astro
const siteJsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'WebSite',
      '@id': `${site}/#website`,
      name: 'YourBrand',
      url: site,
      description: 'the site owner 的商業攝影與獨立開發作品集。',
      inLanguage: 'zh-TW',
      publisher: { '@id': `${site}/#person` },
    },
    {
      '@type': 'Person',
      '@id': `${site}/#person`,
      name: 'the site owner',
      alternateName: ['Laban', '@your-brand'],
      url: site,
      jobTitle: ['Commercial Photographer', 'Independent Developer'],
      homeLocation: { '@type': 'Country', name: 'Taiwan' },
      sameAs: [
        'https://instagram.com/your-brand',
        'https://threads.net/@your-brand',
        'https://x.com/your-handle',
        'https://github.com/your-handle',
      ],
    },
  ],
};
```

**Page-level schema** injected via prop:
```astro
const pageJsonLd = jsonLd && { '@context': 'https://schema.org', ...jsonLd };
// In <head>:
<script type="application/ld+json" set:html={JSON.stringify(siteJsonLd)}></script>
{pageJsonLd && <script type="application/ld+json" set:html={JSON.stringify(pageJsonLd)}></script>}
```

**OG/Twitter tags** — always absolute URL, image dimensions + locale added:
```astro
const imageUrl = new URL(image ?? '/images/og-image.webp', site).href;
// OG
<link rel="canonical" href={Astro.url} />
<meta property="og:image" content={imageUrl} />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="zh_TW" />
// Twitter
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content={imageUrl} />
```

Note: `{image && <meta ...>}` was replaced with unconditional tag that falls
back to the default OG image. This ensures every page has a social card even
if no per-page image is set.

### 2. index.astro — FAQPage JSON-LD on the homepage

```astro
const faqJsonLd = {
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'YourBrand 提供哪些攝影服務？',
      acceptedAnswer: { '@type': 'Answer', text: '人像、婚禮紀實、商業商品與品牌 campaign 攝影，也承接活動記錄與業配拍攝。' },
    },
    {
      '@type': 'Question',
      name: 'YourBrand 是否承接商業合作？',
      acceptedAnswer: { '@type': 'Answer', text: '承接台灣及海外的商業攝影委託與合作，可透過聯絡頁或 Instagram、X 私訊洽談。' },
    },
    {
      '@type': 'Question',
      name: '除了攝影，YourBrand 還提供哪些服務？',
      acceptedAnswer: { '@type': 'Answer', text: 'the site owner 也提供網站與 Landing Page 製作、SEO 與 GEO 優化、企業 AI 導入諮詢、資料庫優化及 App 開發服務。' },
    },
  ],
};
```

Passed as prop: `<Base ... jsonLd={faqJsonLd}>`

### 3. [...slug].astro — per-project CreativeWork schema

```astro
const projectJsonLd = {
  '@type': 'CreativeWork',
  name: title,
  description: `${title} — ${category} 攝影作品。`,
  image: new URL(cover, Astro.site).href,
  dateCreated: date.toISOString(),
  creator: { '@id': 'https://your-brand.example.com/#person' },
  keywords: tags.join(', '),
  url: Astro.url.href,
  ...(location && {
    contentLocation: { '@type': 'Place', name: location },
  }),
};
```

### 4. OG image generation

Source image was a portrait cover (`public/images/chuchu/cover.webp`).
Cropped to 1200×630 with sharp's attention-based cropping:

```bash
node -e "
import sharp from 'sharp';
await sharp('public/images/chuchu/cover.webp')
  .resize(1200, 630, { fit: 'cover', position: 'attention' })
  .webp({ quality: 86 })
  .toFile('public/images/og-image.webp');
"
```

### 5. Crawler files

**public/robots.txt:**
```
User-agent: *
Allow: /

Sitemap: https://your-brand.example.com/sitemap-index.xml
```

**public/llms.txt:**
```
# YourBrand — the site owner
> Taiwan-based commercial photographer and independent developer. The site presents
  photography services, selected work, and product engineering projects.

## About
the site owner, known as @your-brand, works across portrait, wedding,
commercial, and event photography. He also builds web products and automation
systems for businesses.

## Services
- Photography: portrait, wedding documentary, commercial product and brand campaign
  photography, event coverage, sponsored content, studio-lighting guidance, and
  video production.
- Digital product work: landing pages, SEO and GEO optimization, AI workflow
  consulting, database optimization, and mobile app development.

## Key pages
- Home: https://your-brand.example.com/
- Photography and digital services: https://your-brand.example.com/services
- Photography pricing: https://your-brand.example.com/pricing
- Selected photography work: https://your-brand.example.com/projects
- About the site owner: https://your-brand.example.com/about
- Contact: https://your-brand.example.com/contact

## Selected projects
- your-project: https://your-app.example.com/
- FDE Proposal: https://your-proposal.pages.dev/
- 批貨課程: https://your-landing.vercel.app/
```

The service descriptions in `llms.txt` were distilled from actual services
pages on the site — no invented claims.

## Verification

Build: `pnpm run build` → 24 static pages, `sitemap-index.xml`, 714ms.

Parsed built HTML to confirm:

| Page | Schema types | OG image | Canonical |
|---|---|---|---|
| `/` | WebSite, Person, FAQPage | `/images/og-image.webp` | `https://your-brand.example.com/` |
| `/projects/chuchu-2026/` | WebSite, Person, CreativeWork | `/images/chuchu/cover.webp` | `https://your-brand.example.com/projects/chuchu-2026/` |

Verification script:
```js
import { readFile } from 'node:fs/promises';
const html = await readFile('dist/index.html', 'utf8');
const schemas = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)]
  .map(([, json]) => JSON.parse(json));
const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)[1];
```

The `@astrojs/sitemap` integration auto-created `sitemap-index.xml` at `dist/`,
confirming the `robots.txt` path was correct.

## Notes

- The images referenced in OG/image tags point to WebP files from the
  content collection — the `cover` field in content frontmatter already
  pointed to `/images/.../cover.webp` and the Base layout converts to
  absolute URLs.
- No existing OG image was present before this session — the default card
  came from a generated one (first portrait cover cropped to 1200×630).
- The site had no `robots.txt` or `llms.txt` before this session.
- The `.gitignore` had a separate unrelated change that was left untouched.
