# lark-oapi Python SDK — 實裝驗證筆記 (v1.7, 2026-08)

來源：finance-lark-bot 專案實作時對安裝版 `lark-oapi==1.7.x` 逐一 introspect 驗證。
(2026-08-03 實測，Python 3.12, pip install lark-oapi)

## 版本

- PyPI 最新 1.7.x。**不存在 3.x**（2.x 只有 dev 版）。`pip install "lark-oapi>=3.0.0"` → `No matching distribution found`。
- 需求寫 `lark-oapi>=1.7.0`。

## WebSocket 長連接（lark_oapi.ws）

```python
from lark_oapi.ws import Client as WSClient
import lark_oapi as lark

ws = WSClient(
    app_id="cli_xxx",
    app_secret="xxx",
    log_level=lark.LogLevel.INFO,          # 傳 None 會炸: 'NoneType' object has no attribute 'value'
    event_handler=handler,                  # EventDispatcherHandler
    domain=lark.LARK_DOMAIN,                # 'https://open.larksuite.com'（國際版）
                                            # 中國版: lark.FEISHU_DOMAIN ('https://open.feishu.cn')
    auto_reconnect=True,
)
ws.start()  # 阻塞常駐
```

簽名（introspect 所得）：
`Client(app_id, app_secret, log_level=LogLevel.INFO, event_handler=None, domain='https://open.feishu.cn', auto_reconnect=True, source=None, extra_ua_tags=None, headers=None)`

重點：
- `ws.Client` 是**建構子**，不是 builder（`ws.Client.builder()` 不存在）
- 一般 `lark.Client.builder()` 也沒有 `.event_handler()` 方法 — 只有 `app_id/app_secret/app_ticket/app_type/build/cache/domain/enable_set_token/log_level/source/timeout`
- 事件 handler：
  ```python
  handler = (lark.EventDispatcherHandler.builder("", "")
      .register_p2_im_message_receive_v1(on_message)   # 存在，已確認
      .build())
  ```

## 發送訊息（im.v1）

- `CreateMessageRequest.builder()` → `receive_id_type(...)`、`request_body(...)`
- `CreateMessageRequestBody.builder()` → `content(...)`、`msg_type(...)`、`receive_id(...)`、`uuid(...)`
- **沒有 TextMessage model**（`from lark_oapi.api.im.v1.model.text_message import TextMessage` 會 ModuleNotFoundError，grep 整個套件也找不到 class TextMessage）
- content 直接傳 JSON 字串：`json.dumps({"text": text}, ensure_ascii=False)`
- 回覆 DM/群組通用：`receive_id_type="chat_id"` + `receive_id=message.chat_id`

## im.message.receive_v1 事件形狀

```
P2ImMessageReceiveV1
  .event: P2ImMessageReceiveV1Data
    .message: Message        # chat_id, message_id, msg_type, body, mentions, ...
    .sender:  Sender         # id, id_type, sender_name, sender_type, tenant_key
```

- 訊息正文在 `message.body.content`（`MessageBody` 只有 `content` 欄位；`Message` 本身沒有 content/chat_type）
- open_id = `sender.id`（`Sender` 沒有 `sender_id`）
- content 是 JSON 字串 `{"text": "..."}`；群組 @ 訊息會有 `<at user_id="ou_..."></at>` 標籤，需剝掉再當指令解析

## 驗證手法（未來 SDK 升級時重跑）

```bash
.venv/bin/pip install lark-oapi
.venv/bin/python - <<'EOF'
import inspect, lark_oapi as lark
from lark_oapi.ws import Client as WSClient
print(inspect.signature(WSClient.__init__))
print([m for m in dir(lark.Client.builder()) if not m.startswith('_')])
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1, Message, Sender, MessageBody
for cls in (P2ImMessageReceiveV1, Message, Sender, MessageBody):
    print(cls.__name__, [x for x in dir(cls()) if not x.startswith('_')])
EOF
```

模型類是 `_types` dict + `init(self, d, types)` 風格：空實例 `dir()` 只會看到 d=None 時有設的欄位；`sender_id` 不存在、`content` 在 body。
