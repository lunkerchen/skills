# your-project — CF Pages Server-Side SEO 實作對照（2026-08-01）

React + Vite SPA + Cloudflare Pages Functions + D1/R2（已從 FastAPI/Vercel 遷移）。Domain: your-app.example.com。這份記錄是「Edge Functions 注入」架構的**完整已驗證實例**，未來同類 SPA 可直接對照。

## 檔案架構

```
frontend/
├── functions/
│   ├── _middleware.js      # 總路由：/api/* proxy → Worker；/sitemap-trends.xml 攔截；靜態放行；其餘 SPA fallback + injectSeo
│   ├── seo.js              # PUBLIC_ROUTES + GUIDE_ROUTES + listingMetadata() + trendsModelMetadata() + resolveSeo() + injectSeo()
│   ├── content.js          # guide 頁 pre-rendered HTML 內容
│   ├── sitemap.xml.js      # 動態 sitemap（staticPaths + active listings from API，含 lastmod、cursor 分頁 50 頁 × 100）
│   ├── robots.txt.js       # 動態 robots（Disallow private prefixes + Sitemap 宣告）
│   └── *.test.js           # node --test 單元測試（seo/robots/sitemap），npm run test:functions
├── public/
│   ├── robots.txt          # 靜態版（function 優先，殘留需同步）
│   ├── sitemap.xml         # 靜態版（function 動態版優先）
│   ├── llms.txt            # 4KB 完整（About/Features/Pages/Guides/API/Categories/Condition/brands）
│   └── og-image.png        # 1200×630 PNG（原為 webp，統一改 PNG）
└── src/
    ├── config/marketplace.ts + profiles/camera.json   # multi-profile：brand/domain/seo 全從 profile 讀
    ├── components/SEO.tsx  # jsonLd prop（支援 array）、OG 強化、cleanup
    └── pages/*.tsx         # Home(WebSite+Organization array)、Help(FAQPage)、ListingDetail(Product/Demand)、Explore/Guides(ItemList)、GuideDetail(Article+Breadcrumb)、Trends(Dataset)
```

## 關鍵 pattern

### 1. middleware 對每條路由做 server-side injection
```js
// _middleware.js
const metadata = await resolveSeo(url, getListing, getTrendsModel)
const response = await htmlResponse(context, '/index.html', metadata)  // injectSeo 換 meta + 加 JSON-LD
```
- `injectSeo(html, metadata)` 用 regex 清掉舊 title/meta/canonical/所有 JSON-LD，再注入 route-specific 版
- server 注入的 JSON-LD 標記 `data-seo-managed="server"`；client SEO.tsx 掛載時移除 server 版再注入自己的 → 避免重複（**但 Home 頁只剩 client 版：若 client 只有 WebSite、server 有 Organization，Organization 會丟失 — 修法：client jsonLd 用 array 同時帶 WebSite+Organization**）

### 2. 動態行情 sitemap（獨立 URL 型頁面）
```js
// _middleware.js 攔截 /sitemap-trends.xml
async function trendsSitemap() {
  const response = await fetch(`${WORKER_URL}/api/trends/trending?days=365&limit=200`)
  const models = await response.json()
  // → <url><loc>https://your-app.example.com/trends/{brand}/{model}</loc><changefreq>weekly</changefreq></url>
  // catch → 空 urlset（200，不 500）
}
```
robots.txt 同時宣告 `Sitemap: sitemap.xml` + `Sitemap: sitemap-trends.xml`。

### 3. sitemap 動態商品 URL
`sitemap.xml.js` 從 `GET /api/listings/search?sort=newest&page_size=100&cursor=` 分頁拉到全部 active listings，輸出 `/listings/{id}` + lastmod（updated_at/created_at slice 10）。cache-control `max-age=300`。

## 這次修掉的問題（檢查清單）

1. og:image 三處引用不一致（index.html→.png、SEO.tsx/seo.js→.webp，實際只有 .webp 檔）→ 產生 og-image.png 統一全部引用
2. 首頁 client schema 只帶 WebSite 丟失 server 的 Organization → 改 array [WebSite, Organization]
3. sitemap staticPaths 缺 /trends（seo.js 有 PUBLIC_ROUTES /trends 但 sitemap 沒有）→ 補上
4. robots.txt.js 動態版沒宣告 sitemap-trends.xml（public/ 靜態版有）→ 同步 + 測試補 assert

## 驗證

- `npm run test:functions` → node --test functions/*.test.js（mock globalThis.fetch 測 middleware）
- `npx tsc -b` → Home.tsx jsonLd 改 array 型別仍過（SEO jsonLd prop 支援 `Record<string, unknown>[]`）
- 部署：`npm run deploy`（build + `wrangler pages deploy --project-name=your-app --branch main`）
- 部署後 curl 驗證：`/sitemap-trends.xml`、`/robots.txt`、`/og-image.png`
