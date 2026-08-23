---
name: site-seo-geo-audit
description: 全站 SEO+GEO 審計工作流 — site reconnaissance、逐頁 Schema 診斷、內容缺口分析、優先級矩陣、報告產出。被要求分析某個網站的 SEO/GEO 時優先載入此 skill。
read_when:
  - User asks "analyze this site" or "SEO audit" or "GEO analysis"
  - User provides a URL and asks for optimization recommendations
  - Evaluating a website's search visibility from both Google and AI perspectives
related_skills:
  - modern-seo-strategy: 底層 SEO+GEO 策略框架，此 skill 是該框架的 audit 實作工作流
  - geo-article-friendly: 逐篇內容 GEO 改造，audit 完成後的執行步驟
  - deep-research: 當需要深入探索某個主題時用於 fan-out 研究
---

# Site SEO+GEO Audit 工作流

## 核心原則：全站優先於單頁

最常見的錯誤是拿到一個 URL 就直接分析那一頁。**這會錯過**：
- 該頁在站點架構中的位置和權重
- 其他頁面的 Schema 錯誤
- 服務之間的內部連結潛力
- 整體主題權威與內容缺口

**只要有人給你一個網站 URL 請求 SEO/GEO 分析，第一步永遠是：先了解全站結構，再決定 scope。**

---

## 步驟一：Site Reconnaissance（站點盤點）

### 1.1 抓取 Sitemap

```
{domain}/page-sitemap.xml    — 頁面類
{domain}/post-sitemap.xml    — 文章類
{domain}/product-sitemap.xml — 商品類
{domain}/category-sitemap.xml — 分類類
{domain}/sitemap.xml          — 主索引
```

WordPress 站點通常有 Rank Math / Yoast 產出的結構化 sitemap。注意區分：
- **page**（靜態頁面：首頁/服務/關於/合作）
- **post**（部落格文章）
- **product**（WooCommerce 商品）

### 1.2 分類所有頁面類型

| 類型 | 範例 | Schema 標籤 |
|------|------|-------------|
| 商業服務 | /booking/, /pricing/ | LocalBusiness, Service |
| 商店 | /shop/, /studio-sale/ | Product, Store |
| 個人品牌 | /, /about-me/ | Person, ProfilePage |
| 部落格 | /blog/, /category/ | BlogPosting, CollectionPage |
| 合作 | /partnership/ | Service, Offer |
| Podcast | /podcast/ | PodcastSeries, PodcastEpisode |
| 購物流程 | /cart/, /checkout/ | 無（noindex 佳）|
| 政策 | /privacy-policy/ | WebPage（noindex 佳）|

### 1.3 逐頁 Schema 健康檢查

對於每個非文章頁面，確認：
- ✅ Schema 類型是否符合頁面本質？
- ❌ 常見致命錯誤：商業服務頁面用 `BlogPosting`、產品頁面用 `BlogPosting`、合作報價頁用 `BlogPosting`
- ✅ 必要的子屬性是否存在？（Offer / PriceSpecification / FAQ / HowTo）
- ✅ `@id` 正確？`url` 正確？

### 1.4 技術底線檢查

- robots.txt 是否阻擋 AI bot？（CF 用戶特別注意，需完整放行 44+ 款 Verified Bots，含 DevinBot/ManusBot/FirecrawlAgent 等）
- Cloudflare `Content-Signal` 標頭 / `<meta name="ai-content-signal">` 是否已配置？（`ai-train=yes, search=yes, ai-input=yes`）
- 機器可讀端點（RFC 8288 Link headers / HTML `<link>`：`rel="describedby"` `/llms.txt`、`rel="service-desc"` `mcp.json`/`openapi.json`、`rel="alternate"` `.md`）
- llms.txt / llms-full.txt 是否存在？
- H1 是否正確且含關鍵字？
- meta description 是否存在？
- 圖片 alt text 狀況
- 內部連結密度

### 1.5 產出站點地圖

一個表格或資訊圖，包含：
- 所有頁面 URL
- 當前 Schema 類型 vs 應該的 Schema 類型
- 現狀評分（✅/⚠️/❌）
- 優先級

---

## 步驟二：內容缺口分析

### 2.1 主題分類

將所有文章按主題歸類（遊戲、科技、旅遊、攝影…），計算每類篇數。

### 2.2 Pillar Page 機會

判斷是否有足夠內容支撐建立 pillar page → cluster 架構：
- 該主題有 5+ 篇優質文章？
- 這些文章有持續的自然流量？
- 競爭對手有 pillar page？

### 2.3 舊內容新鮮度

- 標記每篇文章的最後更新日期
- ＞3 年 → 考慮合併或更新
- AI 有強烈近期偏誤，關鍵頁面至少每季更新一次

### 2.4 Ahrefs 4 大 AI 搜尋審計維度（AI Search Pillars Audit）

依據 Ahrefs 4 支柱框架審查目標網站的 AI 搜尋準備度：

1. **企業真相來源（Source of Truth）**：
   - 產品規格、功能列表、定價策略、常見問答（FAQ）是否有清晰、結構化的專門頁面？
   - 外部可控 Profiles（G2, Capterra, LinkedIn, Crunchbase, App Store 等）之品牌描述與定價是否與官網同步一致？
2. **外部共識與 SEvO 足跡（Outside Evidence & SEvO Footprint）**：
   - 是否在 YouTube 擁有帶字幕與章節的教學/評測（相關性最強 ~0.737）？
   - 是否在 Reddit、論壇與權威產業媒體有自然品牌討論與未加連結的品牌提及（Unlinked brand mentions）？
3. **抗摘要深度資產（Anti-Summarization & Deep Content）**：
   - 是否有免費互動工具、試算機、評估表（「Free tools」關鍵字抗 AIO 零點擊最有效）？
   - 是否有一手原創數據、深度實驗或獨家調查報告（具備高 Information Gain，迫使 AI 引述來源）？
4. **AI 缺口與過期引用修復（AI Gaps & Outdated Citations）**：
   - 識別 AI Mention Gap（競品被推薦但自家缺席）與 AI Citation Gap（競品被引述但自家無對應資產）。
   - 找出可能被 AI 頻繁引用但內容陳舊（舊定價、已棄用功能）的頁面，列為優先更新項目。

---

## 步驟三：優先級矩陣產出

| 級別 | 定義 | 典型項目 |
|------|------|----------|
| P0 | 當天要做，SEO 基礎錯誤 | Schema 類型全錯、無 H1、llms.txt 缺失 |
| P1 | 本週內，高 ROI | FAQ/Review Schema 導入、外部平台登錄、段落結構化 |
| P2 | 兩週內，中長期 | Pillar page 建立、內部連結強化、分類頁 SEO |
| P3 | 按需，低優先 | Core Web Vitals、舊文合併、品牌提及策略 |

難度分級：低（WP 後台設定）/ 中（批量操作或需開發）/ 高（跨月專案）

### Portfolio / Photography Site Execution Order

For sites with a portfolio/gallery core (photography, design, creative portfolios), follow this execution sequence after the audit:

1. **Check existing infra** — sitemap, robots.txt, GA4, llms.txt. Don't rebuild what works.
2. **Structured data first** — JSON-LD (WebSite + Person + Photographer/Artist/CreativeWork trio in `@graph`). Single highest-impact change for local search.
3. **Title & meta description** — every page gets unique, location+keyword-rich titles. Include city and service keywords.
4. **Content depth for GEO** — expand portfolio descriptions with technical specifics (gear, lighting, location, editing). AI citation requires citeable detail.
5. **llms.txt** — comprehensive list of all entries with URLs and descriptions.
6. **Build-verify** — rebuild and verify expected tags on every page.

For concrete JSON-LD patterns, BreadcrumbList implementation, and GEO description expansion templates, see `content-driven-static-site` skill reference `references/portfolio-seo-geo.md`.

For a real-world execution trace of this audit workflow on an Astro portfolio (execution order, JSON-LD details, GEO batch expansion, llms.txt, verification delegation), see `references/portfolio-ssg-execution.md`.

---

## 步驟四：報告產出

### 4.1 格式

預設產出格式：**HTML 報告**（深色主題，單頁可列印/截圖）。

結構：
- Header：分析日期、目標 URL、平台、綜合評分
- 逐頁 Schema 錯誤表
- 全站共通問題
- GEO 改造要點（含 llms.txt 內容）
- 內容策略建議
- 優先級執行矩陣
- 建議執行時程

### 4.2 內容要點

- 答案置前：每節首句直接給診斷結論
- 用表格 + bullet 取代長段落
- 重要 Schema JSON 直接可複製貼上
- P0 項目特別標註

---

## 注意陷阱

1. **不要只看一頁** — 全站 reconnaissance 永遠在單頁分析之前。用戶給一個 URL 不表示他只想知道那一頁。
2. **不要跳過 sitemap** — 它是理解網站最快的方式。如果 sitemap 不存在，用 site:domain 搜尋。
3. **WP 站點注意** — Rank Math / Yoast 預設 Schema 常設為 BlogPosting，這是全站性錯誤的最常見原因。
4. **CF 用戶注意** — Cloudflare 預設已改為阻擋 AI 機器人，需手動放行 `GPTBot` / `ChatGPT-User` / `Google-Extended`。即便未用 CF，也建議在 robots.txt 明確 `Allow` 這三個 AI crawler — 明示優於默認，成本為零。完整範例見 `static-site-geo` 的 `references/event-landing-page-geo.md`。
5. **Schema 不是越多越好** — 每頁一個主要類型 + 必要的子類型（Offer/FAQ/Review）即可。不要堆疊不相關的 Schema。
6. **不要診斷了不改** — 報告產出後應提供可直接操作的程式碼或設定文字。
