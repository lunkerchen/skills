---
name: web-monitor
description: Monitor web pages for content changes using no_agent cron scripts with fingerprint-based change detection and silent-when-unchanged alert delivery.
created_by: hermes
---

# Web Monitor

## Overview
Set up automated monitoring of web pages for content changes. Uses a no_agent cron script with fingerprinting and local state storage. Silent when unchanged, alerts only when content changes.

## When To Use
- Monitor e-commerce product gifts/promotions changing over time
- Watch for price drops or availability changes
- Detect when a specific page element updates (specs, descriptions, terms)
- Any periodic check where "silent when unchanged, alert on change" is desired

## How It Works

```
[every 60m] → no_agent script → fetch URL → extract data → 
    fingerprint(extracted) ≠ stored_fingerprint? →
        YES: output new data + URL → cron delivers to Telegram
        NO: silent (empty stdout, no delivery)
```

## Step-by-Step

### 1. Create the Script

Place at `$HERMES_HOME/scripts/<job-name>.py`. Pattern:

```python
#!/usr/bin/env python3
import hashlib, json, os, sys, requests
from bs4 import BeautifulSoup

URL = "https://example.com/product/123"
STATE_FILE = os.path.join(os.path.dirname(__file__), f".{os.path.basename(__file__).replace('.py', '')}-state.json")

def extract_gifts(html):
    """Parse page and return list of dicts with key data to monitor."""
    soup = BeautifulSoup(html, 'html.parser')
    gifts = []
    for promo in soup.select('.promo-item'):  # adjust selector
        gifts.append({
            'promoText': promo.get_text(strip=True),
            'actionUrl': promo.get('href', ''),
        })
    return gifts

def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# Fetch
resp = requests.get(URL, timeout=10)
resp.raise_for_status()
gifts = extract_gifts(resp.text)
fp = fingerprint(gifts)

# Compare
if not os.path.exists(STATE_FILE):
    json.dump({'fingerprint': fp, 'gifts': gifts}, open(STATE_FILE, 'w'))
    sys.exit(0)  # First run: store state, silent

old = json.load(open(STATE_FILE))
if fp == old['fingerprint']:
    sys.exit(0)  # No change: silent

# Change detected: update state, output for delivery
json.dump({'fingerprint': fp, 'gifts': gifts}, open(STATE_FILE, 'w'))
print(f"Content changed!\nURL: {URL}")
for g in gifts:
    print(f"  • {g['promoText']}")
```

### 2. Install Dependencies

```bash
pip3 install requests beautifulsoup4 lxml
```

The base Python (not a project venv) must have all packages — cron jobs don't activate venvs.

### 3. Setup Cron

```bash
cronjob action=create \
  name="web-monitor-product-name" \
  schedule="every 60m" \
  script="job-name.py" \
  no_agent=true \
  deliver="telegram"
```

- `no_agent=true`: the script IS the job. No LLM tokens consumed per tick.
- `script`: relative to `$HERMES_HOME/scripts/`
- `deliver=telegram` or user's preferred platform. Only delivers when stdout non-empty.
- State file auto-creates at `$HERMES_HOME/scripts/.<job-name>-state.json` (dotted prefix keeps ls tidy).

### 4. Verify

```bash
# List jobs
cronjob list | grep web-monitor

# Check logs — pattern: "empty stdout — silent run" = no change
grep "<job_id>" $HERMES_HOME/logs/agent.log

# Read current state
python3 -c "import json; d=json.load(open('$HOME/.hermes/scripts/.<name>-state.json')); print(json.dumps(d, indent=2))"
```

### 5. Manual Test Before Cron

Run the script once to create initial state, then modify the state file's fingerprint to simulate a change and re-run to verify delivery works:

```bash
python3 $HERMES_HOME/scripts/job-name.py  # First run: stores state, silent
# Manually edit .<name>-state.json fingerprint to force a change
python3 $HERMES_HOME/scripts/job-name.py  # Should output "Content changed!"
```

## Design Decisions

### Fingerprint vs Full-page Hash
Fingerprint the *structured extracted data* (e.g. list of gift descriptions), not the raw HTML. A full-page hash changes on any page modification (ads, tracking scripts, layout tweaks) causing false alerts. Structured fingerprint only alerts on the data you care about.

### Why no_agent
- Zero LLM cost per tick (the scheduler runs the script directly)
- Deterministic: no prompt interpretation variance
- Delivery is built-in: non-empty stdout = Telegram notification; empty stdout = silent
- State persists in JSON adjacent to the script

### Why Not Browser (Playwright/Puppeteer)
Browser automation requires managing Chrome/Chromium lifecycle in a cron context. If the browser process isn't explicitly killed, zombie processes accumulate. Only use browser if the page requires JavaScript rendering — and if so, the script must clean up after itself. Prefer `requests` + HTML parsing.

## Pitfalls

- **First-run false alert**: Always have the first run store state and exit silently. Otherwise the user gets a spurious "change detected" alert on setup.
- **Page redesign**: If the website changes its HTML structure, the selectors break silently. The user just stops getting alerts. Periodically verify the script still works manually.
- **Network failures**: On timeout/5xx, exit with code 0 and empty stdout to avoid false alerts. The Cron Health Monitor (`agent-maintenance` skill) catches persistent failures across multiple runs.
- **Symlinks not supported**: `$HERMES_HOME/scripts/` rejects symlinks pointing outside the directory. Use `cp` for standalone copies.
- **State file naming**: Prefix with `.` so `ls` doesn't clutter the scripts directory — e.g. `.monitored-site-state.json`.
- **Path to script**: `$HERMES_HOME/scripts/` is the default. The cron scheduler resolves relative script paths there.
- **Dependency drift**: If you upgrade `requests` or `beautifulsoup4`, verify the script still works. Add a version check or a periodic manual test.
- **Multiple monitors per product page**: If you monitor both price AND gifts, use two separate data keys in the state file or two separate state files — don't mix concerns.
