# Wiki Schema

This file defines how agents should maintain this repository, Adam's second brain.

## Core Model

There are two layers, both inside the Obsidian vault so both reach every synced device (including a headless VPS sync client):

1. `wiki/inbox/`: raw and unprocessed material awaiting triage — Web Clipper captures, dropped-in raw sources, anything not yet promoted.
2. `wiki/{topics,pages,crm,journal,field-reports,patterns}/`: the agent-maintained, durable markdown layer. `topics/`+`pages/` compile knowledge for future retrieval, in the "LLM wiki" pattern; `crm/`, `journal/`, `field-reports/`, and `patterns/` are additional first-class directories serving the second brain's other roles (relationship data with a live database sync, daily reflection, structured field capture, and reusable engineering patterns respectively) — see their own `README.md` for each.

`WIKI_SCHEMA.md` itself is the maintenance contract for ingestion, querying, linting, and the repo-versus-vault boundary.

The goal is not to re-read every raw capture from scratch on every question. The goal is to incrementally compile captured material into a persistent, interlinked markdown wiki.

**Historical note:** earlier versions of this schema kept raw source material in a `raw/` directory outside the Obsidian vault, on the theory that raw material was git-versioned and immutable while `wiki/` was Sync-versioned and mutable. That split blocked a real requirement — capturing on one device (open at irregular hours) and processing on another (always-on) — because material outside the vault can never reach Obsidian Sync, full stop. `raw/` was retired and folded into `wiki/inbox/` for this reason. If you see references to `raw/` in older log entries or archived audit reports, they predate this change.

## Core Value: Use-Led Simplicity

This system exists to support Adam's lived use of the second brain: capture, reflection, retrieval, synthesis, and action. Its structure must stay subordinate to that use.

Complexity is allowed only when it earns its keep through repeated practical use. Do not add folders, note classes, workflows, automation, metadata, or agent rituals merely because they are conceptually elegant. If a distinction is not helping capture, review, retrieval, promotion, privacy, or action, prefer the simpler model.

The vault should be led by daily usage, not by abstract technical completeness. Agents maintaining this system should treat simplification as a first-class maintenance behavior: merge redundant categories, retire unused workflows, and keep the user-facing process small enough that the second brain remains survivable as a daily practice.

## Ownership Rules

- The human curates what enters `wiki/inbox/`.
- The agent reads `wiki/inbox/` and maintains the rest of `wiki/`.
- `wiki/inbox/` items marked `status: archived` are provenance records (e.g. a promoted source's `raw_source` target) — do not edit their content in place, only their status.
- The rest of `wiki/` is editable. Prefer incremental edits over wholesale rewrites.
- Git is for versioned maintenance behavior such as scripts, schemas, agent instructions, templates, and selected shared vault configuration.
- Obsidian Sync is the primary live sync path for all vault content, including `wiki/inbox/`.
- Durable note content under `wiki/` may be git-ignored by default.
- The index and log are mandatory maintenance files.
- The deterministic toolchain lives in `scripts/wiki_tool.py` and `scripts/audit_public.py`.

## Instruction Layer vs Content Layer

- `WIKI_SCHEMA.md` is the canonical authoritative instruction source for this repository.
- `ALL_CAPS` markdown files such as `WIKI_SCHEMA.md` and `AGENTS.md` are the instruction layer: they are normative for agent behavior, should be tracked in git, and override conflicting workflow descriptions elsewhere.
- Notes under `wiki/` are the content layer, even when they discuss workflows, systems, or second-brain process. They are durable knowledge, research, or evolving practice, not binding repo instructions by themselves.
- If a workflow or rule first appears in `wiki/` content and later becomes mandatory for maintenance behavior, promote that rule into the instruction layer instead of treating the content page itself as authoritative.
- When deciding whether something belongs in git, use this boundary: instruction-layer files are tracked by default; content-layer notes may remain git-ignored by default.

## Editing Fallback Policy

- Prefer `apply_patch` for manual edits when the edit tool is functioning normally.
- If `apply_patch` or the sandbox path resolver fails on a file that is otherwise readable and writable inside the workspace, a small deterministic repo-local scripted edit is an acceptable fallback.
- Keep fallback edits narrow: target a specific file, use explicit string anchors when possible, and avoid broad rewrite scripts for small changes.
- Prefer existing repo tools and standard library utilities over adding new dependencies just to make edits work around sandbox quirks.
- After any fallback edit to tracked instructions, scripts, or schema files, verify the resulting diff directly and run the normal maintenance checks.

## Directory Conventions

### `wiki/`

- `wiki/.obsidian/`: vault-local Obsidian settings.
- `wiki/` root (loose files): an in-vault inbox for hand-dropped material, distinct from `wiki/inbox/`. The user occasionally pastes or saves files directly at the vault root between sessions. No frontmatter or naming convention is required there. Run `python3 scripts/wiki_tool.py root-inbox` to list what's waiting and triage each file into the correct subdirectory or into `wiki/inbox/` (or delete it if it's debris, e.g. an empty stub). Don't leave files there indefinitely.
- `wiki/inbox/`: single landing zone for everything not yet triaged — raw source material and Web Clipper captures alike. Not catalog-indexed, not linted. See `wiki/inbox/README.md`.
- `wiki/inbox/assets/`: local images, figures, screenshots, or attachments.
- `wiki/index.md`: vault catalog and starting point for navigation.
- `wiki/log.md`: append-only chronological operations log.
- `wiki/overview.md`: high-level map, thesis, and open questions.
- `wiki/topics/`: canonical topic hubs — the navigational index-of-indexes layer for concepts, themes, or subject areas. Kept as a separate folder because it plays a distinct hub/leaf role, not just a content-type distinction.
- `wiki/pages/`: durable compiled knowledge — supporting notes, named entities, ingested sources, and syntheses all live here now, differentiated by `type:` frontmatter (`page`, `entity`, `source`, `synthesis`) rather than by folder. See `wiki/pages/README.md`.
- `wiki/templates/`: starter templates only.
- `wiki/journal/`: dated notes grounded in the wiki and past entries, including daily session logs. See `wiki/journal/README.md`.
- `wiki/crm/`: person records and relationship context. Kept as a separate folder (not `type: entity` inside `wiki/pages/`) because promotion here is gated behind human review for sensitive claims — a privacy boundary, not just a category. Also the source layer for a live one-way sync into adamhaley-com's Client CRM database (`scripts/import_crm_clients.py`) — see `wiki/pages/crm-database-pipeline.md`.
- `wiki/field-reports/`: structured field captures (location, photos, notes) from the Telegram multimodal capture bot. Kept separate from `wiki/journal/` because these are structured/repeatable, not narrative. See `wiki/field-reports/README.md`.
- `wiki/patterns/`: durable technical/architectural patterns coding agents check before building something new in a project, each linked to a real reference implementation. See `wiki/patterns/README.md`.
- `wiki/catalog.jsonl`: generated machine-readable note catalog.
- Most content files under `wiki/` may remain untracked in git except for scaffolding, templates, and explicitly shared configuration.

### `Schema/`

- `Schema/source-manifest.jsonl`: generated machine-readable source coverage manifest.
- `Schema/*.md`: frontmatter, naming, workflow, and command contracts for the tooling layer.

## Capture Policy

Everything uncertain or unprocessed lands in `wiki/inbox/` — raw source material and Web Clipper captures use the same folder now, since both are "not yet triaged" regardless of how they arrived.

- Put external source material and Web Clipper captures in `wiki/inbox/`.
- Put hand-dropped material that lands elsewhere in the vault (pasted notes, drafts, reference clippings) at the `wiki/` root, awaiting triage.
- Put normalized personal reflections, dictated thoughts, daily notes, and session logs in `wiki/journal/`.
- Put durable synthesized knowledge in `wiki/pages/` or `wiki/topics/`.
- Put project/build plans worth keeping as `type: plan` pages in `wiki/pages/`.
- Put person-specific records in `wiki/crm/`.
- Put structured field captures (location, photos, notes from the field) in `wiki/field-reports/`.
- Put durable, reusable technical/architectural patterns in `wiki/patterns/`.

Telegram voice notes may go directly into `wiki/journal/` when an automation has already turned them into coherent dated note entries. They do not need to pass through `wiki/inbox/` first unless the raw transcript itself is worth preserving as source material.

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

Provenance to inbox files should be preserved primarily in frontmatter metadata (`raw_source`, `sources`) and generated manifests, not only as clickable Obsidian links, since inbox items may be deleted once fully promoted.

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

Every ingested source should generally get a `type: source` page in `wiki/pages/` that records:

- what the source is
- when it was ingested
- where the raw file lives (`raw_source`, pointing into `wiki/inbox/`)
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

Compiled durable notes in `wiki/topics/`, `wiki/pages/` (any of `type: page`, `entity`, `synthesis`), and `wiki/crm/` should include:

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

The `sources` field should list repo-relative file paths such as `wiki/inbox/article.md`. Pages promoted from inbox material or journal entries may omit `sources` or reference the originating file path instead.

## CRM Record Shape

CRM records are not just biographies. They should be useful for future contact, follow-up, and eventual structured sync into a database-backed CRM.

Every `type: crm` note should reserve frontmatter fields for contact information, even when the current value is unknown:

```yaml
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
```

Use the body for relationship context, history, judgment, and nuance. Use frontmatter for fields that may later sync cleanly to a database. Do not invent contact details; leave unknown fields explicit until verified.

The markdown CRM notes are the context layer; adamhaley-com's `Client` database is the operational structured layer. `scripts/import_crm_clients.py` performs a one-way sync (`wiki/crm/*.md` → `POST /api/clients`), matching records on `source: second_brain_crm` + `source_external_id: {note filename}`. On conflict the database wins: the sync only fills fields the Client record doesn't already have a value for, never overwrites one — so a value edited directly in the Laravel admin for a field the vault also sets will not be clobbered by the next sync. See `wiki/pages/crm-database-pipeline.md` for the full pipeline.

## Ingest Workflow

Everything in `wiki/inbox/` — raw source material and Web Clipper captures alike — follows the same path now. Whether a given item gets a dedicated `type: source` page or is promoted directly depends on the material, not on which sub-workflow it arrived through.

### Ingesting / Promoting from `wiki/inbox/`

1. Read the item from `wiki/inbox/`.
2. Identify whether it is genuinely new, an update, or redundant.
3. If it warrants standalone provenance tracking: create or update a `type: source` page in `wiki/pages/` with `raw_source` pointing at the `wiki/inbox/` file. If it's more like a journal or clip insight: promote directly into `wiki/topics/`, `wiki/pages/`, or `wiki/crm/` without a separate source page.
4. Update any affected topic, entity, overview, or synthesis pages.
5. Add or revise cross-links.
6. Run `python3 scripts/wiki_tool.py build`.
7. Run `python3 scripts/wiki_tool.py lint`.
8. Run `python3 scripts/wiki_tool.py source-scan --update --accept-covered`.
9. Run `python3 scripts/wiki_tool.py source-lint`.
10. Update `wiki/index.md` if needed beyond the generated structure.
11. Append an entry to `wiki/log.md`.
12. Once an inbox item is fully processed: delete it if it has no durable signal beyond what's now promoted, or mark it `status: archived` in frontmatter if a source page still needs it for `raw_source` provenance.

Prefer processing related items in one themed pass instead of handling every inbox item as an isolated page-creation event — prefer one synthesis or targeted update to existing durable pages over many thin pages when multiple items reinforce the same idea.

### Triaging the `wiki/` Root Inbox

1. Run `python3 scripts/wiki_tool.py root-inbox` to list loose files at the vault root.
2. For each file, decide: promote into the matching subdirectory (`wiki/pages/`, `wiki/journal/`, etc.), move into `wiki/inbox/` for later triage, or delete it if it's debris (e.g. an empty stub from a failed save).
3. Empty files (`bytes: 0` in the command output) can generally be deleted without asking, unless the filename suggests it's a placeholder the user is actively about to fill in.

Default ingest posture:

- Preserve ambiguity when the source is uncertain.
- Mark contradictions explicitly instead of silently choosing a winner.
- Prefer extending existing pages before creating new ones.

## Query Workflow

When asked a substantive question:

1. Read `wiki/index.md` first.
2. Run `python3 scripts/wiki_tool.py search-catalog --query "topic"` when the topic is broad or ambiguous.
3. Read the most relevant linked pages in `wiki/`.
4. Open `wiki/inbox/` material only when compiled notes are insufficient or source-level verification is needed.
5. Synthesize an answer from the wiki, citing the pages used.
6. If the answer creates durable value, offer or perform filing it into `wiki/pages/` as `type: synthesis`.
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

When asked to promote ideas from journal or inbox material into durable wiki pages:

1. Start with helper signals such as:
 - `python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal`
 - `python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2`
 - `python3 scripts/wiki_tool.py orphan-notes`
 - `python3 scripts/wiki_tool.py cross-link-candidates` — plain-text mentions of other notes' titles that aren't linked yet; see `Schema/cross-linking-workflow.md`
 - `python3 scripts/wiki_tool.py dead-links` — existing links that don't resolve to a real file; see `Schema/cross-linking-workflow.md`
2. Treat these outputs as candidate prompts, not automatic truth.
3. Decide whether the material belongs in `wiki/topics/` (hub), `wiki/pages/` (as `type: page`, `entity`, or `synthesis`), or `wiki/crm/`.
4. Promote based on durable future utility, not only repetition. A one-off inbox item, clip, or journal insight can deserve promotion when it is reference-grade, decision-relevant, project-relevant, rare, clarifying, or likely to save rediscovery later.
5. Use `wiki/topics/` for canonical hub pages and `wiki/pages/` for everything else durable, differentiated by `type:` frontmatter.
6. Prefer updating an existing canonical page over creating a new one.
7. Use cross-links to amplify signal selectively. Prefer inbox -> durable page and journal -> durable page synthesis over dense direct link spam between every related item and journal entry.
8. For journal-only promotions, cite relevant journal entries in the body and keep claims modest unless supported by external sources.
9. Run `python3 scripts/wiki_tool.py build`.
10. Run `python3 scripts/wiki_tool.py lint`.
11. Run `python3 scripts/audit_public.py`.
12. Append to `wiki/log.md` if the promotion materially changed the vault.

## Autonomous Promotion Workflow

Autonomous promotion is allowed for high-confidence durable material. The user should not be the default gate for routine promotion.

Use this posture:

- Promote clear durable items without asking first.
- Treat human review as exception-based, not mandatory.
- Ask for input before destructive deletes or merges, sensitive CRM claims, major taxonomy changes, or resolving substantive contradictions.
- Be conservative but active: weak candidates can stay unpromoted, but clear recurring patterns and durable one-off references should become wiki pages.
- Leave an audit trail by preserving provenance, running maintenance commands, and appending to `wiki/log.md` when the vault materially changes.

For headless operation, a scheduler may run:

```bash
scripts/run_autonomous_promotion.sh
```

That runner expects `AUTOPROMOTE_COMMAND` to name the local headless agent command that will read the generated prompt from stdin.

## Weekly Grooming (VPS cron)

`scripts/run_weekly_grooming.sh` is a broader pass than `run_autonomous_promotion.sh` — deterministic baseline + lint fixes + orphan fixes + root-inbox triage + `wiki/inbox/` promotion + `overview.md` freshness check, in one run. Designed to run on a schedule against the vault's headless-Obsidian-sync copy (an always-on machine, not the primary editing device), so `wiki/inbox/` gets processed regularly even when no one opens the vault for weeks.

It expects `GROOMING_AGENT_COMMAND` to name the local headless agent command that will read the generated prompt from stdin, same pattern as `AUTOPROMOTE_COMMAND`.

Example weekly cron (Sunday 3am local):

```cron
0 3 * * 0 cd /path/to/llm-wiki && GROOMING_AGENT_COMMAND='your-agent-command' scripts/run_weekly_grooming.sh
```

## Synthesis Prep Workflow

When you want a deterministic review brief before doing higher-judgment synthesis work:

1. Run `python3 scripts/synthesis_report.py`.
2. Open the newest report under `wiki/pages/reports/`.
3. Review:
 - new or changed journal entries
 - new or changed `wiki/inbox/` items
 - repeated names and phrases
 - possible cross-note connections
 - orphan durable notes
4. Audit the report quality before trusting it:
 - are the surfaced names and phrases materially useful?
 - is the output dominated by filler, transcript boilerplate, or weather-style repetition?
 - did it miss any obvious recurring topic, durable one-off reference, entity, or connection?
5. If the report is structurally noisy or repeatedly misses clear patterns, prefer tuning `scripts/synthesis_report.py` before doing large-scale promotion.
6. Treat the report as synthesis input, not as a substitute for human or agent judgment.
7. Promote the strongest findings into `wiki/topics/`, `wiki/pages/`, or `wiki/crm/`.

## Lint Workflow

When asked to lint or health-check the wiki, look for:

- orphan pages
- duplicate concepts
- stale summaries superseded by newer sources
- contradictions across pages
- missing high-value cross-links
- claims, references, or insights that deserve their own page because they are recurring or durably useful
- index entries that are missing or out of date
- journal insights or `wiki/inbox/` items that deserve promotion into the wiki
- CRM records that are mentioned elsewhere but do not exist yet
- untriaged files sitting at the `wiki/` root inbox
- `wiki/inbox/` items past a couple weeks old with no triage decision made

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
python3 scripts/wiki_tool.py cross-link-candidates
python3 scripts/wiki_tool.py dead-links
python3 scripts/wiki_tool.py root-inbox
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
