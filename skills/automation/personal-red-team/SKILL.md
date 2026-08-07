---
name: personal-red-team
description: Use when 紅隊審計/全系統盤點/找隱藏風險。證據優先掃描 cron+skills+專案→安全修復→決策簡報。
---

# Personal Red Team

對 使用者 的全系統紅隊審計。核心原則：**證據優先，不臆測**。每項發現要有檔案路徑、時間戳、大小或 log 佐證。輸出 = 報告 + 決策簡報（Obsidian），安全可逆的當場修，需判斷的寫 brief。

## 工作流

### 1. 證據收集（平行批次，一次抓完）

- `cronjob action=list` → default profile 的 job（含 last_status、schedule、no_agent）
- 其他 profile：`python3 -c "import json; d=json.load(open('$HOME/.hermes/profiles/<p>/cron/jobs.json')); ..."`（content-profile 是 content profile，有股市 job）
- 專案活動度：`for d in $DEV_PROJECTS/*/; do git -C "$d" log -1 --format='%ci | %s' 2>/dev/null; done` + `du -sh`
- 常駐服務：`launchctl list | grep -iE "hermes|lark|omniroute"` + `ls ~/Library/LaunchAgents/`
- skills：`du -sh $HERMES_HOME/skills/*`、`.usage.json`（created/patched/archived 時間戳）、`.curator_backups/`（快照輪替）、symlink 指向（`ls -la | grep '^l'`，136→~/.agents/skills、20→~/.claude/skills）
- 跨 agent 記憶：`~/.agents/AGENTS.md` — **memory 說的話要對照實體**（例：說 launchd 跑著，實際 LaunchAgents 沒有 plist → 發現）
- 磁碟：`df -h /`、`du -sh` 各目錄、單檔怪獸（find -size +500M）

### 2. 錯誤診斷（cron 失敗必查）

- 每個 error job：`ls -lt $HERMES_HOME/cron/output/<job_id>/` → 讀最新 .md 檔結尾的 `## Error` 區塊
- 同錯誤類別出現在多 job = 系統性問題（例：`RuntimeError: HTTP 500` 全出自 opencode-go provider 不穩，非 job 個別問題）
- `$HERMES_HOME/logs/errors.log`、`agent.log` 查輔證（auxiliary provider error 等）
- no_agent script「error」可能是**歷史殘留**（腳本已被修但狀態沒更新）→ 手動跑一次驗證：`bash <script>`；exit 0 + 預期輸出 = 已自癒
- 失敗史：`grep -c FAILED $HERMES_HOME/cron/output/<id>/*.md` 看持續多久（例：27 次掛 17 次）
- jobs.json.bak-* 可還原狀態史（誰在何時 pause/刪除/re-enable）

### 3. 平行分解（3 個 leaf 子代理）

任務 A 專案組合、B cron 健康、C skill 庫。每個 context 要給：完整 job 清單/目錄清單、已知線索、**唯讀約束**、輸出格式。子代理 summary 在聊天裡會截斷 → **完整版在 `$HERMES_HOME/cache/delegation/subagent-summary-*.txt`，用 read_file 讀**。

### 4. 修復判定

安全修復（當場做，可逆）：暫停指向死路徑的 job、驗證已修腳本、清快取/舊備份、修正誤導 memory。需決策（寫 brief）：刪 job/刪 skill/改 provider/動密鑰/改發布機制。

**坑**：
- `cronjob` 工具只管**目前 profile**。content-profile 的 job 要用 `hermes --profile content-profile cron <pause|edit|add|run> <id>`
- `hermes cron add` 的 prompt 是 **positional** 參數，不是 `--prompt`（create 沒這 flag）
- cron jobs 在 jobs.json **顯式 pin provider** → config 的 fallback_providers 永不啟動
- 06:00/08:00 多 LLM job 同時開火與 provider 失敗相關聯（未證實但可錯峰）
- .env 掃描只列路徑，**絕不讀內容**；驗證 git 只追蹤 .env.example
- 清 node_modules/.next/target 前確認無 launchd/cron 引用

### 5. 交付

Obsidian `04-產出-Hermes-Outputs/紅隊審計-YYYY-MM-DD/`：
- `00-紅隊審計報告.md`：已修復表 + 發現（🔴P1 隱藏失敗 / 🟠P2 浪費 / 🟡機會）+ 弱假設表 + 決策執行紀錄
- `brief-NN-主題.md`：每份 = frontmatter(status: 待決策) + 現況(證據) + 選項(A/B/C) + 建議 + 下一步(2 分鐘可做)

決策執行後：更新報告的決策執行紀錄、同步 memory 與 `~/.agents/AGENTS.md`（memory 每次寫入後同步該檔）。

## 發現分類模板

- 弱假設：記憶/慣例 vs 實體不符（例：說在跑、其實沒 plist）
- 幽靈自動化：cron 指向已遷移/已刪路徑（loop-state 已 done 還在跑）
- 生成>>發布：內容管線產出堆積、無發布機制
- 對撞：同小時多 LLM job、晨間多則 Telegram 簡報
- 冷庫：skills cron 引用僅 1.2MB / 543 個技能 99.7% cold；.curator_backups 無輪替

## 驗收

- 每項發現有證據（路徑/時間戳/大小/log 行）
- 修復清單標 SAFE-FIX vs NEEDS-DECISION
- 簡報每份都有「下一步 2 分鐘」
- 使用者回決策後：執行 → 更新報告 → 同步記憶
