# LLM Wiki

This repository implements a local "LLM wiki" in the style described by Andrej Karpathy.

- `raw/` holds source material for ingestion.
- `wiki/` is the markdown wiki and the Obsidian vault.
- `WIKI_SCHEMA.md` defines the operating rules for agentic maintenance.

The repository root is agent-facing infrastructure. The Obsidian-visible knowledge base lives under `wiki/`.
`raw/` is intentionally noisy and is git-ignored except for its tracked skeleton files.

The intent is simple:

1. Add source material to `raw/`.
2. Ask an agent to ingest it into `wiki/`.
3. Browse or edit the wiki in Obsidian by opening `wiki/` as the vault.
4. Periodically lint and reconcile the wiki.

Both Codex and Claude can use this repo:

- `AGENTS.md` is the Codex entrypoint.
- `CLAUDE.md` is the Claude entrypoint.
- Both point at the shared schema in `WIKI_SCHEMA.md`.

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
  .obsidian/     Obsidian vault settings
  inbox-clips/   Obsidian-visible landing zone for Web Clipper captures
  index.md       vault catalog
  log.md         append-only vault activity log
  overview.md    current top-level map of the knowledge base
  sources/       one page per ingested source
  topics/        concept and theme pages
  entities/      people, orgs, tools, places, etc.
  syntheses/     comparisons, query results, and higher-level analyses
  templates/     starter templates for common page types
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

If you use Obsidian, open `wiki/` as the vault, not the repository root.
