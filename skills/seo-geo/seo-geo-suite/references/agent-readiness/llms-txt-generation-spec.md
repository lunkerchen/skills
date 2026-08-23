---
name: llms-txt-generation
description: Use when 建/修 llms.txt 或查 GEO 可見性。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [seo, geo, llms-txt, nextjs, ssg, content-site]
---# llms.txt 生成與維護

## Boundary & Exclusions

- **Do not trigger** for unrelated general queries or non-matching tasks.

## Extended References & Guides

- [核心原則：靜態 llms.txt 註定過時](references/llms-txt.md)
- [動態生成（Next.js App Router 模式）](references/next-js-app-router.md)
- [檢查清單（audit 或驗收時）](references/audit.md)
- [陷阱](references/guide.md)
- [驗證（build 後）](references/build.md)
- [Trigger Evals](evals/eval_triggers.json): Automated evaluation test fixtures.
