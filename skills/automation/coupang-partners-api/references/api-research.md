# Coupang Partners Taiwan API — Research Notes

## Gateway Discovery

Initial attempts with `api-gateway.coupang.com` (Korean default) returned:
`{"code":"ERROR","message":"The HMAC token is not for the target VDC."}`

The Taiwan-specific gateway `api-gateway.tw.coupang.com` resolved this — HMAC auth succeeded.

## Request Format Testing

### Auth Header Format

Both formats work identically:
- WITH spaces: `CEA algorithm=HmacSHA256, access-key=..., signed-date=..., signature=...`
- WITHOUT spaces: `CEA algorithm=HmacSHA256,access-key=...,signed-date=...,signature=...`

The with-spaces format is documented in the Korean Partners API blog.

### X-MARKET Header

For the OPEN API (seller), Taiwan requests require `X-MARKET: TW` header.
For the Partners API (affiliate), testing showed this header has no effect on the VDC routing — the gateway must match the key's region.

## Deeplink Behavior

| URL Tested | Result |
|-----------|--------|
| `tw.coupang.com/vp/products/{id}` | `rCode":"400"` — url convert failed |
| `tw.coupang.com/vp/products/{id}?itemId=&vendorItemId=...` | `rCode":"400"` — url convert failed |
| `tw.coupang.com/np/search?...` | `rCode":"400"` — url convert failed |
| `tw.coupang.com/` (homepage) | ✅ success — returned `coupa.ng/xxxxx` |

The deeplink API on the Taiwan gateway appears to have limited URL format support for products. Use the search API's built-in `productUrl` instead for individual product affiliate links.

## Search API Response Detail

Full product data fields observed:
- `productId` — numeric ID (15 digits)
- `productName` — full product name
- `productPrice` — price in TWD (integer or float)
- `productImage` — encrypted URL from `ads-partners.tw.coupang.com` (usable directly)
- `productUrl` — complete affiliate link via `coupang.onelink.me` with all tracking params
- `categoryName` — category path string (e.g. "食品", "消費者電子產品/數位產品")
- `isRocket` — boolean for Rocket Delivery eligibility
- `firstPurchasePrice` — first-purchase discount price (may be null)

The `productUrl` contains:
- `pid=coupang_partners` (platform ID)
- `c=AF9547888` (affiliate ID in `lptag` param)
- Full tracking: `traceid`, `requestId`, `ctime`, `sig`

## Affiliate Link Domains

- `link.tw.coupang.com` — Taiwan SEO landing pages (used in search `landingUrl`)
- `coupa.ng` — shortened URLs (used by deeplink API)
- `coupang.onelink.me` — mobile app deep links with tracking (used in search `productUrl`)

## Credential Storage

Keys should be stored in `.env`:
```
COUPANG_ACCESS_KEY=...
COUPANG_SECRET_KEY=...
```
Loaded via `python-dotenv` at runtime. Do NOT hardcode in scripts.

## Code Structure

Minimal `coupang_api.py`:

```python
import hmac, hashlib, requests
from datetime import datetime, timezone
from urllib.parse import quote

GATEWAY = "https://api-gateway.tw.coupang.com"

def _auth(method, uri, access_key, secret_key) -> str: ...

def search(keyword: str, limit: int = 10) -> list[dict]: ...

def deeplink(coupang_url: str) -> str | None: ...
```
