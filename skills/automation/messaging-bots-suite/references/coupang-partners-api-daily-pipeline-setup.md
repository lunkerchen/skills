# Coupang Daily Pipeline — Live Configuration (2026-06-15)

## Project Layout

```
$DEV_PROJECTS/your-affiliate-bot/
├── .env                        # COUPANG_ACCESS_KEY + COUPANG_SECRET_KEY
├── coupang_api.py              # HMAC auth + search + deeplink
├── pipeline.py                 # Search → dedup → score → output
├── build_board.py              # JSON → HTML product board
├── history.json                # Dedup: productIds already promoted
├── board_dist.html             # Generated HTML product board
├── posts_YYYY-MM-DD.md         # Daily LLM-written posts
└── output_YYYY-MM-DD.json      # Daily pipeline output
```

## Cron (LIVE)

- **job_id:** `f0366df97500`
- **Schedule:** `0 9 * * *` (daily 9AM)
- **Mode:** `no_agent=False` (LLM agent)
- **Pipeline:** `pipeline.py` → read output JSON → write storytelling posts → save to `posts_YYYY-MM-DD.md`
- **Also runs:** `build_board.py` for HTML board
- **Profile:** default

## HMAC Credentials

- **Access Key:** `04f3d629-f6ac-4c19-8b82-01a11b810e1e` (in .env)
- **Secret Key:** 40-char HMAC key (in .env)
- **Gateway:** `api-gateway.tw.coupang.com` (Taiwan only)
- Korea gateway returns 403: "not for the target VDC"

## Selection Algorithm (pipeline.py)

- **Keywords:** 10 defaults (咖啡, 泡麵, 零食, 衛生紙, 洗衣精, 尿布, 濕紙巾, 充電線, 行動電源, 寵物飼料)
- **Top N:** 3 products per run
- **Dedup:** `history.json` records productId to prevent repeats
- **Scoring:** `isRocket(+25) + name_length_quality(+10) + price_50to2000(+15)`
- **LLM action:** Writes one natural paragraph per product, storytelling tone

## Content Style (approved 2026-06-15)

- Natural conversational tone ("昨天發現…", "原本想說…")
- No emoji, no hashtags, no bold formatting
- Single paragraph per product, 10-15 lines
- Ends with "這裡" + affiliate link
- No CTA/push/sell language
