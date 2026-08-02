---
name: geo-content-reformatting
description: >-
  Reformat visible H2/H3 into GEO-friendly QA headings.
read_when:
  - User wants GEO optimization but explicitly forbids new visible content sections
  - Reformatting existing feature/benefit sections to be AI-search-friendly
  - Adding GEO benefit without adding DOM elements or changing page layout
related_skills:
  - webapp-geo-optimization: Umbrella skill for invisible GEO optimization
  - geo-article-friendly: Per-article GEO transformation for content sites
---

# GEO Content Reformatting

## Use

當需要提升現有頁面內容的 GEO/AI 搜尋友好度，但不允許新增可視區塊（FAQ、How-It-Works）時。透過改寫既有 **H2/H3 標題** 為問題句式，讓 AI crawler 自然將「標題 + 緊接段落」視為問答對（QA pair）。

## 核心原則

- **不新增 DOM 元素** — 只修改既有 heading 內容文字
- **不改變設計** — heading 樣式（字型、大小、顏色）完全保留
- **問題句式** — 標題從「名詞片語」改為「完整問句」
- **答案保留** — 段落內容不刪除，只調整語氣使其直接回答標題問題
- **與 JSON-LD 互補** — FAQPage JSON-LD 提供結構化資料；可見 heading 重構提供 AI crawler 自然語言 cue

## 轉換規則

| 原文標題風格 | 改寫為問題句式 |
|---|---|
| 名詞標題：`違規停車` | `哪些違規行為可以用這個工具檢舉？` |
| 功能標題：`簡訊內容格式` | `檢舉簡訊需要填寫哪些內容？` |
| 流程標題：`如何使用` | `如何使用這個工具？` |
| 描述標題：`關於我們` | `這個平台是做什麼的？` |

## 執行步驟

1. **盤點現有 heading** — 列出頁面上所有 H2/H3，分類哪些適合改寫
2. **改寫為問題** — 確保問題是使用者會直接在 AI 搜尋中輸入的樣式
3. **微調段落首句** — 段落第一句直接回答問題（答案置前原則）
4. **驗證無設計變動** — 只改了文字內容，heading 樣式/層級/位置不變

## 適合情境

- 工具型 SPA 首頁的功能介紹段落
- 平台說明區塊（How it works 的非標題化版本）
- 服務項目清單
- FAQ 區塊（如果已存在可見的 FAQ）

## 不適合情境

- 純視覺標題（「我們的服務」、「熱門商品」等不需要搜尋曝光的 heading）
- 頁面最頂層的 H1 標題（通常已是品牌/產品名稱）
- 導航相關文字

## Pitfalls

- 不要為了 SEO 把所有 heading 都改成問題 — 只改邏輯上適合做 QA 的自然內容段落
- 問題要像使用者會問的，不是像考試題目。「並排停車的定義是什麼？」而非「試說明並排停車之定義」
- 段落內容必須真正回答該問題，否則 AI crawler 提取後會產生錯誤引用
