# LLM Wiki Maintain

Use this skill for general upkeep.

## Tasks

- rebuild the catalog and indexes
- refresh the source manifest
- identify uncovered raw sources
- detect invalid wiki metadata
- append short deterministic log entries with `wiki_tool.py log`

## Commands

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-coverage
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```
