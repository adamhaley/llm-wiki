# LLM Wiki

This repository is Adam's second brain: a markdown-based hub for personal knowledge, contact/relationship data, reusable engineering patterns, structured field capture, and daily journaling, maintained by AI agents and synced live via Obsidian Sync. Its knowledge-compilation layer (`wiki/inbox/` → `wiki/topics/`/`wiki/pages/`, with deterministic build/lint tooling) follows the "LLM wiki" pattern described by Andrej Karpathy; `wiki/crm/`, `wiki/journal/`, `wiki/field-reports/`, and `wiki/patterns/` are additional first-class directories built on top of that pattern for the vault's other roles. See [Second Brain](wiki/topics/second-brain.md) for the full picture and [LLM Wiki](wiki/topics/llm-wiki.md) for the compiler pattern specifically.

- `wiki/inbox/` holds raw source material and Web Clipper captures awaiting triage — inside the Obsidian vault, so it reaches every synced device.
- `wiki/` is the markdown wiki and the Obsidian vault.
- `WIKI_SCHEMA.md` defines the operating rules for agentic maintenance.
- `scripts/wiki_tool.py` provides deterministic build, lint, and source coverage checks.

The repository root is agent-facing infrastructure and versioned system behavior.
The Obsidian-visible knowledge base lives under `wiki/`, and the vault content — including `wiki/inbox/` — is intended to sync via Obsidian Sync rather than git.
Most note content under `wiki/` should remain git-ignored by default, with the repo tracking only schemas, scripts, agent instructions, templates, and a small amount of vault configuration.

The intent is simple:

1. Add source material or Web Clipper captures to `wiki/inbox/`.
2. Ask an agent to ingest or promote it into the rest of `wiki/`.
3. Browse or edit the wiki in Obsidian by opening `wiki/` as the vault.
4. Let Obsidian Sync handle live content sync across devices — including a headless VPS instance for scheduled grooming.
5. Use git to version the maintenance layer that drives the vault, not the vault's day-to-day content.

For low-friction operation, capture can be followed by scheduled agent work rather than manual review. `scripts/run_synthesis_report.sh` generates changed-material briefs, and `scripts/run_autonomous_promotion.sh` can hand those briefs to a configured headless agent via `AUTOPROMOTE_COMMAND` so high-confidence durable items are promoted without making the human the default gate.

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
wiki/
  .obsidian/     vault settings; only stable shared config is tracked
  inbox/         raw source material and Web Clipper captures, not yet triaged
    assets/      downloaded images and attachments
  index.md       local vault catalog, typically not tracked
  log.md         local append-only vault activity log, typically not tracked
  overview.md    local top-level map of the knowledge base
  topics/        canonical topic hubs
  pages/         everything else durable: type: page, entity, source, or synthesis
  templates/     starter templates that remain tracked
  journal/       dated reflective entries and session logs
  crm/           contact records and relationship context; the source layer for a live sync into adamhaley-com's Client CRM
  field-reports/ structured field captures (location, photos, notes) from the Telegram capture bot
  patterns/      durable technical/architectural patterns coding agents check before building
```

## Suggested Workflow

1. Put a new article, note, PDF, transcript, or Web Clipper capture directly in `wiki/inbox/`.
2. Ask the agent to ingest or promote a specific item from `wiki/inbox/` into the rest of `wiki/`.
3. Review the proposed or completed updates in `wiki/`.
4. Once fully promoted, delete the `wiki/inbox/` item, or mark it `status: archived` in frontmatter if a source page's `raw_source` still needs it for provenance.

## Sync Boundary

- Obsidian Sync is the live sync system for vault content.
- Git is for versioning system code: scripts, schemas, agent instructions, templates, and selected vault configuration.
- Do not treat git as a second live sync path for the active vault content tree.
- If you intentionally want content snapshots in git, do that as a deliberate archival workflow rather than as the default operating mode.

If you use Obsidian, open `wiki/` as the vault, not the repository root.
