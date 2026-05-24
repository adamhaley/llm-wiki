# LLM Wiki Lint

Use this skill when checking repository health before commit or after a larger ingest.

## Workflow

Run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

If raw source coverage changed, also run:

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```
