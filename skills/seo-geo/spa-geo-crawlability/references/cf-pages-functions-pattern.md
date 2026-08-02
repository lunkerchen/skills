# CF Pages Functions SPA Pre-rendering 完整實作

your-project your-marketplace（React SPA on Cloudflare Pages）的真實案例。

## 三檔案架構

```
frontend/functions/
  _middleware.js    — 入口：路由判斷 + 呼叫 seo + content
  seo.js            — route metadata + JSON-LD schema + HTML injection
  content.js        — 各路由的預渲染 HTML + 動態 listing HTML
```

## `_middleware.js`

```js
import { injectSeo, resolveSeo } from './seo.js'
import { getPrerenderedContent, injectPrerenderedContent, getListingContent } from './content.js'

async function htmlResponse(context, assetPath, metadata, prerenderedContent) {
  const response = await context.env.ASSETS.fetch(`https://placeholder${assetPath}`)
  if (!response.ok) return null
  let html = injectSeo(await response.text(), metadata)
  if (prerenderedContent) {
    html = injectPrerenderedContent(html, prerenderedContent)
  }
  return new Response(html, {
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': metadata.noindex ? 'no-cache' : 'public, max-age=0, must-revalidate',
      'x-robots-tag': metadata.noindex ? 'noindex, nofollow' : 'index, follow',
    },
  })
}

export async function onRequest(context) {
  const { request } = context
  const url = new URL(request.url)
  const pathname = url.pathname
  const normalizedPathname = pathname !== '/' && pathname.endsWith('/') ? pathname.slice(0, -1) : pathname

  // Skip static files
  if (STATIC_EXT.test(pathname)) return await next()

  const metadata = await resolveSeo(url, getListing, getTrendsModel)

  // Dynamic: fetch listing data for product pages
  const listingContent = metadata.listingData ? getListingContent(metadata.listingData) : null
  // Static: lookup pre-written HTML for public routes
  const prerenderedContent = listingContent || getPrerenderedContent(normalizedPathname)

  return await htmlResponse(context, '/index.html', metadata, prerenderedContent)
}
```

## `content.js`

```js
// Static content map — each function returns HTML for <div id="root">
const CONTENT_MAP = {
  '/': heroHtml,
  '/about': aboutHtml,
  '/help': helpHtml,
  '/terms': termsHtml,
  '/privacy': privacyHtml,
  '/security': securityHtml,
  '/contact': contactHtml,
  '/explore': exploreHtml,
}

export function getPrerenderedContent(pathname) {
  const fn = CONTENT_MAP[pathname]
  return fn ? fn() : null
}

// Dynamic listing content from API data
export function getListingContent(listing) {
  if (!listing || listing.status !== 'active') return null
  const name = [listing.brand, listing.model].filter(Boolean).join(' ').trim()
  const price = listing.price
  const parts = [
    `出售 ${name}`,
    listing.condition ? `狀況：${listing.condition}` : null,
    price ? `價格 NT$ ${Number(price).toLocaleString('zh-TW')}` : null,
    listing.location ? `地點：${listing.location}` : null,
  ].filter(Boolean)
  return `<div><h1>${name}</h1><ul>${parts.map(p => `<li>${p}</li>`).join('')}</ul>${listing.description ? `<p>${listing.description}</p>` : ''}</div>`
}

export function injectPrerenderedContent(html, content) {
  if (!content) return html
  return html.replace(
    '<div id="root"></div>',
    `<div id="root">${content}</div>`
  )
}
```

## 實戰結果

| 指標 | Before | After |
|------|--------|-------|
| Site score | 19.8 | 30.2 |
| D-grade pages | 21 | 20 |
| C-grade pages | 4 | 5 |
| Pages with readable content | 4 | 8 |
| Score improvement | — | **+10.4 (52.5%)** |

## 重點教訓

1. **Static routes easy, dynamic routes harder** — 靜態路由預先寫好 HTML；listing/product 頁需要 Edge Function 去 fetch API，增加 latency
2. **Test with curl, not browser** — 瀏覽器執行 JS 覆蓋預渲染內容，curl 才看到 crawler 視角
3. **Deploy functions separate from static** — CF Pages deploy 先上 static assets 再上 functions bundle
4. **Rebuild after config changes** — `camera.json` 等 build-time config 改完要 `npm run build` 再 deploy
