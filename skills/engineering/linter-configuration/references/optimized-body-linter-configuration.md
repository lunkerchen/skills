## Workflow

1. **Scan** — `npx @biomejs/biome check <src/>` for baseline diagnostics.
2. **Observe** — read 2–3 representative files to infer existing conventions (quotes, semicolons, trailing commas, indent width, line width).
3. **Emit config** — `biome.json` (or `.prettierrc`, `.eslintrc`) matching observed style. Typical Astro/TS: `lineWidth: 100`, `indentWidth: 2`, `singleQuote: true`.
4. **Migrate if needed** — CLI version mismatches: `npx @biomejs/biome migrate --write`.
5. **Apply safe fixes** — `npx @biomejs/biome check --write <src/>`.
6. **Apply unsafe fixes** — `--write --unsafe` for unused imports/variables removal.
   ⚠️ **NEVER on Astro projects** — Biome parses only the frontmatter `---` JS block, not the template below it. Imports like `Base` (used as `<Base>` in template) appear "unused" because Biome never sees the template usage. `--unsafe` removes them → build breaks with `ReferenceError: Base is not defined`.
   Safe-only fixes (`--write` without `--unsafe`) are sufficient for Astro — the remaining warnings are all false positives you must accept.

7. **Verify build** — After any linter fixes on projects with a build step, verify the output still works:
   ```
   pnpm build   # or npm run build / yarn build / cargo build
   ```
   Safe fixes (`--write` alone) never break the build; unsafe fixes often do on Astro.

## Biome v2 migration (v1 → v2)

| v1 | v2 |
|---|---|
| `--apply` | `--write` |
| `--apply-unsafe` | `--write --unsafe` |
| `organizeImports: { enabled: true }` | `assist.actions.source.organizeImports: "on"` |
| `linter.rules.recommended: true` | `linter.rules.preset: "recommended"` |
| `files.include: [...]` | `files.includes: [...]` |
| `files.ignore: [...]` | `files.includes: ["!..."]` (prefix with `!`) |

## Pitfalls

- **Boolean CLI flags need `=true` syntax in Biome 2.x** — `biome check --files-ignore-unknown` fails with `Error: couldn't parse \`. \`: provided string was not \`true\` or \`false\``. Use `--files-ignore-unknown=true` (or any boolean flag: `--formatter-enabled=false`, `--max-diagnostics=100`). The v2 parser rejects bare boolean flags.
- **`<!-- biome-ignore -->` does NOT suppress inline-`<script>` diagnostics in HTML** — placing an HTML comment `<!-- biome-ignore lint/complexity/noArguments: ... -->` directly before a `<script>` tag produces a `suppressions/unknownRule` warning and the lint error still fires (HTML-comment suppressions only cover HTML-level diagnostics, not JS inside `<script>`). For inline JS, rewrite the code instead — the fix is usually mechanical (`arguments` → rest params, `function` → arrow) and biome's own `--write` may offer a safe auto-fix. Example: GA4's canonical `function gtag(){dataLayer.push(arguments)}` becomes `function gtag(...args){dataLayer.push(args)}`; Meta Pixel's `n.callMethod.apply(n,arguments):n.queue.push(arguments)` becomes `n.callMethod.apply(n,args):n.queue.push(args)`.
- **`$schema` must match CLI version** — `npx @biomejs/biome --version` before writing `$schema` URL. Schema 1.9.4 + CLI 2.x → deserialization error. Pin schema to e.g. `https://biomejs.dev/schemas/2.5.6/schema.json`.
- **`--apply` in v2** — returns "no such flag"; use `--write`.
- **`files.includes` globs** — v2 expects `**/src/**/*.astro` form (not `src/**/*.astro`). Check after `migrate`.
- **Line width vs inline JSON-LD** — `lineWidth: 100` expands inline objects to multi-line. Accept or raise `lineWidth`.
- **Project has no package dep** — `npx @biomejs/biome` resolves globally; pin with `pnpm add -D @biomejs/biome`.
* **JSON files drown output** — `npx @biomejs/biome check <dir/>` also formats JSON files. Large data files (e.g. GeoJSON, 1MiB+) produce massive formatting diffs that bury JS lint results. Mitigations:
  * `--formatter-enabled=false` for lint-only scans.
  * `--max-diagnostics=100` to cap output verbosity.
  * `files.maxSize` (number of bytes) in `biome.json` to raise the size cap.
  * `files.includes` in `biome.json` to scope checks to specific patterns (v2 dropped `files.ignore`; negate globs with `!`).

## Recovery: `--unsafe` broke the build (Astro)

When `--unsafe` removed template-used imports and the build fails:

1. **Revert** affected files — `git checkout -- src/pages/*.astro src/components/*.astro src/layouts/*.astro src/content.config.ts`
2. **Reapply safe-only** — `npx @biomejs/biome check --write src/`
3. **Verify** — `pnpm build` (or equivalent) passes
4. **Accept** — the remaining warnings are all false positives from Astro's dual-format files; suppress with `// biome-ignore` inline if desired

See `references/biome-astro-pitfalls.md` for a full replay of the failure mode.
