# AGENTS.md — Skills Repo Conventions

This repository is a curated public mirror of selected skills from the canonical
source (`~/.hermes/skills/`). Read this before editing anything.

## Ground truth

- The canonical source of every skill is `~/.hermes/skills/<path>/`.
- This repo is a **mirror**. Never edit a skill's `SKILL.md` inside this repo as
  the primary change — edit the canonical source, then run `scripts/sync.sh`.
- `scripts/sync.sh` copies only skills listed in `scripts/allowlist.tsv`
  (`<canonical-relative-path>\t<category>` lines).

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

## Validation

```bash
python3 scripts/scan.py --repo .
```

Exit 0 = clean. The same check runs in CI on every push.

## Adding or updating a skill

1. Edit/improve the skill at its canonical path (`~/.hermes/skills/...`).
2. Add its canonical-relative path to `scripts/allowlist.tsv`.
3. Run `scripts/sync.sh` (copies + scans).
4. Update the category list in `README.md` and `README.zh-TW.md` (both, same
   structure — see `docs/CONTRIBUTING.md` for the i18n rule).
5. `git add -A && git commit` with a conventional message.

## Language policy

- Skills keep their original language (many are Traditional Chinese — that is a
  feature, not a defect).
- README files are bilingual: `README.md` (EN) and `README.zh-TW.md`, always in
  sync, same section structure, language badges on top.
