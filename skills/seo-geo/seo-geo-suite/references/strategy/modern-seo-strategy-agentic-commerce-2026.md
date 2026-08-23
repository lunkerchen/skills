## 新章節：Agentic Commerce（代理式商務）

> **一句話總結**：代理式商務 = AI agent 取代「搜尋 → 點擊 → 逛站 → 結帳」的人類路徑，直接在對話介面完成發現、比較、下單甚至售後。對 SEO/GEO 的意涵：排名不再是唯一戰場，**產品資料的乾淨度、bot 可存取性與交易協定就緒度**，才是被 agent 選進「短名單」的門票（[SEJ, 2026/6](https://www.searchenginejournal.com/surviving-the-impression-squeeze-how-agentic-commerce-is-changing-google-ads-in-2026/579939/)）。

### 為什麼 2026 是轉折年

2025 年 9 月 Google 發布 AP2 支付協定（60+ 夥伴含 Mastercard、Amex、PayPal），OpenAI 同月推出 ChatGPT Instant Checkout 並開源 ACP（[openai.com](https://openai.com/index/buy-it-in-chatgpt/)）。2026 年 1 月 Google 在 NRF 發表 UCP；2 月 Etsy、Wayfair 在 AI Mode/Gemini 內直接結帳（[blog.google](https://blog.google/products-and-platforms/products/shopping/agentic-checkout-holiday-ai-shopping/)）。**5/19 Google I/O 2026 推出 Universal Cart**：橫跨 Search、Gemini、YouTube、Gmail 的跨商家購物車，由 Gemini 自動追價、補貨通知、相容性檢查，基於 Google Wallet，UCP 結帳可走 Google Pay 或轉回商家網站，品牌永遠是 merchant of record（[blog.google](https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/)）。5/20 Marketing Live 再宣布 Merchant Center 新增 Conversational Attributes、BNPL（Affirm/Klarna）與 UCP 擴張（[blog.google](https://blog.google/products-and-platforms/products/shopping/shopping-updates-google-marketing-live/)）。微軟數據指出自動化流量成長速度約為人類流量的 **8 倍**（[Microsoft Advertising](https://about.ads.microsoft.com/en/blog/post/april-2026/win-across-all-three-eras-of-the-web)）。

### 三大協定地圖

| 協定 | 擁有者 | 範圍 | 現況（2026/8） | 商家要做的 |
|---|---|---|---|---|
| **UCP**（Universal Commerce Protocol） | Google（與 Shopify/Target/Walmart/Wayfair/Etsy 共開發） | 完整旅程：發現→購物車→結帳→訂單→退貨→客服（6 大能力：discovery/offers/cart/checkout/fulfillment 等） | 2026/1 發表、2 月上線；Universal Cart 2026 夏於美國 Search+Gemini 上線；擴至加拿大、澳洲、英國；新增飯店訂房與外送垂直（[paz.ai](https://www.paz.ai/blog/ucp-technical-guide-retailers)、[blog.google](https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/)） | Merchant Center feed + Schema.org Product；UCP 整合或透過平台（Shopify 等）間接加入 |
| **ACP**（Agentic Commerce Protocol） | OpenAI + Stripe（開源） | 發現與結帳為主 | 2025/9 上線（Etsy 即時結帳）；2026/3 OpenAI 將 Instant Checkout 轉向「App 模式」（Instacart/Target/Expedia/Booking.com），僅約 12 家 Shopify 商家真正上線（[Rye](https://rye.com/blog/openai-chatgpt-checkout-agentic-commerce)、[Forbes](https://www.forbes.com/sites/jasongoldberg/2026/03/10/why-openais-checkout-retreat-spells-trouble-for-its-commerce-strategy/)） | 向 OpenAI 申請 structured feed（可 15 分鐘更新一次） |
| **AP2**（Agent Payments Protocol） | Google（開放標準） | 付款授權層 | 2025/9 發表；三道數位簽章 Mandate（Intent→Cart→Payment，W3C Verifiable Credentials），防篡改審計軌跡供退貨/爭議使用；2026 下半年起從 Gemini Spark 開始導入 Google 產品（[cloud.google.com](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)、[blog.google](https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/)） | 不需自行建置；確保金流夥伴支援 AP2 即可 |

支付端：三大卡組織全數就位——Mastercard Agent Pay/Verifiable Intent（拉美+東南亞已跑真實交易）、Visa Trusted Agent Protocol → Intelligent Commerce Connect（AWS/Highnote/Mesh 試點）、Amex ACE Developer Kit + 業界首創「Agent Purchase Protection」購買保護（[paz.ai](https://www.paz.ai/blog/card-networks-agentic-commerce)、[americanexpress.com](https://www.americanexpress.com/en-us/company/agentic-commerce)）。

### 電商五個準備方向

1. **Product feed 是新的「排名因子」**。Google 在 NRF 2026 的官方指引明說：feed 屬性是進入 AI 表面的入場券——rich title、lifestyle 圖片、運送與退貨政策缺一不可（[dataiads](https://www.dataiads.io/en/blog/google-guidelines-attributs-merchant-center-ucp-commerce-agentic-protocol)）；I/O 2026 新增 Conversational Attributes，回答「這雙鞋適合雨天穿嗎」這類對話式問題（[azoma.ai](https://www.azoma.ai/insights/google-i-o-2026-what-the-agentic-commerce-announcements-mean-for-brands)）。有 GTIN 的商品可多獲最多 **40% 點擊**（[Merchant Center 官方文件](https://support.google.com/merchants/answer/6324461)）。
2. **乾淨結構化資料 = 被引用門檻**。有結構化資料的頁面被 Google AI Overviews 引用頻率高 **3.1 倍**；ChatGPT 引用的頁面 71%、AI Mode 引用的頁面 65% 含結構化資料（[commercetools](https://commercetools.com/blog/ai-ready-product-data-for-agentic-commerce-success)）。每個 PDP 需 Product+Offer（price/priceCurrency/availability）JSON-LD，加 AggregateRating、ReturnPolicy、FAQPage 更佳（[digitalapplied](https://www.digitalapplied.com/blog/product-data-ai-shopping-merchant-prep-guide)）。
3. **Bot 存取策略翻轉**：封鎖購物 agent ≈ 2010 年封鎖 Googlebot。務必放行 OAI-SearchBot、ChatGPT-User、PerplexityBot、Google-Extended、Claude-Web 等（[SEJ](https://www.searchenginejournal.com/surviving-the-impression-squeeze-how-agentic-commerce-is-changing-google-ads-in-2026/579939/)）；Cloudflare 已提供 Trusted Agent Protocol / Agent Pay 的 managed ruleset，可放行「受信任的付費 agent」同時擋其他爬蟲（[cloudflare.com](https://blog.cloudflare.com/secure-agentic-commerce)）。敏感路徑（/checkout、/account）仍應全封。
4. **協定就緒度**：不必自建 agent——透過 Shopify/Target/Walmart/Amazon 等平台承接協定重活，確保「至少可透過一個協定交易」，且資料格式與平台 feed 完全一致（[SEJ](https://www.searchenginejournal.com/surviving-the-impression-squeeze-how-agentic-commerce-is-changing-google-ads-in-2026/579939/)）。2026/7 Shopify Agentic Storefronts 讓數百萬商家一鍵上架 ChatGPT、Copilot、AI Mode、Gemini（[shopify.com](https://www.shopify.com/news/agentic-commerce-momentum)）。建議先從最高營收類別做起（URBN 先做洋裝與丹寧）（[polarisagency](https://www.polarisagency.com/marketing-insights/agentic-commerce-what-it-means-for-ecommerce-seo)）。
5. **售後支援決定「回購推薦」**：agent 會把過去訂單的支援品質（追蹤、退貨、退款速度）納入下次選擇商家的依據；UCP 涵蓋售後，AP2 的不可篡改 Mandate 讓買賣雙方在退貨/爭議時看同一份紀錄（[fin.ai](https://fin.ai/learn/what-is-agentic-commerce)、[blog.google](https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/)）。「Where's my package?」將變成 agent 對話而非客服工單（[metarouter](https://www.metarouter.io/post/agentic-commerce-trends-statistics)）。

### 內容站（非電商）的意涵

- **流量下滑是結構性，不是演算法波動**：出版商 Google 推薦流量年減 33%（全球）/38%（美國）（[bloxdigital](https://www.bloxdigital.com/resources/news/fighting-traffic-declines-focus-on-owned-channels-geo/article_e6507083-cac8-4921-b150-10fed4b16166.html)）；小型出版商兩年來最多跌 60%（[Neil Patel](https://neilpatel.com/blog/referral-traffic-decline-publishers/)）；Gartner 預測 2026 年底傳統搜尋量減少 25%（[tryaivo](https://www.tryaivo.com/blog/zero-click-crisis-ecommerce-traffic-decline)）。
- 但**被 AI 引用時轉換率高出 4–9 倍**（[tryaivo](https://www.tryaivo.com/blog/zero-click-crisis-ecommerce-traffic-decline)）；Adobe 統計 2025 假期檔生成式 AI 推薦流量暴增 693%（[retailbrew](https://www.retailbrew.com/stories/2026/02/11/google-makes-etsy-and-wayfair-items-shoppable-within-agentic-ai-search)）。
- 策略轉向：選購指南/知識內容需要「被引用策略」而非關鍵字策略——可驗證數據、清楚作者與日期、結構化 Article/FAQ、機器可讀；同時把 Email/社群等自有管道當護城河。86% 消費者會再次驗證 AI 推薦（68% 回 Google、48% 回品牌官網）——**品牌官網仍是信任落點**，但那是「確認」而非「發現」（[SEJ](https://www.searchenginejournal.com/surviving-the-impression-squeeze-how-agentic-commerce-is-changing-google-ads-in-2026/579939/)）。

### 2026 下半年 Checkpoint 清單

| # | Checkpoint | 驗證方式 |
|---|---|---|
| 1 | robots.txt 放行所有主要 AI/購物 crawler | 查 Disallow 規則；用 Ahrefs Site Audit 標記 |
| 2 | 每個 PDP 有完整 JSON-LD（Product+Offer+AggregateRating+ReturnPolicy） | Rich Results Test / Schema validator |
| 3 | Merchant Center feed 補齊 UCP 建議屬性（rich title、多圖、運送、退貨） | Merchant Center 診斷分數 |
| 4 | 評估 Conversational Attributes 缺口 | 對照 I/O 2026 新屬性 schema |
| 5 | 確認至少一個交易協定路徑（Shopify Agentic Storefront / UCP 整合 / ACP 申請） | 平台後台狀態 |
| 6 | 金流與發卡組織支援 AP2/agent 交易（Mastercard/Visa/Amex） | 與金流商確認 |
| 7 | 用 AI Mode / ChatGPT 對主力 SKU 做「短名單測試」（自然語言提問） | 每季記錄能見度 |
| 8 | 售後流程 agent 化：追蹤、退貨、退款可程式化處理 | 支援 API/自動化流程 |
| 9 | 監控 Merchant Center「AI 表面 share of voice」指標（2026 新增） | Merchant Center AI performance insights |
| 10 | 內容站：檢視被 ChatGPT/AI Mode 引用率與來源頁品質 | 引用追蹤工具（如 Otterly/Am I Cited） |

### 台灣市場提醒

多數功能美國先行：Universal Cart 2026 夏美國 Search+Gemini 上線，YouTube/Gmail 隨後；UCP 才剛擴加拿大/澳洲/英國。台灣沒有明確時程，但 Shopify 商家可透過 Agentic Storefronts 提早卡位，且美國案例說明了 feed 與結構化資料的標準只會更嚴格——現在就做是「領先成本」，屆時才做是「追趕成本」。

### 關鍵數據速查

| 數據 | 數值 | 來源 |
|---|---|---|
| Shopping Graph 商品數 | 60B+ | [blog.google](https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/) |
| 結構化資料頁面被 AI Overviews 引用倍率 | 3.1x | [commercetools](https://commercetools.com/blog/ai-ready-product-data-for-agentic-commerce-success) |
| 被 ChatGPT / AI Mode 引用頁面含結構化資料比例 | 71% / 65% | 同上 |
| GTIN 帶來的點擊提升 | +40% | [Google Merchant Center](https://support.google.com/merchants/answer/6324461) |
| 消費者因 AI 發現新品牌（2025/12 調查） | 43% | [Semrush](https://www.semrush.com/blog/ai-tools-the-modern-buyer-journey-study/) |
| 消費者會再次驗證 AI 推薦 | 86% | 同上 |
| Shopify 來自 AI 搜尋的訂單成長（2025） | 15x | [webyes 引 Shopify 總裁](https://www.webyes.com/blogs/structured-data-ai-agents) |
| 生成式 AI 推薦流量成長（2025 假期，Adobe） | +693% | [retailbrew](https://www.retailbrew.com/stories/2026/02/11/google-makes-etsy-and-wayfair-items-shoppable-within-agentic-ai-search) |
| 出版商 Google 推薦流量年減 | -33% 全球 / -38% 美國 | [bloxdigital](https://www.bloxdigital.com/resources/news/fighting-traffic-declines-focus-on-owned-channels-geo/article_e6507083-cac8-4921-b150-10fed4b16166.html) |
| Google Ads 曝光年減（Optmyzr Q1 2026） | -11% | [SEJ](https://www.searchenginejournal.com/surviving-the-impression-squeeze-how-agentic-commerce-is-changing-google-ads-in-2026/579939/) |
| 自動化流量 vs 人類流量成長 | 8x | [Microsoft Advertising](https://about.ads.microsoft.com/en/blog/post/april-2026/win-across-all-three-eras-of-the-web) |
