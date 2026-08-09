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

### 公開子集（admin 完整資料 → user-facing 子集）

把內部完整資料拆出公開子集（如 changelog：admin 看全部 17 項、公開頁只看 3 個版本）時：

1. **保留完整資料**：不要刪 admin 陣列 — 同時匯出 `adminXxxEntries`（完整）與 `publicXxxEntries`（子集），兩個頁面各 import 自己的；admin 功能不受影響
2. **crawler 內聯複製用公開子集**：`content.js` 的內聯陣列改成公開子集的逐字內容（不含內部版本/功能字樣）
3. **leak 測試雙向防漏**：測試同時 assert「公開項目存在（逐字字串）」+ `assert.doesNotMatch(html, /管理員|管理後台|Telegram|GA4|稽核|token|Passkey|JWT|反向代理|TLS|production/)` + 不存在的內部版本不出現（如 `assert.doesNotMatch(html, /開發版 2026|v2\.0/)`）。漏了公開項會紅、洩了內部項也會紅
4. **改完跑逐字同步驗證**：`scripts/verify-duplicated-data-sync.py` 比測試哨兵更嚴（測試只 assert 幾個關鍵字，逐字比對抓漏字/改字）

### 新增公開 SPA 路由的註冊清單

把一個既有 SPA 頁面（如 `/changelog`）加入 edge SEO pipeline，需同步三處 map：

1. `sitemap.xml.js` → `staticPaths`（讓它出現在 `/sitemap.xml`）
2. `seo.js` → `PUBLIC_ROUTES[route]`（title/description，不設 noindex）
3. `content.js` → `CONTENT_MAP[route]`（pre-render HTML 正文，含語意化 h1/摘要）

**`PRERENDERED_ROUTES` 不用動，但 `_middleware.js` 必須有 content 注入接線**：
- `PRERENDERED_ROUTES` 只 gate 建置期產生的靜態 HTML assets（如 `guides/*/index.html`）；純 SPA 路由沒有靜態 asset，不需要進。判定依據：該 route 在 `public/` 是否有建置產生的 `index.html`。
- **`CONTENT_MAP` 註冊 ≠ 自動注入**：`htmlResponse` 必須真的 import 並呼叫 `injectPrerenderedContent`（在 `injectSeo` 之後），`onRequest` 要把 `getPrerenderedContent(normalizedPathname)` 傳進 `htmlResponse`。漏了這步，crawler 只拿到 SEO meta，body 仍是空殼。完整接線與 regression test 模式：`references/middleware-content-wiring.md`

逐檔詳細步驟與「不 deploy 的端到端驗證」：`references/adding-public-route-checklist.md`；Deploy 與 production 雙層驗證：`references/deploy-and-production-verification.md`

## Reference Map

- `references/cf-pages-functions-pattern.md` — CF Pages Functions 完整實作（middleware + content + seo 三檔案架構）
- `references/your-app-cloudflare-implementation.md` — your-project 已驗證實例：完整檔案架構、動態行情 sitemap pattern、og-image 統一、server/client schema 重複處理、部署驗證
- `references/middleware-content-wiring.md` — content.js → _middleware.js 接線 recipe + middleware regression test 模式（mock ASSETS shell 需含 `<div id="root"></div>`）
- `references/deploy-and-production-verification.md` — deploy（project-aware、避免 positional `dist/` 掉 Functions bundle）+ production crawler/user 雙層驗證 + preview 404 propagation 踩坑
- `scripts/verify-duplicated-data-sync.py` — TS/JS 重複資料源逐字同步驗證腳本（版本欄位 + 所有字串項目全比對，`=\s*\[` 錨定避開型別註記坑）

## Pitfalls

- **不要做完整 SSR**：對現有 SPA 加 React SSR 改動極大，Edge Functions 注入是 80% 效果 20% 成本
- **Listing 頁的資料來源**：Edge Function 可以 fetch 同站 API，但要注意跨站延遲；crawl 不到就 fallback 到 JSON-LD only
- **React hydration**：注入的內容會被 React 覆蓋，但在 crawler 的 JS-less 請求中那不重要
- **JSON-LD 重複**：SPA 本身的 SEO component 可能也會注入 JSON-LD，要在 Edge Function 中徹底移除舊的
- **CF Pages Functions bundle 會因 deploy 方式掉包**：從 repo root 用 positional `dist/` 的舊 script deploy 不會把 frontend 的 Functions 一起上傳 → prerender/SEO 靜默失效。含 Functions 的專案一律在 frontend 目錄用 project-aware deploy（`wrangler pages deploy --project-name=<name> --branch main`），deploy 後務必 curl 驗證 `_middleware` 注入真的上線（raw HTML 有 h1/articles）
- **Preview hash URL 可能短暫 404（deployment propagation）**：剛 deploy 完的 `https://<hash>.<project>.pages.dev/<route>` 第一次 smoke 可能 404，稍後重試即 200；custom domain 通常先恢復。production 驗證以 custom domain 為準，preview 404 不要立刻宣告失敗，retry 一次
- **content.js 註冊 ≠ 注入完成**：曾發生 `/changelog` 三處 map 都註冊（sitemap/seo/CONTENT_MAP），但 `_middleware.js` 的 `htmlResponse` 從未 import/呼叫 `injectPrerenderedContent` → prerender HTML 完全沒進 response（SEO meta 有、body 空）。加公開路由後務必檢查 middleware 接線，並用 middleware regression test（mock ASSETS shell 需含 `<div id="root"></div>`，見 `references/middleware-content-wiring.md`）驗證 h1/articles 真的進 HTML
- **Edge Function 不能 import `src/` 的 TS 資料源**：functions 是獨立 bundle，`import ... from '../../src/data/changelog.ts'` 不可行 → 把資料內聯複製進 `content.js`，並在頂端留同步註解標明來源檔案路徑；改資料源時兩處都要改（可用測試 assert 版本數/關鍵字當同步哨兵，或直接跑 `scripts/verify-duplicated-data-sync.py` 做逐字比對）
- **程式化抽取 TS 陣列時 `str.index('[')` 會誤配型別註記**：`export const publicChangelogEntries: ChangelogEntry[] = [` 的第一個 `[` 是 `ChangelogEntry[]` 的型別註記，naive index 會抽出空區塊。必須用 regex 錨定 `=\s*\[` 再以括號深度配對（見 `scripts/verify-duplicated-data-sync.py` 的實作）。另注意 execute_code 沙箱 cwd 與 session 不同，讀檔用絕對路徑
- **patch 工具對含 `\/` 的 regex literal 會雙重轉義**：編輯 SEO 測試裡 `assert.match(html, /https:\/\/your-app.example.com\/.../)` 這類舊檔時，old/new string 的 `\/` 可能被轉成 `\\/` 產生 SyntaxError（Invalid regular expression flags）。patch 後檢查 lint，壞了就立即用正確單層 `\/` 重新 patch；old_string 多帶一兩行相鄰 context 避免「Found 2 matches」歧義（sitemap/seo 測試的 assert 行常重複出現）
- **判斷 Edge Function 內容用 read_file，不要 head/tail 截斷**：曾用 `head -60` 檢查 `_middleware.js`，輸出顯示 `trendsSitemap()` 像空函數（`{ } }`），誤判「sitemap-trends.xml 會 500」列為 P0；實際用 read_file 完整讀取發現函數完整（head 的縮排/截斷渲染誤導）。診斷 server function 前一律 read_file 看完整 body
- **動態 function 版 vs public/ 靜態檔必須同步**：Pages Functions 同名時 function 優先，靜態檔殘留舊內容會造成誤判（public/robots.txt 引用 sitemap-trends.xml 但 function 版沒有）。盤點時兩個版本都要看、都要同步
- **OG image 統一 PNG**：Edge Function 與 index.html 的 og:image 曾各指不同檔案（一個 .png 一個 .webp，實際只有 .webp 檔）。webp 在 Facebook 舊版/LINE 分享卡不支援 → 產生 1200×630 PNG 並統一所有引用點；搜引用用 `search_files pattern='og-image'`