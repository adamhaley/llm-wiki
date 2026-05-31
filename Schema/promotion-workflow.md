# Promotion Workflow

Promotion is intentionally agent-driven. The tooling may surface candidate phrases, names, and orphans, but it does not decide what deserves a durable wiki page.

## Goal

Turn durably useful ideas from `wiki/journal/`, `wiki/sources/`, and existing compiled notes into focused pages under:

- `wiki/topics/`
- `wiki/pages/`
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

These are candidate signals only. They are not reliable enough to create pages automatically, and they are biased toward recurrence. Agents must also look for one-off material with high future utility.

## Agent Decision Rules

Promote when at least one of these is true:

- the same person, project, or topic recurs across multiple entries
- the idea is likely to matter beyond a single day
- the note would make future retrieval faster
- the concept is easier to understand once separated from narrative journal context
- the item is a one-off but reference-grade guide, command, architecture, paper, repository, or explanation
- the item informs a current or likely future decision
- the item is rare, hard-won, project-relevant, or likely to save rediscovery later

Do not promote when:

- the content is purely ephemeral mood or weather
- the phrase is repeated but semantically weak
- the note would become a one-line stub with no future value
- the item is interesting but has no plausible retrieval, decision, project, or reference value

## Promotion Shapes

Use the destination based on semantics:

- `wiki/topics/`: canonical hubs for durable themes, practices, tools, and philosophies; recurrence is helpful but not required when the topic is important
- `wiki/pages/`: supporting durable notes linked from hubs when the note is useful but not itself a canonical topic
- `wiki/entities/`: people, companies, tools, places
- `wiki/crm/`: people with relationship context
- `wiki/syntheses/`: a higher-order memo, decision, comparison, or summary; it may span multiple entries or capture one high-leverage conclusion

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
