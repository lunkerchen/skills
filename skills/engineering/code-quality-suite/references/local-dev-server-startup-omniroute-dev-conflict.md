# OmniRoute Dev Instance Conflict (2026-07-21)

## Context
Engineer has OmniRoute installed via two paths:
1. **System-managed production** — launchd agent `com.omniroute.plist` running binary at `~/.local/bin/omniroute` on port 20128
2. **Git clone** — `/Users/your-user/Developer/Projects/OmniRoute` on branch `feat/i18n-zh-tw`

Goal: update the git clone to v3.8.48 and run it.

## Sequence of Events

1. `git pull` on a branch 320 commits behind → merge resolved with 750 files changed
2. `npm run build` failed — missing `omniglyph` dependency
3. `npm install` fixed the missing dep
4. Build succeeded → `npm run start` failed (EADDRINUSE on 20128)
5. `lsof -i :20128` showed Comet.app network helper (PID 24847) and an omniroute process (PID 24851)
6. Killing the process → immediate respawn by launchd (KeepAlive=true)
7. RTK wrapper created zombie processes
8. Comet Helper kept respawning on the same port
9. Port override to 20129 → worked but user's browser was on 20128
10. Building production `standalone/` output required running from within that directory; path mismatch with `npm run start`
11. Dev server (`node scripts/dev/run-next.mjs dev`) worked after discovering locale-prefixed routes (`next-intl` i18n)
12. Final resolution: `PORT=21128 node scripts/dev/run-next.mjs start`

## Key Discovery

Found `com.omniroute.plist` in `~/Library/LaunchAgents/`:
- Runs `~/.local/bin/omniroute` (the system install, not the git clone)
- KeepAlive=true → always respawns
- RunAtLoad=true → starts on login
- This is a separate binary from the git clone — updating the git repo does NOT update the system install

## Key Commands

```bash
# Check launchd-managed instances
launchctl list | grep -i omni

# View launch agent config
cat ~/Library/LaunchAgents/com.omniroute.plist

# Port conflict diagnosis (multiple layers)
lsof -i :20128 -P | grep LISTEN
ps -p <PID> -o pid,comm,args

# Confirm respawn (kill then re-check)
kill -9 <PID>; sleep 2; lsof -i :20128 | grep LISTEN

# Dev server on alternate port
PORT=21128 node scripts/dev/run-next.mjs start

# Production build
npm run build
```

## OmniRoute API Testing (No Auth on Localhost)

OmniRoute accepts requests on `localhost` without an API key:

```bash
# List models
curl -s http://localhost:20128/v1/models

# Test a chat completion
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto/best-fast","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'

# With retries disabled (fast failure)
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"<model>","messages":[{"role":"user","content":"hi"}],"retries":0,"max_tokens":5}'
```

This is useful for quickly verifying a model/provider works before wiring it into Hermes as a provider.

## Antigravity OAuth Pitfall

When testing antigravity models through OmniRoute, all models fail with:

```
[antigravity/<model>] [422]: Missing Google projectId for Antigravity account.
Auto-discovery via loadCodeAssist found no Cloud Code project.
Please reconnect OAuth in Providers → Antigravity
(and ensure the Google account has completed Gemini Code Assist onboarding).
```

**Root cause:** The OAuth connection is established (shown as 3 connections in the OmniRoute dashboard) but tied to a Google account that hasn't set up a Cloud project with Gemini Code Assist enabled. The OAuth token lacks a `projectId` binding.

**Fix:** Reconnect OAuth in OmniRoute Providers → Antigravity, using a Google account that has:
- A Google Cloud project (billing-enabled or trial)
- Gemini Code Assist enabled on that project
- The OAuth consent screen configured

Or route through other providers (auto/best-fast → opencode-zen, nvidia, openrouter) instead.

## Key Commands (expanded)

```bash
# List all models available through OmniRoute (includes model IDs for all providers)
curl -s http://localhost:20128/v1/models | python3 -m json.tool

# Count models per provider
curl -s http://localhost:20128/v1/models | python3 -c "
import json, sys
models = json.load(sys.stdin)
counts = {}
for m in models.get('data', []):
    model = m.get('id', '')
    provider = model.split('/')[0] if '/' in model else 'other'
    counts[provider] = counts.get(provider, 0) + 1
for p, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'{p}: {c}')
"

# Test specific provider/model
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"<provider>/<model>","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

## Lesson
Distinguish between system-managed (launchd/brew) instances and git-cloned dev copies early. Port override avoids disrupting the user's production instance and avoids launchd respawn loops.
