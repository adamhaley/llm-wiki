# Naming Conventions

- Use lowercase kebab-case filenames for durable pages and raw captures.
- Prefer one canonical page per concept.
- Keep page H1s human-readable even when the filename is terse.
- Use singular durable page names unless the note is naturally plural.
- Keep source filenames stable after ingest when possible. If you move a file into `raw/processed/`, update the corresponding wiki metadata paths.

Directory intent:

- `raw/`: external source material not visible in the Obsidian vault
- `wiki/sources/`: source summaries and provenance pages
- `wiki/topics/`: canonical topic hubs
- `wiki/pages/`: supporting durable pages related to canonical topics
- `wiki/entities/`: people, orgs, places, tools
- `wiki/syntheses/`: comparisons, decisions, query outputs worth keeping
- `wiki/crm/`: named contact records
- `wiki/journal/`: dated reflection and capture notes
