# Next.js / App Router live-site SEO audit — bug classes & probes

來源：2026-08-15 yotron-ai.com（Next.js App Router, Next 新版 + Zeabur）全站稽核。
適用任何 App Router / SSG 站的 live-audit；與 Astro 的 dist 驗證互補（此為對「已部署站」的檢查）。

## 高頻 bug class（App Router 特有，WP/Astro 檢查清單抓不到）

1. **Title template 疊加 → 雙後綴**
   Root layout 設 `title: { default, template: "%s | 品牌" }`，動態路由頁面 metadata.title
   若自帶「| 品牌」（或含頁面層級 suffix），live `<title>` 會變成
   `GEO 是什麼？ | AI 術語表 | 優創智能 | 優創智能`。
   實測 /glossary/* 全部 25 頁中招、/insights/* 亦中招；blog/cases/newsroom 正常
   （其 title 只放頁面名）。
   Fix：頁面 metadata.title 只寫頁面名，品牌後綴一律交給 root template。

2. **`published: false` 只擋列表，不擋直連**
   `getAllPosts()` 有 `.filter(post => post.published)`，但 `getPostBySlug()` 不過濾 →
   hidden 文章直連 200、無 noindex、仍可被爬蟲索引（sitemap 正確排除，llms.txt 卻還列著
   其中一篇舊旗艦文）。
   Fix：`generateMetadata` 對 unpublished 加 `robots: { index: false }`；llms.txt/feed 生成
   時同樣排除 unpublished。

3. **WebSite schema 的 SearchAction 指向 404**
   `generateWebSiteSchema()` 的 `potentialAction.target` 寫死 `/search?q=`，但站上根本沒有
   `/search` 路由 → 結構化資料指向 404。
   Probe：`curl -o /dev/null -w "%{http_code}" https://site/search?q=x`。
   Fix：沒有 search 頁就移除 potentialAction，或真的建 search 路由。

4. **索引/列表頁缺自訂 metadata → 與首頁 title 重複**
   `app/cases/page.tsx` 沒 export metadata/generateMetadata → 繼承 root default，
   title/description 與首頁完全一樣（Google 視為 duplicate）。
   Probe：列所有 `app/**/page.tsx`，凡無 `export const metadata` / `generateMetadata`
   的靜態索引頁都要補。

## Live probe 配方（urllib / curl，無需登入）

- Sitemap 總數與分節：
  `curl -s https://site/sitemap.xml | grep -o '<loc>' | wc -l`
  `curl -s https://site/sitemap.xml | grep -o 'blog/[a-z0-9-]*' | sort -u | wc -l`
- 對照內容目錄：本地 `ls content/blog/*.mdx | wc -l` vs sitemap blog 數 → 差額即
  unpublished 集合（先確認每篇 `published:` 欄位，別當漏抓）。
- Schema 盤點：`curl -s <url> | grep -o '"@type":"[^"]*"' | sort | uniq -c` —
  一眼看出哪頁缺 FAQPage/Article/Service。
- Title 重複偵測：`grep -oE '<title>[^<]*</title>'`，凡含兩個「| 品牌」即 template 疊加。
- 全站 status sweep：把 sitemap locs 全部抓出來逐個打 status，404 的即 sitemap 垃圾
  （實測 yotron sitemap 167 URLs 全 200，健康）。
- llms.txt 過時偵測：`curl -s https://site/llms.txt | grep -c 'site/blog'` vs
  實際 published 數 — 落差 = AI 引擎讀不到近半內容（GEO 硬傷）。

## 本次稽核結論（範例輸出）

基建 B+：Organization/WebSite/LocalBusiness/Article/FAQPage/Service/Event schema 全站
就位、robots/sitemap/llms.txt 三件套齊全、GA4+Ahrefs 有、canonical 每頁有。
P0：SearchAction 404、llms.txt 只列 33/65 篇。P1：glossary 25 頁雙後綴、/cases 無 metadata、
11 篇 unpublished 可索引、robots.txt 未明示放行 AI crawler。P2：sitemap lastmod 全用
部署時間、blog 分頁未入 sitemap、活動頁過期未移除。
