# Vault Log

Append-only chronological log of vault operations.

## [2026-05-23] init | repository scaffold

Created the initial LLM wiki structure with shared schema, cross-agent instructions, root index and log, raw source directories, wiki directories, journal and CRM directories, starter templates, and overview files.

## [2026-05-23] refactor | obsidian-friendly layout

Adjusted the scaffold to better match the Obsidian-friendly pattern described by MindStudio: root `index.md` and `log.md`, `raw/processed/`, plus first-class `journal/` and `crm/` directories.

## [2026-05-23] policy | direct journal capture

Updated the schema and agent instructions to allow normalized Telegram voice-note captures to write directly into `journal/`, while reserving `raw/` for external source material.
