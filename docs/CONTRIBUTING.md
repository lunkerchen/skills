# Contributing

## Adding a skill

1. Improve the skill at its canonical source first (`~/.hermes/skills/...`),
   not inside this repo — this repo is a mirror.
2. Add a `<canonical-relative-path>\t<category>` line to `scripts/allowlist.tsv`.
3. Run `scripts/sync.sh` — it copies the skill and runs the validator.
4. Add a one-line entry to the category list in `README.md` **and**
   `README.en.md`. Both files must stay structurally identical (same
   sections, same order, same table rows) — only the language changes.
5. Commit with a conventional message (`feat:`, `fix:`, `docs:`, `chore:`).

## Standards every skill must meet

- Valid frontmatter: `name` + `description` (trigger in the first ~57 chars).
- Self-contained: no dependency on another skill's directory.
- No secrets, no absolute personal paths (`/Users/...`), no client-specific data.
- Original language preserved — Traditional Chinese is a feature.

## What is NOT accepted

See `.out-of-scope/` for the full list: client/project-specific skills,
commercial toolkits, personal research collections, retired skills.

## License

By contributing you agree your contributions are MIT-licensed, same as the repo.
