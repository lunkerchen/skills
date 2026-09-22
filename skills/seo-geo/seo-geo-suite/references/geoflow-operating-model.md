# GEOFlow 吸收層：把 GEO 做成可驗證的內容工程閉環（完整版）

以下是依 GEOFlow 公開程式與文件可核對的能力，轉譯成適合本工作台的建議；不是 GEOFlow 宣稱的完整 GEO 方法論。只吸收與 GEO 直接相關、可移植到本工作台的模式；不搬 Laravel、PostgreSQL、Redis、佇列或後台 UI。

### AI 內容工程品質層：先判斷，再生成

這是本工作台採用的可重用內容工程流程，不是 Google 的完整官方規格，也不是排名或 AI 引用的安全豁免。適當使用 AI/自動化不因產製方式本身違規；仍須避免大量、低價值、缺乏原創性且主要為操縱排名的 scaled content abuse。每篇內容先完成 Ahrefs 五問 brief（Reader、Promise、Point of view、Evidence、Information gain），再依「題目 brief -> 研究/證據 -> 閘門 -> 草稿 -> 第二人審核 -> 發布 -> 量測」執行。研究、內容缺口、提綱、證據與草稿分開保存；四個品質閘門可繼續、退回或終止。完整判準、證據欄位與事實邊界見 `references/strategy/ai-content-engineering-quality.md`。

### 客戶導向報告輸出契約

產出客戶專屬 SEO/GEO 診斷／提案報告時，不得只交付通用分數或能力矩陣；先選定「在地服務型」或「B2B 產品／製造型」archetype，依 `Metadata -> 01 執行摘要與核心現狀 -> 02 Gap Matrix -> 03 Implementation Artifact -> 04 Roadmap -> CTA／報告邊界／來源` 六段結構交付。每個 finding、可驗收指標、程式碼狀態（current／proposed／deployed）、證據層級與報價估算都必須遵守 `references/strategy/client-report-output-contract.md`；完整契約與 Markdown outline 以該 reference 為準。

### 1. 本工作台轉譯的四層資產模型：不要把 GEO 縮成關鍵字

每個品牌或網站先建立四層資產：

1. **Source of Truth**：官方定位、服務邊界、價格、資格、聯絡方式與更新責任人。
2. **Evidence Assets**：每個可驗證主張綁定來源 URL、發布/有效時間、適用範圍、來源類型、owner 與版本/雜湊；缺證據就標為 `unverified`，不可補寫。
3. **Question Map**：把關鍵字擴成使用者問題，至少覆蓋定義、推薦、How-to、比較、限制/例外與預算情境。
4. **Deep Content**：能提供原創數據、實測、案例、計算方式或清楚方法論的抗摘要資產。

### 2. 標準 GEO 內容管線

```text
題目 brief -> 研究/內容缺口 -> 提綱 -> 證據 -> 四個品質閘門 -> 草稿
  -> 第二人審核 -> 發布前門禁 -> 可信分發 -> 量測與更新
  -> 觀測抓取、搜尋與 AI 提及/引用 -> 回補問題、證據或內容
```

生成器可以提出草稿，但不能決定事實或放行；模型判斷、固定規則評分、人工覆核與最終發布狀態必須分開。

### 3. 發布前 GEO 質量門禁

對文章、服務頁與知識資產逐項檢查：

- **Intent**：首段與 H2/H3 是否直接回答目標問題。
- **Evidence**：每個物質性主張是否有可追溯來源；狀態分 `supported`、`contradicted`、`unverified`。
- **Structure**：答案置頂、獨立段落、步驟/比較/限制條件可被單獨抽取。
- **Integrity**：禁止虛構來源、數字、法規、案例與引用編號；缺資料只能標 `[待補證據]`。
- **Risk**：絕對化承諾、效果保證、過期資訊與主體/範圍錯置進人工覆核或阻擋。
- **Traceability**：保存內容、證據、提示詞、規則版本與模型版本快照，讓之後能重現。

質量分數不是發布結論：分數高但有未驗證的重大主張，仍須 `needs_review`；技術或證據檢索失敗時顯示「未評分」，不可當成通過。

### 4. 快照、失效與回退

生成或審核時記錄 `knowledge_base_id + chunk_id + content_hash + source_hash`，並一併保存 prompt、模型、規則與執行版本。知識內容、來源或治理狀態變更後，舊結果自動失效；只有快照仍吻合才可重用。

只有在事先授權且風險覆蓋、證據覆蓋與結構校驗都通過時，才能從全文檢查降級為確定性抽樣；否則失敗並保留人工重檢入口。失敗回退不得悄悄變成成功。

### 5. 觀測語義必須分層

- AI crawler / agent 存取是**抓取觀測信號**，不等於 ChatGPT、Perplexity 或 Google AI Overviews 已引用。
- GSC 是搜尋成效資料，不冒充 AI 引用資料。
- 每次內容或部署記錄時間戳，至少比較 7/14/28 日變化。
- AI Mention、Citation、Perception 與 SOV 必須保留查詢、引擎、地區、答案快照、引用 URL 和採樣時間；缺少實測就報「未測量」。

### 6. 分發與實體一致性

先確定一個 canonical 事實來源，再依出口能力分發到官網、靜態頁、WordPress/API、社群或影音說明；各出口保留可用的來源與適用範圍。分發成功不代表內容正確。自有網站發布後，依專案能力讀回 URL、狀態碼、canonical、Schema、robots、sitemap、llms.txt 與實際內容；第三方渠道只記錄可取得的發布回執，無法讀回就標為 `unverified`。

### GEOFlow 對本工作台的執行映射

執行跨模組任務時，先依本工作臺的內容管線、證據門禁與發布驗證規則建立 lifecycle，再依下表載入專責 skill；單頁、單一標籤的小修不必啟動完整 pipeline。

| GEOFlow 模式 | 本工作台的最小落地 |
|---|---|
| 知識庫與證據快照 | `geo-content-reformatting` + `site-seo-geo-audit` 的 evidence ledger；不新增資料庫 |
| 主張質檢與門禁 | `seo-geo-suite` 的 deterministic checklist；需要自動化時再加專案腳本 |
| 問題地圖與內容生產 | `ai-gap-analysis` + `geo-article-friendly`，先建 prompt universe 再寫頁面 |
| 靜態/機器可讀分發 | `static-site-geo`、`llms-txt-generation`、`static-site-seo-build-verification` |
| 抓取與引用觀測 | `brand-search-monitoring`、GSC skill；明確區分 crawl signal 與 citation |
| 失效與回退 | 內容/來源雜湊、規則版本、部署時間；禁止未授權的自動放行 |
