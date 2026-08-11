---
name: llm-wiki-ingest
description: Use this skill when ingesting new material from raw sources into the wiki while preserving provenance and updating affected durable notes.
---

# LLM Wiki Ingest

Use this skill when ingesting new material from `wiki/inbox/` into the rest of `wiki/`.

## Workflow

1. Read `WIKI_SCHEMA.md`.
2. Run `python3 scripts/wiki_tool.py source-delta`.
3. Search `wiki/catalog.jsonl` before opening broad `wiki/inbox/` context.
4. Update or create:
   - a `type: source` page in `wiki/pages/`
   - affected durable wiki notes
5. Keep provenance in note frontmatter:
   - `raw_source` for source pages
   - `sources` and `source_count` for compiled notes
6. Run:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```
