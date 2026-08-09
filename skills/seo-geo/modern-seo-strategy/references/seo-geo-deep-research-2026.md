# SEO + GEO 深度研究（完整版）— 2026 年 6 月（2026/8 更新）

> **2026/8/9 更新註記**：本檔為研究底稿。2026/8 起關鍵數據表、工具生態、Agentic Commerce、AI 生態結構變化的最新版本請參閱同目錄下 `seo-geo-key-data-2026-08.md`、`tool-ecosystem-2026-08.md`、`agentic-commerce-2026.md`、`ai-search-ecosystem-2026.md`。下列章節與新檔衝突時，以新檔為準。重大修正：llms.txt 非 citation signal（Google 明確不支援）；ChatGPT 週活躍已達 9 億；AI Mode 10 億月活躍。

## 來源

- arXiv:2311.09735 — GEO: Generative Engine Optimization (Princeton/Georgia Tech/Allen Institute, KDD 2024)
- LLMrefs GEO 2026 Guide (https://llmrefs.com/generative-engine-optimization/)
- Awesome GEO (https://github.com/amplifying-ai/awesome-generative-engine-optimization) — 428 stars
- Search Engine Land GEO 2026 Guide (https://searchengineland.com)
- Conductor 2026 AEO/GEO Benchmarks Report — 13,770 domains, 21.9M searches, 17M AI responses
- Brandlight — GEO research data (70% → <20% SEO-GEO overlap)
- AHHA (https://www.ahha.tw/blog/seogeo) — 中文 SEO vs GEO 說明
- NeurIPS 2025 — C-SEO Bench: Does Conversational SEO Work?
- Ahrefs Brand Radar, SEMrush AI Visibility Toolkit docs
- Google Search Central — Creating Helpful, Reliable, People-First Content

---

## 一、核心命題

搜尋正在典範轉移。Google「藍色連結」不再是唯一入口。使用者直接問 ChatGPT/Perplexity/Gemini，AI 直接給答案。這不是未來 — 已經發生。

> SEO = 讓搜尋引擎找到你 → 排名第一頁
> GEO = 讓 AI 引用你 → 成為答案的一部分

Google 2026 官方立場：GEO 和 AEO 「still SEO」 — 不是新東西，而是 SEO 的延伸。

---

## 二、根本差異：SEO vs GEO

| 維度 | 傳統 SEO | GEO（生成式引擎優化） |
|------|----------|----------------------|
| 輸出形式 | 連結列表 | 合成敘述式答案 |
| 使用者行為 | 點連結找資訊 | 直接得到答案 |
| 查詢長度 | 平均 4 字 | 平均 23 字（對話式） |
| 成功指標 | 排名、CTR、流量 | 被引用次數、品牌 mentions、share of voice |
| 優化焦點 | 關鍵字 + 反向連結 | 內容結構 + 權威信號 |
| 核心問題 | 我們在第一頁嗎？ | 我們在答案裡嗎？ |

**關鍵數字：** GEO 學術論文證明可提升生成式引擎可見度最高 **40%**。

---

## 三、AI 搜尋引擎底層機制

1. **Query fan-out** — AI 拆解成多個子查詢搜尋
2. **RAG Information Retrieval** — 從網路抓取相關段落
3. **Synthesis** — 跨多來源合成連貫答案
4. **Citation** — 附上來源連結

**LLM 非確定性：** 同樣問題問五次→五種不同答案。GEO 目標是 **mention rate（提及率）**，不是固定排名。

---

## 四、SEO 與 GEO 的融合與衝突

### 7 大重疊區
1. 權威性 / EEAT — 兩邊都獎勵
2. 結構化資料（Schema.org）— 兩邊都需要
3. 內容相關性
4. 引用/來源 — 兩邊都看信號
5. 技術效能 — 速度、可爬性
6. 使用者意圖
7. 實體識別

### 7 大衝突點
1. 關鍵字密度 — SEO 需要但 GEO 處罰（-9%）
2. 連結數量 vs 上下文品質
3. 點擊率優化 — GEO 零點擊時代無效
4. 內容長度 — SEO 喜歡長文，GEO 偏好可提取段落
5. FAQ Schema cannibalization
6. 同義詞策略
7. 專業術語用量

### 關鍵數據
- Google ranking vs AI citation overlap 從 70% 降 **<20%**（Brandlight）— 持續擴大中
- C-SEO（NeurIPS 2025）發現多數 GEO 方法無效，傳統 SEO 仍相關 — 暗示基礎要做好
- 結構化列表+引語+統計的頁面 AI 曝光率高 **30-40%**

---

## 五、GEO 五大支柱

### 支柱一：確保 AI 爬蟲可存取
- robots.txt 不阻擋 `ChatGPT-User`、`GPTBot`、`Google-Extended`
- Cloudflare 預設阻擋 AI bot，需手動允許
- Server-side render（AI 不執行 JS）
- 內容不能在 paywall/登入牆/accordion 後面

### 支柱二：結構化以便 AI 提取
- 清晰 heading 層級（H1/H2/H3），一個段落一個主題
- 子彈/列表/表格（可見度 +30-40%）
- 答案置前（inverted pyramid）
- 段落 ≤ 3 句

### 支柱三：針對 fan-out queries
內容策略同時覆蓋長句（使用者問法）和短詞（AI 子查詢）。對每個目標主題，推測 AI 會拆成哪些子查詢，為每個子查詢建立獨立章節。

### 支柱四：權威信號
- 專家引語（附姓名+頭銜+公司）— **效果最強（+41%）**
- 統計來源（「根據 Semrush clickstream 數據」）— **+30%**
- 第一手經驗 — EEAT 的 Experience 元素
- 作者資訊 — 明確的作者頁面與資歷
- 引用來源 — +30%
- 可讀性 — +22%
- ❌ 關鍵字堆砌 — -9%

### 支柱五：內容新鮮度
**3 個月 cliff** — 超過 3 個月 AI 引用率急降。關鍵頁面每季更新。

---

## 六、站外 GEO

- **Unlinked brand mentions** 有效—即使無連結也有加分
- 進入 AI 已引用的來源—最快見效方式（有案例不到 1 小時從零到首次被引用）
- Reddit / YouTube / 論壇—頻繁被 AI 引用
- Wikipedia—AI 訓練資料重要來源（ChatGPT top citation: 47.9% 來自 Wikipedia）
- Wikipedia dominates ChatGPT at 47.9% of top citations; Reddit appears heavily in Gemini and Perplexity

---

## 七、各 AI 引擎特性（2026/8 更新）

| 引擎 | 規模數據（2026/8） | 特性 | 優化重點 |
|------|------|------|----------|
| **ChatGPT** | 9 億週活躍（2026/2）。佔 AI referral 流量 87.4% | 混合即時搜+訓練資料；搜尋+agent 化 | 全面有來源的內容、權威信號、結構化資料（引用頁 71% 含 JSON-LD） |
| **Google AI Overviews** | 25 億月使用者；出現率 25–60%（依 tracker） | SERP 內嵌摘要+行內連結（2026/5 起）；廣告上下列 | 被引用 > 排名；開頭段落；Reddit/LinkedIn/YouTube 平台內容 |
| **Google AI Mode** | 10 億月使用者（推出一週年）；查詢每季翻倍 | 對話式、多模態輸入、query fan-out、Gemini 3.5 Flash 預設；無傳統結果列 | 子問題覆蓋、即時資料、結構化 QA；引用 URL 僅 14% 落在有機 top-10 |
| **Perplexity** | ~22M MAU、~780M 查詢/月 | 強 citation focus。偏愛近期內容。SaaS 轉換率最高 | 新鮮度、來源透明度、權威域 |
| **Gemini** | 950M 月活（Q2 財報 2026/7） | 整合 Google 搜尋基礎設施；SynthID/C2PA 驗證先行 | 強 Google SEO 自動轉 Gemini 可見度；品牌提及、多模態內容 |
| **Claude** | ~19M MAU、~190% YoY | 整合 Safari。偏愛邏輯清晰的結構化內容 | 結構、邏輯論證、引用語句精確 |
| **Copilot** | 80–120M 週搜尋查詢；64% 企業情境 | Windows/Edge/Bing + Microsoft 365 內嵌 | 企業型內容、365/LinkedIn 生態、結構化資料 |
| **Grok** | 117M MAU（SpaceX IPO）；78% 使用在 X 內 | X 即時社交資料原生優勢（41% 查詢涉即時新聞/體育/金融） | X 品牌內容、即時熱點、高速度新聞/財經 |

---

## 八、工具生態

> **2026/8 註記**：本節為 2026/6 底稿。最新版本（Profound $96M Series C 獨角獸、Ahrefs Brand Radar 6 平台、OGTool 等新玩家、GEOFlow 3,156⭐/GEORank 364⭐ 等當日實測）見 `tool-ecosystem-2026-08.md`。

### GEO 專用平台
- **Profound** — 企業級。$35M Series B（Sequoia）。Share of voice + sentiment + prompt-level rankings
- **Ahrefs Brand Radar** — 2025/3 上線。追蹤 5 個 AI 平台。100M+ prompt 資料庫。$129-999/月（含在 Ahrefs 訂閱）
- **SEMrush AI Visibility Toolkit** — $99/月/domain。含 AI Overviews position tracking
- **Otterly.AI** — Google AI Overview + Perplexity 引用分析
- **GEOmetrics** — 幻覺檢測 + AI citation 準確性修復
- **GEO/AEO Tracker** — 開源自架，BYOK，$0/月。支援 ChatGPT/Perplexity/Gemini/Copilot/Grok
- **GeckoCheck** — 電商 GEO 優化
- **Bluefish AI** — 品牌安全 + source attribution + AI ad campaigns

### 企業 SEO 平台（已加入 GEO 功能）
- Ahrefs, SEMrush, HubSpot AI Search Grader, Writesonic

### 開源/免費
- GEO/AEO Tracker（自架）
- llms.txt generators（Apify, llmstxtgenerator.org, WordLift）

### 手動速測（免費）
每月做一次：針對 10-20 個行業相關問題問 ChatGPT + Perplexity + Gemini，記錄品牌是否出現、如何被描述、引用了哪些來源。

---

## 九、中文圈 GEO 實戰

### 12 維度權重表（來源：geo-article-friendly skill）

| 優先級 | 層級 | 維度 | 權重 |
|--------|------|------|:----:|
| P1 | 證據引用層 | 權威原文引語 | 16 |
| P1 | 證據引用層 | 統計數據完整性 | 14 |
| P1 | 證據引用層 | 可引用性/可信來源 | 13 |
| P2 | 結構理解層 | 結構規範性 | 12 |
| P3 | 表達層 | 流暢度、邏輯過渡 | 10 |
| P3 | 語義匹配層 | 實體覆蓋、問題覆蓋 | 8 |
| P4 | 信任層 | 權威信號 | 8 |
| P4 | 專業表達層 | 術語一致性 | 6 |
| P5 | 穩健性層 | 多源支撐/邊界 | 5 |
| P5 | 跨域連接層 | 關聯領域 | 4 |
| P5 | 可讀性層 | 易懂表達 | 3 |
| — | 風險控制 | 無堆砌/無編造 | penalty |

### 語氣保護
- 股癌 tone: 保留口語標記（靠北/笑死/認真說）
- 攝影專業: 保留設備型號、業界報告
- 冷知識: 保留故事鉤子開頭

### Pipeline 順序
```
內容生產 → GEO article transformation → stop-slop 去 AI 味
```
— 順序不可反。stop-slop 在前會砍掉 GEO 加的證據標註。實測：6,300 字長文，GEO 擴至 9,028 字，stop-slop 縮回 7,632 字（-16%），資訊密度不減反增。

### 經典戰術（Darkseoking）
- **Intent Matrix**：`[平台] 的 [操作] 遇到 [問題] 怎麼辦` 公式，AI 批量產出廣覆蓋
- **微上下文權重挾持**：解法後嵌入引導文字→流量權重傳導到商業頁面
- **實體權威養成**：每次解答都在累積領域權威信號
- 約 100+ 篇內容開始見效

---

## 十、五階段執行框架

```
階段 0 — 盤點
  ├── 既有內容 audit（哪些有 ranking / 被 AI 引用潛力）
  ├── 關鍵字/主題地圖繪製
  └── 競爭者 AI visibility 診斷

階段 1 — 技術基礎
  ├── robots.txt / Cloudflare AI bot
  ├── Core Web Vitals
  ├── Server-side rendering
  ├── Schema markup（FAQ、Review、Article）
  └── llms.txt（選配 — 非 citation signal；僅 Anthropic/Perplexity 確認讀取，Google 明確不支援）

階段 2 — 內容生產
  ├── 主題地圖覆蓋（Intent Matrix + 長尾）
  ├── 問題式標題
  ├── 答案置前 + 列表/表格
  ├── 專家引語 + 統計來源 + 實戰案例
  ├── 結構化輸出（H1/H2/H3、短段落）
  └── 內部連接 + 權重傳導

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

---

## 十一、關鍵數據彙整

| 數據 | 值 | 來源 |
|------|----|------|
| GEO 提升 AI 可見度 | 最高 40% | arXiv:2311.09735（KDD 2024） |
| AI referral conversion vs 傳統 | 高 2× | Conductor 2026 Benchmarks |
| ChatGPT 佔 AI referral 流量 | 87.4% | Conductor 2026 Benchmarks |
| Google ranking vs AI citation overlap | <20%（且持續下降） | Brandlight 2026 |
| Vercel 新註冊來自 ChatGPT | 10% | Vercel 官方 |
| 內容新鮮度 cliff | 3 個月 | LLMrefs |
| 結構化內容可見度提升 | +30-40% | 多來源實測 |
| ChatGPT 月活躍 | 8 億週活躍 | OpenAI 官方 |
| Wikipedia 佔 ChatGPT top citations | 47.9% | AI Platform Citation Patterns |
| 引語策略效益 | +41% | KDD 2024 GEO Paper |
| 統計引用策略效益 | +30% | KDD 2024 GEO Paper |
| 關鍵字堆砌處罰 | -9% | KDD 2024 GEO Paper |
| AI 搜尋平均查詢長度 | 23 字 vs 4 字（傳統） | LLMrefs |

> **2026/8 註記**：上表為 2026/6 底稿。最新 26 行數據表 + 32 條來源 URL 見 `seo-geo-key-data-2026-08.md`。重點變更：ChatGPT 8 億→9 億週活躍；zero-click 60%→68%；Sistrix 60% zero-click 查無此報告（實為「AIO 出現時 #1 CTR -60%」）；Conductor「conversion 2x」無直接數據（改以 +22% 轉換率與 Ahrefs 23 倍註冊倍率）。

---

## 十二、Agentic Commerce 補充（2026/8）

代理式商務 = AI agent 取代「搜尋 → 點擊 → 逛站 → 結帳」路徑，直接在對話介面完成發現、比較、下單、售後。

- **三大協定**：UCP（Google，2026/1 發表，Universal Cart 2026 夏美國上線）、ACP（OpenAI+Stripe 開源，2026/3 轉向 App 模式）、AP2（Google 付款授權層，三卡組織全數支援）
- **五個準備方向**：Product feed 乾淨度（GTIN +40% 點擊）、PDP JSON-LD（被引用率 3.1x）、bot 放行（封鎖 ≈ 2010 封 Googlebot）、協定就緒（Shopify Agentic Storefronts 一鍵上架）、售後 agent 化（決定回購推薦）
- **內容站**：出版商 Google 推薦流量年減 33%/38%（結構性）；被 AI 引用轉換率 4–9 倍；86% 消費者會再驗證 AI 推薦
- 完整版（協定細節、10 項 checkpoint、台灣市場提醒、數據速查）見 `agentic-commerce-2026.md`
