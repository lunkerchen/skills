# Lark Bot Dev — API notes & source URLs

Condensed from official docs research (2026-08). All claims sourced to open.larksuite.com.

## Event payload — `im.message.receive_v1` (v2.0)

```json
{
  "schema": "2.0",
  "header": {
    "event_id": "5e3702a84e847582be8db7fb73283c02",
    "event_type": "im.message.receive_v1",
    "create_time": "1608725989000",
    "token": "rvaYgk...F7JV",
    "app_id": "cli_9f5343c580712544",
    "tenant_key": "2ca1d211f64f6438"
  },
  "event": {
    "sender": {
      "sender_id": {
        "union_id": "on_8ed6aa67826108097d9ee143816345",
        "user_id": "e33ggbyz",
        "open_id": "ou_84aad35d084aa403a838cf73ee18467"
      },
      "sender_type": "user",
      "tenant_key": "736588c9260f175e"
    },
    "message": { "...": "message_type, message_id, content, chat_id, etc." }
  }
}
```

- v1.0 structure: `{ts, uuid, token, type: "event_callback", event: {...}}`
- Receive-event scope decides what arrives: DM-scope → all bot DMs; group-all-messages scope → all group messages (not bot's own); @bot scope → only @bot messages.
- Dedupe with `message_id`, never `event_id`.

## Send message — `POST /open-apis/im/v1/messages`

- Query `receive_id_type`: `open_id` (per-app user id, recommended) | `union_id` | `user_id` (needs extra scope) | `email` | `chat_id`
- Body: `receive_id`, `msg_type`, `content` (escaped JSON string), `uuid` (opt, ≤50 chars, same uuid ≤1 msg/hour)
- Size caps: text 150KB; card/rich-text 30KB
- Rate limits: same-user 5 QPS; same-group 5 QPS (shared by bots in group); API-level 1000/min & 50/sec

### content JSON by type
| type | content |
|---|---|
| text | `{"text":"test content"}` — supports `<at user_id="ou_xxx">Tom</at>`, `all` for everyone, `<b><i><u><s>`, `[text](url)` |
| post | `{"zh_cn":{"title":"T","content":[[{"tag":"text","text":"...","style":["bold","underline"]},{"tag":"a","href":"...","text":"..."},{"tag":"at","user_id":"ou_..."}],[{"tag":"img","image_key":"img_..."}],[{"tag":"media","file_key":"file_v2_...","image_key":"cover"}],[{"tag":"hr"}],[{"tag":"code_block","language":"GO","text":"..."}],[{"tag":"md","text":"..."}]]}}` — at least one language key (zh_cn/en_us) |
| image | `{"image_key":"img_..."}` (upload via im/v1/images first) |
| file / audio | `{"file_key":"file_v2_..."}` (upload via im/v1/files) |
| media | `{"file_key":"...","image_key":"cover"}` |
| sticker | `{"file_key":"..."}` — only stickers the bot has received |
| interactive | full card JSON (use CardKit to generate) |
| share_chat / share_user | `{"chat_id":"..."}` / `{"open_id":"..."}` |

## Cards
- Card JSON v2: `{config, header{title, template}, elements[...]}`. Elements: div, button, markdown, img, hr, action, note, column_set...
- Interactive flow: button with `value` → card action callback (POST to card callback URL / via long connection) → app can PATCH the message to update the card.
- CardKit: https://open.larksuite.com/tool/cardbuilder — visual builder, outputs JSON.
- Card update `PATCH /im/v1/messages/{message_id}`: needs bot capability; with user_access_token the user must be the sender; only un-recalled shared cards.

## Auth
- tenant_access_token: `POST /open-apis/auth/v3/tenant_access_token/internal` body `{app_id, app_secret}` → `{code:0, tenant_access_token:"t-...", expire:7200}`. Valid 2h; calling with <30min remaining returns a fresh token (both valid) — cache it.
- Store apps: `POST /open-apis/auth/v3/tenant_access_token` (needs app_ticket).
- Header for calls: `Authorization: Bearer t-...`, `Content-Type: application/json; charset=utf-8`.

## Rate limits
- 429 Too Many Requests; body `{"code":99991400,"msg":"request trigger frequency limit"}`; headers `x-ogw-ratelimit-limit` (window, s) + `x-ogw-ratelimit-reset` (recovery seconds → sleep then retry).
- Levels: L1 10/min → L4 1000/min+50/s → L9 50/s → L11 100/s. Custom bot: 100/min, 5/s. Message/Group/Base have special (non-table) frequency control.
- No self-service raise — contact CSM.

## SDK snippets
- Go: `go get -u github.com/larksuite/oapi-sdk-go/v3`; `larkws.NewClient(appID, appSecret)`; dispatcher `OnP2MessageReceiveV1`.
- Python: `pip install lark-oapi -U`; `lark.ws.Client(app_id, app_secret, event_handler=lark.EventDispatcherHandler.builder("", "").register_p2_im_message_receive_v1(do_p2_im_message_receive_v1))`; `cli.start()`.
- Node: `npm install @larksuiteoapi/node-sdk`; `new Lark.WSClient({appId, appSecret, domain: Lark.Domain.Lark})`; `eventDispatcher.register('im.message.receive_v1', ...)`. **Default domain is open.feishu.cn — must set `Lark.Domain.Lark` for international.**
- SDK also auto-manages tenant_access_token.

## Source URLs (official docs)
- Bot overview: https://open.larksuite.com/document/client-docs/bot-v3/bot-overview
- Custom bot guide: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/bot-v3/use-custom-bots-in-a-group
- Self-built app dev process: https://open.larksuite.com/document/home/introduction-to-custom-app-development/self-built-application-development-process
- Event overview: https://open.larksuite.com/document/server-docs/event-subscription/overview-of-event-subscription
- WebSocket receive: https://open.larksuite.com/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-subscription-configure-/use-websocket
- Webhook (send to dev server): https://open.larksuite.com/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-subscription-configure-/choose-a-subscription-mode/send-notifications-to-developers-server
- Receive message event: https://open.larksuite.com/document/server-docs/im-v1/message/events/receive
- Send message: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
- Message content formats: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json
- Message card overview: https://open.larksuite.com/document/common-capabilities/message-card/introduction-of-message-cards
- CardKit builder: https://open.larksuite.com/tool/cardbuilder
- Server SDK: https://open.larksuite.com/document/ukTMukTMukTM/uETO1YjLxkTN24SM5UjN
- tenant_access_token: https://open.larksuite.com/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
- Rate limits: https://open.larksuite.com/document/ukTMukTMukTM/uUzN04SN3QjL1cDN
- Server error codes: https://open.larksuite.com/document/server-docs/getting-started/server-error-codes
