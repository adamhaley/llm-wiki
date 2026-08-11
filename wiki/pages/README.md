# Pages

Durable, compiled knowledge lives here — the flat notes layer of the wiki. This includes what used to be split into separate `entities/`, `sources/`, and `syntheses/` folders; that split was folded in because each file already carries its real type in frontmatter (`type: page`, `entity`, `source`, or `synthesis`), so a dedicated directory per type was redundant with data already on the file.

- Use `type: page` for general supporting notes linked from topic hubs.
- Use `type: entity` for named entities (people, orgs, tools, places).
- Use `type: source` for one page per ingested source (requires `raw_source` pointing into `wiki/inbox/`).
- Use `type: synthesis` for comparisons, decision memos, and query outputs worth preserving.
- Use `wiki/crm/` instead of `type: entity` for people who are contacts/relationships — CRM stays a separate folder because promotion there is gated behind human review for sensitive claims.
- Use `wiki/topics/` instead for canonical hub pages — topics stay separate as the navigational index-of-indexes layer.

Prefer one canonical page per concept; merge duplicates instead of proliferating near-copies.
