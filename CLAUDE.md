# Claude Instructions

This repository is a personal "LLM wiki".

Read and follow [WIKI_SCHEMA.md](WIKI_SCHEMA.md) before making any changes.

## Role

Maintain the local markdown wiki in `wiki/`, which is the user-facing vault, from the immutable source material in `raw/`.

- Do not rewrite or "clean up" raw sources in place.
- Search `wiki/catalog.jsonl` before opening broad raw context.
- Keep provenance machine-readable with `raw_source`, `sources`, and `source_count`.
- Run `python3 scripts/wiki_tool.py build`, `lint`, and `source-lint` after material wiki maintenance and before meaningful tooling or schema commits.
- Use promotion helpers to surface candidates, but keep topic/entity promotion decisions agent-driven.
- Treat `wiki/topics/` as canonical hubs and `wiki/pages/` as supporting durable notes.
- Keep wiki pages interlinked.
- Prefer incremental synthesis over chat-only answers.
- Update `wiki/index.md` and append to `wiki/log.md` when the vault changes materially.
- Use `wiki/journal/` and `wiki/crm/` as first-class vault areas when asked.
- Normalized Telegram voice-note captures may be written directly into `wiki/journal/`.
- Treat git as the versioned maintenance layer, not as the primary live transport for vault content.

This file mirrors `AGENTS.md` on purpose so the repository works with multiple coding agents.
