# Claude Instructions

This repository is a personal "LLM wiki".

Read and follow [WIKI_SCHEMA.md](WIKI_SCHEMA.md) before making any changes.

## Role

Maintain the markdown wiki in `wiki/`, which is the user-facing vault, from the immutable source material in `raw/`.

- Do not rewrite or "clean up" raw sources in place.
- Keep wiki pages interlinked.
- Prefer incremental synthesis over chat-only answers.
- Update `wiki/index.md` and append to `wiki/log.md` when the vault changes materially.
- Use `wiki/journal/` and `wiki/crm/` as first-class vault areas when asked.
- Normalized Telegram voice-note captures may be written directly into `wiki/journal/`.

This file mirrors `AGENTS.md` on purpose so the repository works with multiple coding agents.
