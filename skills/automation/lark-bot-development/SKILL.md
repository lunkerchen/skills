---
name: lark-bot-development
description: Use when 開發 Lark/飛書 BOT、機器人、事件訂閱、發送訊息、卡片互動，或 Bitable/多維表格 API 與自動化整合。
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
  - 實裝模式（finance-lark-bot 2026-08 驗證）：ws handler 收到 LLM 指令 → 立刻 `reply_text(chat_id, "處理中…")` → `ThreadPoolExecutor` 派工 → 執行緒內**重新 `db.connect()`**（SQLite 連線不可跨執行緒共用）→ 跑完再 `reply_text`。執行緒內包 try/except 不 crash 進程。

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

## lark-oapi Python SDK — 實裝驗證 (v1.7, 2026-08)

**版本陷阱**：PyPI 最新是 **1.7.x**，沒有 3.x — `pip install "lark-oapi>=3.0.0"` 會報找不到版本。用 `>=1.7.0`。

**WebSocket client 是建構子，不是 builder**（`Client.builder()` 沒有 `.event_handler()`）：
```python
import lark_oapi as lark
from lark_oapi.ws import Client as WSClient

ws = WSClient(
    app_id=config.app_id, app_secret=config.app_secret,
    log_level=lark.LogLevel.INFO,
    event_handler=handler,                    # EventDispatcherHandler.builder("","").register_p2_im_message_receive_v1(fn).build()
    domain=lark.LARK_DOMAIN,                  # 國際版；中國版用 lark.FEISHU_DOMAIN
)
ws.start()                                    # 阻塞常駐
```

**發送文字訊息：content 是純 JSON 字串，沒有 TextMessage model**：
```python
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
req = (CreateMessageRequest.builder().receive_id_type("chat_id")
    .request_body(CreateMessageRequestBody.builder()
        .receive_id(chat_id).msg_type("text")
        .content(json.dumps({"text": text}, ensure_ascii=False)).build()).build())
client.im.v1.message.create(req)              # client = lark.Client.builder().app_id(...).app_secret(...).build()
```

**事件形狀（`im.message.receive_v1`）**：
- `data.event` → `.message` / `.sender`
- 訊息正文在 **`message.body.content`**（JSON 字串 `{"text": "..."}`；群組訊息含 `<at user_id="...">` 標籤要剝掉）
- open_id 在 **`sender.id`**（沒有 `sender_id`）
- `Message` 沒有 `chat_type` 欄位 — 回覆一律 `receive_id=message.chat_id` + `receive_id_type="chat_id"`，DM 與群組通用
- SDK 驗證手法：`pip install` 後直接 `inspect.signature(WSClient.__init__)` / `dir()` introspect，別靠猜或舊文件

完整欄位清單與驗證指令：`references/lark-oapi-python-sdk-verified.md`。

## 報表唯讀讀取（sheets / bitable）— finance-lark-bot 驗證 2026-08

用 `tenant_access_token` + `Authorization: Bearer <token>` GET 即可，不需 SDK；stdlib urllib 就夠（token 取得見上節 endpoint）。

- **sheets**：`GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}`（range 例 `Sheet1!A1:Z10`）→ `data.valueRange.values`（列陣列）
- **bitable**：`GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=N` → `data.items`；`data.has_more` + `data.page_token` 翻頁（防呆設總數上限，如 500 筆）
- 失敗判定：HTTP 非 2xx 或 body `code != 0`（例 99991 permission denied = bot 未被加為表格協作者 — bind 後要提醒使用者加 bot 檢視權限）
- 讀取層設計建議：`token_fn` 注入（可測）+ timeout + 錯誤訊息絕不含 token；未設憑證 → 明確報錯而非靜默
- 值格式化：數字千分位、None/空串 → 空、bool → 是/否（`app/report/reader.py` 有完整實作可參考）

## Bitable 作為資料層 — 外部資料寫入與自動化（2026-08 研究）

多維表格可以承接「外部系統 → 表格」的資料流，但它是**資料層不是抓取引擎**：Gmail 讀信、主旨解析、去重、重試、標籤回寫應在外部（Apps Script / n8n / Make / 自建 service），Base 負責儲存、視圖、儀表盤、狀態與協作。完整研究：`references/bitable-external-ingestion.md`。

- **寫入 API**：單筆 `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records`、批次 `records/batch_create`（≤1000 筆）；查重用 `records/search` + filter（`{"conjunction":"and","conditions":[{"field_name":...,"operator":"is","value":[...]}]}`）；更新 `PUT .../records/{record_id}`。用 tenant 或 user token；app 必須是 Base 的 owner/collaborator，否則 99991。
- **一致性鐵則（先寫成功才標記來源）**：讀 Gmail → 解析 → 依 message_id 查重 → 不存在才新增 → 讀回確認 → 才加 Gmail「已匯入」label。先標後寫 = 寫失敗就丟候選人。解析失敗 → 寫「待人工確認」+ 異常 label，不靜默丟棄、不標正常處理。
- **去重鍵 = Gmail message ID**，不是姓名或姓名+職位（同名重投/轉寄/多職缺都會誤判）。文字欄位無唯一約束保證 — 去重靠 app 端查詢 + 序列化寫入（同表不可併發寫，撞 1254291 LockNotObtainedError）。
- **原生自動化能力**：webhook 觸發（外部 POST → 新增/更新記錄）、「發送 HTTP 請求」action（開發者功能：僅公開 URL、60 秒上限、不支援內網）、Outlook 連接器已確認。
- **國際版 Gmail → Base：官方 AnyCross 範本已確認（2026-08-06）** — `Archive Email from Gmail to Lark Base`（https://anycross.larksuite.com/documentation/template/all/archive-gmail-to-base）。AnyCross = Lark 官方 Zapier 類產品（https://www.larksuite.com/en_us/product/anycross）。**Gmail Trigger 每 5 分鐘輪詢，不是即時 push**（官方文件明載）。國際版優先試 AnyCross；中國版飛書與租戶等級的連接器清單仍須在實際連接器中心實測，別假設相同。

## Codex-only 路徑：lark-cli user OAuth（finance-lark-bot 2026-08 定案）

新架構不用 bot：Vicky → Codex → lark-cli(`--as user`) → Sheets/Bitable。報表操作一律用**使用者的 user_access_token**，不是 tenant token。

- **身份檢查（盤點/接手第一件事）**：`lark-cli auth status` — 回傳 `identities.bot` 與 `identities.user` 雙身份。`defaultAs: user` 但 `identity: bot` = user 身份不可用。
- **Pitfall：user refresh token 會過期**。`identities.user.status: "missing (refresh token expired)"` + `refreshExpiresAt` 已過 → 所有 `report-*` 指令失敗。修復：`lark-cli auth login --recommend`（使用者瀏覽器 OAuth，約 2 分鐘）。identity 只剩 bot ≠ 程式壞，先查這個再 debug。
- 排程 bridge：`python -m app.jobs.codex_schedule --emit --db-path bot.db`，只有 callback 回 `delivered`/`acknowledged` 才標已提醒。
- 本機工具入口：`python -m app.finance_tool report-*`（preview → 確認 → commit → read-back，audit 不存 token）。

## lark-cli 綁錯 app：授權頁出現「Hermes Content Hub 使用權限」（2026-08 踩過）

Hermes 環境的 lark-cli 預設綁 **Hermes workspace 的 app**（`lark-cli config show` 會看到 `workspace: hermes` 和一個陌生的 `appId`），不是公司 app。拿這個狀態跑 device flow，使用者會卡在授權頁的「你沒有 Hermes Content Hub 使用權限」→ 永遠無法完成。

- **診斷**：`lark-cli config show` — 若 `appId` 不是專案的 app（專案 `.env` 的 `FEISHU_APP_ID`）、`workspace: hermes`，就是綁錯。`lark-cli doctor` 輔助：`identity_ready: fail` + `User identity: missing (refresh token expired)` = 需要重新授權（`app do not have bot` 是 warn 可忽略，user 身份路徑不需要 bot）。
- **修復**：為公司 app 建獨立 profile，不動 hermes workspace（secret 走 stdin，不進 argv/對話）：
  ```bash
  printf '%s\n' "$SECRET" | lark-cli profile add --name company --app-id cli_xxx --brand lark --lang zh --app-secret-stdin --use
  ```
- 然後**重新**跑 `lark-cli auth login --recommend --no-wait --json` + `lark-cli auth qrcode`。brand 決定授權網域：`feishu` → `accounts.feishu.cn`（中國版）、`lark` → `accounts.larksuite.com`（國際版）— 換 app 後 verification_url 網域會跟著變，屬正常。
- `lark-cli update`：1.0.48 → 1.0.84（doctor 會提示）。

## 公司集中 OAuth + MCP 接入（lark-oauth.yotron-ai.com, 2026-08 驗證）

公司 Lark 集中 OAuth 已上線：`https://lark-oauth.yotron-ai.com`（finance-lark-oauth service，Cloudflare 代管）。App 的 redirect URI 固定為 `https://lark-oauth.yotron-ai.com/oauth/callback` — 使用者要求認證連結一律用這顆，不要 localhost。

- endpoints：`/healthz`（回 `oauth_ready`）、`/login`（302 → Lark authorize）、`/oauth/callback`、`/auth/status`、`/logout`
- **這是 OAuth provider，不是 MCP endpoint**：`/mcp`、`/sse` 都 404。接 MCP 前先 probe 分類，別把 MCP client 指到 OAuth-only domain（踩過：寫了 `[mcp_servers.lark_company]` 到 Codex config 再刪掉）。
- 驗證 callback 是否真被使用：`curl -i https://lark-oauth.yotron-ai.com/login` 的 302 Location 裡的 `redirect_uri` param 就是 App 實際註冊值。

**官方 `@larksuiteoapi/lark-mcp` CLI 的 OAuth 綁死 localhost**（`dist/auth/handler/handler.js`）：`callbackUrl = http://${host}:${port}/callback`，provider 用 `callbackUrl + '?redirect_uri=' + client.redirect_uris[0]` 組 authorize/token 請求。`--host`/`--port` 只改本機 listener，無法把 redirect 指到遠端 domain → 與 App 註冊的 redirect 不符時撞 Lark **20029**（redirect_uri mismatch）。要用公司 OAuth 就得自己寫 bridge（`app/oauth_service` 就是），不要指望官方 CLI 接遠端 callback。

詳細 source 位置與 probe 結果：`references/lark-mcp-oauth.md`。

## Sheets 內嵌 Bitable 連結解析（Lark 特殊型別）

使用者給的 `/sheets/` 連結可能是「嵌在 Sheets 文件裡的多維表格區塊」，不是一般 sheets。`sheets/v3/.../sheets/{sheet_id}` 回 `resource_type: "bitable"`。解法：

1. `GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/metainfo` → 該分頁 `blockInfo.blockToken`
2. blockToken 格式 `{app_token}_{table_id}`，拆出後用一般 bitable API：
   ```
   blockToken = "YOUR_APP_TOKEN_YOUR_TABLE_ID"
   → app_token = "YOUR_APP_TOKEN", table_id = "YOUR_TABLE_ID"
   ```
3. 可正常打 `/bitable/v1/apps/{app}/tables/{tbl}/...`

注意：既有連結解析器（`app/report/reader.py` `_bind()`）只認 `/sheets/`、`/base/`、`/bitable/`、`/wiki/` 開頭，不認內嵌型別 — 要接這類資料源前先補解析分支或手動拆 token。

## Reminder scheduling pitfall — 假日順延的到期日掃描

週期提醒遇假日順延時，`next_due(today)` 在「順延後的到期日」當天會直接滾到下個週期 — 例：每月 23 號事件，8/23(日) 順延到 8/24；8/24 當天 `next_due` 已回 9/23，所以「到期當天通知」(notify_days=0) **永遠不會發**。修正：每日掃描需回查前一週期（`next_due(today-1)`），其 remind date == today 即發；務必為「順延後到期日當天」寫回歸測試（finance-lark-bot 踩過，已修）。

建議語意（finance-lark-bot 採用）：通知日 = 順延後到期日 - notify（預設 0 = 到期日當天），且**通知日也 clamp 到工作日**（往前移到最近的工作日，絕不在假日/週末發送）。

## LangBot 替代路徑（免自己寫 bot server）

若要「知識庫 RAG → Lark 問答」而非手寫 bot：**LangBot**（開源 IM bot 平台，v4.10.6）內建 Lark adapter（WebSocket 長連線、免公網）、插件化 Knowledge Base（LangRAG + GeneralParsers）、HTTP API `/api/v1/*` 供同步 script 上傳文件。Obsidian 資料夾 → LangBot → Lark 的完整架構與坑（含 iCloud mount 死鎖、繁中 embedding 選型、引用來源渲染未承諾）見 `team-knowledge-base` 的 `references/langbot-obsidian-rag-lark.md`。

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
