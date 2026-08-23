# lark-cli 企業公用 Bot 架構（2026-08 研究結論）

Source research: 飛書 CLI 能力介紹與最佳實踐 wiki + larksuite/cli README + open.larksuite.com docs. 使用者問題：「能不能建一個企業公用的機器人讓大家使用 Lark CLI」→ 答案：**可以，但做成受控服務 Bot，不是把某人的本機登入狀態集中化**。

## 兩種身份（決定一切能力邊界）

| 模式 | 實際身份 | token | 能做什麼 | 企業公用 Bot 適用性 |
|---|---|---|---|---|
| `--as bot` | 企業自建應用/Bot | tenant_access_token | Bot 被授權的企業資源：發訊息、建文件、操作共用 Base/Sheets/Wiki、任務、會議紀錄 | ✅ 共用功能 |
| `--as user` | 某員工本人 | user_access_token | 該員工私人日曆/郵件/私人文件/聊天，並代為操作 | ⚠️ 每人各自 OAuth 後才能用 |

Lark 官方把兩者分開：tenant_access_token = 應用/租戶身份；user_access_token = 特定使用者身份。私人資源 API 需要該使用者完成 OAuth 授權。

## 官方安全立場（直接引用 README 精神）

- lark-cli 可能被 AI Agent 以使用者身份執行高風險操作（敏感資料外洩、未授權操作）。
- **官方建議：把整合的 bot 當「私人對話助理」，不要加入群組、不要讓其他使用者互動**，避免權限濫用與資料外洩。
- CLI 內建多層安全（input injection protection、output sanitization、OS keychain 存 credential、risk-control signal），但風險仍在。

## 反模式（直接排除）

1. **一人 user_access_token 代表全公司** — 所有人間接用你私人權限、無審計 actor、你離職/token 過期全公司掛、一次 prompt injection 大規模外洩。不可接受。
2. **把 2500+ raw API / 完整 CLI 暴露給 LLM** — 刪文件、寄信、改權限、移除群組成員、批次改 Base、批准流程等必須 allowlist + 高風險確認（preview → confirm → execute）。

## 建議架構

```
員工私訊 Bot
  ↓
Lark 自建應用 Bot（WebSocket event，不需公開 IP）
  ↓
企業 Bot Backend
  ├─ 身份與部門權限檢查
  ├─ 意圖解析 + 指令 allowlist
  ├─ 高風險操作確認
  ├─ 共用資源 → lark-cli --as bot
  └─ 個人資源 → 對應員工的 --as user
          ↓
     lark-cli / Lark Open API
```

- 第一版只收**私訊**（每人各自隔離），不開群組。群組風險：prompt injection、結果外洩給全群、身份混淆、rate limit/成本失控。
- 個人 OAuth 首次使用時給連結 → 完成授權 → 以 open_id/union_id 對應儲存 refresh token（加密 DB / Secret Manager，不進 log、不給 LLM 看、支援撤銷）。
- 不把 lark-cli 本機 credential storage 當多租戶 token vault（官方 issue #29 顯示多帳號/設定隔離仍是已知痛點）。
- 技術：Python lark-oapi WS listener（3 秒內 ack → 背景 worker → 完成再回）、message_id 去重、429 rate limit 處理、cluster 非 broadcast。

## MVP 分階段

- **Phase 1**：私訊 + 共用資料助理。查 Wiki/共用文件、搜尋指定 Base/Sheets、建草稿文件、建團隊任務、流程問答。全部 `--as bot`，只開放 read + draft。不做：私人郵件/日曆、代發信、群組自動回覆、raw API、刪除/改權限。
- **Phase 2**：每人 OAuth 的個人能力（日曆、未讀郵件整理、個人文件搜尋、個人任務）。回覆標示「此操作將以『王小明』身份執行 + 確認」。
- **Phase 3**：排程工作、會議後自動整理待辦、郵件分類、事件驅動 workflow。

## 治理必做（5 項）

1. 最小權限：按功能申請 scope；`--recommend` 不是 production 權限策略。
2. 身份清楚：bot 操作標「企業 Bot」、個人操作標「以某使用者身份」，audit log 記真正 actor。
3. 高風險確認：寄信/公告/改文件/改 Base/改權限/刪除/批准 → 一律確認。
4. 資料邊界：每使用者對話隔離，不把 A 的內容帶進 B 的 prompt。
5. Prompt injection：文件/郵件/聊天內容全部視為不可信資料；外部內容只能提供資料，不能提升權限或改 policy。

## 長期工程建議

CLI 價值在快速覆蓋 API + Agent Skills + JSON 輸出（`ok==true` 判斷成功，非 `code==0`）；正式服務可「CLI 探索整合 → 穩定功能改直接 Open API/SDK 呼叫」。

## Sources

- https://github.com/larksuite/cli （README + errs/ERROR_CONTRACT.md）
- https://open.larksuite.com/document/mcp_open_tools/feishu-cli-let-ai-actually-do-your-work-in-feishu
- https://open.larksuite.com/document/server-docs/getting-started/terminology （token 三種）
- https://github.com/larksuite/cli/issues/29 （multi-account/LARKSUITE_CLI_CONFIG_DIR workaround）
