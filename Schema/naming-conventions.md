# Naming Conventions

- Use lowercase kebab-case filenames for durable pages and inbox captures.
- Prefer one canonical page per concept.
- Keep page H1s human-readable even when the filename is terse.
- Use singular durable page names unless the note is naturally plural.
- Keep inbox filenames stable after ingest when possible. If you mark a `wiki/inbox/` file `status: archived`, update the corresponding wiki metadata paths (`raw_source`) if the filename changes.

Directory intent:

- `wiki/inbox/`: raw source material and Web Clipper captures, not yet triaged; inside the vault so Sync carries it everywhere
- `wiki/` root: in-vault inbox for hand-dropped files awaiting triage, distinct from `wiki/inbox/`. List with `python3 scripts/wiki_tool.py root-inbox`. No naming convention required.
- `wiki/topics/`: canonical topic hubs
- `wiki/pages/`: everything else durable — supporting pages (`type: page`), named entities (`type: entity`), source summaries (`type: source`), and syntheses (`type: synthesis`) — differentiated by frontmatter, not by folder
- `wiki/crm/`: named contact records, also the source layer for a live sync into adamhaley-com's Client CRM
- `wiki/journal/`: dated reflection and capture notes, including daily session logs
- `wiki/field-reports/`: structured field captures (location, photos, notes), timestamped filenames, one per capture session
- `wiki/patterns/`: durable technical/architectural patterns, kebab-case pattern name per file
