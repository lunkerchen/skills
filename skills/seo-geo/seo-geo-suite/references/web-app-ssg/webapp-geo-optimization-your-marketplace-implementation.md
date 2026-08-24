# Camera Market — GEO 實戰記錄

React + Vite SPA, FastAPI backend, C2C 二手攝影器材平台。

## 版本上下文

- 目標版本：`main` branch（Passkey 功能版）
- 前端 port：5173（後端 config.py 的 `webauthn_origin` 綁定此 port）
- 部署版：frontend-sepia-seven-66.vercel.app（同一份 code）
- 教訓：第一次執行時在 `fix/auto-20260627-1942` branch 上做，與生產版不一致，整包 revert

## 實作項目與 code pattern

### 1. index.html — Organization + WebSite schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "your-marketplace",
  "url": "https://your-marketplace.example.com",
  "description": "台灣最專門的二手相機、鏡頭、攝影配件 C2C 交易平台",
  "inLanguage": "zh-TW",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://your-marketplace.example.com/explore?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "your-marketplace",
  "alternateName": "Camera Market",
  "url": "https://your-marketplace.example.com",
  "logo": "https://your-marketplace.example.com/icons/icon-512.svg",
  "description": "描述文字",
  "areaServed": "Taiwan",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "availableLanguage": ["zh-Hant", "en"]
  }
}
</script>
```

### 2. SEO.tsx — jsonLd prop + OG 強化

```tsx
import { useEffect, useId } from 'react'

interface SEOProps {
  title?: string
  description?: string
  image?: string
  url?: string
  type?: string
  /** Optional JSON-LD structured data — injected as <script type="application/ld+json"> */
  jsonLd?: Record<string, unknown>
}

const SITE_NAME = 'your-marketplace'
const DEFAULT_DESC = '台灣最專門的二手相機、鏡頭、攝影配件 C2C 交易平台'
const DEFAULT_IMAGE = '/icons/icon-512.svg'  // 使用 512×512 取代 192
const OG_IMAGE_W = 1200
const OG_IMAGE_H = 630

// 在 useEffect 中：
setMeta('property', 'og:image:width', String(OG_IMAGE_W))
setMeta('property', 'og:image:height', String(OG_IMAGE_H))
setMeta('name', 'twitter:card', 'summary_large_image')  // 取代 summary
setMeta('name', 'twitter:image', image)                   // 新增

// JSON-LD injection:
if (jsonLd) {
  const data = { '@context': 'https://schema.org', ...jsonLd }
  let script = document.getElementById(jsonId) as HTMLScriptElement | null
  if (!script) {
    script = document.createElement('script')
    script.id = jsonId
    script.type = 'application/ld+json'
    document.head.appendChild(script)
  }
  script.textContent = JSON.stringify(data)
}
```

### 3. Home.tsx — FAQPage JSON-LD (invisible only)

```tsx
import SEO from '../components/SEO'

const faqJsonLd = {
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'your-marketplace是什麼？',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'your-marketplace（Camera Market）是台灣最專門的二手攝影器材 C2C 交易平台...',
      },
    },
    // 3-5 questions total
  ],
}

// In render:
<SEO jsonLd={faqJsonLd} />
```

Key: no visual FAQ section, no "How it works" section. Only head-injected JSON-LD.

### 4. ListingDetail.tsx — Product JSON-LD

```tsx
import SEO from '../components/SEO'

// Constants for condition → Schema.org mapping
const schemaConditions: Record<string, string> = {
  new: 'https://schema.org/NewCondition',
  like_new: 'https://schema.org/RefurbishedCondition',
  excellent: 'https://schema.org/ExcellentCondition',
  good: 'https://schema.org/GoodCondition',
  used: 'https://schema.org/UsedCondition',
  broken: 'https://schema.org/DamagedCondition',
}

const categoryLabels: Record<string, string> = {
  camera: '相機機身', lens: '鏡頭', accessory: '配件',
  film: '底片相機', drone: '空拍機', lighting: '燈光設備',
}

// After item is loaded:
const mainImage = images[0]?.url || ''
const schemaCondition = schemaConditions[item.condition] || 'https://schema.org/UsedCondition'
const categoryLabel = categoryLabels[item.category || ''] || item.category || '攝影器材'
const productJsonLd = {
  '@type': 'Product',
  name: `${item.brand} ${item.model}`,
  brand: { '@type': 'Brand', name: item.brand },
  model: item.model,
  image: mainImage || 'https://your-marketplace.example.com/icons/icon-512.svg',
  category: categoryLabel,
  sku: item.id,
  offers: {
    '@type': 'Offer',
    price: item.price,
    priceCurrency: 'TWD',
    availability: item.status === 'sold' ? 'https://schema.org/SoldOut' : 'https://schema.org/InStock',
    itemCondition: schemaCondition,
    url: `https://your-marketplace.example.com/listings/${item.id}`,
  },
}

// In render:
<SEO
  title={`${item.brand} ${item.model} — ${categoryLabel}`}
  description={`${item.brand} ${item.model} · ${conditionLabels[item.condition]} · NT$ ${item.price.toLocaleString()} · your-marketplace`}
  image={mainImage || undefined}
  url={`https://your-marketplace.example.com/listings/${item.id}`}
  jsonLd={productJsonLd}
/>
```

### 5. robots.txt / sitemap.xml

Standard boilerplate (see SKILL.md Phase 5).

## 關鍵教訓

1. **絕對不動畫面** — 使用者明確拒絕了可視的「如何交易」「常見問題」區塊。改動集中在 `<head>` 和靜態檔案
2. **Branch 一致性** — 第一次在錯的 branch 上做，整包 revert。第二次先在 `main` branch 確認再動手
3. **Passkey port** — `webauthn_origin` 在 `backend/app/config.py` 第 70 行，綁定 `http://localhost:5173`。前端 dev server 必須跑這個 port，不然 passkey 登入會失敗
4. **npm install** — 切 branch 後若依賴不同，`npx vite` 會報 `ERR_MODULE_NOT_FOUND`，先跑 `npm install`
