# 7 大旗艦功能模組與 5 大標準執行管線（完整版）

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
0. **AI 內容工程品質層**：
   - 先回答 Reader、Promise、Point of view、Evidence、Information gain 五問，保存題目 brief、研究/內容缺口、提綱、證據與草稿等階段產物。
   - 在題目、提綱、證據、草稿之間執行四個品質閘門；每閘門可繼續、退回或終止。
   - 指定具體 owner 與第二位人類審閱者；人工審核必須能挑戰前提、追問證據、刪章節、換角度、補研究或取消發布，不只是修字。
   - 若任務是客戶專屬診斷／提案報告，另讀取 `references/strategy/client-report-output-contract.md`；不要在本節重複整份報告規範。
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
1. **Robots.txt 與 Content-Signal 分開設定**：
   - `robots.txt` 僅放 `User-agent`、`Allow`、`Disallow`、`Sitemap` 等支援語法；依專案政策設定 AI 爬蟲規則。
   - `Content-Signal: ai-train=yes, search=yes, ai-input=yes` 若採用，放在 HTTP response header，不放進 robots.txt。
   - `Agentmap`、`llms.txt` 等連結只在實際支援且有驗證方式時宣告。
2. **可選的 `llms.txt` 與 `llms-full.txt` 內容索引**：
   - 若專案採用，從內容來源生成，不手動維護，並做 URL 雙向驗證。
   - `## When to use this site` 可作為內容慣例，但不是必要標準，也不代表 Google 支援或 AI citation signal。
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
1. **`robots.txt`**：依 RFC 9309 放置 AI crawler 的 `User-agent`、`Allow`、`Disallow` 與 `Sitemap:` 規則；`Content-Signal` 若採用，另放 HTTP response header；`Agentmap` 僅在實際支援時宣告。
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

