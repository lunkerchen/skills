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

### 2.4 各 AI 引擎特性速查

| 引擎 | 特性 |
|------|------|
| **ChatGPT** | 市佔 ~70%。混合即時搜+訓練資料。偏愛全面有來源的內容 |
| **Google AI Overviews/AI Mode** | 整合傳統 ranking。已有 organic 排名者有利 |
| **Perplexity** | 強 citation focus。偏愛近期內容。SaaS 轉換率高 |
| **Gemini** | 成長最快。強 Google SEO 自動轉 Gemini 可見度 |
| **Claude** | 整合 Safari。偏愛邏輯清晰的結構化內容 |

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
  └── llms.txt 建立（官方規格，Google Search Central 已支援）

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

## 第五章：工具生態

### GEO 專用工具
- **Profound** — 企業級，$35M Series B（Sequoia）。Share of voice + sentiment + prompt-level rankings
- **Ahrefs Brand Radar** — 追蹤 5 個 AI 平台，1 億+ prompt 資料庫
- **SEMrush AI Visibility Toolkit** — $99/月/domain
- **Otterly.AI** — Google AI Overview + Perplexity 引用分析
- **GEO/AEO Tracker** — 開源自架，BYOK，$0/月

### 開源 GEO 生態（姚金剛）
- **GEOFlow**（2.7k ⭐）— 開源 GEO 內容工程與多站點分發系統。PHP 8.2 + PostgreSQL(pgvector) + Docker。覆蓋知識庫/RAG、多模型生成、審核發布、WordPress/HTTP Agent 分發、llms.txt/Schema/sitemap。`github.com/yaojingang/GEOFlow`
- **yao-geo-skills**（468 ⭐）— 20 個 GEO 專用 skill，含戰略診斷、頁面技術、內容生產、知識資產、歸因監測、GEOFlow 運營。`github.com/yaojingang/yao-geo-skills`
- **yao-meta-skill**（1.6k ⭐）— Skill OS 框架：把 workflow 編譯為跨平台可復用的 agent skill 包，含 eval、審查門戶、證據帳本。`github.com/yaojingang/yao-meta-skill`
- **測量框架論文**：《From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms》— 由姚金剛發表的跨平台 GEO 效果測量方法

### 手動速測（免費）
每月做一次：針對行業相關問題問 ChatGPT + Perplexity + Gemini，看品牌是否出現、如何被描述、引用了哪些來源。

---

## 關鍵數據參考

| 數據 | 來源 |
|------|------|
| GEO 提升 AI 可見度最高 40% | arXiv:2311.09735（KDD 2024） |
| AI referral conversion 比傳統高 2× | Conductor 2026 Benchmarks |
| ChatGPT 佔 AI referral 流量 87.4% | Conductor 2026 Benchmarks |
| Google ranking vs AI citation overlap <20% | Brandlight 2026 |
| Vercel 10% 新註冊來自 ChatGPT | Vercel 官方 |
| 3 個月內容新鮮度 cliff | LLMrefs 資料 |
| 結構化內容可見度 +30-40% | 多來源實測 |
| ChatGPT 8 億週活躍用戶 | OpenAI 官方 |

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
- `references/seo-geo-deep-research-2026.md` — 本研究的完整資料
- `references/darkseoking-strategy.md` — Darkseoking 意圖矩陣策略原始說明
