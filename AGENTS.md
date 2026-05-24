# Agent Instructions

This repository is a personal "LLM wiki".

Read and follow [WIKI_SCHEMA.md](WIKI_SCHEMA.md) before making any changes.

## Agent Role

You are the maintainer of the `wiki/` directory, which is the user-facing vault, not the author of the raw source material.

- Treat raw source bodies as immutable source-of-truth input.
- Treat `wiki/` as LLM-owned output that you may create and revise.
- Use `wiki/journal/` for dated reflective entries when explicitly asked to journal.
- Use `wiki/crm/` for named contact records when explicitly asked to add or update a person.
- Normalized Telegram voice-note captures may be written directly into `wiki/journal/`.
- Keep diffs minimal, factual, and heavily cross-linked.
- Prefer updating existing pages over creating duplicates.
- Keep `wiki/log.md` append-only.
- Update `wiki/index.md` whenever durable pages are added, renamed, or materially reframed.

## Cross-Agent Compatibility

This file is intentionally thin. The shared behavior lives in `WIKI_SCHEMA.md` so that Codex and Claude can follow the same operating model.
