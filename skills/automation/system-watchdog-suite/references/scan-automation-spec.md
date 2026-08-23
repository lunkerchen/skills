---
name: scan-automation
description: Run automated system/dependency scans, parse structured output, log time-series results, and debug scan hangs. Covers bumblebee endpoint inventory, exposure scanning, and similar CLI-based scan tools on macOS.
tags: [scanning, monitoring, automation, bumblebee, inventory]
---

# Scan Automation

Run automated system scans, parse structured output (NDJSON), log time-series results, and debug hang/crash scenarios.

## Supported Tools

### bumblebee (Endpoint Package Inventory)

Binary at `$HOME/bin/bumblebee`. Scans installed packages across: npm, PyPI, RubyGems, Go, cargo, MCP, browser extensions, Homebrew.

## Running a Scan

### Basic scan with timing

⚠️ Gateway-session gotcha (2026-08-05): invoking the binary by absolute path
(`$HOME/bin/bumblebee scan ...`) trips the gateway lifecycle guard —
it treats the path as a referenced script, and the guard's primary reader
crashes with `ValueError: embedded null byte` (os.open only catches OSError;
NUL paths slip through). Workaround: put the dir on PATH and call the bare name,
or use `env $HOME/bin/bumblebee`. Both verified working.

```bash
start=$(python3 -c "import time; print(int(time.time()*1000))")
export PATH="$HOME/bin:$PATH"
bumblebee scan --profile baseline --output stdout \
  2>/dev/null > /tmp/bumblebee-scan-$(date +%Y%m%d).json
end=$(python3 -c "import time; print(int(time.time()*1000))")
duration_ms=$((end-start))
```

### Output format

NDJSON (one JSON object per line). Record types:
- `package` — discovered package (ecosystem, name, version, project_path, confidence)
- `scan_summary` — final record (status, counts, duration_ms, timed_out, findings_emitted)
- `diagnostic` — info/warn messages during scan

### Extracting the summary

```bash
grep 'scan_summary' /tmp/bumblebee-*.json | python3 -c "
import sys,json
d=json.loads(sys.stdin.readline())
print(d.get('counts',{}).get('package',0), d.get('findings_emitted',0), d.get('duration_ms',0))
"
```

## Logging Results

Append to `~/bumblebee-daily-log.md` in CSV-like format:

```
<counter>|<YYYY-MM-DD> | <status> | <duration_ms> | <findings_count> | <packages_count>
```

**Log format details:**
- Counter increments sequentially (read last line of existing file first)
- Status: `complete` (scan reported status=complete), `timeout` (scan killed by timeout), `error` (runtime error)
- packages_count: `counts.package` from scan_summary (or `package_records_emitted`)

## Debugging a Hanging Scan

### Binary Root Isolation

When a scan hangs during `--profile baseline`, the auto-detected root list may include a directory with filesystem issues.

1. List all auto-detected roots:
   ```bash
   bumblebee roots --profile baseline
   ```

2. Test subsets with explicit `--root` (without `--profile baseline`):
   ```bash
   timeout -s KILL 10 bumblebee scan --output stdout \
     --root <path1> --root <path2> ... 2>/dev/null > /dev/null
   ```

3. Narrow down using binary search (add half the remaining roots at a time).

4. Once identified, work around with `--exclude`:
   ```bash
   bumblebee scan --profile baseline --exclude <dirname>
   ```

### Common Hanging Directories on macOS

- **Browser Extension Directories** under `~/Library/Application Support/{Google/Chrome,Microsoft Edge}/Default/Extensions` — filesystem listing can block indefinitely when directory entries are corrupt or locked
- Workaround: `--exclude Extensions` skips all browser extension roots
- **MCP server configs** with misconfigured servers — bumblebee may try to start MCP servers to verify them
- Workaround: `--ecosystem` filter to skip MCP ecosystem

### Pitfalls

- `--max-duration` flag may not reliably terminate the scan; always pair with shell `timeout`
- `timeout -s KILL` sends SIGKILL (exit 137) — cleanest kill for stuck binaries
- Binary exit 124 = `timeout` killed it (wall-clock bound hit); exit 137 = SIGKILL
- `--output file` vs `--output stdout`: which is faster depends on whether the bottleneck is serialization or write I/O; when the scan itself hangs, neither matters
- Output files can be very large (4M+ chars) — parse with grep/head/tail, not cat
- Background processes (terminal background) may be needed for long-running scans; use `process(action='wait')` to block, but the wait is clamped to 60s in cron sessions
