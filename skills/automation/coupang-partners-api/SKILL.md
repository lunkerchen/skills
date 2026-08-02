---
name: coupang-partners-api
description: 酷澎台灣分潤（Coupang Partners Taiwan API）整合 — HMAC 簽章、商品搜尋、分類/特價/PL 商品、deeplink 轉換、分潤報表（點擊/訂單/收益/取消/廣告）、自動選品 pipeline。覆蓋 partners.tw.coupang.com 的 API 使用模式。
version: 1.1.0
---

# 酷澎台灣分潤 API 整合 (Coupang Partners Taiwan API)

## When to Use

- User asks about 酷澎分潤、Coupang Partners Taiwan、coupa.ng
- User wants to build automated product selection + affiliate link generation for Coupang Taiwan
- User has Coupang Partners API keys (Access Key + Secret Key) from `partners.tw.coupang.com`
- User wants programmatic access to Coupang Taiwan product search as an affiliate

## Quick Reference

| Item | Value |
|------|-------|
| Partners Portal | `https://partners.tw.coupang.com` |
| API Gateway (Taiwan) | `https://api-gateway.tw.coupang.com` |
| Base URL (official) | `https://api-gateway.tw.coupang.com/v2/providers/affiliate_open_api/apis/openapi/v1/` |
| API Gateway (Korea) | `https://api-gateway.coupang.com` |
| Auth | HMAC-SHA256, CEA format |
| SEO landing domain | `link.tw.coupang.com` |
| Short link domain | `coupa.ng` |
| API key issuance | Partners Portal → Tools → 合作夥伴 API |
| Search rate limit | 50 calls/min |
| Reports rate limit | 500 calls/hour (all endpoints) |
| Reports data refresh | Daily 12:00 PM (previous day's data) |
| Goldbox data refresh | Daily 7:30 AM |

## API Endpoints

Base URL: `https://api-gateway.tw.coupang.com/v2/providers/affiliate_open_api/apis/openapi/v1/`

**Note on URL paths:** The official docs use path segments relative to the base URL above (e.g. `/products/search`). The codebase's `coupang_api.py` historically uses the full path `/v2/providers/affiliate_open_api/apis/openapi/products/search` without the `/v1/` — both resolve successfully.

### Product Endpoints

#### Search

```
GET /products/search?keyword={keyword}&limit={n}
```

Searches Coupang Taiwan products by keyword, returns results with ready-to-use affiliate links. **Rate limit:** 50 calls/minute.

**Response structure:**
```json
{
  "rCode": "0",
  "rMessage": "在撰寫文章時，您必須聲明「我可能會從合作夥伴的活動中收取佣金」。",
  "data": {
    "landingUrl": "https://link.tw.coupang.com/gl/tw/AFFSRP?...",
    "productData": [
      {
        "productId": 265257129820171,
        "productName": "GEORGIA 喬亞 滴濾無糖黑咖啡",
        "productPrice": 499,
        "productImage": "https://ads-partners.tw.coupang.com/image1/...",
        "productUrl": "https://coupang.onelink.me/yowQ?pid=coupang_partners&c=AF...",
        "categoryName": "食品",
        "isRocket": true,
        "firstPurchasePrice": 299
      }
    ]
  }
}
```

**Key fields:**
- `productUrl` — **already an affiliate link** (onelink.me with tracking params), ready to use directly
- `productImage` — encrypted image URL from ads-partners subdomain; usable as-is
- `isRocket` — Rocket Delivery eligibility
- `productPrice` — current price in TWD
- `firstPurchasePrice` — first-purchase discount price (may be lower)

#### Best Categories

```
GET /products/bestcategories/{categoryId}
```

Returns best-selling products within a specific category.

#### Goldbox (Daily Deals)

```
GET /products/goldbox
```

Returns daily deal/sale products. **Data refreshes daily at 7:30 AM.**

#### Coupang PL (Private Label)

```
GET /products/coupangPL
GET /products/coupangPL/{brandId}
```

Returns Coupang's own brand products. Optionally filtered by brand ID.

### Reports Endpoints

**Rate limit:** 500 calls/hour across all reports endpoints.
**Data refresh:** Daily at 12:00 PM (noon). Data from the previous day becomes available.

Each endpoint takes optional query parameters for date range filtering (format based on Korean API conventions — likely `startDate`/`endDate` in `yyyy-MM-dd`).

#### Commission

```
GET /reports/commission
```

Returns daily commission/earnings data.

#### Clicks

```
GET /reports/clicks
```

Returns daily click-through data from your affiliate links.

#### Orders

```
GET /reports/orders
```

Returns daily order data attributed to your affiliate links.

#### Cancels

```
GET /reports/cancels
```

Returns daily cancellation/refund data.

#### Ads Reports

```
GET /reports/ads/impression-click    — Ad requests, responses, impressions, clicks
GET /reports/ads/orders              — Ad-attributed orders
GET /reports/ads/cancels             — Ad-attributed cancellations
GET /reports/ads/performance         — Daily eCPM
GET /reports/ads/commission          — Ad revenue
```

These cover category banners and dynamic banner ad performance.

### Deeplink

Converts Coupang URLs to affiliate short links (coupa.ng).

```
POST /deeplink
Body: {"coupangUrls": ["https://www.tw.coupang.com/..."]}
```

**Note:** The Taiwan deeplink endpoint currently only successfully converts some URL formats. The search API's built-in `productUrl` is more reliable for individual product affiliate links.

## HMAC Authentication

### Signature Generation

```
datetime = UTC in yyMMdd'T'HHmmss'Z' format
message = datetime + HTTP_METHOD + path [+ query_string]
signature = HmacSHA256(message, secret_key).hexdigest()
Authorization: CEA algorithm=HmacSHA256, access-key={ACCESS_KEY}, signed-date={datetime}, signature={signature}
```

### Python Implementation

```python
import hmac, hashlib
from datetime import datetime, timezone

def make_auth(method: str, uri: str, access_key: str, secret_key: str) -> str:
    parts = uri.split("?")
    path, query = parts[0], (parts[1] if len(parts) > 1 else "")
    dt = datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")
    msg = dt + method + path + query
    sig = hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return (f"CEA algorithm=HmacSHA256, access-key={access_key}, "
            f"signed-date={dt}, signature={sig}")
```

### Important Notes

- **Auth header format uses spaces after commas:** `CEA algorithm=HmacSHA256, access-key=...` (with spaces)
- **Signature expires in ~5 minutes** — regenerate for each request
- **Gateway is region-specific:**
  - Taiwan keys ➔ `api-gateway.tw.coupang.com` (key: `TW`)
  - Korea keys ➔ `api-gateway.coupang.com`
  - Wrong gateway returns `"The HMAC token is not for the target VDC."`

## Automated Pipeline Architecture

### Project Layout

```bash
$DEV_PROJECTS/your-affiliate-bot/
├── .env                        # COUPANG_ACCESS_KEY + COUPANG_SECRET_KEY
├── coupang_api.py              # Core: HMAC auth + search + deeplink (stdlib, no dotenv)
├── pipeline.py                 # Pipeline: search → filter → score → output JSON
├── cron_daily.py               # Cron entry point
├── build_board.py              # HTML product board builder
├── board.html                  # Board template
├── history.json                # Dedup: productIds already promoted
└── output_YYYY-MM-DD.json      # Daily recommendations (JSON for LLM cron)
```

### Pipeline Flow

```
cron trigger
  → search(keyword) for each keyword in SEARCH_QUERIES
  → dedup by productId (against history.json)
  → score products (rocket + name quality + price range)
  → pick top N (default 3)
  → generate platform-specific content via content_gen.py (Threads/IG/Twitter)
  → save output JSON + update history
```

### Cron Setup

**LIVE daily run** (job_id `YOUR_CRON_JOB_ID`, confirmed running daily 9AM):

```yaml
cronjob:
  action: create
  schedule: "0 9 * * *"
  name: coupang-daily-pick
  prompt: "Run $DEV_PROJECTS/your-affiliate-bot/pipeline.py, read the output JSON, then write storytelling-style social posts for each product — natural conversational tone, no emoji/hashtags/formatting, from a life-scene hook per product."
  no_agent: false
  deliver: origin
  enabled_toolsets: ["terminal", "file"]
```

This is the preferred setup: `no_agent=False` (LLM writes unique copy per product, Mode A above). The agent reads `output_$(date +%Y-%m-%d).json`, runs `build_board.py` for the HTML product board, and writes `posts_$(date +%Y-%m-%d).md`.

**Alternative: no_agent script mode** (faster, template-based Mode B):

```yaml
cronjob:
  action: create
  schedule: "0 9 * * *"
  name: coupang-daily-picks
  script: $DEV_PROJECTS/your-affiliate-bot/cron_daily.py
  no_agent: true
  deliver: origin
```

### Search Keywords (default 10)

```
咖啡, 泡麵, 零食,
尿布, 濕紙巾, 充電線, 行動電源, 寵物飼料
```

### Scoring Formula (simple)

```
score = (20 if isRocket else 0) + min(10, len(name)//5) + (10 if 50 ≤ price ≤ 2000 else 0)
```

### Content Generation — LLM Storytelling Mode

User preference: *data dumps 會被直接拒絕。* Pipeline 只負責輸出 JSON（商品資料）。文案由 cron LLM 從 JSON 讀取後撰寫，不走樣板。

- `content_gen.py` 已移除（死程式碼，格式與核准語氣相反）

**Approved tone (confirmed 2026-06-15):**
- 像在跟朋友閒聊時提到「對了我前幾天買了這個…」
- 從一個生活場景或小困擾切入 — 什麼情境下發現需要這個東西
- 可以自言自語、可以有語氣詞（欸、其實、結果、原本想說…）
- 全文就是一段話，不分點、不用列表、不用 emoji 裝飾
- 不用下結論、不用鼓吹別人買
- 結尾簡單帶一句「這裡」加連結就好
- 不要 hashtag

**Example output (live 2026-06-15):**
```
昨天發現老媽那條 iPhone 充電線又破皮了，接头那邊黑色橡膠都裂開看得見裡面的線。
本來想說叫她去夜市買一條就好，但又覺得那種用沒兩個月就一樣爛。
就在酷澎滑了一下看到這條 POLYWELL 編織線，想說才 86 塊，比一杯手搖還便宜，
試試看也不會痛。結果今天到貨摸了一下，編織材質確實比原廠那種橡膠紮實很多，
插上去也有順利跳出充電，沒什麼好嫌的。

這裡
https://...
```

## Pitfalls

- **Reports API exists — don't assume only search/deeplink are available.** The Taiwan portal documents a full reports suite: commission, clicks, orders, cancels, and 5 ad-reporting endpoints. Always check the Document tab at `partners.tw.coupang.com/#help/open-api` for the latest list.
- **Rate limits differ by endpoint type:** search is 50 calls/minute, reports are 500 calls/hour across all report endpoints.
- **Reports data refreshes at 12:00 PM daily.** Data from day N becomes available at noon on day N+1. Goldbox refreshes at 7:30 AM.
- **Taiwan vs Korea gateway is critical.** The default `api-gateway.coupang.com` returns 403 "not for the target VDC" for Taiwan-issued keys. Always use `api-gateway.tw.coupang.com` for Taiwan.
- **Deeplink may fail for individual product URLs** on Taiwan gateway. The search API's `productUrl` field is more reliable and already contains affiliate tracking parameters.
- **API key issued only to final-approved Partners members.** If not yet approved, the Tools → 合作夥伴 API menu won't show the key generation button. Contact partner support.
- **Search API limit:** max 10 products per request (observed server-side cap).
- **Product price is current price** (may not reflect discounts). `firstPurchasePrice` is the promo price for first-time buyers.
- **No product description or specs** returned by search API — only name, price, image, category, rocket badge.
- **API key expiry:** OPEN API keys expire every 180 days. Partners API keys may have different validity — monitor if calls start failing.
- **Affiliate disclosure required:** The API response `rMessage` contains the required disclosure text: "在撰寫文章時，您必須聲明「我可能會從合作夥伴的活動中收取佣金」。"
- **Content must be engaging, not a data dump.** User explicitly rejected "好物推薦｜名稱💰$價格👇連結" format. Every post needs a hook (pain point / scenario / curiosity), benefit-driven body, and a closer with CTA. See Content Generation section for the approved template.

## References

- `references/daily-pipeline-setup.md` — live running config (pipeline.py, cron job_id, HMAC creds, selection algorithm)
- `references/api-research.md` — initial API research findings (gateway discovery, auth testing)
- `references/portal-api-docs.md` — full API endpoint catalog from the Taiwan Partners portal Document tab
- `$DEV_PROJECTS/your-affiliate-bot/` — full working project
- `coupang_api.py` — core API wrapper with HMAC auth
- `pipeline.py` — product selection and content generation pipeline
- Korean Partners API blog: https://coupang-partners.tistory.com/
- Taiwan Partners portal: https://partners.tw.coupang.com
