# Momo Gift Monitor — Session Reference

## Context
Request: 幫我監測這個商品每個小時檢查一下它附贈的贈品有沒有改變如果有改變的話發送商品連結到Telegram 給我
URL: https://s.momoshop.com.tw/s/nHx5VpfQ
Product: NIVEA 妮維雅 亮白極致嫩膚乳液400mlx3入

## Current Gifts (as of 2026-07-23)
1. 【妮維雅】指定品項滿2199贈乖乖變色杯
2. 【妮維雅】指定品項滿1099贈止汗噴霧
3. 【妮維雅】指定品項贈三重防曬
4. 【妮維雅】指定品項贈乳液+31冰淇淋券

## Script
`$HERMES_HOME/scripts/momo-gift-monitor.py` — no_agent cron script
`$HERMES_HOME/scripts/.momo-gift-state.json` — state file (fingerprint + current gifts)

## Cron Job
- Name: `momo-gift-monitor`
- ID: `7063a2ee020f`
- Schedule: `every 60m`
- Delivery: `telegram`
- Mode: `no_agent=true`

## Logs
All runs logged in `$HERMES_HOME/logs/agent.log`:
- `empty stdout — silent run` = gifts unchanged
- If stdout non-empty = change detected and delivered

## Fingerprint
SHA256 of the sorted JSON gift list. Structure:
```json
{
  "fingerprint": "da48547066cbe6175208d32f25cd050d26a075c3e3daafe409a7292735893d21",
  "gifts": [
    {"promoText": "...", "actionUrl": "..."}
  ]
}
```

## Initial State
First run stores fingerprint and exits silently (no alert). Subsequent runs compare.
