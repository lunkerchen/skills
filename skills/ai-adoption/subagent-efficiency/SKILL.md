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

## Failed delegates still leave evidence

A subagent that dies (model HTTP 500, max_iterations) is not a zero-output run.
Its live transcript is append-only at
`$HERMES_HOME/cache/delegation/live/<deleg_id>/task-<n>.log` — every tool call,
result, and partial chain is preserved. Before re-dispatching, read the log and
salvage partial findings: a blind-audit delegate that died after 5 vision passes
still returned its checked frames and transcribed card text (caught a background
Wi-Fi credential in a video frame, 2026-08-04). Re-run only the missing slice,
not the whole task — and treat a salvaged-but-incomplete audit as unverified for
the parts it never reached.

## Stalled-but-alive subagents: the search-phase stall signature

A subagent can also be **alive but not progressing** — different from dying. The
signature: the live transcript grows to kickoff + 1-2 tool calls, then stops for
minutes with no results, no errors, no further lines. This happens with
research-heavy briefs (dozens of candidates × multiple fields) on flash/cheap
aux models — the agent loops inside a search tool without producing output.
Waiting does not help. Confirm via the transcript (`file_size` tiny, no tool
result lines), then re-dispatch ONE consolidated synthesis agent with an exact
count + compact output constraint, or collapse the work to the main session.
(2026-08-07: three parallel 33-34-item research briefs all stalled this way;
recovery = one consolidated synthesis agent + main-session source verification.)

## Related

- `loop-fix` — the verification loop this pattern was discovered in
- `hermes-parallel` — delegation patterns for parallel work
