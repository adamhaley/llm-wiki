# Wiki Schema

This file defines how agents should maintain this repository as a personal "LLM wiki".

## Core Model

There are three layers:

1. `raw/`: source material awaiting or after ingestion.
2. `wiki/`: the local Obsidian vault and LLM-maintained markdown knowledge base.
3. `WIKI_SCHEMA.md`: the maintenance contract for ingestion, querying, linting, and the repo-versus-vault boundary.

The goal is not to re-read every raw source from scratch on every question. The goal is to incrementally compile source material into a persistent, interlinked markdown wiki.

## Ownership Rules

- The human curates what enters `raw/`.
- The agent reads `raw/` and maintains `wiki/`.
- Raw source bodies are immutable. Do not edit them in place.
- `wiki/` is editable. Prefer incremental edits over wholesale rewrites.
- Git is for versioned maintenance behavior such as scripts, schemas, agent instructions, templates, and selected shared vault configuration.
- Obsidian Sync or another vault-native transport should be the primary live sync path for note content when the vault is used across devices.
- Durable note content under `wiki/` may be git-ignored by default.
- The index and log are mandatory maintenance files.
- The deterministic toolchain lives in `scripts/wiki_tool.py` and `scripts/audit_public.py`.

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
- `wiki/topics/`: canonical topic hubs for concepts, themes, or subject areas.
- `wiki/pages/`: general durable pages that support or elaborate on canonical topics without necessarily being topic hubs themselves.
- `wiki/entities/`: named entities such as people, companies, places, or tools.
- `wiki/syntheses/`: comparisons, decision memos, query outputs worth preserving.
- `wiki/templates/`: starter templates only.
- `wiki/journal/`: dated notes grounded in the wiki and past entries.
- `wiki/crm/`: person records and relationship context.
- `wiki/catalog.jsonl`: generated machine-readable note catalog.
- Most content files under `wiki/` may remain untracked in git except for scaffolding, templates, and explicitly shared configuration.

### `Schema/`

- `Schema/source-manifest.jsonl`: generated machine-readable source coverage manifest.
- `Schema/*.md`: frontmatter, naming, workflow, and command contracts for the tooling layer.

## Capture Policy

Use the destination based on the kind of material, not the transport that delivered it.

- Put external source material in `raw/`.
- Put Web Clipper captures that benefit from immediate visibility in `wiki/inbox-clips/`.
- Put normalized personal reflections, dictated thoughts, and daily notes in `wiki/journal/`.
- Put durable synthesized knowledge in `wiki/`.
- Put person-specific records in `wiki/crm/`.

Telegram voice notes may go directly into `wiki/journal/` when an automation has already turned them into coherent dated note entries. They do not need to pass through `raw/` first unless the raw transcript itself is worth preserving as source material.
Web Clipper captures may land in `wiki/inbox-clips/` first and later be normalized into `raw/` or promoted into curated wiki pages.

## Sync Boundary

- Treat Obsidian Sync as the live sync system for note content when available.
- Treat git as the versioned system layer, not as a second bidirectional sync engine for the active vault.
- If git-based automation needs a clean worktree, prefer a separate clean clone rather than operating inside the active synced vault.
- Content snapshots in git should be deliberate archival actions, not the default transport.

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

Because `raw/` lives outside the Obsidian vault on purpose, provenance to raw files should be preserved primarily in frontmatter metadata and generated manifests, not only as clickable Obsidian links.

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
sources:
source_count:
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

Source page frontmatter should include:

```yaml
---
title:
type: source
status:
created:
updated:
raw_source:
source_kind:
tags:
  - source
---
```

Compiled durable notes in `wiki/topics/`, `wiki/pages/`, `wiki/entities/`, `wiki/syntheses/`, and `wiki/crm/` should include:

```yaml
---
title:
type:
status:
created:
updated:
sources:
source_count:
tags:
---
```

The `sources` field should list repo-relative raw file paths such as `raw/article.md` or `raw/processed/article.md`.

## Ingest Workflow

When asked to ingest a source:

1. Read the source from `raw/` or `wiki/inbox-clips/`, depending on where it landed.
2. Identify whether it is genuinely new, an update, or redundant.
3. Create or update the source page in `wiki/sources/`.
4. Update any affected topic, entity, overview, or synthesis pages.
5. Add or revise cross-links.
6. Run `python3 scripts/wiki_tool.py build`.
7. Run `python3 scripts/wiki_tool.py lint`.
8. Run `python3 scripts/wiki_tool.py source-scan --update --accept-covered`.
9. Run `python3 scripts/wiki_tool.py source-lint`.
10. Update `wiki/index.md` if needed beyond the generated structure.
11. Append an entry to `wiki/log.md`.
12. Move the processed source into `raw/processed/` unless the user wants it left in place.

Default ingest posture:

- Preserve ambiguity when the source is uncertain.
- Mark contradictions explicitly instead of silently choosing a winner.
- Prefer extending existing pages before creating new ones.

## Query Workflow

When asked a substantive question:

1. Read `wiki/index.md` first.
2. Run `python3 scripts/wiki_tool.py search-catalog --query "topic"` when the topic is broad or ambiguous.
3. Read the most relevant linked pages in `wiki/`.
4. Open raw sources only when compiled notes are insufficient or source-level verification is needed.
5. Synthesize an answer from the wiki, citing the pages used.
6. If the answer creates durable value, offer or perform filing it into `wiki/syntheses/`.
7. Append to `wiki/log.md` only if the query materially changed the vault.

## Journal Workflow

When asked to create or update a journal entry:

1. Prefer one dated markdown note per day or per capture session, depending on the user's pattern.
2. Preserve the user's voice and intent when the entry originated from dictation.
3. Add light provenance when useful, such as `source: telegram-voice`.
4. Link to relevant wiki or CRM pages when the connection is durable.
5. Update `wiki/index.md` only if the journal structure itself changed materially.
6. Append to `wiki/log.md` if the change was an intentional vault maintenance action rather than a routine automated capture.

## Promotion Workflow

When asked to promote ideas from journal or source material into durable wiki pages:

1. Start with helper signals such as:
   - `python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal`
   - `python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2`
   - `python3 scripts/wiki_tool.py orphan-notes`
2. Treat these outputs as candidate prompts, not automatic truth.
3. Decide whether the material belongs in `wiki/topics/`, `wiki/pages/`, `wiki/entities/`, `wiki/crm/`, or `wiki/syntheses/`.
4. Use `wiki/topics/` for canonical hub pages and `wiki/pages/` for supporting durable pages linked from those hubs.
5. Prefer updating an existing canonical page over creating a new one.
6. Add explicit links where they improve retrieval or context, but avoid blanket backlink spam.
7. For journal-only promotions, cite relevant journal entries in the body and keep claims modest unless supported by external raw sources.
8. Run `python3 scripts/wiki_tool.py build`.
9. Run `python3 scripts/wiki_tool.py lint`.
10. Run `python3 scripts/audit_public.py`.
11. Append to `wiki/log.md` if the promotion materially changed the vault.

## Synthesis Prep Workflow

When you want a deterministic review brief before doing higher-judgment synthesis work:

1. Run `python3 scripts/synthesis_report.py`.
2. Open the newest report under `wiki/pages/reports/`.
3. Review:
   - new or changed journal entries
   - new or changed inbox clips
   - repeated names and phrases
   - possible cross-note connections
   - orphan durable notes
4. Audit the report quality before trusting it:
   - are the surfaced names and phrases materially useful?
   - is the output dominated by filler, transcript boilerplate, or weather-style repetition?
   - did it miss any obvious recurring topic, entity, or connection?
5. If the report is structurally noisy or repeatedly misses clear patterns, prefer tuning `scripts/synthesis_report.py` before doing large-scale promotion.
6. Treat the report as synthesis input, not as a substitute for human or agent judgment.
7. Promote the strongest findings into `wiki/topics/`, `wiki/pages/`, `wiki/entities/`, `wiki/crm/`, or `wiki/syntheses/`.

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

The deterministic baseline is:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

Useful non-mutating promotion helpers:

```bash
python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal
python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2
python3 scripts/wiki_tool.py orphan-notes
python3 scripts/synthesis_report.py --dry-run
```

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
3. `wiki/catalog.jsonl`
4. `Schema/source-manifest.jsonl` when raw coverage changed

Do not leave those behind in the local vault state.

When the repository is operating in system-code mode, those files may still be intentionally absent from git history or pending removal from tracking. The maintenance requirement is about local vault coherence, not automatic inclusion in commits.
