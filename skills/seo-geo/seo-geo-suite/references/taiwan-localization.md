# 台灣在地化環境與法規適配規範（Taiwan Localization Standards）

為確保網站在台灣市場、在地搜尋引擎與繁體中文 AI 代理中具備最高可信度與合規性，必須嚴格落實以下在地化規範：

### 1. 語言、時區與幣別標記
- **HTML 語系**：一律採用 `<html lang="zh-TW">`，嚴禁使用 `zh-CN` 或無地區碼的泛 `zh`。
- **OpenGraph**：`<meta property="og:locale" content="zh_TW">`，若有英文版搭配 `<meta property="og:locale:alternate" content="en_US">`。
- **JSON-LD 語系**：在 `@graph` 宣告 `"inLanguage": "zh-TW"`。
- **時區與時間戳**：排程、活動與發布時間一律標註 `Asia/Taipei`（UTC+08:00，如 `2026-08-24T10:00:00+08:00`）。
- **幣別標記**：電商與報價 Schema 之 `priceCurrency` 預設為 `"TWD"`，前端顯示慣例為 `NT$ 1,200` 或 `新台幣 1,200 元`。

### 2. 台灣商業實體與組織結構化（Entity Anchoring）
- **統一編號與稅籍**：在 `Organization` / `LocalBusiness` 中注入 `"taxID": "83xxxxxx"`（台灣 8 碼統編）。
- **標準台灣地址（PostalAddress）**：
  ```json
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "忠孝東路四段310號11樓",
    "addressLocality": "大安區",
    "addressRegion": "台北市",
    "postalCode": "106",
    "addressCountry": "TW"
  }
  ```
- **在地客服與通訊管道**：
  - 市話格式：`+886-2-xxxx-xxxx`（台北/基隆）、`+886-4-xxxx-xxxx`（台中）、`+886-7-xxxx-xxxx`（高雄）。
  - 手機/簡訊：`+886-9xx-xxx-xxx` 或 `09xx-xxx-xxx`。
  - LINE 官方帳號：將 `https://line.me/R/ti/p/@yourbrand` 寫入 `sameAs` 與 `contactPoint`。

### 3. 台灣在地搜尋與社群證據矩陣
AI 引擎在評估台灣本土品牌與主題權威（Topic Authority）時，高度權重依賴以下在地信任源：
- **主要搜尋環境**：Google 台灣 (`google.com.tw`)、Yahoo 奇摩搜尋。
- **高權重社群與論壇證據**：Threads（台灣極高活躍度）、Facebook 粉專/社團、Dcard、PTT（批踢踢實業坊）、Mobile01、YouTube。
- **在地徵才與企業信用**：104 人力銀行、Yourator 職缺頁面連結。

### 4. 台灣電商、物流與消保法規遵循
- **金流串接宣告**：支援台灣主流金流（綠界科技 ECPay、藍新金流 NewebPay、LINE Pay、街口支付、台灣 Pay）。
- **超商與在地物流**：7-ELEVEN / 全家便利商店店到店、黑貓宅急便、郵局快捷。
- **消保法第 19 條退換貨標記（hasMerchantReturnPolicy）**：
  - 實體商品：依消保法宣告 7 日猶豫期（鑑賞期）。
  - 數位內容 / 客製化商品：依《通訊交易解除權合理例外情事適用準則》在 Schema 中明確標註排除條款（如 `merchantReturnDays: 0` 並附說明網址），避免 AI 購物代理誤判。

### 5. 繁體中文技術與商業用語標準
全站文案、Schema 與 Markdown 一律遵循台灣在地慣用術語：
- `程式碼 / 程式`（非 代碼）、`資訊 / 訊息`（非 信息）、`專案`（非 項目）
- `伺服器`（非 服務端）、`介面 / 接口`（非 接口）、`快取`（非 緩存）
- `預設`（非 默認）、`演算法`（非 算法）、`資料 / 資料庫`（非 數據/數據庫）
- `套件 / 模組`（非 包/插件）、`使用者`（非 用戶）、`解析度`（非 分辨率）
