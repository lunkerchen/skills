---
name: agentic-commerce-readiness
description: 電商/產品頁優化給 AI 購物代理 — UCP/ACP/AP2 與 PDP Schema。
version: 1.0.0
author: community
license: MIT
read_when:
  - User asks to optimize e-commerce, product pages (PDP), pricing, or booking pages for AI shopping agents
  - Optimizing products or booking flow for ChatGPT Search, Google AI Mode, Copilot, or Gemini shopping
  - Checking Google UCP (Universal Commerce Protocol), OpenAI ACP (Agentic Commerce Protocol), or AP2 payment standards
  - Auditing Product/Offer JSON-LD for AI crawler compliance (GTIN, return policy, shipping details)
  - Configuring Cloudflare WAF / robots.txt to allow shopping bots while protecting checkout endpoints
metadata:
  hermes:
    tags: [seo, geo, ecommerce, agentic-commerce, schema, ucp, acp, ap2]
---

# Agentic Commerce Readiness（代理式商務與購物 Agent 審計）

## When to Use

當你需要將電商產品頁（PDP）、預約服務頁（如美甲、顧問、課程）或定價頁面優化為「AI Agent 可直接發現、比價、推薦甚至下單」的狀態時使用此 Skill。

---

## 核心認知：代理式商務三大協定（2026/8）

1. **Google UCP（Universal Commerce Protocol）**：
   - 核心標準：整合 Merchant Center Product Feed + Schema.org `Product`/`Offer`。
   - 表現：在 Google AI Mode / AI Overviews / Universal Cart 中直接進入購物候選與一鍵結帳清單。
2. **OpenAI ACP（Agentic Commerce Protocol）**：
   - 核心標準：支援 App/Storefront 模式（Instacart/Shopify 原生對接）與結構化 Product Feed。
   - 表現：在 ChatGPT Search 與對話框中直接以產品卡片呈現並引導支付。
3. **AP2（Agent Payments Protocol）**：
   - 核心標準：Google 提出的開放授權支付標準，Visa/Mastercard/Amex 全數支援「Agent 授權防護（Mandate）」。
   - 表現：確保金流支援不可篡改的代理授權記錄，保障退款與爭議處理。

---

## 審計與落地 4 步走

### 步驟 1：PDP 結構化資料加固（JSON-LD）

AI 購物 Agent 對缺少關鍵屬性的產品頁直接過濾。每個產品/服務頁必須包含以下完整欄位：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "產品或服務名稱",
  "image": ["https://example.com/images/1x1/photo.jpg"],
  "description": "40-60 字精準功能描述與核心規格",
  "sku": "SKU-12345",
  "gtin13": "4711234567890",
  "brand": {
    "@type": "Brand",
    "name": "品牌名稱"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/123",
    "priceCurrency": "TWD",
    "price": "6880",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "TW",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 7,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "TWD"
      },
      "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "TW"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 0,
          "maxValue": 1,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 3,
          "unitCode": "DAY"
        }
      }
    }
  }
}
</script>
```

> **關鍵檢查清單**：
> - [ ] `gtin` / `sku` 是否存在（GTIN 在 Google AI 購物比價中可獲得 +40% 優先曝光）
> - [ ] `priceValidUntil` 是否未過期
> - [ ] `hasMerchantReturnPolicy` 是否明確定義
> - [ ] `itemCondition` 是否標記（如 `UsedCondition`、`NewCondition`）

---

### 步驟 2：Bot 存取分流策略（robots.txt & WAF）

封鎖購物 Agent 相當於放棄 AI 推薦流量。必須實施「**公開催告放行，交易敏感端點隔離**」：

#### 1. `robots.txt` 宣告：
```robots.txt
# 允許 AI 搜尋與購物代理爬取產品與價格
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: Google-Extended
User-agent: PerplexityBot
User-agent: Claude-Web
Allow: /products/
Allow: /services/
Allow: /pricing/
Allow: /llms.txt

# 阻擋敏感個人資料與支付路徑
Disallow: /checkout/
Disallow: /cart/
Disallow: /account/
Disallow: /api/order/
```

#### 2. Cloudflare WAF / 防火牆設定：
- 檢查 Security → Bots 設定，**不要開啟全局 AI Scraper 封鎖**。
- 將 `OAI-SearchBot` 與 `ChatGPT-User` 加入 Trusted Agent / Allow 清單。

---

### 步驟 3：Conversational Attributes 補充（對話意圖屬性）

AI 購物代理通常處理對話式長句（如「預算 2 萬內、適合女生單手拿、對焦快的二手相機」）。在頁面 HTML 中必須提供獨立可抽取的「規格對照區」：

- **適用對象（Who it's for）**：直接以 1-2 句說明適合客群。
- **核心限制（Trade-offs / Limitations）**：誠實揭露不適合情境（AI 會據此判定內容真實客觀而大幅提升推薦權重）。
- **參數結構表（Markdown Table）**：尺寸、重量、保固天數、適用環境以表格呈現。

---

### 步驟 4：驗證與回檢（5 項驗證門戶）

1. **Schema 語意驗證**：以 Google Rich Results Test 或 Schema.org 測試工具驗證 `Product` + `Offer` 無 Warning。
2. **SSR 直出檢測**：使用 `curl -A "ChatGPT-User" <URL>` 確保產品名稱、價格、庫存狀態在 HTML 原始碼內，非客戶端 JS 動態渲染。
3. **新鮮度檢驗**：確認價格變動時，頁面中的 `dateModified` 與 JSON-LD 同步更新。
4. **回購/售後信號**：退換貨政策與客服聯絡方式是否有獨立 URL 且被首頁 `/llms.txt` 索引。
