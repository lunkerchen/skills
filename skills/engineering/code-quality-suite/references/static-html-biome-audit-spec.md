---
name: static-html-biome-audit
description: Biome lint for single HTML. Fix CSS/a11y/semantic.
---

# Static HTML Biome Audit

Run `@biomejs/biome` on a standalone `.html` file and fix all findings. Designed for single-file pages with inline `<style>` and `<script>`.

## When to Use

- User asks "用 biome 掃一下專案" or "跑 lint" on a single HTML file
- Pre-deployment quality gate for static HTML pages
- Part of a broader static-html-polish workflow (run this step before RWD/SEO audit)

## Workflow

### 1. Run Biome Check

```bash
npx @biomejs/biome check <file>.html
```

**`biome` on PATH may be the WRONG package.** On this Mac, `$HOME/.local/bin/biome` is the env-manager `biome@0.3.3` (dotenv-style tool), NOT the linter — running it outputs `ESLint output (JSON parse failed: EOF...)` and exits 1. Always invoke the real linter via `npx --yes @biomejs/biome`; version check: `npx --yes @biomejs/biome --version` → `Version: 2.5.6`. Prefer `npx --yes` so a stale local copy never shadows latest.

**Biome 2.x flag syntax (verified 2026-08):** boolean flags REQUIRE `=true`/`=false`.
- ✅ `./node_modules/.bin/biome check --files-ignore-unknown=true .`
- ❌ `biome check --files-ignore-unknown .` → "unexpected argument" error, wasted run.
When scanning a whole project dir, add `--files-ignore-unknown=true` so HTML files don't trip over non-linted types.

**Pre-flight (repo context):** before linting/committing a static site, check what you're actually working against:
- `git worktree list` — stale worktree branches (e.g. `.worktrees/v2`) may still hold OLD content AND their tests get picked up by vitest (`npx vitest` scans all worktrees). Confirm which branch is the live one before trusting "all tests pass" or editing.
- `.vercel/project.json` — reveals the actual deployed project id/name; no `git remote` means the deploy path is local `vercel --prod`, not push-based. Don't assume a remote exists.
- `git remote -v` empty + uncommitted changes = changes live on one disk only. Commit protection before deploy.

### 2. Common Fix Patterns

| Issue | Fix Strategy |
|-------|-------------|
| `noDescendingSpecificity` | Reorder CSS rules: lower-specificity selector must appear before higher-specificity. Swap the rule blocks. |
| `noImportantStyles` | Run `--unsafe` auto-fix: `npx @biomejs/biome check --write --unsafe <file>.html` — safe for `prefers-reduced-motion` `!important` overrides. **Intentional `!important` (e.g. RWD inline-grid overrides that classes can't beat):** `/* biome-ignore lint/complexity/noImportantStyles: ... */` comments in CSS are NOT honored — Biome reports `suppressions/unused` ("Suppression comment has no effect"). Fix = project-level `biome.json` disabling the rule: `{ "linter": { "rules": { "complexity": { "noImportantStyles": "off" } } } }`. Keep biome.json comment-free (strict JSON validators reject comments) and explain the RWD rationale in the commit so the disable isn't cargo-culted. |
| `useAriaPropsSupportedByRole` | The ARIA attr needs a supporting `role`. Add `role="group"` to the element, or better: remove redundant ARIA when the semantic relationship is already clear from visible markup. |
| `useSemanticElements` | Replace `<div role="list">` → `<ul>`, `<div role="group">` → `<fieldset>` (or just remove ARIA). For rollup-style meta lists, convert `<div class="cta-meta">` to `<ul class="cta-meta">` with `<li>` children. Remember to reset `list-style`, `margin`, `padding` on the `<ul>`. |
| `noArguments` (inline `<script>`) | HTML comment suppression (`<!-- biome-ignore ... -->`) does NOT work on inline `<script>` blocks — Biome's HTML parser can't attach suppression to JS inside HTML. Must actually refactor: replace `arguments` usage with rest params (`function(...args)`), or `Array.from(arguments)`. Third-party minified snippets (GA4, Meta Pixel) → rewrite only the flagged construct, don't auto-format the whole blob. **Two-step trap:** after fixing with `function(...args)`, Biome fires `useArrowFunction` (FIXABLE) on the same expression if it doesn't use `this` — go straight to arrow `(...args)=>` in one edit to avoid a second run. |
| `noScriptSrc` / `noVoid` on `javascript:` links | Privacy/legal links using `href="javascript:void(0)"` trip both a11y and security rules. Convert the anchor to `<button type="button">` — keeps the handler, satisfies both rules. |
| Test-file churn on `--write` | Biome auto-formats test files; a 500+ line whitespace-only diff in `__tests__/*.test.js` is normal and safe, but commit it separately from the feature change to keep history readable. |

### 3. Iterate Until Clean

```bash
npx @biomejs/biome check <file>.html
# exit 0 = clean
```

## Verification

- No errors or warnings from Biome
- Visual diff confirms the page still renders correctly (no broken CSS, no layout shifts)
- **Mobile sanity (overflow + grids + touch targets):** run `scripts/verify-mobile-overflow.js <url> 390 844` (needs `npm i playwright-core` + `npx --yes playwright install chromium` once). It asserts `document.documentElement.scrollWidth <= window.innerWidth` at the viewport and prints computed `gridTemplateColumns` for the common RWD classes — a single-length result (e.g. `"300px"`) means that grid folded to 1 column. Use it after any responsive edit: `overflow-x:hidden` on `html`/`body` plus `touch-action:pan-y` should make overflow impossible, but inline `style="grid-template-columns:repeat(4,minmax(0,1fr))"` grids need the `!important` attribute-selector overrides (see rwd-mobile-rules) — the probe's `div[style*="repeat(4"]` selector confirms those actually applied.
- **Card-count check:** after adding the Nth card to a staggered grid (`.reveal-delay-N`), verify the CSS class actually exists for N — the definition list often caps at 5 while content grew to 6. `search_files(pattern='reveal-delay-[0-9]')` and compare max in CSS vs max in markup. Also add a tablet breakpoint (`repeat(2,1fr)`) when a grid grows past 4 columns at ~968px.

## Session Reference

- `references/session-example.md` — real run transcript: Biome 2.x flag error, inline-script suppression failure, javascript: URL conversion, worktree/vitest interplay, commit-splitting pattern.
- `references/deployed-landing-hardening.md` — P0 checklist for DEPLOYED single-page sites: canonical/robots/sitemap, og:image file existence (curl → 200), llms.txt freshness, conditional tracking-ID loading (GA4/Pixel/Turnstile placeholders), click-to-load YouTube iframe (incl. the empty-iframe-eats-clicks pitfall + thumbnail placeholder), Pillow og-cover generation. Use after Biome is clean when the page is about to go live.
- `references/backend-less-admin-github.md` — when the user wants an admin/content backend on a static site: videos.json source of truth + admin.html editing via GitHub Contents API (token in localStorage, `btoa(unescape(encodeURIComponent(...)))` for CJK, sha for PUT), deploy-gap pitfall, front-page fallback + multi-item thumbnail grid.
