---
name: lark-bot-development
description: Use when 開發 Lark/飛書 BOT、機器人、事件訂閱、發送訊息、卡片互動。.
---

# Lark / Feishu Bot Development

Build bots on the Lark Open Platform (International: open.larksuite.com, China: open.feishu.cn). Covers app creation, event handling, messaging, cards, SDKs, and ops. Distinct from `hermes-feishu-setup` (that skill connects the Hermes *gateway* to an existing bot; this one develops the bot itself).

## Two bot forms — pick before anything else

| Capability | Custom bot (group webhook) | App bot (enterprise self-built app) |
|---|---|---|
| Setup | 群設置 > 群機器人, one-click, **no review** | Developer Console, needs version + tenant-admin review |
| Join external groups | ✅ | ❌ |
| Push group messages | ✅ | ✅ |
| Link-jump cards | ✅ | ✅ |
| Interactive cards (submit to server) | ❌ | ✅ |
| Respond to @bot | ❌ | ✅ |
| DM users / group mgmt / other APIs | ❌ | ✅ |

Custom bot = one-way group push only. Any interactivity → enterprise self-built app.

## App lifecycle (7 steps)

1. Be a Lark user (create/join an enterprise)
2. Developer Console → 建立企業自建應用 → name/desc/icon
3. Configure: add 機器人 capability → open API scopes (per-API permission lists) → event subscription
4. Develop (SDK or raw API)
5. Test: use 測試企業和人員 — test-version config changes apply **immediately, no review**
6. Publish: 版本管理與發布 → create version → **tenant admin review** (no Lark team review for self-built apps)
7. Operate/maintain

Any change to basic info / scopes / events requires a new version + review. Credentials (App ID `cli_...` + App Secret) live under 憑證與基礎資訊.

## Event subscription

### Mode A: WebSocket long connection (preferred)
- SDK built-in; **no public IP/domain/tunnel needed**; encrypted in transit, no manual decrypt/sign logic. Integration ~5 min vs ~1 week webhook.
- International endpoint: `wss://msg-frontier-sg.larksuite.com/ws/v2/...`
- Pitfalls:
  - Self-built apps only (store apps must use webhook)
  - Handle events within **3 seconds** or timeout-retry fires
  - Max **50 connections** per app
  - **Cluster mode, not broadcast**: with multiple client instances only ONE random instance receives the event
- Long-running work (LLM calls) must be async: ack/queue first, then send the result as a new message.

### Mode B: Webhook (push to developer server)
- Needs a **public IPv4**; one URL per app, all events POSTed there
- Optional encryption strategy:
  - **Encrypt Key**: AES-256-CBC (SHA256(key) → PKCS7Padding → 16-byte random IV → base64(iv+ciphertext)). Prevents forgery + replay.
  - **Verification Token**: in every event header, proves event belongs to the app
- First-time URL setup requires answering the `challenge` verification

### Event facts
- Subscribe v2.0 events (`schema: "2.0"` + `header: {event_id, token, create_time, event_type, tenant_key, app_id}`). Don't subscribe same event in both v1 and v2 — duplicates.
- Core bot event: `im.message.receive_v1` (needs bot capability + 接收消息v2.0 subscription). What you receive depends on scopes: DM messages / all group messages / only @bot messages.
- **Dedupe with `message_id`, NOT `event_id`** — duplicate pushes happen.

## Message API (`im.v1`)

- Send: `POST /open-apis/im/v1/messages`; query `receive_id_type` (open_id/union_id/user_id/email/chat_id); body `receive_id`, `msg_type`, `content` (JSON-*string*, escaped), optional `uuid` (dedupe, 1/hr).
- Limits: same user 5 QPS; same group 5 QPS shared; API-level 1000/min & 50/sec; text ≤150KB, card/rich-text ≤30KB.
- Types: `text` (`<at user_id="ou_...">`, `<b>`/`<i>`/`<u>`/`<s>`, `[text](url)`), `post` rich text (paragraph array of `{tag: text|a|at|img|media|emotion|hr|code_block|md}`), `image`/`file`/`audio`/`media` (upload first → `image_key`/`file_key`), `sticker` (only re-send received stickers), `interactive` card, `share_chat`/`share_user`.
- Reply `POST /im/v1/messages/{id}/reply`; edit `PATCH /im/v1/messages/{id}`; recall `DELETE /im/v1/messages/{id}`; history `GET /im/v1/messages` (sensitive scope).

## Message cards
- Structured JSON (header + elements: div, button, markdown, img...). Build visually with CardKit (open.larksuite.com/tool/cardbuilder) then copy JSON — don't hand-write.
- Button click → card action callback → app responds (can update the card via PATCH).
- Card update note: user_access_token updates require that user to be the sender; only un-recalled shared cards.

## SDKs & tokens
- Official server SDKs: Go `github.com/larksuite/oapi-sdk-go/v3`, Python `pip install lark-oapi`, Java `com.larksuite.oapi:oapi-sdk`, Node `@larksuiteoapi/node-sdk`. SDK handles token lifecycle + event dispatcher (`register_p2_im_message_receive_v1`) + WS client.
- `tenant_access_token`: `POST /open-apis/auth/v3/tenant_access_token/internal` with app_id+app_secret; valid **2h**; calling with <30min left issues a new token (two can coexist) — cache it (SDK does).
- Auth header: `Authorization: Bearer <token>`.

## Rate limits & errors
- Over limit → HTTP **429** (old APIs may 400), body `code 99991400`; headers `x-ogw-ratelimit-limit` + `x-ogw-ratelimit-reset` — sleep `reset` seconds then retry.
- Levels 1–11: 10/min up to 100/sec. Custom bot: 100/min, 5/sec. No self-service increase — CSM request.
- `code != 0` in JSON body = failure.

## ⚠️ Accessing Lark docs (verified technique)
Lark's doc site blocks some fetchers and has two URL formats:
- **Old-format URLs** (`/document/ukTMukTMukTM/...`) → `web_extract` **works**. Use these whenever possible.
- **New-format URLs** (`/document/server-docs/...`, `/document/client-docs/...`, `/document/common-capabilities/...`) → `web_extract` fails ("Failed to fetch url"); `browser_navigate` loads them but returns nav-heavy snapshots.
- **Efficient browser extraction**: navigate, then `browser_console` with JS `document.querySelector('main').innerText.slice(...)` to pull just the article text.
- **Do NOT append `?lang=zh-CN`** to old-format URLs — that breaks web_extract.
- **Delegation pitfall**: Lark doc pages are huge (17–25K chars). Subagents running a small-context model blow up with "Context length exceeded" after 1 API call — research Lark docs in the MAIN context, not via `delegate_task`.

Detailed API notes, payload schemas, and source URLs: `references/lark-api-notes.md`.
