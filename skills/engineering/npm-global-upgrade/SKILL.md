---
name: npm-global-upgrade
description: Upgrade npm globals handling allow-scripts and symlinks.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [npm, upgrade, maintenance, macos]
    category: devops
---

# npm-global-upgrade Skill

Check and upgrade globally-installed npm packages on macOS, handling npm's install-scripts allow-list, symlinked local dev repos, dependency-pinned conflicts, and OSV advisory noise.

## When to Use

- User asks to check which npm packages have updates (`npm outdated -g` scenario)
- User asks to upgrade global tools (wrangler, codex, opencode, playwright, ...)
- `npm install` output shows `npm warn install-scripts` blocked scripts

## How to Run

1. **Check**: `npm outdated -g` — lists Current/Wanted/Latest per package.
2. **Inspect symlinks first**: `npm ls -g --depth=0`. Any package shown as `-> /path/to/dir` is a symlinked local dev repo (e.g. your-tool → $DEV_PROJECTS/your-tool). **Never `npm install -g` those** — it breaks the link. Update them via git instead (see its maintenance skill).
3. **Batch upgrade**: `npm install -g pkg1@latest pkg2@latest ...` (one command, one resolve pass).
4. **Handle allow-scripts**: npm blocks postinstall scripts for packages not in the allow list (fsevents, workerd, esbuild, opencode-ai, ...). Verify the binary still works before chasing it: `node -e "require('<pkg>')"` or run the bin directly. If it loads, the block is harmless — just persist the list so future installs stay quiet: `npm config set allow-scripts=fsevents,workerd,esbuild,opencode-ai --location=user`.
5. **OSV advisory triage**: npm may flag `[HIGH] Package has live OSV advisory data`. These are often historical advisories. Look up the GHSA id, read the "fixed in" version, compare to the version you just installed. If current >> fixed, ignore (real examples: GHSA-8c93-4hch-xgxp wrangler fixed <3.1.1; GHSA-vxw4-wv6m-9hhh / GHSA-c83v-7274-4vgp opencode-ai fixed 1.0.216 / 1.1.10).
6. **Verify**: `npm outdated -g` should be empty (minus symlinked repos).

## Pitfalls

- **Dependency-pinned staleness**: `npm outdated -g` may show a package that won't move because a symlinked repo's dependency tree pins it (real case: your-tool's `@playwright/test@1.61.1` kept top-level `playwright@1.61.1`). Force the top level: `npm install -g playwright@X.Y.Z`; the old version nests inside the symlinked repo's tree — that's fine, not a conflict.
- **`--allow-scripts` is NOT allowed in project-scoped installs.** Use the package.json `allowScripts` field or a repo `.npmrc` instead. It only works for global installs.
- **Checking whether a service listens: query the exact port.** `lsof -iTCP:<port> -sTCP:LISTEN`. A `lsof -iTCP -sTCP:LISTEN | grep ... | head -N` list truncates and produced a false "server is down" conclusion (the port was listening past the head cutoff). Verify before declaring a service dead.
- **Blocked postinstall ≠ broken install.** npm blocks the script but ships the binary; require/bin check decides.
- After upgrading a tool that runs as a persistent server, remember the running process still executes old code — rebuild + restart it (see its maintenance).

## Verification

- `npm outdated -g` shows only symlinked local repos (expected) or nothing.
- `npm config get allow-scripts` shows the persisted list.
- Each upgraded package's bin runs (`pkg --version`).
