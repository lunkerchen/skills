#!/usr/bin/env python3
"""
agentic session hygiene audit — Hermes state.db 掃描
來源: microsoft/AI-Engineering-Coach 45 條反模式規則 (MIT), 2026-08 吸收
用法: python3 session-hygiene-audit.py [--days 30] [--min-mega 100]
輸出: 繁中報告, 每項附證據 (SQLite 實查, 非猜測)
"""
import argparse, datetime, json, os, sqlite3, sys

HOME = os.path.expanduser("~")
DB = os.environ.get("HERMES_STATE_DB", f"{HOME}/.hermes/state.db")
PROJECTS = os.path.expanduser("~/Developer/Projects")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--min-mega", type=int, default=100, help="mega-session 訊數門檻")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cutoff = datetime.datetime.now().timestamp() - args.days * 86400
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    def q(sql, params=()):
        return cur.execute(sql, params).fetchall()

    out = {}
    def sec(key, label, rows, fmt):
        out[key] = {"label": label, "count": len(rows), "rows": rows}
        if not args.json:
            print(f"\n== {label} ({len(rows)}) ==")
            for r in rows:
                print("  " + fmt(r))

    # 1. mega-sessions
    sec("mega", "Mega Sessions (>=%d 訊息)" % args.min_mega,
        [dict(r) for r in q("""SELECT COALESCE(title,'(untitled)') t, message_count, tool_call_count,
                              ROUND((ended_at-started_at)/3600,1) h FROM sessions
                              WHERE started_at > ? AND message_count >= ? ORDER BY message_count DESC LIMIT 10""",
                            (cutoff, args.min_mega))],
        lambda r: f"{r['t'][:40]:42} {r['message_count']:5} msgs {r['tool_call_count']:4} tools {r['h']}h")

    # 2. abandon-sessions (<=2 msgs)
    rows = q("SELECT COUNT(*) c FROM sessions WHERE started_at > ? AND message_count <= 2", (cutoff,))
    out["abandon"] = {"label": "Abandoned Sessions (<=2 msgs)", "count": rows[0]["c"], "rows": []}
    if not args.json:
        print(f"\n== Abandoned Sessions (<=2 msgs) == {rows[0]['c']}")

    # 3. late-night coding (00-05)
    rows = q("""SELECT COUNT(*) c FROM sessions WHERE started_at > ? AND
                CAST(strftime('%H', started_at, 'unixepoch','localtime') AS INT) < 6""", (cutoff,))
    out["late_night"] = {"label": "Late-Night Sessions (00-05)", "count": rows[0]["c"], "rows": []}
    if not args.json:
        print(f"== Late-Night Sessions (00-05) == {rows[0]['c']}")

    # 4. weekend overwork
    rows = q("""SELECT COUNT(*) c FROM sessions WHERE started_at > ? AND
                strftime('%w', started_at, 'unixepoch','localtime') IN ('0','6')""", (cutoff,))
    out["weekend"] = {"label": "Weekend Sessions", "count": rows[0]["c"], "rows": []}
    if not args.json:
        print(f"== Weekend Sessions == {rows[0]['c']}")

    # 5. cache-hit starvation (input>5K, cache<10%)
    sec("cache", "Prompt Cache Starvation (input>5K, cache<10%)",
        [dict(r) for r in q("""SELECT COALESCE(title,'(untitled)') t, input_tokens, cache_read_tokens,
                              ROUND(cache_read_tokens*100.0/input_tokens,1) pct FROM sessions
                              WHERE started_at > ? AND input_tokens > 5000 AND cache_read_tokens*1.0/input_tokens < 0.1
                              ORDER BY input_tokens DESC LIMIT 10""", (cutoff,))],
        lambda r: f"{r['t'][:40]:42} in={r['input_tokens']:>10,} cache={r['pct']}%")

    # 6. premium waste (cost>$1, output<500 tok) — 免費 model 成本為 0 時自然空
    sec("waste", "Premium Waste (cost>$1, output<500 tok)",
        [dict(r) for r in q("""SELECT COALESCE(title,'(untitled)') t, model, ROUND(estimated_cost_usd,2) cost,
                              output_tokens FROM sessions WHERE started_at > ? AND estimated_cost_usd > 1
                              AND output_tokens < 500 ORDER BY estimated_cost_usd DESC LIMIT 10""", (cutoff,))],
        lambda r: f"{r['t'][:36]:38} {str(r['model'])[:24]:26} ${r['cost']} out={r['output_tokens']}")

    # 7. model mix (30d)
    rows = [dict(r) for r in q("""SELECT s.model, COUNT(*) c, SUM(s.api_call_count) calls
              FROM session_model_usage s JOIN sessions s2 ON s.session_id=s2.id
              WHERE s2.started_at > ? AND s.model IS NOT NULL GROUP BY s.model ORDER BY calls DESC LIMIT 10""", (cutoff,))]
    out["models"] = {"label": "Model Mix (top 10)", "count": len(rows), "rows": rows}
    if not args.json:
        print("\n== Model Mix (top 10) ==")
        for r in rows:
            print(f"  {str(r['model'])[:44]:46} {r['c']:4} sessions {r['calls']:6} calls")

    # 8. verbose output (>20k chars assistant)
    rows = q("""SELECT COUNT(*) c FROM messages WHERE role='assistant' AND content IS NOT NULL
                AND LENGTH(content) > 20000 AND timestamp > ?""", (cutoff,))
    out["verbose"] = {"label": "Verbose Output (>20k chars)", "count": rows[0]["c"], "rows": []}
    if not args.json:
        print(f"== Verbose Output (>20k chars) == {rows[0]['c']}")

    # 9. repeated prompts — 排除系統注入 (skill header/cron/compression)
    sec("repeat", "Repeated Prompts (exact dup, user-origin)",
        [dict(r) for r in q("""SELECT content, COUNT(*) c FROM messages
              WHERE role='user' AND content IS NOT NULL AND timestamp > ? AND LENGTH(content) > 30
              GROUP BY content HAVING c > 1 ORDER BY c DESC LIMIT 10""", (cutoff,)) if
         not r["content"].startswith(("[IMPORTANT","[Your active task","You've reached"))],
        lambda r: f"x{r['c']:3}  {r['content'][:70]}")

    # 10. runaway agent loops
    sec("loops", "Runaway Agent Loops (tool_call_count>100)",
        [dict(r) for r in q("""SELECT COALESCE(title,'(untitled)') t, message_count, tool_call_count, api_call_count
              FROM sessions WHERE started_at > ? AND tool_call_count > 100
              ORDER BY tool_call_count DESC LIMIT 10""", (cutoff,))],
        lambda r: f"{r['t'][:40]:42} {r['message_count']:4} msgs {r['tool_call_count']:4} tools {r['api_call_count']:4} api")

    # 11. instruction-bloat (>5KB instruction files in Projects, 排除 .build/docs i18n)
    bloat = []
    skip_dirs = {"node_modules", ".git", ".next", "dist", "build", ".venv", "venv", ".build"}
    for pat in ("AGENTS.md", "CLAUDE.md", "CONTEXT.md", ".cursorrules"):
        for root, dirs, files in os.walk(PROJECTS):
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.endswith(("-i18n", "i18n"))]
            if pat in files:
                p = os.path.join(root, pat)
                sz = os.path.getsize(p)
                if sz > 5000:
                    bloat.append({"file": p.replace(HOME, "~"), "bytes": sz})
    bloat.sort(key=lambda x: -x["bytes"])
    out["ibl"] = {"label": "Instruction Bloat (>5KB)", "count": len(bloat), "rows": bloat[:10]}
    if not args.json:
        print(f"\n== Instruction Bloat (>5KB, top 10 of {len(bloat)}) ==")
        for r in bloat[:10]:
            print(f"  {r['bytes']:>8,}  {r['file']}")

    # 12. mcp tool bloat (config.yaml mcp_servers 數)
    mcp_count = 0
    cfg = os.path.expanduser("$HERMES_HOME/config.yaml")
    if os.path.exists(cfg):
        in_mcp = False
        for line in open(cfg):
            if line.startswith("mcp_servers:"):
                in_mcp = True
                continue
            if in_mcp:
                import re as _re
                if _re.match(r"^  [A-Za-z0-9_.-]+:$", line):
                    mcp_count += 1
                elif line.strip() and not line.startswith(" "):
                    break
    out["mcp"] = {"label": "MCP Servers in config.yaml (近似)", "count": mcp_count, "rows": []}
    if not args.json:
        print(f"== MCP Servers in config.yaml (近似) == {mcp_count}")

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == "__main__":
    main()
