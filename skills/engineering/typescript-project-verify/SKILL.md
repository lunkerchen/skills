---
name: typescript-project-verify
description: 'Run after builds/deploys: 5-gate verification for TypeScript monorepos — tsc, vitest, build, format, smoke.'
category: engineering
---

# TypeScript Project Verification Gates

Standard 5-gate verification sequence for TypeScript monorepos with a Vite/React frontend and Hono/Cloudflare Workers backend (e.g., your-project).

## Standard 5-Gate Sequence

```bash
# === Gate 1: Frontend build (tsc + vite + static pages) ===
cd frontend && npm run build 2>&1

# === Gate 2: Backend type check ===
cd backend-api && npx tsc --noEmit 2>&1

# === Gate 3: Backend tests ===
cd backend-api && npx vitest run 2>&1 | tail -30

# === Gate 4: Frontend Node.js tests (Cloudflare Pages Functions) ===
cd frontend && node --test functions/*.test.js 2>&1

# === Gate 5: Code formatting check ===
cd backend-api && npx prettier --check src/ 2>&1 || true
```

## Results Format

Write to `loop-output/test-results.md`:

```markdown
| # | Gate | Result (PASS/FAIL/SKIP) | Detail |
|---|------|------------------------|--------|
| 1 | Frontend Build | ✅ PASS | ... |
| 2 | Backend tsc | ✅ PASS | ... |
```

Compare against the previous run's baseline. If any gate FAILs, classify as:
- **Regression**: was PASS in previous run, now FAIL → needs urgent fix
- **Baseline failure**: new gate or known pre-existing issue → lower priority

## Pitfalls

### `node --test` relative path
When you `cd frontend`, the test glob is `functions/*.test.js`, NOT `frontend/functions/*.test.js`. Running with the wrong path produces `1..0 (0 tests)` — no error, just zero tests discovered.

### Project Root Discovery
The project may be at a different path than expected. Common locations:
- `$DEV_PROJECTS/your-marketplace/` (legacy Python-era path)
- `$DEV_PROJECTS/your-project/` (current TypeScript-era path)

Check both if `cd` fails.

### Prettier check as new gate
Prettier is often not part of the CI pipeline. When adding it as a new gate, expect baseline failures. Auto-fix with:
```bash
cd backend-api && npx prettier --write src/
```

### Interpret test output
- `npm run build` output: look for "✓ built in Xms", PWA generation messages, and module count
- `npx tsc --noEmit`: empty output + exit code 0 = clean. Any `error TSxxxx:` is a failure
- `vitest run` tail: look for "Test Files X passed (X)" and "Tests X passed (X)" in the last few lines. Failures appear as `✗` in the body
- `node --test` output: TAP format. `# tests 10 / # pass 10 / # fail 0` = clean
- `prettier`: `[warn]` lines = unformatted files; no output = clean
