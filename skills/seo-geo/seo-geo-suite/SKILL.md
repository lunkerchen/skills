---
name: seo-geo-suite
description: SEO、GEO與AEO全能工作台：三軌搜尋策略、問答抽取、全站審計與文章改造。
version: 1.1.0
author: community
license: MIT
read_when:
  - User asks about SEO, GEO, AEO, Answer Engine Optimization, or AI search visibility
  - User wants to optimize a website, web app, or single page for Google, Perplexity, and ChatGPT
  - User wants direct answers, featured snippets, voice search, or AI citations
  - User wants to transform articles or copy into AI-friendly citeable QA content
  - User needs an end-to-end SEO/GEO/AEO workflow (audit -> optimize -> verify -> monitor)
  - User mentions llms.txt, Markdown Twin, Schema markup, Speakable, or AI crawlers
metadata:
  hermes:
    tags: [seo, geo, aeo, ai-search, suite]
    related_skills:
      - modern-seo-strategy: 核心戰略、Ahrefs 4 支柱與 AEO 實戰手冊
      - site-seo-geo-audit: 全站 SEO+GEO+AEO 審計與優先級矩陣
      - geo-article-friendly: 逐篇長文/短文/腳本之 GEO 證據與結構改造
      - geo-content-reformatting: 既有 H2/H3 標題與段落轉為 AEO/QA 結構
      - webapp-geo-optimization: Web 應用 / SPA / 首頁隱式 GEO 優化
      - static-site-geo: 靜態站 / Astro JSON-LD + OG Image 生成管線
      - markdown-twin-aeo: Markdown Twin 與 Content Negotiation 實作
      - llms-txt-generation: llms.txt 與 llms-full.txt 規範生成
      - spa-geo-crawlability: SPA 爬蟲預渲染與 Cloudflare Functions 路由
      - static-site-seo-build-verification: 靜態站建置期 5 道 SEO/GEO 驗證門戶
      - brand-search-monitoring: 品牌詞搜尋與 AI Share of Voice 監控 Cron
      - geolook-tw: 台灣在地化 GEO 審計方法論
---

# SEO × GEO × AEO 全能工作台（SEO-GEO-AEO Suite）

## When to Use

當你需要一站式處理傳統搜尋（SEO）、生成式引擎（GEO）、問答引擎（AEO）與 AI 搜尋能見度的完整工作流時載入此 Skill：
1. **整體戰略**：制定跨 Google、Perplexity、ChatGPT、Claude、Gemini 的三軌搜尋策略
2. **全站審計**：深度診斷全站結構、Schema、Ahrefs 4 支柱準備度與 AEO 直接問答抽取率
3. **內容工程**：長文/短文/腳本之 GEO 證據重構、40-60 字答案置頂與高引用格式轉換
4. **技術架構**：靜態站/SPA/SaaS 的 JSON-LD (`@graph`)、Markdown Twin、llms.txt 與 SSR 預渲染
5. **品質驗證**：上線前 5-Gate 自動化測試與品牌搜尋 / AI Share of Voice 長期監控

---

## 核心認知：三軌搜尋架構（SEO vs. GEO vs. AEO）

2026 搜尋生態已演化為三大層次，彼此互補而非對立：

```
                               ┌──────────────────────────────────────────────┐
                               │           現代搜尋生態三軌架構               │
                               └──────────────────────┬───────────────────────┘
                                                      │
             ┌────────────────────────────────────────┼────────────────────────────────────────┐
             ▼                                        ▼                                        ▼
   【SEO 搜尋引擎優化】                     【GEO 生成式引擎優化】                   【AEO 答案引擎優化】
    Search Engine Optimization               Generative Engine Optimization           Answer Engine Optimization
  • 標的：Google, Bing 藍色連結            • 標的：ChatGPT, Gemini, Claude, AI Mode • 標的：Perplexity, AIO, 語音助理, Snippets
  • 核心：排名 (Rankings) & 點擊 (Clicks)  • 核心：品牌共識 (Consensus) & 聲量 (SOV)• 核心：直接答案 (Direct Answers) & 引用
  • 手段：Topic Clusters、反向連結、CWV    • 手段：外部證據 (YouTube/Reddit)、原創數據• 手段：40-60 字首句、Passage 獨立性、QA Schema
  • 指標：SERP 排名、有機流量、CTR         • 指標：AI Mentions、Citations、Perception• 指標：精選摘要率、Direct Answer 引用率
```

### 三者核心維度對比

| 維度 | SEO（傳統搜尋） | GEO（生成式引擎） | AEO（答案引擎） |
|---|---|---|---|
| **目標引擎** | Google / Bing 傳統頁面 | ChatGPT, Gemini, Claude, AI Mode | Perplexity, Google AIO, 語音助理, Siri/Alexa |
| **回覆形式** | 10 條藍色連結列表 | 多來源合成之對話敘述 | 精準直接答案卡 + 權威來源角標 |
| **使用者路徑** | 搜尋 → 點擊網頁 → 瀏覽探索 | 提問 → 閱讀合成分析 → 深入追問 | 提問 → 即刻取得答案 → 點擊來源驗證 |
| **內容組織** | 完整長文、廣泛主題覆蓋 | 深度內容 (Deep Content)、獨家數據 | 倒金字塔結構、40–60 字答案置頂、獨立段落 |
| **結構化要求** | WebSite, Article, Breadcrumb | Product, Organization, Knowledge Graph | FAQPage, QAPage, HowTo, Speakable |
| **成功關鍵** | 域名權威 (DR)、搜尋意圖吻合 | 品牌全網提及 (0.664)、YouTube 逐字稿 (~0.737) | **段落可提取性（Passage Citability）**（134–167 字） |

---

## 快速意圖路由器（Intent Router）

| 使用者需求場景 | 推薦子技能 | 核心執行任務 |
|---|---|---|
| **「規劃跨 Google、AI 與問答引擎的整體策略」** | `modern-seo-strategy` | 盤點主題地圖、Ahrefs 4 支柱、Fan-out queries、AEO 引用手冊 |
| **「全面體檢網站的 SEO、GEO 與 AEO 準備度」** | `site-seo-geo-audit` | Site Reconnaissance、全頁 Schema 檢查、4 支柱落差、產出 P0~P3 矩陣 |
| **「讓文章/長文/腳本能被 AI 快速引用與直接回答」** | `geo-article-friendly` | 12 維度證據強化、40-60 字結論置頂、數據口徑補充（後接 `stop-slop`） |
| **「不動頁面版面，將標題與內文改為問答抽取友善」** | `geo-content-reformatting` | 既有 H2/H3 改為高引用問句（How-to/Vs/Best/Top），段落首句直給答案 |
| **「為 Web 應用 / SPA / SaaS 導入隱式 GEO/AEO」** | `webapp-geo-optimization` | 首頁語意加固、JSON-LD `@graph`、OG Image 生成、隱式語意錨定 |
| **「靜態網站（Astro/Next.js）加入結構化資料與 OG」** | `static-site-geo` | JSON-LD 三件套（WebSite+Person+LocalBusiness）、SVG 生成管線 |
| **「建立 Markdown Twin 或設定 AI 爬蟲 Content Negotiation」**| `markdown-twin-aeo` | `Accept: text/markdown` 標頭支援、.md 鏡像、Vary/Alternate 宣告 |
| **「為網站生成標準 llms.txt 與 llms-full.txt」** | `llms-txt-generation` | 依據 llmstxt.org 標準生成結構化 Markdown 目錄與專案語意描述 |
| **「解決 SPA / React 前端在 AI 爬蟲前內容空白問題」** | `spa-geo-crawlability` | Cloudflare Pages Functions 中間件、UA 判斷、SSR 預渲染注入 |
| **「在 CI/CD 或部署前自動驗證全站 SEO/GEO/AEO 標籤」** | `static-site-seo-build-verification` | 跑 5-Gate 驗證腳本（Title/Meta/JSON-LD/OG/Canonical），防止發布缺陷 |
| **「監控品牌詞在 Google 與 AI 助手中的 Share of Voice」** | `brand-search-monitoring` | 設定排程 Cron，監控品牌提及率、AI 引用變化與過期資訊預警 |
| **「針對台灣市場進行在地化 GEO/AEO 診斷」** | `geolook-tw` | 繁體中文語意距離、在地實體對齊、消保/政府開放資料關聯分析 |

---

## 6 大核心功能模組

```
                              ┌─────────────────────────────────────────┐
                              │    SEO × GEO × AEO Suite 統一工作台     │
                              └────────────────────┬────────────────────┘
                                                   │
       ┌──────────────┬─────────────┬──────────────┴────────────┬─────────────┬──────────────┐
       ▼              ▼             ▼                           ▼             ▼              ▼
  【1. 戰略規劃】 【2. 全站審計】 【3. 內容與 AEO 抽取】       【4. 網站工程】 【5. AI 協議】  【6. 驗證監控】
  modern-seo-    site-seo-geo-  geo-article-friendly        webapp-geo-    markdown-twin- static-site-seo-
  strategy       audit          geo-content-reformatting    static-site-   llms-txt-gen   build-verify
  geolook-tw                    stop-slop                   spa-crawl                     brand-monitor
```

### 模組 1：戰略規劃（Strategy & Research）
- **三軌並進**：傳統搜尋關鍵字 + AI 生成意圖矩陣 + AEO 精準問答庫。
- **Ahrefs 4 大支柱**：企業真相源（Source of Truth）、外部共識（Outside Evidence）、抗摘要資產（Deep Content）、平均 SOV 追蹤。
- **Fan-out Query 佈局**：預判 AI 扇出子查詢，建立對應的細分主題群集（Topic Clusters）。

### 模組 2：全站審計（Audit & Reconnaissance）
- **全站優先原則**：Sitemap 爬取 → 頁面類型分類 → 逐頁 Schema 語意檢查。
- **AEO 抽取率檢查**：檢查重要頁面是否有「首段 40-60 字直接答案」與 FAQ/HowTo 標記。
- **輸出成果**：深色單頁 HTML 審計報告 + P0/P1/P2/P3 優先級落地清單。

### 模組 3：內容與 AEO 抽取工程（Content & Answer Extraction）
- **倒金字塔問答法**：每節標題採用精準問句，第一段前 40-60 字直接給結論，不作懸念鋪墊。
- **Passage Citability**：段落長度控制在 134–167 字（英文）/ 150–250 字（繁中），確保單段自洽可被獨立引述。
- **高引用格式對齊**：對齊「Best」(7.06%)、「How-to」(6.35%)、「Top」(5.50%)、「Vs」(4.88%) 結構。
- **人聲還原**：改造後自動串接 `stop-slop` 去除 AI 機械套話，保護作者原始語氣。

### 模組 4：網站與應用架構（Web & App Engineering）
- **結構化資料核心**：JSON-LD `@graph` 整合 WebSite + Organization/Person + Service/Product。
- **AEO 專用標記**：注入 `FAQPage`、`QAPage`、`HowTo` 以及 `Speakable`（語音抽取專用）。
- **SPA 預渲染守門**：透過 Edge Functions 對 AI 爬蟲直出完整 HTML，消除白屏風險。

### 模組 5：AI 專屬協議與中繼（AI Protocols & LLM Assets）
- **Markdown Twin**：配置 Content Negotiation，使 AI Agent 透過 `Accept: text/markdown` 取得乾淨內文。
- **llms.txt 體系**：輸出 `/llms.txt`（輕量目錄）與 `/llms-full.txt`（完整脈絡），服務 Cursor/Claude Code 等開發 Agent。

### 模組 6：自動化驗證與監控（Verification & Watchdog）
- **發布前 5 門戶驗證**：自動化腳本驗證全站每頁的 H1、Title、Description、JSON-LD 與 Canonical。
- **長期聲量監控**：排程追蹤 AI 提及率（AI Mentions）、引用率（AI Citations）與 AI Share of Voice (SOV)。

---

## AEO 可引用性標準規範（Citability Playbook）

若要讓內容成為 Perplexity、Google AI Overviews、ChatGPT Search 的首選引用答案，必須遵守以下黃金法則：

1. **40–60 字答案置頂（Answer-First / Inverted Pyramid）**：
   - 在每個 H2/H3 標題下方，第一句話直接回答核心問題，定義事實、給出數字或結論。
   - 範例：「*什麼是 GEO？GEO（生成式引擎優化）是指透過優化網站內容與外部權威信號，讓品牌在 ChatGPT、Perplexity 與 Google AI Overviews 等生成式答案中被引用與推薦的技術。*」
2. **段落獨立性（Self-Contained Passages）**：
   - 避免代名詞指涉（如「如前所述」、「正如上文提到的它」）。每個段落必須具備獨立可讀性，抽離上下文依然完整。
3. **實體錨定與數據口徑（Entity Anchoring & Citation Discipline）**：
   - 專有名詞、品牌名首次出現附帶全名與類別。
   - 引用數據必附來源口徑（如「*根據 Ahrefs 2026 年對 75,000 個品牌的研究顯示...*」），讓 AI 具備強烈信心進行引用。
4. **表格與結構化清單（Tables & Lists）**：
   - 實測顯示表格在 AI 回答中被直接引用的機率為純散文的 **2.5 倍**。對比、定價、參數一律使用 Markdown 表格。

---

## 標準執行管線（Standard Pipelines）

### 管線 A：新網站 / 新專案上線標準 6 步走
1. **結構化標記**：導入完整 JSON-LD（`static-site-geo` / `webapp-geo-optimization`）。
2. **爬蟲放行**：robots.txt 明確 Allow 核心 AI crawlers + sitemap 宣告。
3. **AI 協議生成**：產出 `/llms.txt` 與 `/llms-full.txt`（`llms-txt-generation`）。
4. **內容 AEO 化**：重要介紹區塊 H2/H3 轉為問答式標題，段落答案置前（`geo-content-reformatting`）。
5. **建置前驗證**：執行 `verify-seo.mjs` 跑過 5 道品質門戶（`static-site-seo-build-verification`）。
6. **部署與回檢**：正式站部署完成後，以 curl 抽檢 SSR 與 OG tags。

### 管線 B：內容產出至發布標準管線
```
[撰寫草稿] 
   │
   ▼
[geo-article-friendly] ── (AEO 答案置頂 + 12 維度證據強化 + 數據口徑)
   │
   ▼
[stop-slop] ─────────── (砍除套路贅字，還原自然人聲)
   │
   ▼
[格式清洗與發布] ───── (依平台排版如 方格子 / WordPress / Astro)
```

---

## 注意陷阱與防錯原則

1. **先全站後單頁**：收到 URL 時，永遠先看全站架構與 Sitemap，切忌只看單一 URL 就下結論。
2. **語氣優先於結構**：做文章 GEO/AEO 改造時，若結構化會破壞創作者原始魅力，應以保留特色口吻為優先。
3. **管線順序不可逆**：內容改造必須先跑 `geo-article-friendly` 再跑 `stop-slop`；反過來會使證據標籤被誤殺。
4. **拒絕虛構數據**：缺少數據時僅能標註 `[建議補充數據口徑]`，嚴禁 AI 自行捏造統計數字或研究名稱。
5. **程式碼必須可落地**：審計診斷結束後，必須輸出可直接複製貼上的 JSON-LD、robots.txt 或改寫代碼。
