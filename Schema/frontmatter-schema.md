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

Source notes live in `wiki/pages/` with `type: source` and point back to raw material with a path field into `wiki/inbox/`.

```yaml
---
title: Why LLM Wiki Video Notes
type: source
status: active
created: 2026-05-24
updated: 2026-05-24
raw_source: wiki/inbox/why-llm-wiki.md
source_kind: article
tags:
  - source
  - llm-wiki
---
```

## Compiled Notes

Compiled notes in `wiki/topics/`, `wiki/pages/` (`type: entity`, `synthesis`, or `page`), and `wiki/crm/` keep provenance in machine-readable `sources` metadata.

```yaml
---
title: Search Compiled Notes First
type: topic
status: seed
created: 2026-05-24
updated: 2026-05-24
sources:
  - wiki/inbox/why-llm-wiki.md
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
- Every `sources` path must exist under `wiki/inbox/`.
- `type` should match the note's role — `wiki/pages/` now holds `page`, `entity`, `source`, and `synthesis` types side by side, differentiated by this field rather than by directory.

## CRM Notes

CRM notes should include structured contact fields in frontmatter so the vault can later sync with a database-backed CRM without losing relationship context.

```yaml
---
title: Contact Name
type: crm
status: active
created: 2026-08-11
updated: 2026-08-11
source_count: 0
emails: []
phones: []
websites: []
social_profiles: []
preferred_contact: unknown
location: unknown
company: unknown
role: unknown
relationship_stage: unknown
last_contacted: unknown
next_follow_up: unknown
crm_external_id: unknown
crm_sync_status: local-only
tags:
  - crm
---
```

Unknown contact information should stay explicit rather than guessed.

## Journal Notes

`wiki/journal/` may use lighter frontmatter when the note is a normalized capture rather than a curated knowledge page. The tooling catalogs these notes but does not require provenance fields.
