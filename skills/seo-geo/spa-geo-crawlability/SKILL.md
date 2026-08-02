---
name: spa-geo-crawlability
description: Fill SPA empty HTML via Edge Functions
  for AI crawlers.
---

# SPA GEO Crawlability

## Use

當一個 React/Vue 等前端 SPA 的 GEO 審計報告顯示「靜態 HTML 幾乎無正文，AI 抓取器讀不到內容」（D 級，0 詞）、或結構化數據（JSON-LD）缺失時觸發。

**類別**：web app GEO 的子領域；專注 SEO/GEO 的「可抓取性」層，不涵蓋內容策略或外部陣地建設。

## 問題

SPA 的部署輸出是一個空 HTML 殼（`<div id="root"></div>`），內容靠 JS 渲染。多數 AI crawler（GPTBot、Claude、Perplexity 等）不執行 JS，看到的頁面是空的。GEO 審計工具判定此頁「0 詞正文，D 級」。

## 解法：Edge Functions 注入

不需要完整 SSR。在 Edge Runtime（CF Pages Functions、Vercel Edge Functions）攔截請求，注入：

1. **Route-specific SEO meta**（title, description, OG, canonical）
2. **Route-specific JSON-LD schema**（AboutPage, ContactPage, Product, FAQPage 等）
3. **Pre-rendered HTML content** 放進 `<div id="root">` —— crawler 看到正文，瀏覽器端 React 接手覆蓋

### 架構

```
請求 → Edge Function (middleware)
         ├→ resolveSeo(url) → route metadata + schema
         ├→ getPrerenderedContent(route) → static HTML
         │   (or: getListingContent(data) → dynamic HTML)
         ├→ injectSeo(html, metadata) → 換 meta + 加 JSON-LD
         └→ injectContent(html, prerendered) → 填入 <div id="root">
      → 回應給 crawler/browser
```

### 重要邊界

- **static routes**（about, terms, contact, privacy, help, home）: 預先寫好完整 HTML 正文，含 GEO 可抽取塊（定義、數字、FAQ）
- **dynamic routes**（listing/product pages）: 在 Edge Function 中透過 API 抓取資料，動態生成 HTML 正文
- **JSON-LD + meta**：所有路由都注入
- **SEO meta 優先於 body**：crawler 至少讀到 title/description/schema，即使 body 注入出錯
- **不出錯**：Edge Function 應有 try/catch，fallback 到原始 SPA index.html

## Reference Map

- `references/cf-pages-functions-pattern.md` — CF Pages Functions 完整實作（middleware + content + seo 三檔案架構）
- `references/your-app-cloudflare-implementation.md` — your-project 已驗證實例：完整檔案架構、動態行情 sitemap pattern、og-image 統一、server/client schema 重複處理、部署驗證

## Pitfalls

- **不要做完整 SSR**：對現有 SPA 加 React SSR 改動極大，Edge Functions 注入是 80% 效果 20% 成本
- **Listing 頁的資料來源**：Edge Function 可以 fetch 同站 API，但要注意跨站延遲；crawl 不到就 fallback 到 JSON-LD only
- **React hydration**：注入的內容會被 React 覆蓋，但在 crawler 的 JS-less 請求中那不重要
- **JSON-LD 重複**：SPA 本身的 SEO component 可能也會注入 JSON-LD，要在 Edge Function 中徹底移除舊的
- **CF Pages Functions bundle**：`content.js` 等被 `_middleware.js` import 的檔案會自動打包
- **判斷 Edge Function 內容用 read_file，不要 head/tail 截斷**：曾用 `head -60` 檢查 `_middleware.js`，輸出顯示 `trendsSitemap()` 像空函數（`{ } }`），誤判「sitemap-trends.xml 會 500」列為 P0；實際用 read_file 完整讀取發現函數完整（head 的縮排/截斷渲染誤導）。診斷 server function 前一律 read_file 看完整 body
- **動態 function 版 vs public/ 靜態檔必須同步**：Pages Functions 同名時 function 優先，靜態檔殘留舊內容會造成誤判（public/robots.txt 引用 sitemap-trends.xml 但 function 版沒有）。盤點時兩個版本都要看、都要同步
- **OG image 統一 PNG**：Edge Function 與 index.html 的 og:image 曾各指不同檔案（一個 .png 一個 .webp，實際只有 .webp 檔）。webp 在 Facebook 舊版/LINE 分享卡不支援 → 產生 1200×630 PNG 並統一所有引用點；搜引用用 `search_files pattern='og-image'`