---
name: subagent-efficiency
description: >-
  Patterns for deciding when to use delegate_task (subagents) vs direct execution.
  Every subagent spawn has overhead — inference startup, context initialization,
  result summarization. This skill catalogs cases where direct execution is faster
  and cases where delegation is worth the cost.
version: 0.1.0
tags: [delegation, efficiency, subagent, optimization]
---

# Subagent Efficiency

`delegate_task` spawns a full subagent with its own context window, model inference,
and toolset. This is powerful for complex tasks but wasteful for trivial ones.

## When NOT to delegate

Spawn a subagent only when the task genuinely benefits from isolated context.
Fix these directly in the main session:

| Task type | Example | Cost of delegating |
|-----------|---------|-------------------|
| Auto-format | `npx prettier --write src/` | ~2K+ context tokens for a single terminal call |
| Package reinstall | `rm -rf node_modules && pnpm install` | Subagent spends time rediscovering your project structure |
| Git cleanup | `git clean -fd`, `git restore .` | Subagent doesn't have your git context |
| Simple file write | `write_file(path, content)` | Subagent needs full context about why and where |
| Single-command test run | `npx vitest run` | Output is small enough for main context |
| Formatting fix in verification loop | Prettier/Biome/ruff format failure | Spawning a Fixer subagent adds 30-90s for a 1s fix |

**Threshold rule of thumb:** If the fix fits in one terminal command (or one tool call)
and has no side effects, execute it directly. If it requires reading files, making
judgments, looping, or multi-step changes, use a subagent.

## When TO delegate

| Task type | Example | Why delegate |
|-----------|---------|-------------|
| Code audit / discover | Scan a large codebase and report | Keeps thousands of lines out of main context |
| Multi-file bug fix | Read 3-5 files, understand logic, patch | Needs its own reasoning chain |
| Parallel independent work | Backend + frontend changes | Runs concurrently with other work |
| Research + synthesis | Web research, compare options | Keeps long web results contained |
| Complex debugging | Stack trace → root cause → fix | Full debug chain doesn't clutter main session |

## Formatting shortcut in loops

When running a verification loop (loop-fix or similar):
- Test phase runs formatting checks (Prettier, Biome, ruff, etc.)
- If the only failure is formatting → fix with the format command directly
- Then re-run just the formatting gate to confirm
- Proceed to phase=done — skip the Fixer subagent entirely

This avoids the ~30-90s overhead of spawning, warming up, and summarizing
a subagent for what amounts to a one-liner.

## Related

- `loop-fix` — the verification loop this pattern was discovered in
- `hermes-parallel` — delegation patterns for parallel work
