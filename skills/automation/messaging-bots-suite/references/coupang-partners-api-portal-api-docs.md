# Taiwan Partners Portal — API Documentation (2026-07-20)

Source: `partners.tw.coupang.com/#help/open-api` → Document tab

## Base URL

```
https://api-gateway.tw.coupang.com/v2/providers/affiliate_open_api/apis/openapi/v1/
```

All endpoints below are relative to this base URL.

## Products

### Search
- **Endpoint:** `GET /products/search?keyword={keyword}&limit={n}`
- **Rate limit:** 50 calls/minute
- Returns product data with affiliate-ready `productUrl`

### Best Categories
- **Endpoint:** `GET /products/bestcategories/{categoryId}`
- Returns best-selling products in a given category

### Goldbox (Daily Deals)
- **Endpoint:** `GET /products/goldbox`
- **Refresh:** Daily 7:30 AM
- Returns daily deal/sale products

### Coupang PL (Private Label)
- **Endpoint:** `GET /products/coupangPL`
- **Endpoint:** `GET /products/coupangPL/{brandId}`
- Returns Coupang own-brand products

## Reports

**Rate limit:** 500 calls/hour across all report endpoints.
**Data refresh:** Daily at 12:00 PM (previous day's data becomes available).

| Endpoint | Description |
|----------|-------------|
| `GET /reports/commission` | Daily commission/earnings |
| `GET /reports/clicks` | Daily click-through data |
| `GET /reports/orders` | Daily order data |
| `GET /reports/cancels` | Daily cancellation/refund data |
| `GET /reports/ads/impression-click` | Ad requests, responses, impressions, clicks |
| `GET /reports/ads/orders` | Ad-attributed orders |
| `GET /reports/ads/cancels` | Ad-attributed cancellations |
| `GET /reports/ads/performance` | Daily eCPM |
| `GET /reports/ads/commission` | Ad revenue |

All reports are GET requests. Date range query parameters not documented in the Taiwan UI but follow Korean API conventions.

## Links

### Deeplink
- **Endpoint:** `POST /deeplink`
- **Body:** `{"coupangUrls": ["https://www.tw.coupang.com/..."]}`
- Converts Coupang URLs to `coupa.ng` affiliate short links

## Key Observations

1. The `/v1/` suffix in the base URL is present in the official docs but the existing `coupang_api.py` uses the full path without `/v1/` — both resolve successfully.
2. The Document tab is organized into three collapsible sections: `products`, `reports`, `links`.
3. The Guide tab covers HMAC auth setup with code examples in Java, Python, PHP, C#, Node.js.
4. There's a separate **Reco API** tab and an **FAQ** tab that were not explored.
