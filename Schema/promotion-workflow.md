# Promotion Workflow

Promotion is intentionally agent-driven. The tooling may surface candidate phrases, names, and orphans, but it does not decide what deserves a durable wiki page.

## Goal

Turn recurring or durable ideas from `wiki/journal/`, `wiki/sources/`, and existing compiled notes into focused pages under:

- `wiki/topics/`
- `wiki/entities/`
- `wiki/crm/`
- `wiki/syntheses/`

## Deterministic Helper Signals

Use these commands to surface likely work:

```bash
python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal
python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2
python3 scripts/wiki_tool.py orphan-notes
```

Interpretation:

- `promotion-candidates --mode names` surfaces repeated capitalized names across notes.
- `promotion-candidates --mode phrases` surfaces repeated multi-word phrases across notes.
- `orphan-notes` surfaces compiled notes that currently have no inbound links from other compiled notes.

These are candidate signals only. They are not reliable enough to create pages automatically.

## Agent Decision Rules

Promote when at least one of these is true:

- the same person, project, or topic recurs across multiple entries
- the idea is likely to matter beyond a single day
- the note would make future retrieval faster
- the concept is easier to understand once separated from narrative journal context

Do not promote when:

- the content is purely ephemeral mood or weather
- the phrase is repeated but semantically weak
- the note would become a one-line stub with no future value

## Promotion Shapes

Use the destination based on semantics:

- `wiki/topics/`: recurring themes, practices, tools, philosophies
- `wiki/entities/`: people, companies, tools, places
- `wiki/crm/`: people with relationship context
- `wiki/syntheses/`: a higher-order memo or summary spanning multiple entries

## Linking Guidance

- Link new durable pages outward to relevant existing pages.
- Add at least one inbound path by updating another durable page when practical.
- Journal links are optional and should be added selectively, not mechanically.
- Prefer a few useful links over blanket backlink spam.

## Provenance Guidance

If a durable page is grounded only in journal entries:

- keep claims modest and factual
- cite the relevant journal entries in the body
- leave `sources` empty unless an external raw source also supports the claim
- avoid overstating conclusions drawn from a single reflection

If a durable page is grounded in external source material:

- keep `sources` populated with raw file paths
- keep `source_count` accurate

## Finish

After a promotion pass, run:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/audit_public.py
```

Append to `wiki/log.md` if the promotion materially changed the vault.
