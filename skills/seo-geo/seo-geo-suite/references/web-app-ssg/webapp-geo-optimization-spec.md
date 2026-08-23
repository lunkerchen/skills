---
name: webapp-geo-optimization
description: Generative Engine Optimization (GEO) 專為 Web Application。涵蓋 Schema.org 結構化資料（Organization/Product/FAQ/WebSite）、SEO 元件強化、JSON-LD 注入、robots.txt + sitemap。設計不可見為原則，可視區塊需使用者明確要求。
metadata:
  author: community
  maturity: stable
  tags: GEO, SEO, structured-data, JSON-LD, schema-org
---

# Web App GEO 優化（custom）

## Use

當使用者要求對一個 Web 應用（非文章/內容）做 GEO/AI 搜尋友好化優化時觸發。包括 C2C 平台、電商、工具型網站等。

**不適用**：純內容網站/部落格（用 `geo-article-friendly`）、從零寫作。

## Critical Rule — Design Preservation

**NEVER add visible UI sections, content blocks, or design elements to existing pages unless the user explicitly requests visible changes.** GEO optimization for web apps should be invisible by default:

✅ JSON-LD structured data (WebSite, Organization, Product, FAQPage)
✅ Meta tag / OG tag / Twitter card enhancement
✅ robots.txt + sitemap.xml
✅ Per-page meta title/description via SEO component

❌ "How it works" sections on home page — only add if user asks
❌ FAQ visible sections — only add if user asks
❌ Any visible content block inserted into an existing page layout

The user's existing UI design is a hard boundary. GEO improvements that require visibility (FAQ sections, content blocks) must be explicitly requested or offered as a separate phase with clear warning that it changes the page design.

## Required Reading

執行前載入：
- `skill_view(name='geo-article-friendly', file_path='references/geo-article-transformation-method.md')` — 了解 GEO 原理與權重邏輯
- `skill_view(name='webapp-geo-optimization', file_path='references/your-marketplace-implementation.md')` — Camera Market 實戰參考（完整實作 pattern）

## Reference Map

- `references/your-marketplace-implementation.md` — Camera Market 實戰記錄：完整的 6 項 GEO 改動（index.html schema 追加、SEO 元件強化、Product JSON-LD 注入、FAQPage JSON-LD、robots.txt + sitemap.xml），含可復用的 code pattern
- `scripts/generate-og-image.py` — 可重複使用的 OG image 產生腳本（Pillow），自訂品牌色、文字、圖示
- 重要教訓：可視內容區塊（FAQ、How-It-Works）被退回，GEO 改動應優先不可見

## Workflow

### Phase 0：盤點現狀

**0a. 確認參考版本** — 在改動之前，先確認使用者期望的目標版本：
- 是 local HEAD？生產部署？Vercel/GitHub Pages preview？
- 檢查 Vercel URL、production domain，用 `git log --oneline` 比對差異
- 如果有部署版存在，且使用者說「版本不對」，那就是你該切過去的版本
- **不要假設 local HEAD 就是目標版本** — 使用者可能用 preview deployment 當 reference

**0b. Passkey/port 相容性檢查** — 如果專案有 WebAuthn/Passkey 功能：
- 確認後端 `config.py` 的 `webauthn_origin` 與前端 dev port 一致
- 常見不匹配：後端設 `localhost:5173` 但前端跑在 `54349`
- 不一致的話 passkey 會直接失敗，修正方式：前端改跑正確 port 或更新 config

**0c. 既有結構化資料盤點**：

- [ ] index.html 有基礎 meta tags（title, description, OG, Twitter）
- [ ] 已有 SEO 元件（動態管理 per-page meta）
- [ ] WebSite JSON-LD（含 SearchAction）
- [ ] Organization JSON-LD
- [ ] Product JSON-LD（商品/產品頁）
- [ ] FAQPage JSON-LD
- [ ] 首頁有自然語言內容（How it works, 平台介紹）
- [ ] robots.txt
- [ ] sitemap.xml
- [ ] llms.txt（GEO 標準，AI crawler 直接讀取）
- [ ] OG image 是真實圖片（非 SVG icon，1200×630 PNG）

### Phase 1：SEO 元件強化

若專案有共用 SEO 元件（如 `SEO.tsx`），強化以下：

1. 新增 `jsonLd?: Record<string, unknown>` prop → useEffect 注入 `<script type="application/ld+json">`
2. 新增 `og:image:width` / `og:image:height`（1200×630 標準）
3. `twitter:card` 升級為 `summary_large_image`
4. 加 `twitter:image`
5. 確保每次 rerender 正確更新/清理 JSON-LD script（useId + cleanup）

### Phase 2：index.html 結構化資料

**WebSite schema**（強化）：
```json
{
  "@type": "WebSite",
  "name": "站名",
  "url": "https://domain.tw",
  "description": "描述",
  "inLanguage": "zh-TW",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://domain.tw/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

**Organization schema**（新增）：
```json
{
  "@type": "Organization",
  "name": "站名",
  "alternateName": "English Name",
  "url": "https://domain.tw",
  "logo": "https://domain.tw/logo.png",
  "description": "描述",
  "areaServed": "Taiwan",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "availableLanguage": ["zh-Hant", "en"]
  }
}
```

### Phase 2.5：OG Image 生成

若專案的 OG image 是 SVG icon（社群分享效果差），產生真實 1200×630 PNG：

```bash
python3 scripts/generate-og-image.py \
    --name "站名" \
    --subtitle "English Name" \
    --desc "一句話描述" \
    --accent "#EA3B4D" \
    --output public/og-image.png
```

腳本路徑：`scripts/generate-og-image.py` — 自訂品牌色、背景色、是否顯示相機圖示。

### Phase 3：商品/產品頁 Product JSON-LD

動態生成（從 API 資料），每個商品頁注入：

```json
{
  "@type": "Product",
  "name": "品牌 型號",
  "brand": { "@type": "Brand", "name": "品牌" },
  "model": "型號",
  "description": "描述（截斷 300 字）",
  "image": "主圖 URL",
  "category": "分類中文名",
  "sku": "商品 UUID",
  "offers": {
    "@type": "Offer",
    "price": 價格,
    "priceCurrency": "TWD",
    "availability": "InStock / SoldOut",
    "itemCondition": "Schema.org condition URL",
    "url": "商品頁 URL"
  }
}
```

需要對應的 condition → Schema.org 對照表：
- new → NewCondition
- like_new → RefurbishedCondition  
- excellent → ExcellentCondition
- good → GoodCondition
- used → UsedCondition
- broken → DamagedCondition

### Phase 4：FAQPage JSON-LD（不可見，預設執行）

注入 **不可見的 FAQPage JSON-LD** 到首頁或其他合適頁面。5 題左右，覆蓋：
- 這是什麼平台？
- 怎麼使用？（購買流程）
- 需要費用嗎？
- 支援哪些分類？
- 安全嗎？

**實作方式**：在頁面元件中定義 `faqJsonLd` 常數，透過 `<SEO jsonLd={faqJsonLd} />` 注入到 `<head>`。不修改頁面視覺內容。

```tsx
const faqJsonLd = {
  '@type': 'FAQPage',
  mainEntity: [
    { '@type': 'Question', name: '...', acceptedAnswer: { '@type': 'Answer', text: '...' } },
    // ...
  ],
}

// In render:
<SEO jsonLd={faqJsonLd} />
```

### Phase 4b：可視內容區塊（僅限使用者要求）

⚠️ **跳過此階段，除非使用者明確要求可見的內容改動。** 預設不加入任何可見的 FAQ 或 How-It-Works 區塊。

如果使用者要求了，建議位置在頁面底部（CTA/Stats 之後），使用既有設計語彙（`bg-surface-card`、`text-text-muted`、既有間距規格）。

### Phase 5：robots.txt + sitemap.xml + llms.txt

**robots.txt**（`/public/robots.txt`）：
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /messages/
Disallow: /account/

Sitemap: https://domain.tw/sitemap.xml
```

**sitemap.xml**（`/public/sitemap.xml`）：
```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://domain.tw/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
  ...
</urlset>
```

涵蓋所有靜態頁面。動態頁面（商品詳情）建議後端產生完整 sitemap。

**llms.txt**（`/public/llms.txt`）— GEO 標準：讓 AI crawler 直接讀取平台摘要、關鍵頁面連結：

```markdown
# 站名 — English Name
> 一句話描述

## About
平台介紹（2-3 句）

## Key features
- 功能清單

## Pages
- Home: https://domain.tw/
- Explore: https://domain.tw/explore
...

## Relevant links
- Privacy: https://domain.tw/privacy
- Terms: https://domain.tw/terms
```

遵循 [llmstxt.org](https://llmstxt.org) 規範。AI crawler（GPTBot, ChatGPT-User, Google-Extended）在訪問根目錄時自動尋找此檔案。

## 驗證清單

- [ ] TypeScript 編譯 0 errors（`npx tsc --noEmit`）
- [ ] 前端測試通過（`npx vitest run`）
- [ ] SEO 元件 jsonLd prop 正常注入/更新/清理
- [ ] 動態 Product JSON-LD 在每個商品頁正確生成
- [ ] FAQPage JSON-LD 與可視 FAQ 內容一致
- [ ] robots.txt 可訪問
- [ ] sitemap.xml 格式正確
- [ ] llms.txt 存在且格式正確
- [ ] OG image 為 1200×630 真實 PNG/JPEG
- [ ] 改造後建議 run `stop-slop` 確保無 AI 味（文章類內容）

## Hard Rule (the user)

**GEO 改動不得修改頁面視覺設計。** 只允許：
- `index.html` — 加 JSON-LD script blocks、強化 meta tags
- `SEO.tsx` / 共用 SEO 元件 — 加 `jsonLd` prop、強化 OG/Twitter tags（元件 render null，不影響視覺）
- 商品詳情頁 — 加 Product JSON-LD（透過 SEO 元件 inject，不可見）
- 首頁 — 可加 FAQPage JSON-LD data constant + `<SEO jsonLd={...} />`（不可見）
- `robots.txt` + `sitemap.xml` — 新檔案，不影響 UI

**禁止**：在頁面 JSX 中加任何可視區塊（How it works、FAQ 卡片、說明段落、aria-label section）。GEO 內容只以 structured data 形式存在，不可見於頁面上。

## Pitfalls

- **JSON-LD 不清理 bug**：React 元件 unmount 時必須清理 inject 的 script tag，否則頁面切換會累積多個 schema
- **Product JSON-LD description 長度**：`description` 建議截斷 200-300 字，過長會被 AI 搜尋引擎忽略或引發解析異常。直接取 `item.description?.slice(0, 300)` 即可。
- **OG image 要是真實圖片**：SVG icon 在 AI 搜尋引擎的分享卡中效果極差，優先產生 1200×630 PNG/JPEG
- **Server-side sitemap**：靜態 sitemap 只涵蓋主要頁面，大量動態頁面須後端產生
- **GEO ≠ keyword stuffing**：不做關鍵詞堆砌，圍繞真實使用者問題組織內容
- **SPA limitation**：純前端 SPA 的 meta tags 靠 JS 動態注入，不是所有 crawler 都執行 JS。pre-rendering / SSR 是進階解法
- **Visible sections are opt-in**：首次執行時絕對不要加可見內容區塊。使用者的 UI 是硬邊界。將 GEO 改為可視內容（FAQ 區塊、How-It-Works 步驟）會直接被退回。慣例：先做不可見的 JSON-LD，可視改動永遠當成獨立選項而非預設執行
- **Deployment awareness**：改動前先確認 production/deployed 版本的狀態。使用者可能用 Vercel preview deployment 版本當成 reference（例如 `frontend-sepia-seven-66.vercel.app`），local HEAD 可能跟那個版本完全不同。改動內容與部署版不一致時，使用者會要求整包 revert 而不是 patch
- **Passkey port matching**：如果專案有 WebAuthn/Passkey，後端 `config.py` 的 `webauthn_origin` 決定了前端必須跑哪個 port。開發時先用 `grep webauthn_origin backend/app/config.py` 確認，不一致就直接用正確 port 啟動前端
- **npm install after branch switch**：不同 branch 可能有不同依賴（例如 `vite-plugin-compression`）。切 branch 後如果 `npx vite` 報 `ERR_MODULE_NOT_FOUND`，先跑 `npm install`，不要假設 node_modules 相容
