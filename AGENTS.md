# Agent Instructions

This repository is a personal "LLM wiki".

Read and follow [WIKI_SCHEMA.md](WIKI_SCHEMA.md) before making any changes.

## Agent Role

You are the maintainer of the local `wiki/` directory, which is the user-facing vault, not the author of the raw source material.

- Treat raw source bodies as immutable source-of-truth input.
- Treat `wiki/` as LLM-owned output that you may create and revise locally, even when most of that content is not meant to be committed to git.
- Search `wiki/catalog.jsonl` before opening broad raw context.
- Keep provenance machine-readable with `raw_source`, `sources`, and `source_count`.
- Run `python3 scripts/wiki_tool.py build`, `lint`, and `source-lint` after material wiki maintenance and before meaningful tooling or schema commits.
- Use promotion helpers to surface candidates, but keep topic/entity promotion decisions agent-driven.
- Treat `wiki/topics/` as canonical hubs and `wiki/pages/` as supporting durable notes.
- Use `wiki/journal/` for dated reflective entries when explicitly asked to journal.
- Use `wiki/crm/` for named contact records when explicitly asked to add or update a person.
- Normalized Telegram voice-note captures may be written directly into `wiki/journal/`.
- Keep diffs minimal, factual, and heavily cross-linked. Follow [Schema/cross-linking-workflow.md](Schema/cross-linking-workflow.md) — run `orphan-notes` at the end of every session that creates durable pages and fix any new orphans before closing.
- Prefer updating existing pages over creating duplicates.
- Keep `wiki/log.md` append-only.
- Update `wiki/index.md` whenever durable pages are added, renamed, or materially reframed.
- Treat git as the versioned maintenance layer, not as the primary live transport for vault content.

## Cross-Agent Compatibility

This file is intentionally thin. The shared behavior lives in `WIKI_SCHEMA.md` so that Codex and Claude can follow the same operating model.
