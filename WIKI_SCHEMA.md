# Wiki Schema

This file defines how agents should maintain this repository as a personal "LLM wiki".

## Core Model

There are three layers:

1. `raw/`: source material awaiting or after ingestion.
2. `wiki/`: the Obsidian vault and LLM-maintained markdown knowledge base.
3. `WIKI_SCHEMA.md`: the maintenance contract for ingestion, querying, and linting.

The goal is not to re-read every raw source from scratch on every question. The goal is to incrementally compile source material into a persistent, interlinked markdown wiki.

## Ownership Rules

- The human curates what enters `raw/`.
- The agent reads `raw/` and maintains `wiki/`.
- Raw source bodies are immutable. Do not edit them in place.
- `wiki/` is editable. Prefer incremental edits over wholesale rewrites.
- The index and log are mandatory maintenance files.

## Directory Conventions

### `raw/`

- `raw/`: newly dropped source material awaiting ingest.
- `raw/processed/`: source material that has already been ingested.
- `raw/assets/`: local images, figures, screenshots, or attachments.
- `raw/` is intentionally outside the Obsidian vault and may be git-ignored except for tracked skeleton files.

### `wiki/`

- `wiki/.obsidian/`: vault-local Obsidian settings.
- `wiki/inbox-clips/`: Obsidian-visible landing zone for Web Clipper captures.
- `wiki/index.md`: vault catalog and starting point for navigation.
- `wiki/log.md`: append-only chronological operations log.
- `wiki/overview.md`: high-level map, thesis, and open questions.
- `wiki/sources/`: one page per source with provenance and extracted takeaways.
- `wiki/topics/`: concept, theme, or subject pages.
- `wiki/entities/`: named entities such as people, companies, places, or tools.
- `wiki/syntheses/`: comparisons, decision memos, query outputs worth preserving.
- `wiki/templates/`: starter templates only.
- `wiki/journal/`: dated notes grounded in the wiki and past entries.
- `wiki/crm/`: person records and relationship context.

## Capture Policy

Use the destination based on the kind of material, not the transport that delivered it.

- Put external source material in `raw/`.
- Put Web Clipper captures that benefit from immediate visibility in `wiki/inbox-clips/`.
- Put normalized personal reflections, dictated thoughts, and daily notes in `wiki/journal/`.
- Put durable synthesized knowledge in `wiki/`.
- Put person-specific records in `wiki/crm/`.

Telegram voice notes may go directly into `wiki/journal/` when an automation has already turned them into coherent dated note entries. They do not need to pass through `raw/` first unless the raw transcript itself is worth preserving as source material.
Web Clipper captures may land in `wiki/inbox-clips/` first and later be normalized into `raw/` or promoted into curated wiki pages.

## Naming

- Use short kebab-case filenames.
- Put each durable page in the most specific directory that fits.
- Page titles should be human-readable H1s.
- Prefer one canonical page per concept. Merge duplicates instead of proliferating near-copies.

## Link Policy

- Use relative markdown links.
- Every substantive page should link outward to related pages.
- When adding a new page, add at least one inbound path by updating another page to point to it.
- Prefer explicit links over relying on text search alone.

## Page Shape

Use light YAML frontmatter when it helps, but do not turn pages into metadata dumps.

Recommended frontmatter fields:

```yaml
---
title:
type:
status:
created:
updated:
source_files:
tags:
---
```

Recommended body sections:

1. `Summary`
2. `Key Points`
3. `Evidence` or `Notes`
4. `Links`
5. `Open Questions` when applicable

Not every page needs every section. Keep pages compact and composable.

## Source Page Requirements

Every ingested source should generally get a page in `wiki/sources/` that records:

- what the source is
- when it was ingested
- where the raw file lives
- the key claims or takeaways
- related entities, topics, and syntheses
- unresolved contradictions or uncertainties

Do not copy large source texts into the wiki. Summarize and quote sparingly.

## Ingest Workflow

When asked to ingest a source:

1. Read the source from `raw/` or `wiki/inbox-clips/`, depending on where it landed.
2. Identify whether it is genuinely new, an update, or redundant.
3. Create or update the source page in `wiki/sources/`.
4. Update any affected topic, entity, overview, or synthesis pages.
5. Add or revise cross-links.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md`.
8. Move the processed source into `raw/processed/` unless the user wants it left in place.

Default ingest posture:

- Preserve ambiguity when the source is uncertain.
- Mark contradictions explicitly instead of silently choosing a winner.
- Prefer extending existing pages before creating new ones.

## Query Workflow

When asked a substantive question:

1. Read `wiki/index.md` first.
2. Read the most relevant linked pages in `wiki/`.
3. Synthesize an answer from the wiki, citing the pages used.
4. If the answer creates durable value, offer or perform filing it into `wiki/syntheses/`.
5. Append to `wiki/log.md` only if the query materially changed the vault.

## Journal Workflow

When asked to create or update a journal entry:

1. Prefer one dated markdown note per day or per capture session, depending on the user's pattern.
2. Preserve the user's voice and intent when the entry originated from dictation.
3. Add light provenance when useful, such as `source: telegram-voice`.
4. Link to relevant wiki or CRM pages when the connection is durable.
5. Update `wiki/index.md` only if the journal structure itself changed materially.
6. Append to `wiki/log.md` if the change was an intentional vault maintenance action rather than a routine automated capture.

## Lint Workflow

When asked to lint or health-check the wiki, look for:

- orphan pages
- duplicate concepts
- stale summaries superseded by newer sources
- contradictions across pages
- missing high-value cross-links
- recurring claims that deserve their own page
- index entries that are missing or out of date
- journal insights that deserve promotion into the wiki
- CRM records that are mentioned elsewhere but do not exist yet

Prefer producing concrete fixes, not only observations.

## Writing Style

- Be factual, compressed, and specific.
- Separate observations from speculation.
- Preserve provenance when making claims.
- Avoid hype and generic prose.
- Keep the wiki readable by humans first.

## Minimum Maintenance Standard

Any change that creates or materially changes a durable wiki page should also update:

1. `wiki/index.md`
2. `wiki/log.md`

Do not leave those behind.
