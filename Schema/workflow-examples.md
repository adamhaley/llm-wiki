# Workflow Examples

## Ingest A New Source

1. Put the source file in `raw/`.
2. Run `python3 scripts/wiki_tool.py source-delta` to see untracked raw sources.
3. Create or update:
   - one source page in `wiki/sources/`
   - any affected topic, entity, synthesis, or CRM pages
4. Add the raw path into compiled note `sources`.
5. Run:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

6. Append to `wiki/log.md` if the ingest materially changed the vault.

## Answer A Question From The Wiki

1. Open `wiki/index.md`.
2. Run `python3 scripts/wiki_tool.py search-catalog --query "topic"`.
3. Read the most relevant wiki pages.
4. Open raw sources only if the compiled notes are insufficient or the user asks for source-level verification.
5. If the answer becomes durable knowledge, file it into `wiki/syntheses/` and rerun the maintenance commands.

## Move A Processed Source

1. Move the source file from `raw/` to `raw/processed/`.
2. Keep the existing `raw/...` reference updated in any affected wiki note metadata.
3. Run `python3 scripts/wiki_tool.py source-scan --update --accept-covered`.
4. Run `python3 scripts/wiki_tool.py source-lint`.

## Promote Journal Ideas Into Durable Wiki Notes

1. Surface candidates:

```bash
python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal
python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2
python3 scripts/wiki_tool.py orphan-notes
```

2. Review the suggested names and phrases as prompts, not decisions.
3. Choose only durable concepts, people, projects, or syntheses worth keeping.
4. Create or update canonical notes in `wiki/topics/`, `wiki/entities/`, `wiki/crm/`, or `wiki/syntheses/`.
5. Use `wiki/pages/` for supporting durable notes that belong under a topic hub rather than acting as peer topics.
6. Add explicit links back from relevant journal entries or durable notes where useful.
7. Keep provenance factual. Journal-only promotions may cite the journal note paths in the body while leaving `sources` empty unless a raw source also supports the claim.
8. Run:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/audit_public.py
```

## Generate A Synthesis Review Brief

1. Run:

```bash
python3 scripts/synthesis_report.py
```

2. Open the newest file under `wiki/pages/reports/`.
3. Review:
   - new journal entries
   - new inbox clips
   - repeated names
   - repeated phrases
   - potential cross-note connections
   - orphan durable notes
4. Decide what deserves promotion into `wiki/topics/`, `wiki/pages/`, `wiki/entities/`, `wiki/crm/`, or `wiki/syntheses/`.
5. Keep the report as a review aid, not as a substitute for canonical notes.
