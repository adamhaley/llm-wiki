---
name: llm-wiki-promote
description: Use this skill when promoting durable ideas from journal entries, source pages, or existing wiki notes into canonical topic hubs, supporting pages, entity, CRM, or synthesis pages.
---

# LLM Wiki Promote

Use this skill when promoting durable ideas from journal entries, source pages, or existing wiki notes into canonical topic hubs, supporting pages, entity, CRM, or synthesis pages.

## Workflow

1. Read `WIKI_SCHEMA.md` and `Schema/promotion-workflow.md`.
2. Surface candidates without making automatic semantic decisions:

```bash
python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal
python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2
python3 scripts/wiki_tool.py orphan-notes
```

3. Review the most relevant journal or wiki notes.
4. Promote only durably useful ideas. Recurrence is a signal, not a requirement; one-off items can be promoted when they are reference-grade, decision-relevant, project-relevant, rare, clarifying, or likely to save rediscovery later:
   - durable canonical concepts -> `wiki/topics/`
   - supporting durable notes -> `wiki/pages/`
   - people/orgs/tools -> `wiki/entities/`
   - relationship-specific people -> `wiki/crm/`
   - multi-note summaries or high-leverage conclusions -> `wiki/syntheses/`
5. In autonomous mode, promote high-confidence durable material without asking first. Ask only for sensitive CRM claims, destructive deletes or merges, major taxonomy changes, or unresolved contradictions.
6. Prefer updating canonical pages over creating duplicates.
7. Add explicit links where they materially improve navigation.
8. Keep provenance factual. Journal-only promotions should cite journal entries in the body; external-source-backed notes should keep `sources` accurate.
9. Run:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/audit_public.py
```
