# Baseline Comparison Pattern

When running verification gates, compare results against the previous run's `loop-output/test-results.md`.

## Regression vs Baseline Failure

| Previous result | Current result | Classification |
|----------------|----------------|---------------|
| ✅ PASS | ✅ PASS | Stable — no action |
| ✅ PASS | ❌ FAIL | **Regression** — needs immediate fix |
| (not present) | ❌ FAIL | **Baseline failure** — new gate or known issue, lower priority |
| (not present) | ✅ PASS | **New gate** — new baseline established |

## Template When Writing Results

```
> Regression from previous run: baseline was taken {date}.
> {n} gates pass, {m} gates fail.
```

### Regression Summary Section
```
## Regression Summary

- **Gates 1–4**: All passing — no regression.
- **Gate 5 (Prettier)**: 27 files need formatting. Baseline failure (new gate), not a regression.
```

## Example: your-project 2026-07-30

Previous run had 3 gates (Python-era: lint + pytest + build). Current run has 5 gates (TypeScript-era: build + tsc + vitest + node:test + prettier). Gates 2 and 5 are new — their failures are baseline, not regressions.
