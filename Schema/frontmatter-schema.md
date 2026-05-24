# Frontmatter Schema

The deterministic tooling validates wiki notes under `wiki/` using light frontmatter rather than requiring heavyweight databases or plugins.

## Core Notes

These note types are linted strictly:

- `source`
- `topic`
- `entity`
- `synthesis`
- `crm`

Required fields:

```yaml
---
title:
type:
status:
created:
updated:
tags:
---
```

## Source Notes

Source notes live in `wiki/sources/` and point back to raw source material with a path field because `raw/` intentionally lives outside the Obsidian vault.

```yaml
---
title: Why LLM Wiki Video Notes
type: source
status: active
created: 2026-05-24
updated: 2026-05-24
raw_source: raw/why-llm-wiki.md
source_kind: article
tags:
  - source
  - llm-wiki
---
```

## Compiled Notes

Compiled notes in `wiki/topics/`, `wiki/entities/`, `wiki/syntheses/`, and `wiki/crm/` keep provenance in machine-readable `sources` metadata.

```yaml
---
title: Search Compiled Notes First
type: topic
status: seed
created: 2026-05-24
updated: 2026-05-24
sources:
  - raw/why-llm-wiki.md
source_count: 1
aliases:
  - query-compiled-wiki-first
tags:
  - topic
  - llm-wiki
---
```

Rules:

- `source_count` must equal the number of `sources`.
- Every `sources` path must exist under `raw/` or `raw/processed/`.
- `type` should match the note's directory.

## Journal Notes

`wiki/journal/` may use lighter frontmatter when the note is a normalized capture rather than a curated knowledge page. The tooling catalogs these notes but does not require provenance fields.
