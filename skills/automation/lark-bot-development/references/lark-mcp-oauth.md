# Lark MCP / 集中 OAuth 接入（2026-08 實測）

## 公司集中 OAuth service（lark-oauth.yotron-ai.com）

repo：`~/Developer/Projects/finance-lark-bot` → `app/oauth_service/`（Python stdlib HTTPServer）
部署：Cloudflare proxy（`server: cloudflare`，DNS 指向 CF anycast）；後端本機 listener `127.0.0.1:8788`
環境檔：`deploy/lark-oauth.environment.example`，`LARK_OAUTH_REDIRECT_URI=https://lark-oauth.yotron-ai.com/oauth/callback`

實測（2026-08-06）：

```
curl -i https://lark-oauth.yotron-ai.com/healthz
→ 200 {"status":"ok","configured":{"app_id":true,"redirect_uri":true,"app_secret":true,"keychain":true},"oauth_ready":true}

curl -i https://lark-oauth.yotron-ai.com/login
→ 302 Location: https://accounts.larksuite.com/open-apis/authen/v1/authorize?client_id=cli_...&redirect_uri=https%3A%2F%2Flark-oauth.yotron-ai.com%2Foauth%2Fcallback&...（含 code_challenge, state）

curl -i https://lark-oauth.yotron-ai.com/mcp   → 404 {"error":"not_found"}
curl -i https://lark-oauth.yotron-ai.com/sse   → 404 {"error":"not_found"}
```

route 表（`app/oauth_service/server.py` `do_GET`）：`/healthz` | `/login?return_to=` | `/oauth/callback` | `/auth/status` | `/logout`，其餘 404 JSON。

## 官方 lark-mcp CLI 為何不能接遠端 callback

`~/.local/lib/node_modules/@larksuiteoapi/lark-mcp/dist/`：

- `auth/handler/handler.js` L11-13：
  ```js
  get callbackUrl() { return `http://${this.options.host}:${this.options.port}/callback`; }
  ```
- `auth/provider/oauth.js` L29 / L53：authorize 與 token exchange 都組
  ```js
  redirect_uri: this._options.callbackUrl + '?redirect_uri=' + client.redirect_uris[0]
  ```
- `auth/handler/handler-local.js`：local client `client_id_for_local_auth`，callback 在 `this.app.get('/callback')`

結論：`--host`/`--port` 只改本機 listener。官方 CLI 的 OAuth 流程永遠回呼 localhost → 若 Lark App 註冊的 redirect 不是該 localhost 字串，Lark 回 **20029**（redirect_uri mismatch）。

## Probe-before-wire 規則

拿到一個「要接 MCP」的 URL 時，先分類再寫 config：

| probe | 回傳 | 判讀 |
|---|---|---|
| `GET /healthz` | 200 JSON | 是服務（可能是 OAuth/app） |
| `GET /mcp` 或 `/sse` | 200 + MCP handshake | 是 MCP endpoint |
| `GET /mcp` 404 JSON | — | 不是 MCP，別把 client 指過去 |

本 session 教訓：先寫了 `[mcp_servers.lark_company]` 到 `~/.codex/config.toml`（指到 OAuth-only domain），probe 後刪除。順序應為 probe → classify → 才動 config。
