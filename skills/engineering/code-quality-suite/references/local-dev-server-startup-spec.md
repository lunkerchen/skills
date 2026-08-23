---
name: local-dev-server-startup
description: "Start dev servers on macOS alongside system-managed instances — diagnose port conflicts, handle launchd/brew service respawn loops, use port overrides. Use when user asks to start/restart a server from a git clone and you need to avoid disrupting existing services."
triggers:
  - "重新啟動 server"
  - "啟動*server"
  - "Start*server"
  - "npm run dev"
  - "npm run start"
  - "dev server"
---

# Local Dev Server Startup & Service Conflicts

When user asks to start a server from a git clone, the project may already be running as a **system-managed service** (launchd on macOS, systemd on Linux, Homebrew services). Always check before starting.

## Diagnosis Sequence (run in parallel)

```bash
# 1. Check for system-managed instances
launchctl list | grep -i <project-name>
brew services list | grep -i <project-name>

# 2. What's actually on the port?
lsof -i :<default-port> -P 2>/dev/null | grep LISTEN

# 3. Check for launch agents
ls ~/Library/LaunchAgents/*<project>* 2>/dev/null
cat ~/Library/LaunchAgents/com.<project>.plist 2>/dev/null

# 4. Confirm respawn behaviour
kill <PID>; sleep 2; lsof -i :<port> | grep LISTEN
```

If the process respawns after kill → it's launchd (KeepAlive=true). Do NOT try to kill-loop.

## Resolution Strategies (ordered by safety)

### A. Port override (safest — no service disruption)

Start the dev server on a different port:

```bash
PORT=21128 npm run dev
PORT=21128 node scripts/dev/run-next.mjs start
```

Tell the user: "System-managed instance stays on the default port. Dev version is on PORT N."

### B. Unload launch agent (temporary)

```bash
# Stop launchd management
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.<project>.plist

# Dev server now works on default port. Reload later:
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<project>.plist
```

### C. Stop Homebrew service

```bash
brew services stop <project>
```

## macOS Pitfall: Desktop App Network Helpers

Desktop apps (e.g., Hermes client / Comet.app) often run a network helper that occupies a specific port and respawns when killed. Resolution: port override (A), or quit the desktop app entirely.

## End-of-Session Rules

- **If you unloaded a service**: restart it (`bootstrap`) before finishing, or explicitly tell the user it's stopped.
- **If you used port override**: nothing to restore — the system service stays up.
- **Do not kill the user's long-running dev server** at end of session unless asked.

## Related

- `engineering-local-maintenance` (manually authored) — broader project maintenance, removal, system diagnostics.
- Reference: `omniroute-dev-conflict.md` (in references/) — OmniRoute port/launchd conflict, no-auth localhost testing, model verification, and antigravity OAuth troubleshooting.
