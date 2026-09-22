# AGENTS.md — Skills Repo Conventions

This repository is a curated public mirror of selected skills from the canonical
source (`~/.hermes/skills/`). Read this before editing anything.

## Ground truth

- The canonical source of every skill is `~/.hermes/skills/<path>/`. When a skill
  is missing there (moved to the cross-agent shared store), `sync.sh` falls back
  to `~/.agents/skills/<path>/`.
- This repo is a **mirror**. Never edit a skill's `SKILL.md` inside this repo as
  the primary change — edit the canonical source, then run `scripts/sync.sh`.
- `scripts/sync.sh` copies only skills listed in `scripts/allowlist.tsv`
  (`<canonical-relative-path>\t<category>` lines; optional third column
  `sanitize` rewrites personal paths via `scripts/sanitize.py`).

## Hard rules

1. **No secrets.** No API keys, tokens, cookies, `.env` values, private URLs,
   or credentials. `scripts/scan.py` blocks them — run it before every commit.
2. **No absolute personal paths.** `/Users/...`, `~/...` machine-specific paths
   must be rewritten to relative or placeholder form before mirroring.
3. **No client/project-specific data.** Skills about a specific business or
   client do not belong here; see `.out-of-scope/`.
4. Every `SKILL.md` needs valid frontmatter: `name` (lowercase, hyphens) and
   `description` (self-contained trigger + one-line behavior; first ~57 chars
   must carry the trigger).
5. Keep skills small, composable, and dependency-free. A skill that needs
   another skill's directory is broken — make it self-contained.

## Repo-native exception

- `skills/plugin/labangram-agent` is the one business-owned skill in this repo.
  It exists because the root `plugin.json` / `mcp.json` (agent-plugins.org
  manifest) register the public Labangram MCP endpoints and the skill is their
  required companion. Do not delete it as "project-specific"; it still mirrors
  from canonical `~/.hermes/skills/labangram-agent/` via the allowlist like
  every other skill.
- The repo-root `SKILL.md` is also repo-native: it is the router the skills CLI
  installs when users run `npx skills add <git-url>` (the CLI only discovers a
  root-level SKILL.md; nested suites are reached through this router). Keep its
  routing table in sync with `scripts/allowlist.tsv` whenever skills are added
  or removed.

## Versioning

- Repo-level version lives in `CHANGELOG.md` and must match `plugin.json`
  `version` (single source, bumped together per release).
- Per-skill `version:` frontmatter is independent and owned by each skill.

## Validation

```bash
python3 scripts/scan.py --repo . --strict
python3 scripts/eval.py --repo .
```

Exit 0 = clean. Both run in CI on every push. The eval scores every golden
prompt in `scripts/golden.tsv` against the skill corpora and hard-fails on a
routing miss, an ambiguous tie, or a skill with no golden prompt.

## Adding or updating a skill

1. Edit/improve the skill at its canonical path (`~/.hermes/skills/...`).
2. Add its canonical-relative path to `scripts/allowlist.tsv`.
3. Run `scripts/sync.sh` (copies + scans + routing eval).
4. Add ≥1 golden prompt row to `scripts/golden.tsv` (coverage is enforced —
   a skill with no golden prompt fails `eval.py`).
5. Update the category list in `README.md` (zh-TW primary) **and** `README.en.md` (both, same
   structure — see `docs/CONTRIBUTING.md` for the i18n rule).
6. `git add -A && git commit` with a conventional message.

## Language policy

- Skills keep their original language (many are Traditional Chinese — that is a
  feature, not a defect).
- README files are bilingual: `README.md` (繁體中文 — primary landing page) and `README.en.md` (English), always in
  sync, same section structure, language badges on top.
