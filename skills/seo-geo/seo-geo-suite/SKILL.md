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

## 全能意圖路由器（Intent Router）

14 個典型場景 → 模組 1–7 → SOP 的完整對照表見 `references/modules-and-pipelines.md`「全能意圖路由器」一節；先定場景、再派模組。

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

## 防錯原則與高壓陷阱

核心六則：全站優先於單頁、管線順序不可逆（先 AEO 後 stop-slop）、嚴禁虛構數據、`Accept: text/markdown` 必帶 `Vary`、拒絕 Soft-404、審計必須附可落地修復代碼。九條完整論證與 AEO 泡沫／1% 點擊實測：`references/pitfalls.md`（執行前必讀）。

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
