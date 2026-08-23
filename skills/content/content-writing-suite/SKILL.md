---
name: content-writing-suite
description: 文字內容工程與長文發布旗艦：去除 AI 寫作機械味（stop-slop）、人性化潤色（writing-humanizer）、簡轉繁台灣在地化（s2t-taiwan）、方格子科技長文 SOP（vocus-article-writing-sop）與單檔高質感 HTML 文章排版（html-article-author）。
version: 1.0.0
author: Community
license: MIT
read_when:
  - User asks to write, edit, rewrite, polish, humanize, or remove AI smell from articles or copy
  - User wants to translate/convert Simplified Chinese to Taiwan Traditional Chinese with local terminology
  - User asks to write a deep-dive tech article or Vocus-style journalism story
  - User wants to output or format an article as a self-contained, beautiful, responsive HTML page
metadata:
  hermes:
    tags: [content, writing, anti-slop, humanizer, localization, vocus, html-author, suite]
---

# 文字內容工程與長文發布旗艦（Content Writing Suite）

一站式處理文章構思、繁體中文在地化、AI 贅字清洗、人性化潤色到單檔精美 HTML 文章排版的全流程旗艦工作台。

---

## 核心管線：內容產出至發布標準流

```
[原始選題 / 草稿 / 新聞來源]
       │
       ▼
[模組 1：方格子深度長文架構] ──> 科技記者視角、精準大標、倒金字塔摘要、數據口徑
       │
       ▼
[模組 2：簡轉繁台灣在地化] ────> 術語校準（程式碼、伺服器、專案、資訊、資料庫）
       │
       ▼
[模組 3：stop-slop AI 贅字清洗] ─> 剃除「在...的浪潮下」、「值得注意的是」、「綜上所述」
       │
       ▼
[模組 4：人性化口吻潤色] ──────> 調整句式節奏、口語親和力、專業自洽
       │
       ▼
[模組 5：單檔 HTML 精緻排版] ──> 自帶字體、RWD 排版、深色/淺色自適應、SEO 元件
```

---

## 旗艦模組一覽

### 模組 1：方格子科技長文 SOP（Vocus Longform SOP）
- **科技記者視角**：以洞察為核心，非產品公關稿。
- **結構三要素**：
  1. 破題：一句話帶出核心矛盾或產業轉折。
  2. 深度剖析：技術原理、商業模式與生態位對比。
  3. 結論與行動指引：對個人/企業的具體啟示。

### 模組 2：台灣繁中在地化（Taiwanese Localization）
- **專業術語精確轉換**：
  - 代碼 ➔ 程式碼 / 程式
  - 服務端 ➔ 伺服器
  - 項目 ➔ 專案
  - 信息 ➔ 資訊 / 訊息
  - 緩存 ➔ 快取
  - 默認 ➔ 預設

### 模組 3：去除 AI 機械味（Anti-Slop Engine）
- **必殺禁用詞清單**：
  - 「在這個快速變遷的時代 / 浪潮下...」
  - 「總結來說 / 綜上所述 / 無疑是...」
  - 「不容忽視 / 值得注意的是 / 扮演著關鍵角色...」
- **修復手法**：直接切入事實主詞，用具體動作取代虛詞鋪墊。

### 模組 4：人性化與節奏調整（Writing Humanizer）
- **長短句交錯**：短句定調，長句展開，打破 AI 平均句長之呆板節奏。
- **真實視角引入**：適度加入第一人稱工程/實戰經驗與具體案例。

### 模組 5：單檔 HTML 文章發布（HTML Article Author）
- **單一自洽 HTML**：免外部 CSS/JS 相依，整合 Google Fonts（Noto Sans TC）、響應式排版、代碼高亮與社群分享標籤。
