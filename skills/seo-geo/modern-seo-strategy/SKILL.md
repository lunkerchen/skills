---
name: modern-seo-strategy
description: 現代 SEO + GEO 整合策略 — 從傳統搜尋引擎優化到生成式引擎優化的完整框架。EEAT、語意網路、主題地圖、AI 引用優化、內容結構化。
read_when:
  - User asks about SEO strategy, content strategy, or Google ranking
  - User asks about GEO, Generative Engine Optimization, AI search visibility
  - Building a content site (AI-scale or handcrafted)
  - Planning content for competitive niches (crypto, finance, YMYL, SaaS)
  - Discussing topical authority, EEAT, semantic search
  - User wants content to appear in ChatGPT/Perplexity/Gemini/Claude responses
  - Optimizing existing content for both Google and AI search engines
related_skills:
  - geo-article-friendly: Per-article GEO transformation with tone preservation
  - stop-slop: Remove AI writing smell after GEO expansion
---

# 現代 SEO + GEO 整合策略

## 核心前提：搜尋已分裂為兩個世界

2026 年搜尋生態已分裂為兩種截然不同的模式：

| 模式 | 傳統搜尋（Google/Bing） | 生成式搜尋（ChatGPT/Perplexity/Gemini/Claude） |
|------|------------------------|-----------------------------------------------|
| 輸出 | 藍色連結列表 | 合成敘述式答案 |
| 使用者行為 | 點擊連結找資訊 | 直接得到答案，可能點擊引用來源 |
| 查詢長度 | 平均 4 字 | 平均 23 字（對話式） |
| 成功指標 | 排名、CTR、流量 | 被引用次數、share of voice |
| 核心問題 | 我們在第一頁嗎？ | 我們在答案裡嗎？ |

**你的策略必須同時服務這兩種模式** — 它們不是替代關係，是互補。研究顯示 Google 排名第一頁與 AI 引用來源的 overlap 已從 70% 降至 **<20%**（Brandlight, 2026），這表示排名高不等於被 AI 引用，反之亦然。

---

## 第一章：SEO（傳統搜尋部分）

### 1.1 語意網路基礎

Google 核心演算法已是神經網路。它不再看關鍵字密度，而是測量**語意距離**（semantic distance）。要建立權威，必須完整覆蓋主題上下左右的關聯知識，形成**主題地圖**（topic map）。

**實務要點：**
- 主題地圖覆蓋：一個主題下的所有子主題、問題、痛點都要有對應內容
- 實體關聯：確保 Google 能理解你的內容在談論哪些實體（品牌、人物、產品、概念）
- EEAT 非選項：Experience, Expertise, Authoritativeness, Trustworthiness 影響雙方

### 1.2 技術 SEO 底線

- 網站速度（Core Web Vitals）
- 行動端 RWD
- 可爬性（robots.txt、sitemap、internal linking）
- Schema markup（FAQ、Review、Product、Article）

### 1.3 反向連結

連結依然重要。不僅因為 Google ranking，也因為：
1. AI 使用即時網路搜尋，強 backlink profile 幫助子查詢排名
2. 連結增加在 Common Crawl（LLM 訓練資料集）中的曝光率

---

## 第二章：GEO（生成式引擎優化部分）

### 2.1 AI 搜尋引擎工作原理

AI 不是把使用者問題直接拿來搜，而是執行 **query fan-out**（查詢扇出）：

```
使用者問：「遠端團隊 10 人以下最好的專案管理工具？」
→ AI 拆成子查詢：
  • "best project management 2026"
  • "remote team collaboration tools"
  • "project management pricing small business"
→ RAG 抓取 → 多來源合成 → 附引用回覆
```

→ **你的內容必須針對這些子查詢優化，不只是使用者輸入的長句**

### 2.2 GEO 五大支柱

#### 支柱一：確保 AI 爬蟲可存取
- robots.txt 不阻擋 `ChatGPT-User`、`GPTBot`、`Google-Extended`
- **Cloudflare 用戶注意**：CF 預設已改為阻擋 AI 機器人，需手動允許
- 重要內容 **server-side render**（AI crawler 不執行 JS）
- 內容不在 paywall、登入牆、accordion 後面

#### 支柱二：結構化以便 AI 提取
- 清晰 H1/H2/H3 層級，一個段落一個主題
- 子彈清單 + 編號列表 + 比較表（實測可見度 +30-40%）
- **答案置前**：每段開頭直接給答案，不鋪墊
- 段落 ≤ 3 句（長段落 AI 不易提取引用）

#### 支柱三：針對 fan-out queries
內容策略同時覆蓋兩個層級：
- 長句（使用者問的問題樣式）
- 短詞（AI 拆解後的子查詢樣式）

做法：對你的每個目標主題，想「AI 會拆成哪些子查詢？」並為每個子查詢建立獨立章節/段落。

#### 支柱四：權威信號
AI 評估引用可信度看：
- **專家引語**：附姓名+頭銜+公司
- **統計來源**：不寫「數據顯示」，寫「根據 Semrush clickstream 數據」
- **第一手經驗**：真實案例、具體範例。這是 EEAT 的 Experience 元素
- **作者資訊**：明確的作者頁面與資歷

#### 支柱五：內容新鮮度
AI 有強烈**近期偏誤**。內容超過 **3 個月**，AI 引用次數急遽下降。關鍵頁面至少每季更新一次。

### 2.3 站外 GEO 策略
- **Unlinked brand mentions** 有效 — 即使無連結，單純提到品牌也有加分
- **進入 AI 已引用的來源** — 找出哪些頁面已被 AI 引用，讓你的品牌出現在那裡（Reddit 回文、請部落客補充等）
- Reddit / YouTube / 論壇 — 頻繁出現在 AI 回應中
- **Wikipedia** 是 AI 訓練資料的重要來源

### 2.4 各 AI 引擎特性速查（2026/8 更新）

| 引擎 | 規模（2026/8） | 特性 | 優化重點 |
|------|------|------|----------|
| **Google AI Overviews** | 25 億月用戶；出現率 25–60%（依 tracker） | SERP 內嵌摘要 + 行內連結（2026/5 起）；下方仍有傳統結果 | 被引用 > 排名；開頭段落；平台內容（Reddit 21%/YouTube/LinkedIn） |
| **Google AI Mode** | **10 億月用戶**（推出一年內）；查詢每季翻倍 | 獨立對話介面、無傳統結果列、多模態輸入、query fan-out；Gemini 3.5 Flash 預設 | 子問題覆蓋、即時資料、結構化 QA；引用落在 top-10 僅 14% → 排名工具量不到 |
| **ChatGPT** | 9 億週活躍（2026/2）；佔 AI referral 流量 87.4% | 混合即時搜+訓練資料；搜尋+agent 化 | 引用追蹤、可驗證數據、平台提及；引用頁 71% 含結構化資料 |
| **Perplexity** | ~22M MAU、~780M 查詢/月 | 強 citation focus。偏愛近期內容。SaaS 轉換率高 | 引用格式、來源品質、權威域 |
| **Gemini** | 950M 月活（Q2 財報 2026/7） | 成長最快。強 Google SEO 自動轉 Gemini 可見度；SynthID/C2PA 驗證先行 | 品牌提及、多模態內容 |
| **Claude** | ~19M MAU、~190% YoY | 整合 Safari。偏愛邏輯清晰的結構化內容 | 結構、邏輯論證、引用語句精確 |
| **Copilot** | 80–120M 週搜尋查詢；64% 企業情境 | Windows/Edge/Bing + **Microsoft 365 內嵌**（Word/Outlook/Teams） | 企業型內容、365/LinkedIn 生態、結構化資料 |
| **Grok** | 117M MAU（SpaceX IPO 揭露）；78% 使用在 X 內 | X 即時社交資料原生優勢（41% 查詢涉即時新聞/體育/金融） | X 品牌內容、即時熱點、高速度新聞/財經 |

### 2.5 內容出處驗證（C2PA/SynthID）與資訊代理

**出處驗證成為新信任訊號**（I/O 2026）：SynthID 驗證擴到 Search 與 Chrome（全球已用 5,000 萬次），C2PA Content Credentials 可查「是否相機原始檔、是否被修改、用什麼工具改」；OpenAI 同日加入 C2PA 委員會並承諾嵌入 SynthID。這是**媒體出處驗證，不是對 AI 文字的懲罰**——但可驗證的出處將成為 agent 評估可信度的權威信號。

→ 準備動作：原創照片/圖表掛 C2PA Content Credentials；發布流程加入出處標記；AI 生成內容明確揭露；authorship/schema 保持乾淨。

**Search agents / Personal Intelligence**：agent 24/7 監控「變化」並主動推送；常青內容要「可被反覆重新檢索」（定期更新的事實、結構化 QA），即時/變動型資料（價格、庫存、changelog）價值上升，「寫完不動」的靜態長文與「一次訂閱換一次解答」模式被侵蝕。44.2% 的 LLM 引用來自內文前 30% → 最強主張、數據、結論放最前面。

### 2.6 Agentic Commerce（代理式商務）

> AI agent 取代「搜尋 → 點擊 → 逛站 → 結帳」人類路徑，直接在對話介面完成發現、比較、下單甚至售後。**產品資料的乾淨度、bot 可存取性與交易協定就緒度**，是 agent 選進「短名單」的門票。

**三大協定地圖（2026/8）**：

| 協定 | 擁有者 | 現況 | 商家要做的 |
|---|---|---|---|
| **UCP**（Universal Commerce Protocol） | Google | 2026/1 發表、2 月上線；Universal Cart 2026 夏美國上線；擴至加拿大/澳洲/英國 | Merchant Center feed + Schema.org Product；或透過 Shopify 等平台間接加入 |
| **ACP**（Agentic Commerce Protocol） | OpenAI + Stripe（開源） | 2026/3 OpenAI 轉向「App 模式」（Instacart/Target/Expedia）；僅約 12 家 Shopify 商家上線 | 向 OpenAI 申請 structured feed |
| **AP2**（Agent Payments Protocol） | Google（開放標準） | 三卡組織全數支援（Mastercard/Visa/Amex 含 Agent Purchase Protection） | 不需自建；確認金流夥伴支援 |

**五個準備方向**：
1. **Product feed 是新的「排名因子」** — rich title、多圖、運送/退貨政策；GTIN 可多獲最多 40% 點擊；I/O 2026 新增 Conversational Attributes
2. **乾淨結構化資料 = 被引用門檻** — 結構化資料頁面被 AIO 引用率高 3.1 倍；ChatGPT 引用頁 71% 含結構化資料；每個 PDP 需 Product+Offer JSON-LD
3. **Bot 存取策略翻轉** — 封鎖購物 agent ≈ 2010 年封鎖 Googlebot；放行 OAI-SearchBot/ChatGPT-User/PerplexityBot/Google-Extended/Claude-Web；/checkout、/account 仍全封；Cloudflare 已有 Trusted Agent Protocol managed ruleset
4. **協定就緒度** — 不必自建 agent；透過 Shopify/Target/Walmart 承接；2026/7 Shopify Agentic Storefronts 讓數百萬商家一鍵上架 ChatGPT/Copilot/AI Mode/Gemini；先從最高營收類別做起
5. **售後支援決定「回購推薦」** — agent 把過往支援品質（追蹤、退貨、退款速度）納入下次選商依據；AP2 不可篡改 Mandate 供退貨/爭議使用

**內容站意涵**：出版商 Google 推薦流量年減 33%（全球）/38%（美國）是**結構性**的；但被 AI 引用時轉換率高出 4–9 倍。86% 消費者會再次驗證 AI 推薦（68% 回 Google、48% 回品牌官網）→ 品牌官網是「確認」落點而非「發現」；選購指南需「被引用策略」+ 自有管道（Email/社群）護城河。

**Checkpoint（每季）**：robots.txt 放行購物 crawler → PDP JSON-LD 完整 → Merchant Center feed 屬性 → 至少一個交易協定路徑 → 金流支援 AP2 → AI Mode/ChatGPT 短名單測試 → 售後流程 agent 化 → Merchant Center AI share of voice。

完整版（含協定細節、10 項 checkpoint 表、台灣市場提醒、數據速查）見 `references/agentic-commerce-2026.md`。

---

## 第三章：SEO × GEO 融合框架

### 3.1 五階段策略

```
階段 0 — 盤點
  ├── 既有內容 audit（哪些頁面已有 ranking / 被 AI 引用潛力）
  ├── 關鍵字/主題地圖繪製
  └── 競爭者 AI visibility 診斷（手動或工具）

階段 1 — 技術基礎
  ├── robots.txt / Cloudflare AI bot 設定
  ├── Core Web Vitals 達標
  ├── Server-side rendering 確認
  ├── Schema markup 導入（FAQ、Review、Article）
  └── llms.txt 建立（選配 — 僅 Anthropic/Perplexity 確認讀取；Google 明確不支援，非 citation signal）

階段 2 — 內容生產
  ├── 主題地圖覆蓋（Intent Matrix + 長尾）
  ├── 問題式標題（吻合使用者問 AI 的方式）
  ├── 答案置前 + 子彈 / 列表 / 表格
  ├── 專家引語 + 統計來源 + 實戰案例
  ├── 結構化輸出（H1/H2/H3、短段落）
  └── 內部連接 + 權重傳導（微上下文植入）

階段 3 — 維護與新鮮度
  ├── 每季刷新關鍵頁面
  ├── 追蹤 AI citation 變化
  └── 第三方品牌提及擴散

階段 4 — 衡量與迭代
  ├── Google ranking（GSC）
  ├── Share of voice in AI responses
  ├── Citation frequency
  ├── AI referral traffic（log 搜 "ChatGPT-User"）
  └── Brand mention accuracy
```

### 3.2 Pipeline 順序

特定類別型內容（深度文章）：

```
內容生產 → GEO article transformation → stop-slop 去 AI 味
```
— 順序不可反，stop-slop 在前會砍掉 GEO 加的證據標註。

參見 `geo-article-friendly` skill（含 12 維度權重表 + 語氣保護規則）。

---

## 第四章：經典戰術（Darkseoking 策略）

適用場景：**AI 批量內容產出 + 競爭激烈的 YMYL 領域**

### 4.1 AI 跑意圖矩陣（Intent Matrix）

傳統長尾詞無效率。更高階做法是抓底層公式。

**公式：** `[平台/交易所] 的 [操作/功能] 遇到 [問題/狀況] 怎麼辦`

讓 AI 把幾十家平臺 × 幾百種狀況全部寫出來，不管搜尋量先廣覆蓋。語意距離極近，爬蟲判定你把痛點講透了。

### 4.2 微上下文權重挾持

痛點文本身不賺錢。關鍵是在解法後順理成章嵌入引導文字，把流量權重**傳導**到真正要排名的商業頁面。

### 4.3 實體權威養成

每次使用者點進來找解答，都在告訴 Google「這是領域權威」。資訊訊號疊加後，Google 因這些看似與大詞不相干的內容開始信任你，商業大詞排名會暴衝。

### 4.4 補充
- 過期權重域名對 YMYL 極有效
- 約 100+ 篇 AI 內容開始見效
- 完整細節見 `references/darkseoking-strategy.md`

---

## 第五章：工具生態（2026/8 更新）

> 更新日期：2026/8/9（GitHub star 數為當日 API 實測）。GEO 已從新名詞變成月搜 22,000 次的成熟類別，工具分三種任務：引用追蹤、可見度稽核、內容優化。

### 5.1 付費 GEO 工具

| 工具 | 2026/8 現況 | 價格 | 適合誰 |
|---|---|---|---|
| **Profound**（tryprofound.com） | 已成為 GEO 首家獨角獸：2026/2 完成 $96M Series C（Lightspeed 領投），估值 $10 億。客戶含 Figma、Ramp、MongoDB、Plaid 等 | 免費入門方案 + 企業客製報價 | 品牌大廠；要 share of voice + sentiment + prompt 層級排名的企業 |
| **Ahrefs Brand Radar**（ahrefs.com） | 追蹤 6 平台（Google AI Overviews/AI Mode、ChatGPT、Perplexity、Gemini、Copilot），prompt 資料庫 2.18–2.39 億筆；延伸 YouTube/TikTok/Reddit 追蹤（beta）。第三方評測指其 ChatGPT/Perplexity 追蹤有準確度落差 | 內含於 Ahrefs Lite $129/月起；部分方案加購模組約 $398–699/月（未確認） | 已是 Ahrefs 用戶、主戰場在 Google AI Overviews 者 |
| **SEMrush AI Visibility Toolkit**（semrush.com） | 單獨加購 $99/月/domain；Semrush One（SEO+AI 一套）$199–549/月。prompt 庫 1.3 億+，覆蓋 7 引擎 | $99/月起 | 已是 Semrush 用戶，想 SEO 與 AI 可見度一個儀表板搞定 |
| **Otterly.AI**（otterly.ai） | 仍是最低門檻付費工具：追蹤 7 引擎（含 AI Mode、Copilot），每日追蹤 + 引用分析 + GEO 稽核 | Lite $29/月（15 prompts）→ Standard $189 → Premium $489/月 | 個人/小團隊，想低成本開始每日追蹤 |
| **OGTool**（ogtool.com） | 2026 竄紅新玩家（創辦人前 Stanford）：ChatGPT 關鍵字可見度 + Reddit 監控與 AI 回文、幻覺偵測。另有代管服務（Reddit $6,000/月、GEO $9,000/月） | Starter $99/月 → Growth $199 → Scale $399 | 想同時經營 Reddit 社群訊號 + AI 可見度的品牌 |
| **其他新面孔** | Gauge（$99/月起）、ZipTie.Dev（$99/月）、AIclicks（$59–499/月）、SE Ranking Visible（$49/月起）、Peec AI（約 €75/月）、Writesonic GEO（$199/月） | 見各官網 | 依預算與引擎覆蓋選擇 |

### 5.2 開源 GEO 生態（2026/8/9 GitHub API 驗證）

| 專案 | Stars | 現況 | 用途 |
|---|---|---|---|
| **GEOFlow**（github.com/yaojingang/GEOFlow） | 3,156 ⭐（727 forks，持續更新） | 開源 GEO 內容工程 + 多站點分發：AI 任務、RAG/語意分塊、GEOFlow Agent、WordPress 發佈、Analytics。Apache-2.0、多語言文件 | 自架內容生產與多站分發流水線 |
| **GEORank**（github.com/yaojingang/GEORank） | 364 ⭐（2026 新專案） | 開源 GEO 排名追蹤：Next.js + FastAPI，多模型 Provider 池、額度控管、GEO 診斷規則 | 自架排名/可見度追蹤（補「測量」環節） |
| **yao-geo-skills**（github.com/yaojingang/yao-geo-skills） | 687 ⭐ | 20 個 GEO 專用 skill，持續更新 | Agent 驅動的 GEO 工作流 |
| **yao-meta-skill**（github.com/yaojingang/yao-meta-skill） | 2,354 ⭐ | Skill OS 框架：workflow 編譯為跨平台 agent skill，含 eval、審查門戶、證據帳本 | 把 GEO 流程打包成可重用 skill |
| **GEO/AEO Tracker**（github.com/danishashko/geo-aeo-tracker） | 活躍 | 開源、local-first 可見度儀表板：BYOK、6 模型並行、13 個功能頁、Vercel 一鍵部署。資料費僅 Bright Data PAYG（約 $1.5/1K 筆） | $0 月費的品牌追蹤 |
| **awesome-generative-engine-optimization**（github.com/amplifying-ai/awesome-generative-engine-optimization） | 442 ⭐ | 2026 持續維護的 GEO 資源清單 | 找工具/研究入口 |

測量方法論文《From Citation Selection to Citation Absorption》仍為跨平台 GEO 測量的學術基準。

### 5.3 免費手動速測：仍是最務實的入門

業界共識：**≤30–50 個 prompts、單一市場、每月一次**用手動即可（Google Sheet 追蹤，每週 1–2 小時）；超過 100 prompts、跨 4+ 引擎、要趨勢線與競爭者對比時必須自動化。免費官方數據源別漏：GA4 的 AI referral 流量、GSC 的 AI Overviews 曝光。

### 5.4 2026/8 推薦組合

- **免費（$0）**：GA4 + GSC + 手動速測（每季）→ 需自動化時自架 GEO/AEO Tracker（BYOK）或 GEORank + GEOFlow
- **輕量付費（$29–99/月）**：Otterly Lite、OGTool Starter、ZipTie 三選一，搭配手動競品抽查
- **中階（$99–299/月）**：Semrush One 或 Ahrefs Lite（含 Brand Radar 基本）+ Otterly Standard
- **企業（客製）**：Profound 或 Ahrefs Brand Radar 全模組，配 OGTool 代管做 Reddit 訊號經營

完整版見 `references/tool-ecosystem-2026-08.md`。

---

## 關鍵數據參考（2026/8 更新）

| 數據 | 值 | 來源 |
|------|------|------|
| ChatGPT 週活躍用戶 | 9 億+（2026/2） | OpenAI via Reuters |
| Gemini app 月活躍 | 950M（DAU 一年 3 倍） | Google Q2 財報 2026/7 |
| Google AI Mode 月活躍 | 10 億（推出一年內） | Google I/O 2026 |
| AI Overviews 月活躍 | 25 億+ | Google I/O 2026 |
| 消費者以 AI 開始搜尋 | 37% | Eight Oh Two（SEJ）2026/1 |
| Google zero-click（US） | 68%（2024: 60%） | SparkToro 2026/5 |
| AIO 出現 → #1 CTR | -58%；AIO 查詢 zero-click 83% | Ahrefs 2025/12；Digital Bloom |
| Google top10 ↔ AI 引用 overlap | 70% → **<20%** | Brandlight via 5WPR 2026/5 |
| AIO 引用來源在 organic top10 | 38%（原 76%） | Ahrefs Brand Radar 2026/3 |
| LLM 引用在 Google top100 外 | 80%（僅 12% 在 top10） | Ahrefs 2025 末 |
| Referring domains 效應 | 32K+ RD 被引用率為 <200 的 3.5 倍 | SE Ranking（2.3M 頁面）2026/6 |
| AI citations 來自 earned media | 84%（付費僅 0.3%） | Muck Rack 2026/5 |
| 新內容進 citation pool | 3–5 工作天；14 天未更新 -23% | tentenco 2026/3 |
| 新鮮度效應 | 50% citations <13 週；ChatGPT 引用比 organic 新 25% | Amsive/Ahrefs |
| GEO 效果時間線 | 3–6 個月建立穩定 citation authority | tentenco；5WPR |
| Organic 掉 ↔ AI citation 掉 | 11/11 站全數同步（平均 -22.5%） | Lily Ray 2026/2 |
| AI referral 流量 | 佔 1.08%、YoY +340%；轉換 3.49% vs 2.86% | Conductor/Digital Applied 2026 |
| ChatGPT 佔 AI referral 流量 | 87.4% | Conductor 2026/1 |
| Vercel 新註冊來自 ChatGPT | 10%（6 個月 10 倍） | Vercel LLM SEO playbook |
| GEO 最高可見度提升 | +40%；結構化內容 +30–40% | arXiv:2311.09735（KDD 2024） |
| Gartner 預測 | 2026 底傳統搜尋量 -25% | Gartner（預測） |

完整 26 行數據表 + 32 條來源 URL + 變更摘要見 `references/seo-geo-key-data-2026-08.md`。

---

## 使用情境

載入此 skill 的觸發條件：
1. 任何 SEO/GEO/content strategy 相關討論
2. 新網站或內容專案規劃
3. 想要內容同時在 Google 和 AI 搜尋中被發現
4. AI-scale 內容量產策略（Intent Matrix + darkseoking 戰術）
5. 評估既有內容是否需要 GEO 改造（則參考 geo-article-friendly）

## 參考文件

本 skill 含以下參考文件：
- `references/seo-geo-deep-research-2026.md` — 本研究的完整資料（2026/6 底稿，2026/8 更新）
- `references/seo-geo-key-data-2026-08.md` — 26 行關鍵數據表 + 32 條來源 URL（2026/8 版）
- `references/agentic-commerce-2026.md` — Agentic Commerce 完整研究（協定細節、10 項 checkpoint、台灣市場、數據速查）
- `references/ai-search-ecosystem-2026.md` — AI Mode citation 行為、Search agents、C2PA/SynthID 完整研究
- `references/tool-ecosystem-2026-08.md` — 工具生態完整版（含付費/開源/組合推薦）
- `references/darkseoking-strategy.md` — Darkseoking 意圖矩陣策略原始說明
