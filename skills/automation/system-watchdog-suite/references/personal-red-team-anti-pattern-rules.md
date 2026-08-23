# Agentic 反模式規則庫（45 條,吸收自 microsoft/AI-Engineering-Coach, MIT, 2026-08）

來源 repo 的規則本體是「VS Code/Copilot session log 分析」用的 markdown 規則。本檔把它
分類成對 Hermes 的可用性，避免重新抓取。

## A. Hermes state.db 可直接掃（`scripts/session-hygiene-audit.py` 已含 12 項）

| # | 規則 | state.db 對應 | 門檻 |
|---|---|---|---|
| 1 | Mega Sessions | sessions.message_count | >=100 |
| 2 | Abandoned Sessions | message_count<=2 | 計數 |
| 3 | Prompt Cache Starvation | cache_read_tokens/input_tokens<10%, input>5K | 每 session |
| 4 | Premium Waste | estimated_cost_usd>1 & output_tokens<500 | 每 session |
| 5 | Model Overreliance / Auto Model Avoidance | session_model_usage 分布 | 單 model >95% |
| 6 | Verbose Output | assistant content LENGTH>20K | 計數 |
| 7 | Repeated Prompts | user content GROUP BY (排除系統注入前綴) | c>1 |
| 8 | Runaway Agent Loops | tool_call_count>100 | 每 session |
| 9 | Instruction Bloat | Projects 下 AGENTS/CLAUDE/CONTEXT/.cursorrules >5KB | 每檔 |
| 10 | Late-Night Coding | strftime %H in 0-5 | 計數 |
| 11 | Weekend Overwork | strftime %w in 0,6 | 計數 |
| 12 | Tool/MCP Bloat | config.yaml mcp_servers 數（近似） | 手動判斷 |

## B. 部分可查 / 需 proxy 或人工判斷

| 規則 | 代理信號 |
|---|---|
| Session Drift | title 變更次數、compression_fallback_streak |
| Speed Accept / Copy-Paste Blindness | 大輸出後 <10s 就下一個 user msg |
| Vibe Coding | output_tokens/input_tokens 高 + 無後續 review 訊息 |
| No Spec-Driven / Unstructured Task Starts | session 開頭 user prompt 是否含規格/計畫關鍵字 |
| Lazy Prompting | coding session 的 user prompt <30 chars |
| Low Constraint Usage | user prompt 缺 do not/must/avoid/only 等 |
| Excessive File Context | 單 request 掛 >10 檔（tool_calls 附件數） |
| Verbose Prompts No Compression | user prompt >2000 chars |
| Reasoning Effort Overuse | reasoning_tokens/input_tokens >50% |
| Agentic Without Tools | tool_call_count=0 的 agentic session |

## C. 行為教練（審計報告當 checklist 提醒，不自動偵測）

- Broken Flow State（長 pause 碎片化）、Slow Responses（latency 是 infra 問題非行為）
- Frustration Signals / Caps Lock Rage / Hostile Language（內容層，低價值）
- Excessive Cancellations（Hermes 無 cancel 日誌）
- No Language Exploration（portfolio 廣度）、Single-Workspace Tunnel Vision
- Low Markdown Output Ratio（文件品質，與 stop-slop 重疊）

## D. VS Code/Copilot 專用 → 對 Hermes 無意義（skip）

- Agent Mode for Simple Questions、Never Uses Plan Mode、No Slash Commands
- Auto-Approved Terminal / YOLO Mode（Hermes approval 無 state.db 日誌；hooks skill 已管）
- Unsandboxed Terminal Execution / No Devcontainer（Hermes 原生 sandbox 議題不同）
- No Custom Instructions / No Skills（Hermes 有系統 prompt + 100+ skill，等效已存在）

## 使用時機

- red-team 證據收集步驟直接跑 script；B 類當線索手動查；C 類寫進報告 checklist；
  D 類永不引用（避免報告塞 VS Code 噪音）。
