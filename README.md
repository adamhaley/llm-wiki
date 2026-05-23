# Brain

This repository implements a local "LLM wiki" in the style described by Andrej Karpathy, using an Obsidian-friendly vault layout:

- `raw/` holds newly clipped or imported source material.
- `raw/processed/` holds source material after ingestion.
- `wiki/` holds LLM-maintained markdown pages.
- `journal/` holds dated journal entries.
- `crm/` holds person records.
- `WIKI_SCHEMA.md` defines the operating rules for agentic maintenance.

The intent is simple:

1. Add source material to `raw/`.
2. Ask an agent to ingest it into `wiki/`.
3. Ask questions against the wiki and file useful answers back into it.
4. Periodically lint and reconcile the wiki.

Both Codex and Claude can use this repo:

- `AGENTS.md` is the Codex entrypoint.
- `CLAUDE.md` is the Claude entrypoint.
- Both point at the shared schema in `WIKI_SCHEMA.md`.

## Directory Layout

```text
index.md        root catalog for the vault
log.md          append-only chronological activity log
raw/
  processed/    source files after ingestion
  assets/       downloaded images and attachments referenced by sources
wiki/
  overview.md   current top-level map of the knowledge base
  sources/      one page per ingested source
  topics/       concept and theme pages
  entities/     people, orgs, tools, places, etc.
  syntheses/    comparisons, query results, and higher-level analyses
  templates/    starter templates for common page types
journal/        dated reflective entries
crm/            contact records and relationship notes
```

## Suggested Workflow

1. Put a new article, note, PDF, transcript, or markdown file directly in `raw/`.
2. Ask the agent to ingest a specific source.
3. Review the proposed or completed updates in `wiki/`.
4. Move the source into `raw/processed/` once it has been ingested.

If you use Obsidian, open this repository as a vault.
