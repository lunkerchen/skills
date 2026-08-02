# SEO + GEO 深度研究（完整版）— 2026 年 6 月

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

## 七、各 AI 引擎特性

| 引擎 | 特性 | 優化重點 |
|------|------|----------|
| **ChatGPT** | ~70% 市佔。混合即時搜+訓練資料。87.4% AI referral 流量來自 ChatGPT | 全面有來源的內容、權威信號 |
| **Google AI Overviews/AI Mode** | 整合傳統 ranking + AI synthesis | 已有 organic 排名者有利。Schema markup |
| **Perplexity** | 強 citation focus。偏愛近期內容。SaaS 轉換率最高 | 新鮮度、來源透明度 |
| **Gemini** | 成長最快。整合 Google 搜尋基礎設施 | 強 Google SEO 自動轉 Gemini 可見度 |
| **Claude** | 整合 Safari。偏愛邏輯清晰的結構化內容 | 結構、邏輯論證 |

---

## 八、工具生態

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
  └── llms.txt

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
