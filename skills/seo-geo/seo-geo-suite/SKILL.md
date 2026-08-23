---
name: seo-geo-suite
description: SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台：涵蓋傳統搜尋、生成式引擎、問答抽取、Is-Agentic 100分規範、Cloudflare L0-L5、全站審計、內容改造與自動化驗證。
version: 2.0.0
author: Community
license: MIT
read_when:
  - User asks about SEO, GEO, AEO, Answer Engine Optimization, or AI search visibility
  - User wants to optimize a website, web app, or single page for Google, Perplexity, ChatGPT, Claude, DeepSeek
  - User asks to check or improve site score with is-agentic.com (npx is-agentic) or isitagentready.com
  - User wants direct answers, featured snippets, voice search, or AI citations
  - User wants to transform articles or video transcripts into AI-friendly citeable QA content
  - User needs an end-to-end SEO/GEO/AEO/Agentic workflow (audit -> optimize -> verify -> monitor)
  - User mentions llms.txt, Markdown Twin, Content Negotiation, Schema markup, Speakable, or AI crawlers
  - User wants to analyze Google Search Console (GSC) searchAnalytics or properties data
metadata:
  hermes:
    tags: [seo, geo, aeo, agentic, is-agentic, cloudflare, llms-txt, schema, gsc, suite]
---

# SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台

整合傳統搜尋引擎優化（SEO）、生成式引擎優化（GEO）、答案引擎優化（AEO）與 AI 代理就緒標準（Agent-Readiness / Is-Agentic）的一體化全能解決方案。

---

## 核心認知：現代搜尋與 Agentic 四軌體系

```
                               ┌────────────────────────────────────────────────────────┐
                               │             現代搜尋與 Agentic 四軌體系 (2026+)        │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
         ┌─────────────────────────┬───────────────────────┴────────────────────────┬─────────────────────────┐
         ▼                         ▼                                                ▼                         ▼
【SEO 搜尋引擎優化】        【GEO 生成式引擎優化】                           【AEO 答案引擎優化】       【Agent-Readiness 代理就緒】
  Search Engine Optimization Generative Engine Optimization                  Answer Engine Optimization  Agent-Native Architecture
 • 標的：Google, Bing 藍色連結• 標的：ChatGPT, Claude, DeepSeek, Gemini     • 標的：Perplexity, AIO, 語音 • 標的：Autonomous AI Agents
 • 核心：排名 (Rankings) & 點擊 • 核心：品牌共識 (SOV) & 深度抗摘要內容     • 核心：直接答案 (Direct Answer) • 核心：可發現、可存取、可操作
 • 手段：Topic Cluster、反向連結• 手段：全網證據 (Reddit/YouTube)、原創數據 • 手段：40-60字首句、QA Schema  • 手段：Is-Agentic 100分、MCP、
 • 指標：SERP 排名、有機流量、CTR• 指標：AI Mentions、Citations、Perception  • 指標：精選摘要率、Direct 引用率 • 指標：Is-Agentic Score、RFC 9457
```

---

## 全能意圖路由器（Intent Router & Execution Matrix）

| 使用者場景與意圖 | 對應旗艦模組 | 核心執行任務與 SOP |
|---|---|---|
| **「規劃跨 Google、AI 與問答引擎的整體策略」** | **模組 1：戰略規劃** | 盤點主題地圖、Ahrefs 4 支柱、Fan-out 查詢、競品 AI Mention/Citation 落差分析。 |
| **「全面體檢網站的 SEO、GEO、AEO 與 Agent 友好度」**| **模組 2：全站審計** | 跑 `npx is-agentic <url>` + Sitemap Reconnaissance + 逐頁 Schema 診斷，輸出 P0~P3 矩陣。 |
| **「讓文章/長文/腳本能被 AI 快速引用與直接回答」** | **模組 3：內容工程** | 倒金字塔 40-60 字結論置頂、Passage Citability（150-250字獨立段落）、串接 `stop-slop`。 |
| **「影音/Podcast 逐字稿轉為高引用問答與 FAQ」** | **模組 3：內容工程** | 逐字稿清洗、高引用問句提取（How/Why/Best/Vs）、注入 FAQPage & Speakable Schema。 |
| **「靜態網站（Astro/Hugo/Next）加入結構化與 OG」**| **模組 4：架構優化** | JSON-LD 三件套（WebSite+Organization/Person+Service）、SVG OG Image 自動管線。 |
| **「Web 應用 / SPA / SaaS 導入隱式 GEO/AEO」** | **模組 4：架構優化** | 首頁語意加固、JSON-LD `@graph`、產品 PDP Schema、保護結帳路徑同時放行購物 Agent。 |
| **「設定 AI 爬蟲 Content Negotiation 與 Markdown」**| **模組 5：代理就緒** | 支援 `Accept: text/markdown`、配置 `Vary: Accept, Accept-Encoding`、產出 .md 雙生檔案。 |
| **「建立/維護標準 llms.txt 與 llms-full.txt」** | **模組 5：代理就緒** | 依據 llmstxt.org 標準動態/靜態生成，強制注入 `## When to use this site` 任務指引。 |
| **「解決 SPA / React 前端在 AI 爬蟲前內容空白問題」** | **模組 5：代理就緒** | Cloudflare Pages Functions 中間件、UA 判斷、SSR 預渲染 HTML 與 Schema 注入。 |
| **「設定 Cloudflare Agent-Readiness (L0-L5) 與 MCP」**| **模組 5：代理就緒** | `Content-Signal` 標頭、`/.well-known/mcp/server-card.json`、`/.well-known/ai-catalog.json`。 |
| **「查詢與分析 Google Search Console 搜尋成效」** | **模組 6：GSC 數據** | 透過 GSC API 抓取 clicks/impressions/CTR/position、URL Inspection 診斷與提交 Sitemap。 |
| **「CI/CD 或部署前自動驗證全站標籤與 404 引導」** | **模組 7：驗證門戶** | 執行 6-Gate 自動化測試（H1/Title/Meta/JSON-LD/Canonical/Agent 404 / Vary）。 |
| **「排程監控品牌在 Google 與 AI 中的聲量」** | **模組 7：長效監控** | 設定 Cron 定期檢查品牌詞第一頁能見度、AI Mention/Citation 變化與過期預警。 |

---

## 7 大旗艦功能模組

### 模組 1：戰略規劃與 AI 引用缺口分析 (Strategy & Gap Analysis)
1. **Ahrefs 4 大支柱**：
   - 企業真相源（Source of Truth）：清晰不可被曲解的官方定位。
   - 外部共識（Outside Evidence）：YouTube 逐字稿 (~0.737 相關度)、Reddit、維基與權威目錄。
   - 抗摘要深度資產（Deep Content）：具備獨家數據、案例、計算公式之實戰內容。
   - 平均 SOV（Share of Voice）量化追蹤。
2. **AI Mention & Citation Gap 診斷**：
   - 收集同業在 ChatGPT / Perplexity / AIO 的推薦情境。
   - 鎖定「競品被提及而自家缺席」的語意缺口（Context Gaps）。
3. **台灣在地化語意對齊（GeoLook TW）**：
   - 繁體中文市場用語校準、消保/政府開放資料關聯、在地實體對齊。

### 模組 2：全站與單頁深度審計 (Full-Site & Is-Agentic Audit)
1. **Site Reconnaissance 盤點**：
   - 抓取全站 Sitemap（page, post, product, category），依頁面類型分類。
   - 檢查每頁的 H1、Canonical、Meta Description、JSON-LD `@graph`。
2. **Is-Agentic（Vercel Labs / Ora）100 分審計流程**：
   - 執行 `npx is-agentic <url> --json`。
   - **Essential（80 分池）**：No-JS SSR 內容（H1 + 500+ 字元）、AI 爬蟲無阻擋、真實 404/301/302、Markdown 協商帶 `Vary: Accept, Accept-Encoding`、OpenAPI 規格與 RFC 9457 結構化錯誤。
   - **Recommended（20 分池）**：`llms.txt` 具備 `When to use this site` 指引、Sitemap 存在、內容效率 $\ge 5\%$、Rich JSON-LD、信任錨點頁（/about, /contact, /privacy）、RateLimit 標頭、100% 原生控制項與 Accessible Names。
   - **Bonus（+5 分上限）**：MCP Apps（`ui://`）、Generative UI、無 a11y Prompt Injection。

### 模組 3：內容工程、問答抽取與 AEO 改造 (Content Engineering & AEO)
1. **倒金字塔 40–60 字答案置頂（Answer-First Principle）**：
   - 每個 H2/H3 下方第一句話直接回答核心問題，定義事實、給出數字或結論。
2. **Passage Citability（段落可提取性）**：
   - 單段長度控制在 150–250 繁中字（134–167 英文單字），具備上下文獨立性，禁止無主詞的指涉代名詞。
3. **高引用結構轉換**：
   - 對齊「Best」(7.06%)、「How-to」(6.35%)、「Top」(5.50%)、「Vs」(4.88%) 四大高引用句型。
4. **影音/Podcast 逐字稿 AEO 化**：
   - 逐字稿清洗口語贅字，轉為高引用問答段落，注入 `FAQPage`、`QAPage` 與 `Speakable` 標籤。
5. **去除 AI 套話（串接 stop-slop）**：
   - 內容改造後自動去除樣板化廢話與機械感連接詞，保留創作者原始口吻。

### 模組 4：靜態站 (SSG) 與 Web 應用 (SPA/SaaS) 架構優化
1. **JSON-LD `@graph` 規格**：
   - 整合 `WebSite`、`Organization` / `Person`（含 `contactPoint`、`address`、`sameAs`）、`Service` / `Product`、`BreadcrumbList`。
2. **電商與產品頁 Agentic Commerce（UCP/ACP/AP2）**：
   - `Product` + `Offer` 補齊 `priceCurrency`、`availability`、`hasMerchantReturnPolicy`、`shippingDetails`。
   - 放行 AI 購物搜尋 Bot，隔離保護結帳與支付端點。
3. **動態 OG Image 管線**：
   - SVG 模板或 Satori 自動生成 1200×630 高清社群分享卡。

### 模組 5：AI 專屬協定、機器可讀中繼與 Agent 就緒 (Agent-Readiness & Machine Interfaces)
1. **Robots.txt & Content-Signal**：
   - `Content-Signal: ai-train=yes, search=yes, ai-input=yes`
   - 放行主流 AI 爬蟲（`GPTBot`, `ClaudeBot`, `ora-agent`, `DeepSeekBot`, `ChatGPT-User`, `Google-Extended`, `PerplexityBot`, `Bytespider`, `Meta-ExternalAgent` 等）。
   - 宣告 `Sitemap`、`LLMs-txt` 與 `Agentmap`。
2. **標準 `llms.txt` 與 `llms-full.txt` 規格**：
   - 必須包含 `## When to use this site (Agent instructions / 給 AI Agent 的使用指引)`。
   - 列出適用查詢、不適用查詢、核心服務、定價與客服閉環導引。
3. **Markdown Content Negotiation**：
   - 伺服器支援 `Accept: text/markdown` 回傳乾淨 Markdown。
   - 標頭必須帶 `Vary: Accept, Accept-Encoding`，避免 CDN 快取污染。
4. **Cloudflare Level 0–5 協定矩陣**：
   - L1: `robots.txt`, `sitemap.xml`, RFC 8288 `Link` 標頭。
   - L2: `Content-Signal` 標頭與 AI 爬蟲規則。
   - L3: Markdown 內容協商與 `X-Markdown-Tokens`。
   - L4: MCP Server Card (`/.well-known/mcp/server-card.json`)、Agent Skills Index (`/.well-known/agent-skills/index.json`)、RFC 9727 API Catalog。
   - L5: Agentic Auth metadata (`/auth.md` & `/.well-known/oauth-protected-resource`)。
5. **SPA 爬蟲預渲染（Edge Functions Rescue）**：
   - 透過 Cloudflare Pages Functions 或 Edge 中間件識別 AI Bot UA，注入完整 SSR HTML 與結構化資料。

### 模組 6：Search Console 數據獲取與分析反饋 (GSC Analytics & Performance Loop)
1. **GSC API 授權與查詢**：
   - 透過 Google ADC / OAuth 存取 Search Console API。
   - 依維度（query, page, country, device）撈取 clicks, impressions, CTR, average position。
2. **部署反饋時序與成效追蹤**：
   - 記錄修改部署時間戳，追蹤 7天 / 14天 / 28天 之成效位移。
3. **自動化 URL Inspection & Sitemap 重新提交**。

### 模組 7：發布前自動化門戶驗證與長效監控 (Verification Gates & Long-term Watchdog)
1. **發布前 6 道品質門戶（6 Quality Gates）**：
   - **Gate 1：HTML 語意與標籤**（單一 H1、Title 長度 30-60 字元、Description 70-150 字元）。
   - **Gate 2：結構化資料驗證**（JSON-LD 語法正確、必填欄位無缺漏）。
   - **Gate 3：Canonical 與 OpenGraph**（Canonical 絕對路徑、OG 標籤完備）。
   - **Gate 4：機器可讀檔案**（`robots.txt`、`sitemap.xml`、`llms.txt` 存在且格式合法）。
   - **Gate 5：Agent-Friendly 404 驗證**（404 狀態碼真實回傳，頁面帶 Markdown 導航指示）。
   - **Gate 6：HTTP 標頭與快取合規**（`Vary: Accept, Accept-Encoding`、安全標頭）。
2. **品牌搜尋與 AI SOV 長效監控（Brand Watchdog Cron）**：
   - 排程每日/每週檢查品牌詞第一頁能見度與 AI 引用提及率，異常時主動警報。

---

## 5 大標準執行管線

### 管線 1：新網站 / 新專案建置上線 8 步標準流程（Greenfield Deployment）
```
1. 語意架構設計 ──> 2. 結構化資料注入 ──> 3. AI 爬蟲與權限聲明 ──> 4. llms.txt 生成
   (HTML5 + a11y)      (JSON-LD @graph)     (robots.txt + Signals)  (含 When-to-use)
          │                                                                 │
          ▼                                                                 ▼
8. 部署與 Live 抽檢 <── 7. 6-Gate 建置驗證 <── 6. L5 代理就緒套件  <── 5. Markdown 協商
   (curl 驗證 Header)   (verify-seo 腳本)       (10大協議端點到位)      (Middleware 攔截)
```

#### 新專案 Level 5 Agent-Native 一次到位清單（必備 10 大檔案與設定）
1. **`robots.txt`**：注入 RFC 9309 AI Bot 放行規則 + `Sitemap:` + `Agentmap:` + `Content-Signal:`。
2. **`next.config.ts` / HTTP Headers**：配置 `Content-Signal`、RFC 8288 `Link` 標頭（關聯 `llms.txt`、`sitemap.xml`、`agent-skills`、`api-catalog`、`mcp-server-card`）與 `Vary: Accept, Accept-Encoding`。
3. **`proxy.ts` / Middleware**：支援 `Accept: text/markdown` 內容協商，自動導流至 Markdown 雙生頁與 `X-Markdown-Tokens` 計算。
4. **`/.well-known/agent-skills/index.json`**：符合 RFC v0.2.0 規範，各技能含真實 `sha256:{hex}` 與 `SKILL.md`。
5. **`/.well-known/mcp/server-card.json` & `mcp.json`**：發布 MCP Server Card，定義 Tools、Resources、Prompts、Website 與 Repository。
6. **`/.well-known/agent-card.json`**：發布 A2A Agent Card，宣告支援介面、傳輸協議與 AP2 擴充。
7. **`/.well-known/ai-catalog.json`**：發布 ARD 能力清單（`urn:air:...` 格式與 `representativeQueries`）。
8. **`/auth.md`**：發布 `# auth.md`，並於 `/.well-known/oauth-authorization-server` 宣告 `agent_auth` 匿名與斷言註冊。
9. **`/.well-known/api-catalog`**：提供 RFC 9727 `application/linkset+json` 格式之 API 目錄。
10. **`/.well-known/oauth-protected-resource` / `jwks.json` / WebMCP**：補齊 OAuth PRM、Bot 簽名目錄與前端 `navigator.modelContext.registerTool()`。

### 管線 2：既有網站 Agentic & SEO 全面升級（Retrofit & Modernization）
1. 跑 `npx is-agentic <url> --json` 取得基線報告與扣分清單。
2. 補齊 `robots.txt` 放行 AI Bot 與 Content-Signal。
3. 新增/更新 `llms.txt`，補上 `## When to use this site`。
4. 消除 Soft-404，配置標準 Agent-Friendly 404。
5. 配置 CDN `Vary: Accept, Accept-Encoding` 標頭。
6. 重新掃描 `npx is-agentic <url>` 驗證分數提升至 80+ / 90+。

### 管線 3：內容文章與影音逐字稿轉 AEO 高引用（Content-to-AEO Pipeline）
```
[原始文稿 / 影音逐字稿]
       │
       ▼
[AEO 改造] ────> 提取核心問句 H2/H3 + 首句 40-60 字結論直給 + 150-250 字獨立段落 + 數據口徑
       │
       ▼
[stop-slop] ───> 去除 AI 套話廢話，還原作者真實語氣
       │
       ▼
[Schema 封裝] ─> 注入 FAQPage / QAPage / Speakable JSON-LD
```

### 管線 4：SPA / Client-Side 爬蟲預渲染救援（SPA Crawlability Rescue）
1. 在 Cloudflare Pages Functions / Next.js Middleware 攔截請求。
2. 依 `User-Agent` 識別 AI Bot（`ChatGPT-User`, `ClaudeBot`, `ora-agent` 等）。
3. Bot 請求：由 Edge 端直出預渲染之純 HTML 正文 + JSON-LD（避免空白 App Shell）。
4. 一般使用者：正常載入 Client-side SPA。

### 管線 5：CI/CD 自動化驗證與長效監控（Verification & Watchdog）
1. 在 build 後自動執行 `verify-seo.mjs`，未通過直接擋下 build。
2. 配置週/月 Cron 定期查詢 GSC API 與執行 Is-Agentic 掃描，產出健康指標。

---

## 防錯原則與高壓陷阱指南

1. **全站優先於單頁**：收到 URL 審計需求時，永遠先看全站結構與 Sitemap，不可只看單一 URL。
2. **語氣優先於模板**：做文章 GEO/AEO 改造時，若結構化會破壞創作者原始風格，以保留特色口吻為優先。
3. **管線順序不可逆**：內容改造必須先做 AEO 證據與結構重構，再跑 `stop-slop`；反過來會使事實標籤被誤刪。
4. **嚴禁虛構數據**：缺少統計或來源時僅能標註 `[建議補充數據口徑]`，絕對不可捏造研究機構或數字。
5. **Vary 標頭必不可少**：凡有支援 `Accept: text/markdown` 之站點，回應標頭必須帶 `Vary: Accept, Accept-Encoding`，否則 CDN 會將快取的 HTML 回給 Agent 或反之。
6. **拒絕 Soft-404**：不存在的路由必須回傳真正的 404/410 HTTP 狀態碼，不可用 200 SPA App Shell 混充。
7. **程式碼必須可直接落地**：任何審計報告必須附帶可直接複製貼上的 JSON-LD、robots.txt、_headers 或修復代碼。

---


---

## 🇹🇼 台灣在地化環境與法規適配規範（Taiwan Localization Standards）

為確保網站在台灣市場、在地搜尋引擎與繁體中文 AI 代理中具備最高可信度與合規性，必須嚴格落實以下在地化規範：

### 1. 語言、時區與幣別標記
- **HTML 語系**：一律採用 `<html lang="zh-TW">`，嚴禁使用 `zh-CN` 或無地區碼的泛 `zh`。
- **OpenGraph**：`<meta property="og:locale" content="zh_TW">`，若有英文版搭配 `<meta property="og:locale:alternate" content="en_US">`。
- **JSON-LD 語系**：在 `@graph` 宣告 `"inLanguage": "zh-TW"`。
- **時區與時間戳**：排程、活動與發布時間一律標註 `Asia/Taipei`（UTC+08:00，如 `2026-08-24T10:00:00+08:00`）。
- **幣別標記**：電商與報價 Schema 之 `priceCurrency` 預設為 `"TWD"`，前端顯示慣例為 `NT$ 1,200` 或 `新台幣 1,200 元`。

### 2. 台灣商業實體與組織結構化（Entity Anchoring）
- **統一編號與稅籍**：在 `Organization` / `LocalBusiness` 中注入 `"taxID": "83xxxxxx"`（台灣 8 碼統編）。
- **標準台灣地址（PostalAddress）**：
  ```json
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "忠孝東路四段310號11樓",
    "addressLocality": "大安區",
    "addressRegion": "台北市",
    "postalCode": "106",
    "addressCountry": "TW"
  }
  ```
- **在地客服與通訊管道**：
  - 市話格式：`+886-2-xxxx-xxxx`（台北/基隆）、`+886-4-xxxx-xxxx`（台中）、`+886-7-xxxx-xxxx`（高雄）。
  - 手機/簡訊：`+886-9xx-xxx-xxx` 或 `09xx-xxx-xxx`。
  - LINE 官方帳號：將 `https://line.me/R/ti/p/@yourbrand` 寫入 `sameAs` 與 `contactPoint`。

### 3. 台灣在地搜尋與社群證據矩陣
AI 引擎在評估台灣本土品牌與主題權威（Topic Authority）時，高度權重依賴以下在地信任源：
- **主要搜尋環境**：Google 台灣 (`google.com.tw`)、Yahoo 奇摩搜尋。
- **高權重社群與論壇證據**：Threads（台灣極高活躍度）、Facebook 粉專/社團、Dcard、PTT（批踢踢實業坊）、Mobile01、YouTube。
- **在地徵才與企業信用**：104 人力銀行、Yourator 職缺頁面連結。

### 4. 台灣電商、物流與消保法規遵循
- **金流串接宣告**：支援台灣主流金流（綠界科技 ECPay、藍新金流 NewebPay、LINE Pay、街口支付、台灣 Pay）。
- **超商與在地物流**：7-ELEVEN / 全家便利商店店到店、黑貓宅急便、郵局快捷。
- **消保法第 19 條退換貨標記（hasMerchantReturnPolicy）**：
  - 實體商品：依消保法宣告 7 日猶豫期（鑑賞期）。
  - 數位內容 / 客製化商品：依《通訊交易解除權合理例外情事適用準則》在 Schema 中明確標註排除條款（如 `merchantReturnDays: 0` 並附說明網址），避免 AI 購物代理誤判。

### 5. 繁體中文技術與商業用語標準
全站文案、Schema 與 Markdown 一律遵循台灣在地慣用術語：
- `程式碼 / 程式`（非 代碼）、`資訊 / 訊息`（非 信息）、`專案`（非 項目）
- `伺服器`（非 服務端）、`介面 / 接口`（非 接口）、`快取`（非 緩存）
- `預設`（非 默認）、`演算法`（非 算法）、`資料 / 資料庫`（非 數據/數據庫）
- `套件 / 模組`（非 包/插件）、`使用者`（非 用戶）、`解析度`（非 分辨率）

## 擴充參考資源索引（Extended References Map）

本 Skill 之詳細代碼範本與實戰手冊已收錄於 `references/` 目錄：
- **戰略與理論 (`references/strategy/`)**：`modern-seo-strategy-spec.md`, `ahrefs-geo-strategy-2026.md`, `ai-search-ecosystem-2026.md`, `ai-gap-analysis-spec.md`, `geolook-methodology.md`
- **全站審計手冊 (`references/audit/`)**：`site-seo-geo-audit-spec.md`, `portfolio-ssg-execution.md`
- **AEO 內容與影音 (`references/aeo-content/`)**：`geo-content-reformatting-spec.md`, `video-transcript-aeo-spec.md`, `your-demo-implementation.md`
- **Web 應用與 SSG (`references/web-app-ssg/`)**：`static-site-geo-spec.md`, `webapp-geo-optimization-spec.md`, `agentic-commerce-readiness-spec.md`, `astro-portfolio-implementation.md`, `og-image-svg-pipeline.md`
- **Agent 就緒與協定 (`references/agent-readiness/`)**：`cloudflare-agent-readiness-spec.md`, `protocol-specs.md`, `llms-txt-generation-spec.md`, `markdown-twin-aeo-spec.md`, `spa-geo-crawlability-spec.md`, `cf-pages-functions-pattern.md`
- **GSC 數據運維 (`references/gsc-data/`)**：`google-search-console-api-spec.md`, `oauth-loopback-flow.md`, `gsc-deployment-feedback-timing.md`, `gsc-health-check.md`
- **驗證與監控 (`references/verification/`)**：`static-site-seo-build-verification-spec.md`, `verification-checklist-run-don-t-eyeball.md`, `brand-search-monitoring-spec.md`, `scripts.md`
