---
name: seo-geo-suite
description: SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台：涵蓋傳統搜尋、生成式引擎、問答抽取、Is-Agentic 100分規範、Cloudflare L0-L5、全站審計、內容改造與自動化驗證。
version: 2.1.0
author: Community
license: MIT
read_when:
  - User asks about SEO, GEO, AEO, or AI search visibility
  - User wants to optimize a site or page for Google, Perplexity, ChatGPT, Claude, DeepSeek
  - User wants an is-agentic.com score, direct answers, featured snippets, or AI citations
  - User wants to transform articles or transcripts into AI-citeable QA content
  - User needs an end-to-end SEO/GEO/AEO workflow (audit -> optimize -> verify -> monitor)
  - User mentions llms.txt, Markdown Twin, Content Negotiation, Schema, or AI crawlers
  - User wants to analyze Google Search Console searchAnalytics data
metadata:
  hermes:
    tags: [seo, geo, aeo, agentic, is-agentic, cloudflare, llms-txt, schema, gsc, suite]
---

# SEO × GEO × AEO × Agent-Readiness 全能旗艦工作台

整合 SEO、生成式引擎優化（GEO）、答案引擎優化（AEO）與 AI 代理就緒標準（Agent-Readiness / Is-Agentic）的一體化全能解決方案。

---

## 核心認知：現代搜尋與 Agentic 四軌體系

| 軌道 | 標的 | 核心 | 手段 | 指標 |
|---|---|---|---|---|
| **SEO** 搜尋引擎優化 | Google、Bing 藍色連結 | 排名與點擊 | Topic Cluster、反向連結 | SERP 排名、有機流量、CTR |
| **GEO** 生成式引擎優化 | ChatGPT、Claude、DeepSeek、Gemini | 品牌共識（SOV）與抗摘要深度內容 | 全網證據（Reddit/YouTube）、原創數據 | AI Mentions、Citations、Perception |
| **AEO** 答案引擎優化 | Perplexity、AIO、語音 | 直接答案 | 40–60 字首句、QA Schema | 精選摘要率、Direct 引用率 |
| **Agent-Readiness** 代理就緒 | Autonomous AI Agents | 可發現、可存取、可操作 | Is-Agentic 100 分、MCP、RFC 9457 | Is-Agentic Score、RFC 9457 合規 |

---

## GEOFlow 吸收層：內容工程運作模型（摘要）

只吸收可移植的內容工程模式。流程：五問 brief（Reader、Promise、Point of view、Evidence、Information gain）→ 研究/證據 → 四道品質閘門 → 草稿 → 第二人審核 → 發布 → 量測；生成器不決定事實、不放行。配套：四層資產（Source of Truth／Evidence／Question Map／Deep Content，缺證據標 `unverified`）、六項發布前門禁（Intent/Evidence/Structure/Integrity/Risk/Traceability，有未驗證主張即 `needs_review`）、雜湊快照失效、觀測分層（抓取 ≠ 引用、GSC ≠ AI 引用、缺實測報「未測量」）、分發後讀回。客戶報告先選 archetype，依六段契約交付。

判準與契約：`references/strategy/ai-content-engineering-quality.md`、`references/strategy/client-report-output-contract.md`；完整六節與 GEOFlow 執行映射表：`references/geoflow-operating-model.md`。

## 全能意圖路由器（Intent Router & Execution Matrix）

| 使用者場景與意圖 | 對應旗艦模組 | 核心執行任務與 SOP |
|---|---|---|
| **「規劃跨 Google、AI 與問答引擎的整體策略」** | **模組 1：戰略規劃** | 盤點主題地圖、Ahrefs 4 支柱、Fan-out 查詢、競品 AI Mention/Citation 落差。 |
| **「全面體檢網站的 SEO、GEO、AEO 與 Agent 友好度」**| **模組 2：全站審計** | `npx is-agentic <url>` + Sitemap Reconnaissance + 逐頁 Schema 診斷 → P0~P3 矩陣。 |
| **「讓文章/長文/腳本能被 AI 快速引用與直接回答」** | **模組 3：內容工程** | 五問 brief → 四個品質閘門 → 草稿 → 第二人審核 → 發布 → 量測；40-60 字結論置頂、150-250 字獨立段、串接 `stop-slop`。 |
| **「產出客戶專屬 SEO/GEO 診斷／提案報告」** | **模組 1 + 2 + 3 + 7：客戶報告輸出** | 先選 archetype，依六段契約結構交付；finding 附證據與驗收方法，成效改寫為可驗收指標。 |
| **「影音/Podcast 逐字稿轉為高引用問答與 FAQ」** | **模組 3：內容工程** | 逐字稿清洗、高引用問句提取（How/Why/Best/Vs）、注入 FAQPage & Speakable。 |
| **「靜態網站（Astro/Hugo/Next）加入結構化與 OG」**| **模組 4：架構優化** | JSON-LD 三件套（WebSite+Organization/Person+Service）、SVG OG 管線。 |
| **「Web 應用 / SPA / SaaS 導入隱式 GEO/AEO」** | **模組 4：架構優化** | 首頁語意加固、JSON-LD `@graph`、PDP Schema、保護結帳同時放行購物 Agent。 |
| **「設定 AI 爬蟲 Content Negotiation 與 Markdown」**| **模組 5：代理就緒** | `Accept: text/markdown`、`Vary: Accept, Accept-Encoding`、.md 雙生檔案。 |
| **「建立/維護 llms.txt 與 llms-full.txt」** | **模組 5：代理就緒** | 從內容來源生成並做 URL 雙向驗證；不宣稱為 Google 支援或 citation signal。 |
| **「解決 SPA / React 前端在 AI 爬蟲前內容空白問題」** | **模組 5：代理就緒** | Pages Functions 中間件、UA 判斷、SSR 預渲染 HTML 與 Schema 注入。 |
| **「設定 Cloudflare Agent-Readiness (L0-L5) 與 MCP」**| **模組 5：代理就緒** | `Content-Signal` 標頭、`/.well-known/mcp/server-card.json`、`ai-catalog.json`。 |
| **「查詢與分析 Google Search Console 搜尋成效」** | **模組 6：GSC 數據** | GSC API 抓 clicks/impressions/CTR/position、URL Inspection、提交 Sitemap。 |
| **「CI/CD 或部署前自動驗證全站標籤與 404 引導」** | **模組 7：驗證門戶** | 6-Gate 測試（H1/Title/Meta/JSON-LD/Canonical/Agent 404/Vary）。 |
| **「排程監控品牌在 Google 與 AI 中的聲量」** | **模組 7：長效監控** | Cron 檢查品牌詞能見度、AI Mention/Citation 變化與過期預警。 |

---

## 7 大旗艦功能模組（一覽）

1. **戰略規劃與 AI 引用缺口**：Ahrefs 4 支柱、競品 AI Mention/Citation Gap、GeoLook TW 在地語意。
2. **全站與單頁審計**：Sitemap Reconnaissance + `npx is-agentic <url> --json` → P0~P3 修正矩陣。
3. **內容工程與 AEO**：五問 brief 與四閘門、40–60 字答案置頂、150–250 字可提取段落、高引用句型、FAQPage/Speakable、stop-slop。
4. **SSG / SPA 架構**：JSON-LD `@graph`、Agentic Commerce Offer、SVG/Satori OG 管線。
5. **Agent 就緒**：robots.txt 與 Content-Signal 分設、llms.txt 雙向驗證、Markdown 協商＋`Vary`、Cloudflare L0–L5、Edge 預渲染。
6. **GSC 數據**：searchAnalytics 查詢、部署後 7/14/28 日成效位移、URL Inspection 與 Sitemap 重提。
7. **驗證與監控**：發布前 6 道門戶（H1/Title、JSON-LD、Canonical/OG、機器可讀檔、真實 404、Vary）＋品牌與 AI 引用 Cron。

完整 SOP：`references/modules-and-pipelines.md`。

---

## 5 大標準執行管線（一覽）

1. **Greenfield 8 步**：語意架構 → JSON-LD → AI 爬蟲權限 → llms.txt → Markdown 協商 → L5 十大端點 → 6-Gate → Live 抽檢。
2. **Retrofit 既有站**：is-agentic 基線 → robots/Content-Signal → llms.txt → 消 Soft-404 → `Vary` → 複掃 80+/90+。
3. **Content-to-AEO**：問句 H2/H3＋答案置頂＋獨立段＋數據口徑 → stop-slop → Schema 封裝（順序不可逆）。
4. **SPA 爬蟲救援**：Edge 攔截 → 識別 AI Bot → 直出預渲染 HTML＋JSON-LD。
5. **CI/CD 驗證與監控**：build 後 `verify-seo.mjs` 失敗擋板；週/月 Cron 查 GSC 與 Is-Agentic。

步驟全文與圖解：`references/modules-and-pipelines.md`。

---

## 防錯原則與高壓陷阱指南

1. **全站優先於單頁**：先看全站結構與 Sitemap，不只看單一 URL。
2. **語氣優先於模板**：結構化若破壞原始風格，以保留口吻為先。
3. **管線順序不可逆**：先 AEO 證據與結構重構，再跑 stop-slop。
4. **嚴禁虛構數據**：缺來源只標 `[建議補充數據口徑]` 或退回補證據；人工審核不是安全豁免。
5. **Vary 標頭必不可少**：支援 `Accept: text/markdown` 必帶 `Vary: Accept, Accept-Encoding`。
6. **拒絕 Soft-404**：不存在路由回真實 404/410，不用 200 App Shell 混充。
7. **程式碼必須可落地**：審計報告附可直接貼上的 JSON-LD、robots.txt、_headers 修復代碼。
8. **警惕 AEO 泡沫與過度優化反噬**：學術與實測（arXiv:2607.14035、C-SEO Bench、SAGEO Arena）顯示多數戰術無效甚至使引用 −6~9%；規模化生成與人造新鮮度招致降權。以真實深度內容與站外自然提及為本。
9. **首屏擠壓與 1% 點擊**：AIO ~1200px 把 #1 推到折疊線下；AIO 出現時傳統點擊 15%→8%，僅 1% 點 AIO 來源；但 AI 轉介轉換率為傳統 4.4 倍（Semrush）。追求高意圖轉換，不期待 AI 大流量。

完整論證：`references/pitfalls.md`。

---

## 台灣在地化環境與法規適配（Taiwan Localization Standards）

`lang="zh-TW"`、`og:locale=zh_TW`、`Asia/Taipei`、`TWD`；統編／PostalAddress／LINE `sameAs` 實體錨定；Threads、Dcard、PTT、104 在地證據；ECPay／NewebPay 金流與消保法 7 日猶豫期；繁中用語標準。完整規範：`references/taiwan-localization.md`。

---

## 擴充參考資源索引（Extended References Map）

兩階段索引：先依下表找到子目錄，再讀 `references/INDEX.md` 取得完整檔名。

| 目錄 | 內容 |
|---|---|
| `references/strategy/` | 戰略規格、Ahrefs GEO 策略、AI 內容品質層、客戶報告契約、GeoLook TW |
| `references/audit/` | 全站 SEO/GEO 審計規格與執行手冊 |
| `references/aeo-content/` | AEO 內容改寫、影音逐字稿、含圖報告實作 |
| `references/web-app-ssg/` | 靜態站/Web 應用 Geo、Agentic Commerce、OG 管線 |
| `references/agent-readiness/` | Cloudflare L0–L5、llms.txt、Markdown Twin、SPA 可抓取性 |
| `references/gsc-data/` | GSC API 規格、OAuth loopback、部署反饋時序 |
| `references/verification/` | 6 道建置驗證、品牌監控、部署後 Live 驗收 |

運作文件：`references/geoflow-operating-model.md`、`references/modules-and-pipelines.md`、`references/taiwan-localization.md`、`references/pitfalls.md`。
