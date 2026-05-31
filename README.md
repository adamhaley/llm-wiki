# LLM Wiki

This repository implements a local "LLM wiki" in the style described by Andrej Karpathy.

- `raw/` holds source material for ingestion.
- `wiki/` is the markdown wiki and the Obsidian vault.
- `WIKI_SCHEMA.md` defines the operating rules for agentic maintenance.
- `scripts/wiki_tool.py` provides deterministic build, lint, and source coverage checks.

The repository root is agent-facing infrastructure and versioned system behavior.
The Obsidian-visible knowledge base lives under `wiki/`, but the vault content is intended to sync via Obsidian Sync rather than git.
`raw/` is intentionally noisy and is git-ignored except for its tracked skeleton files.
Most note content under `wiki/` should also remain git-ignored by default, with the repo tracking only schemas, scripts, agent instructions, templates, and a small amount of vault configuration.

The intent is simple:

1. Add source material to `raw/`.
2. Ask an agent to ingest it into `wiki/`.
3. Browse or edit the wiki in Obsidian by opening `wiki/` as the vault.
4. Let Obsidian Sync handle live content sync across devices.
5. Use git to version the maintenance layer that drives the vault, not the vault's day-to-day content.

Both Codex and Claude can use this repo:

- `AGENTS.md` is the Codex entrypoint.
- `CLAUDE.md` is the Claude entrypoint.
- Both point at the shared schema in `WIKI_SCHEMA.md`.

## Deterministic Layer

Run these commands as the maintenance baseline:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

Local generated artifacts:

- `wiki/catalog.jsonl`
- `wiki/index.md`
- `wiki/*/index.md`
- `Schema/source-manifest.jsonl`

Promotion helpers:

- `python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal`
- `python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2`
- `python3 scripts/wiki_tool.py orphan-notes`

## Directory Layout

```text
AGENTS.md
CLAUDE.md
WIKI_SCHEMA.md
raw/
  README.md      intake policy for raw capture
  processed/     source files after ingestion
  assets/        downloaded images and attachments referenced by sources
wiki/
  .obsidian/     vault settings; only stable shared config is tracked
  inbox-clips/   Obsidian-visible landing zone for Web Clipper captures
  index.md       local vault catalog, typically not tracked
  log.md         local append-only vault activity log, typically not tracked
  overview.md    local top-level map of the knowledge base
  sources/       one page per ingested source
  topics/        canonical topic hubs
  pages/         supporting durable pages linked from topics
  entities/      people, orgs, tools, places, etc.
  syntheses/     comparisons, query results, and higher-level analyses
  templates/     starter templates that remain tracked
  journal/       dated reflective entries
  crm/           contact records and relationship notes
```

## Suggested Workflow

1. Put a new article, note, PDF, transcript, or markdown file directly in `raw/`.
2. Use `wiki/inbox-clips/` for Web Clipper captures that should stay visible in Obsidian.
3. Ask the agent to ingest a specific source into `wiki/`.
4. Move or normalize useful clipped content from `wiki/inbox-clips/` into `raw/` or directly into the wiki, depending on the workflow.
5. Review the proposed or completed updates in `wiki/`.
6. Move the source into `raw/processed/` once it has been ingested when you want to retain a processed raw record.

## Sync Boundary

- Obsidian Sync is the live sync system for vault content.
- Git is for versioning system code: scripts, schemas, agent instructions, templates, and selected vault configuration.
- Do not treat git as a second live sync path for the active vault content tree.
- If you intentionally want content snapshots in git, do that as a deliberate archival workflow rather than as the default operating mode.

If you use Obsidian, open `wiki/` as the vault, not the repository root.
