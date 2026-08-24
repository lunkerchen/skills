# GSC 部署後成效反饋時序指南 (Deployment Feedback Timing)

本指南說明網站進行 SEO、GEO、AEO 或技術架構（如 Schema 注入、Markdown Twin、Is-Agentic 協議）改造後，Google Search Console 與 AI 搜尋引擎各階段反饋的預期時序與評估標準。

---

## 一、 四階段反饋生命週期

```
  [0 ~ 48 小時]        [3 ~ 7 天]           [7 ~ 14 天]          [28 天以上]
  技術建置與驗證 ───> 爬蟲探索與狀態移轉 ───> 關鍵字曝光與位移 ───> 統計穩定與 SOV 驗收
  (Live Verification)  (Indexing Status)    (Search Analytics)   (MoM & Attribution)
```

---

## 二、 各階段詳細時序與檢驗重點

### 第一階段：部署立即與 0 ~ 48 小時（技術建置與觸發）
- **核心目標**：確保生產環境完全符合規範，爬蟲能正確解析。
- **行動清單**：
  1. 執行 6-Gate 建置前與部署後現場驗證（Live Verification）。
  2. 檢查 `robots.txt`、`sitemap.xml`、`llms.txt` 與 Link Header。
  3. 透過 GSC 後台或 API 重新提交 `sitemap.xml`。
  4. 使用網址審查 (URL Inspection Tool) 針對重點變更頁面點擊「要求編入索引」。
- **預期現象**：GSC 報表數據尚未更新（正常現象，GSC 數據有 2~3 天延遲）。

### 第二階段：3 ~ 7 天（爬蟲探索與狀態移轉）
- **核心目標**：觀察 Googlebot 與 AI 爬蟲（GPTBot, ClaudeBot, PerplexityBot 等）抓取頻率。
- **預期現象**：
  - 伺服器 Access Logs 出現爬蟲集中抓取改造頁面與 `/llms.txt`。
  - GSC 索引涵蓋率報表中，網址從「未探索」或「排除」移轉至「已編入索引」。
  - 增強功能 (Rich Results) 開始顯示偵測到的新 Schema 項目（如 FAQPage、Product 等）。
- **注意事項**：若 7 天後仍停留在 `已探索 - 目前尚未編入索引`，需立即補強內部連結與頁面資訊密度。

### 第三階段：7 ~ 14 天（關鍵字曝光與初階位移）
- **核心目標**：評估新關鍵字詞組的曝光 (Impressions) 與平均排名 (Position)。
- **預期現象**：
  - Search Analytics 報表開始出現針對改寫後 H2/H3 問句題目的曝光量。
  - 長尾問題關鍵字開始進入前 20 名（第 2 ~ 3 頁）。
  - Perplexity 與 ChatGPT 聯網搜尋開始於生成答案中引用該頁面片段。

### 第四階段：28 天以上（統計顯著性與整體驗收）
- **核心目標**：計算點擊率 (CTR)、整體自然流量增長與 AI SOV (Share of Voice)。
- **評估公式**：
  - **曝光增長率** = `(最近 28 天曝光 - 改造前 28 天曝光) / 改造前 28 天曝光 × 100%`
  - **點擊率變動** = `最近 28 天平均 CTR - 改造前 28 天平均 CTR`
- **預期成果**：
  - 結構化 Rich Results 帶動 CTR 提升 15% ~ 35%。
  - 具有 AEO 問答特性的段落獲得 Google AI Overview (AIO) 置頂摘要引用。

---

## 三、 常見誤區與抗焦慮守則

1. **勿於 48 小時內依據 GSC 報表做二次改動**：GSC 報表天然存在 48–72 小時的資料延遲（Data Lag），前兩天的空白不代表改動無效。
2. **區分 Indexing Lag 與 Ranking Lag**：
   - 頁面進入索引通常需要 1–5 天。
   - 排名與曝光權重重新計算通常需要 10–21 天。
3. **快取失效時間 (Cache TTL)**：Cloudflare 或 CDN 快取需確保於部署後即時清除，否則爬蟲抓取到的仍為舊版 HTML。
