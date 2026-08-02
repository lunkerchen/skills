# Session Examples

## 1. landing-wireframe.vercel.app

### File
Single HTML (~64KB) with inline `<style>` and inline `<script>`. Hand-drawn wireframe aesthetic using `oklch()` colors, custom fonts, `skew`/`rotate` transforms.

### Biome Issues Found & Fixed

| Issue | Count | File Ref |
|-------|-------|----------|
| `noImportantStyles` | 3 | `prefers-reduced-motion` block — auto-fixed with `--unsafe` |
| `noDescendingSpecificity` | 1 | `.tab .tab-mark::before` (0,2,1) appeared after `.tab[aria-pressed="true"] .tab-mark::before` (0,3,1) — swapped order |
| `useAriaPropsSupportedByRole` | 2 | `aria-labelledby` on plain `<div>` — removed (heading already in markup); `aria-label` on `<div>` — converted to `<ul>` |
| `useSemanticElements` | 2 | Changed `<div class="cta-meta">` with 4 `<span>` to `<ul class="cta-meta">` with `<li><span>`; added CSS reset (`list-style:none; margin:0; padding:0`) on the `<ul>` |

### Key Lessons

- Biome v2.5.6 handles HTML with inline JS/CSS natively
- `--write --unsafe` is safe for `!important` in `prefers-reduced-motion` blocks
- CTA meta badge lists are good candidates for `<ul>` semantic conversion
- Always add `list-style: none; margin: 0; padding: 0` when converting `<div>` to `<ul>`

## 2. course-landing-yongtai (批貨課程網站)

### Context
Landing page updated in 3 rounds (course months → Sep–Dec, featured badge move, 6 testimonial cards), then `biome check` run as a pre-deploy gate. Single `index.html` + GAS backend (`Code.gs`) + vitest tests.

### Biome 2.x flag error (first run failed)
```
$ ./node_modules/.bin/biome check --files-ignore-unknown . 
→ "unexpected argument" — Biome 2.x requires boolean flags with =true/=false
$ ./node_modules/.bin/biome check --files-ignore-unknown=true .  # ✅ exit 0
```

### Issues Found & Fixed (3 errors + 3 warnings)

| Issue | Fix |
|-------|-----|
| `noArguments` ×2 (GA4 + Meta Pixel inline scripts) | Tried `<!-- biome-ignore -->` HTML comment first — **does not work inside inline `<script>`**. Refactored `function(...args)` → rest params / arrow function. For third-party minified blobs, change only the flagged construct. **Follow-on:** after `function(...args)`, Biome flagged the same expression with FIXABLE `useArrowFunction` — rewrote once more to arrow `(...args)=>` (no `this` usage, safe) and got to zero. One-shot it: arrow + rest params in a single edit. |
| `noVoid` / a11y on `href="javascript:void(0)"` (privacy link) | Converted `<a href="javascript:void(0)">` → `<button type="button">`. Satisfies both security and a11y rules in one edit. |
| Test file formatting | `--write` reformatted `__tests__/form.test.js` (563-line whitespace churn, 38 tests still pass). Safe, but commit separately from feature change. |

### Non-biome findings during verification
- **Card-count check:** 6th testimonial card used `reveal-delay-6`, but CSS only defined up to `reveal-delay-5` → added the missing class + tablet `repeat(2,1fr)` breakpoint.
- **Worktree trap:** `.worktrees/v2` (branch `v2`) still had Jul/Aug dates; vitest ran BOTH main and v2 test suites (76 = 38×2, all pass). Checked `git worktree list` + `.vercel/project.json` (project `course-landing-yongtai`) to confirm main was the deploy source.
- **No remote:** `git remote -v` empty → changes only on local disk; committed locally (`060608c`) before deploy decision.
- **Backend placeholder:** `SHEET_URL` in `api/submit.js` still `YOUR_DEPLOYMENT_ID` — form fails safely with a "尚未完成設定" message; not a blocker but flag it.

### Key Lessons
- HTML comment suppression does NOT apply to inline `<script>` content — refactor or configure biome.json instead
- Boolean Biome flags need `=true`
- After growing any staggered grid, verify the CSS delay class exists for the new max N
- Stale git worktrees are both content hazards and test-suite doubles — verify which branch is live before trusting "all tests pass"

### Multi-section sync checklist (course landing pages)
Class names/dates live in 8+ places in this file. Changing 開課班別 means sweeping ALL:
JSON-LD `hasCourseInstance[]` (name + ISO startDate) · FAQ `acceptedAnswer` · hero `card-label` + CTA onclick · schedule cards (badge/h3/onclick) · form price strip summary · form `<select>` options (+ `（熱門推薦）` marker) · CSS grid `repeat(N,1fr)` (+ tablet 2-col breakpoint for 4+ cards) · featured badge position.
Dates follow "first Sunday of the month" — derive with Python, don't eyeball. After the edit, `grep` for the old month names (both 七月 and 7月 forms) to confirm zero residue.
