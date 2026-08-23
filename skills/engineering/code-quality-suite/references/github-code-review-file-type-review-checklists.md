# File-Type Review Checklist Injection

> Pattern: 動態掃描 diff 中的 changed files，映射到領域審查重點，
> 將 matched checklists 的 union 注入 reviewer subagent context。
> 來源設計: [shyuan/skills opencode-review](https://github.com/shyuan/skills/tree/main/skills/opencode-review)

## How It Works

1. `git diff <base>...HEAD --name-only` → 取 changed file list
2. 每個 file 走 first-match 規則匹配 checklist（glob pattern）
3. 取所有 matched checklists 的 union → 動態 prompt fragment
4. 注入到 `delegate_task` 的 reviewer `context` field

## Checklist Registry

第一個匹配的 pattern 生效（first-match wins）:

### `*.sql` / `*migration*` / `*schema*`
- [ ] SQL injection: raw string interpolation in queries?
- [ ] Migration rollback plan exists? Down migration written?
- [ ] Index impact: new indexes on large tables?
- [ ] Column type changes: data loss risk on existing rows?
- [ ] Foreign key constraints: ON DELETE/UPDATE behavior?
- [ ] Transaction boundaries: partial commit risk?

### `*.{ts,tsx,js,jsx}`
- [ ] XSS: innerHTML / dangerouslySetInnerHTML / DOMPurify usage?
- [ ] State management: stale closure / missing dependency in useEffect?
- [ ] Type safety: `any` escape hatches in new code?
- [ ] Event handler cleanup: addEventListener without remove?
- [ ] Async error: unhandled Promise rejection / missing try-catch?
- [ ] Bundle impact: large import that should be lazy/dynamic?

### `*.{py}`
- [ ] Injection: f-string / format in SQL / shell / eval?
- [ ] Resource cleanup: file/DB connections closed? context manager used?
- [ ] Type hints: missing on public function signatures?
- [ ] Pickle / exec / eval with external input?
- [ ] N+1 query pattern in loops?
- [ ] Exception handling: bare `except:` / swallowed errors?

### `*.{go}`
- [ ] Error handling: `_` discarding error return?
- [ ] Goroutine leak: no context cancellation / WaitGroup mismatch?
- [ ] Race condition: shared state without mutex?
- [ ] Resource leak: unclosed HTTP body / DB rows / file handle?
- [ ] Defer in loop: deferred cleanup delayed until function return?

### `*.{css,scss,less}`
- [ ] z-index wars / !important overuse?
- [ ] Mobile: touch target < 44px?
- [ ] Dark mode: hardcoded colors ignoring theme variables?
- [ ] Print stylesheet: page-break / visibility concerns?

### `*.yaml` / `*.yml` / `*.toml` / `*.json` (config files)
- [ ] Secrets / credentials hardcoded?
- [ ] Default values safe for production?
- [ ] Breaking change in config schema?
- [ ] Required fields missing defaults (will break on deploy)?

### `*.{sh,bash}`
- [ ] Shell injection: unquoted variables / eval on user input?
- [ ] set -e / set -o pipefail present?
- [ ] Hardcoded paths that won't exist in CI?
- [ ] Temporary file cleanup?

### `Dockerfile` / `docker-compose*`
- [ ] Base image pinned to digest or latest?
- [ ] Multi-stage build (don't ship build tools)?
- [ ] Secrets in build args (baked into image layers)?
- [ ] Health check defined?

### `*.tf` / `*.hcl` (Terraform)
- [ ] State backend configured?
- [ ] Variables with defaults safe?
- [ ] Destroy-recreate vs in-place update (lifecycle rules)?
- [ ] Sensitive outputs marked?

### `test*` / `*test*` / `*spec*`
- [ ] Assertions actually verify behavior (not just "no crash")?
- [ ] Edge cases covered (empty, null, boundary)?
- [ ] External dependency mocked (no live API/DB in unit test)?
- [ ] Test isolation: shared state between tests?

### `*migration*` / `*seed*`
- [ ] Idempotent: can run twice without error?
- [ ] Production-safe: no test data in prod seed?
- [ ] Ordered correctly: dependencies satisfied?

### Default (no match)
- [ ] Secrets / credentials visible?
- [ ] TODO/FIXME/HACK left behind intentionally?
- [ ] Error handling present?
- [ ] Debug logging / console.log removed?

## Usage in delegate_task

```python
# Step 1: get changed files
files = terminal("git diff main...HEAD --name-only")

# Step 2: match checklists (conceptual — do this in the orchestrator's reasoning)
# For each file, first-match against patterns above.

# Step 3: inject into reviewer context
checklists = dedupe(matched_checklists)
reviewer_context = f"""
{checklists}

<code_review_focus>
In addition to general review criteria, pay EXTRA attention to the
file-type-specific checklist items above. Flag violations explicitly.
</code_review_focus>
"""

# Step 4: delegate_task with enriched context
delegate_task(
    goal="Review this diff for correctness, security, and design...",
    context=reviewer_context + diff_text
)
```

## Customization

Add project-specific rules by extending this file. Common additions:
- `*wrangler*` / `wrangler.toml` → Cloudflare Workers / D1 / KV review
- `*.astro` → Astro island architecture, SSR vs SSG correctness
- `*schema.prisma` → Prisma migration safety
- `*firebase*` → Security rules, Firestore indexing
