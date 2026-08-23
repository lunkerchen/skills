---
name: ai-gap-analysis
description: 診斷競品被 AI 推薦而自家缺席 — Mention 與 Citation 缺口。
version: 1.0.0
author: community
license: MIT
read_when:
  - User asks why competitors appear in ChatGPT/Perplexity/Google AI Overviews but their brand does not
  - Performing AI Mention Gap or AI Citation Gap analysis for a brand, product, or service
  - Auditing outside evidence, category consensus, and earned media citations for GEO
  - Formulating an off-page GEO strategy (Reddit, YouTube, Wikipedia, industry directories)
metadata:
  hermes:
    tags: [seo, geo, gap-analysis, share-of-voice, competitive-analysis, mentions]
---

# AI Gap Analysis（AI 搜尋缺口與外部共識分析）

## When to Use

當你需要診斷「為什麼使用者問 ChatGPT / Perplexity / Google AI Overviews 推薦方案時，競品總是被列入推薦短名單，而自家品牌卻缺席」時使用此 Skill。

> **核心原理**：AI 推薦不依賴單一網頁的關鍵字排名，而是基於**「全網類別共識（Category Consensus）」**。當第三方來源（Reddit、YouTube、評測媒體、行業報告）反覆將競品與特定問題錨定在一起時，AI 會產生強大的關聯信心。

---

## 缺口診斷雙維度

```
                              ┌─────────────────────────────────────────┐
                              │            AI 搜尋缺口分析               │
                              └────────────────────┬────────────────────┘
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   ▼                                                               ▼
       【AI Mention Gap（提及缺口）】                                  【AI Citation Gap（引用缺口）】
   競品被列入推薦名單，自家品牌缺席。                                   競品被當作權威數據引用，自家無對應資產。
   • 根因：缺乏第三方共識與外部背書                                     • 根因：缺乏原創數據與 Information Gain
   • 解法：補齊 Reddit/YouTube/公關報導                                • 解法：打造深度實測、行業報告、抗摘要工具
```

---

## 4 步診斷與修復流程

### 步驟 1：建構 10–20 組意圖 Prompt 探針

依據業務場景生成 4 種維度的探針查詢：
1. **直接推薦型**：「2026 年適合 [目標客群] 的最佳 [產品/服務類別] 有哪些？」
2. **對比抉擇型**：「[競品 A] vs [競品 B]，有其他更推薦的選擇嗎？」
3. **場景痛點型**：「遇到 [具體業務難題] 時，業界通常使用什麼工具或方案？」
4. **預算/門檻型**：「預算 [金額範圍] 內最值得導入的 [解決方案]？」

---

### 步驟 2：執行跨引擎盲測與來源逆向

在 ChatGPT（啟用 Search）、Perplexity 與 Google AI Mode 輸入上述探針，記錄：
- **推薦短名單**：出現了哪些品牌？排序如何？
- **引用來源角標（Citations）**：AI 引用了哪些具體網址？
  - 是否來自 Reddit 討論串？
  - 是否來自 YouTube 影片逐字稿？
  - 是否來自特定部落客的評測列表（Best/Top/Vs 文章）？
  - 是否來自 Wikipedia / G2 / Crunchbase？

---

### 步驟 3：產出缺口矩陣（Gap Matrix）

| 探針問題 | 競品提及 | 引用來源類型 | 自家缺席原因 | 突破路徑 |
|---|---|---|---|---|
| 「企業 AI 導入顧問推薦」 | 競品 A, B | 某科技媒體報導、YouTube 訪談 | 缺少第三方專訪與外部案例報導 | 安排客戶案例發布至 Medium/科技論壇 |
| 「台北二手相機收購推薦」 | 競品 C, D | PTT/Dcard 討論串、Google 地圖評論 | 社群討論度不足，未被 RAG 檢索收錄 | 整理客戶真實收購評價與透明估價表 |

---

### 步驟 4：高 ROI 外部共識修復清單

依據 2026 AI 引用權重，按優先級執行補強：

1. **進入「已被 AI 引用的文章」**（見效最快）：
   - 找出 AI 頻繁引用的第三方評測清單（如「2026 十大推薦...」）。
   - 聯絡作者或網站編輯，提供最新產品資料與測試帳號請求補入清單。
2. **Reddit / PTT / Dcard 深度回文（Brand Mentions）**：
   - 在相關問題的討論串下，以客觀、無廣告感的「真實使用心得」提及品牌與核心優勢（Unlinked Mention 亦有強效）。
3. **YouTube 影音逐字稿注入（權重最強 ~0.737）**：
   - 拍攝 1–2 部針對痛點的實測影片，並在說明欄與逐字稿中完整包含品牌名稱與解決方案。
4. **打造抗摘要資產（Information Gain）**：
   - 發布一份帶有原創統計數據的行業調查或開源工具，成為同業與 AI 的引用真相源（Source of Truth）。
