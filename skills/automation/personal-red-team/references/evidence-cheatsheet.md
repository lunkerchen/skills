# 證據收集命令速查

按區塊執行，一次平行批次抓完。所有輸出保留在 session 內，重要發現記路徑。

## 1. Cron 盤點

```bash
# default profile（工具）
cronjob action=list

# 其他 profile（直接讀 jobs.json，比 CLI 快且完整）
python3 -c "
import json
d = json.load(open('$HOME/.hermes/profiles/<profile>/cron/jobs.json'))
jobs = d if isinstance(d, list) else d.get('jobs', [])
for j in jobs:
    print(j.get('name','?')[:40], '|', j.get('schedule','?'), '| enabled=', j.get('enabled'),
          '| last=', j.get('last_status','?'), '| script=', bool(j.get('script')))"

# 狀態史（誰在何時 pause/刪除/re-enable）
ls -la $HERMES_HOME/cron/jobs.json.bak-*
```

## 2. 專案活動度

```bash
for d in $DEV_PROJECTS/*/; do
  printf "%-42s" "$d"
  git -C "$d" log -1 --format='%ci | %s' 2>/dev/null || echo "(no git)"
done

# 大小與垃圾
du -sh $DEV_PROJECTS/* 2>/dev/null | sort -rh | head -25
find ~/Developer/Projects -maxdepth 5 -type d -name node_modules -not -path '*/node_modules/*' | while read d; do du -sh "$d"; done
du -sh $DEV_PROJECTS/*/.next $DEV_PROJECTS/*/target 2>/dev/null | sort -rh | head -10
# 單檔怪獸
find ~/Developer/Projects -type f -size +500M -not -path '*/.git/*' 2>/dev/null | head -10
```

## 3. 常駐服務

```bash
launchctl list | grep -iE "hermes|lark|omniroute|finance"
ls -la ~/Library/LaunchAgents/
# plist 可能是模板：grep 佔位符
grep -l "PATH/TO\|USERNAME\|xiaoqi" ~/Library/LaunchAgents/*.plist 2>/dev/null
# 遠端機：先確認連線能力（tailscale status / ping），連不上 = 無法驗證 = 發現
```

## 4. Skills 庫

```bash
du -sh $HERMES_HOME/skills/* 2>/dev/null | sort -rh | head -15
ls -la $HERMES_HOME/skills | grep '^l'          # symlink 指向（跨 agent 共享）
python3 -c "
import json
u = json.load(open('$HOME/.hermes/skills/.usage.json'))
# created/patched/archived 時間戳；幽靈記錄 = 記錄存在但目錄已刪
print(len(u), 'records')"
du -sh $HERMES_HOME/skills/.curator_backups $HERMES_HOME/skills/.hub $HERMES_HOME/skills/.archive 2>/dev/null
# 冷庫估算：cron 引用的 skills 加總大小 vs 全部
```

## 5. 跨 agent 記憶對照

```bash
cat ~/.agents/AGENTS.md
# 記憶宣稱 vs 實體：每個「在跑/已部署/有 plist」都要找到對應實體
# 找不到 = 弱假設發現
```

## 6. 錯誤診斷

```bash
# 每個 error job 的最新輸出結尾
ls -lt $HERMES_HOME/cron/output/<job_id>/ | head -3
tail -30 $HERMES_HOME/cron/output/<job_id>/$(ls -t $HERMES_HOME/cron/output/<job_id>/ | head -1)
# 失敗史
grep -c "FAILED" $HERMES_HOME/cron/output/<job_id>/*.md 2>/dev/null
# 系統性錯誤佐證
grep -E "ERROR|Traceback|unhealthy|payment" $HERMES_HOME/logs/errors.log | tail -20
# no_agent script 驗證（歷史殘留 vs 真壞）
bash -x $HERMES_HOME/scripts/<script>.sh; echo "EXIT:$?"
```

## 7. 憑證掃描（只列路徑，不讀內容）

```bash
find ~/Developer/Projects -maxdepth 4 \( -name '.env' -o -name '.env.*' -o -name '*.pem' \) -not -path '*/node_modules/*' 2>/dev/null
# 確認 git 只追蹤 .env.example
git -C <repo> ls-files | grep -E "\.env"
```

## 8. 磁碟總覽

```bash
df -h /
du -sh ~/Library/Caches/* 2>/dev/null | sort -rh | head -10
ls -laS $HERMES_HOME/logs/ | head -10        # 肥大 log 也是發現
```
