# Biome + Astro: Known Failure Mode

## The problem

Biome parses only the JavaScript frontmatter block (`--- ... ---`) in `.astro` files.
It has no awareness of the template/HTML section below the second `---`.

This means:

**`import Base from '../layouts/Base.astro'`** looks unused to Biome (it never sees `<Base>` in the template).
**`const { Content } = await render(project)`** looks unused (template uses `Content` only in markup).
**Any destructured layout prop** (`title`, `description`) looks unused when only the template reads it.

## The unsafe-fix trap

Running `npx @biomejs/biome check --write --unsafe src/` on an Astro project:

1. Removes `import Base` from all pages that use `<Base>` in template
2. Removes `import { Image }` from `index.astro` (used in `<Image>` template tags)
3. Prepend `_` to variables like `currentPath` (used in `<nav>` template)
4. Removes `import Gallery` from `projects/index.astro`

Result: build fails with `ReferenceError: Base is not defined` on every page.

## Recovery steps

```bash
# 1. Revert all affected Astro files
git checkout -- src/pages/*.astro src/components/*.astro src/layouts/*.astro

# 2. Reapply safe-only fixes
npx @biomejs/biome check --write src/

# 3. Verify
pnpm build
```

## Prevention

- **Safe-only is the max for Astro projects.** `--write` (without `--unsafe`) fixes formatting, import sorting, and trailing commas — enough to keep code clean.
- The 20–50 warnings that remain are all false positives. Accept them. Suppress with `// biome-ignore lint/correctness/noUnusedVariables` on individual declarations if the noise bothers you, but they're harmless.
- If you must eliminate a warning, use `// biome-ignore` comments on the specific line — never blanket `--unsafe`.

## Real-world example (your-brand, Jul 2026)

- 9 files fixed by safe-only: import sorting, trailing commas, quote style
- 53 unsafe suggestions: all would have broken the build
- 35 remaining warnings post-safe: all Astro false positives
- Build: 36 pages, 0 errors after safe-only run
