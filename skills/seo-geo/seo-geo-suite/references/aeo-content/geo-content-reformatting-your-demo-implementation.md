# your-demo — GEO 實戰記錄

交通違規檢舉工具（SPA），單頁 utility web app。Vercel static deploy。

## 專案特性

- 純靜態 SPA（無 SSR/SSG），單一頁面 `index.html`
- 工具型應用（非內容站、非電商）
- 使用者輸入地址 + 違規事實 → 產生簡訊內容
- 無後端、無資料庫、無動態路由

## 實作的 GEO 技術

### 1. Visible heading reformatting（geo-content-reformatting 首次實戰）

將既有 H3 從名詞片語改為問題句式，不新增 DOM 元素：

- `簡訊內容格式` → `檢舉簡訊需要填寫哪些內容？`
- `違規停車` → `哪些違規行為可以用簡訊檢舉？`

段落首句同步調整為直接回答該問題。

### 2. `@graph` JSON-LD with WebApplication

使用 Schema.org `@graph` 容器合併 WebSite + WebApplication：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://your-demo.vercel.app/#website",
      "url": "https://your-demo.vercel.app/",
      "name": "交通違規檢舉工具 — 簡訊報案",
      "inLanguage": "zh-TW",
      "applicationCategory": "Utility"
    },
    {
      "@type": "WebApplication",
      "@id": "https://your-demo.vercel.app/#webapp",
      "url": "https://your-demo.vercel.app/",
      "name": "交通違規檢舉工具 — 簡訊報案",
      "operatingSystem": "Web",
      "applicationCategory": "UtilityApplication",
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "TWD" }
    }
  ]
}
```

### 3. Meta tags 強化

- `description` 擴充涵蓋關鍵字：違規停車、紅線停車、並排停車、22縣市警察局簡訊電話
- OG/Twitter tags：`og:type=website`, `og:locale=zh_TW`, `twitter:card=summary`
- hreflang：`zh-TW` + `x-default`
- Canonical URL
- Favicon：SVG data URI（藍色驚嘆號）

### 4. 爬蟲檔案

- `robots.txt`：僅 `Allow: /` + Sitemap，移除非標準的 `Allow: /$`
- `sitemap.xml`：單一 URL（`/`），lastmod 設為部署日
- `llms.txt`：llmstxt.org 格式，列出功能摘要與 URL

## 注意點

- Vercel static deploy 需確認 `vercel.json` 不會阻擋 `/llms.txt`、`/robots.txt`、`/sitemap.xml`
- 單頁 SPA 不作 `changefreq`/`priority` 也可接受，sitemap 主要功能是讓 crawler 知道頁面存在
