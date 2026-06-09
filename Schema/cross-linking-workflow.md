# Cross-Linking Workflow

## The Problem

The wiki tool enforces structure and frontmatter deterministically, but it cannot determine semantic relevance — it can only detect the absence of links, not suggest what should exist. Cross-linking requires agent judgment.

The result without an explicit protocol: pages get created, linked outward to things they reference, but nothing links back to them. They become reachable from the index but invisible from within related pages.

## Mandatory Step: Run orphan-notes After Every Session

After any session that creates or substantially updates durable pages:

```bash
python3 scripts/wiki_tool.py orphan-notes
```

Any page listed as an orphan must have at least one inbound link added before the session ends. An orphan is not a broken page — it just means no existing page links to it yet.

## Deciding What Should Link Where

Apply these heuristics in order:

1. **Cluster membership**: if a new page belongs to an obvious cluster (e.g. all the workflow/architecture pages), every page in that cluster should link to it and it should link back to all of them.

2. **Topic hub**: if the new page supports a canonical topic in `wiki/topics/`, add a link from the topic hub to the new page.

3. **Natural reference**: if an existing page mentions the concept, entity, or project covered by the new page — even in passing — add a link from that page.

4. **Portfolio/resume pages**: any page with resume or career relevance should be linked from `wiki/pages/wiki-as-portfolio.md` and vice versa.

Err toward more links, not fewer. Obsidian's graph view becomes useful only when the link density is high enough to reveal real clusters.

## Minimum Standard

Every durable page in `wiki/pages/`, `wiki/topics/`, `wiki/entities/`, `wiki/syntheses/`, and `wiki/crm/` must have:

- At least one **outbound** link to a related page
- At least one **inbound** link from another page (verified by `orphan-notes`)

Pages in `wiki/journal/` and `wiki/inbox-clips/` are exempt — they are capture zones, not durable reference pages.

## When to Consider a Deterministic Script

A deterministic title/alias scan is feasible: extract all page titles and `aliases` frontmatter values, then search other pages' body text for unlinked occurrences. This would surface "you mention X on this page but don't link to it."

Add this script when:
- The vault exceeds ~100 durable pages and manual orphan-checking becomes unreliable
- Repeated orphan patterns suggest the heuristics above aren't being applied consistently

Until then, `orphan-notes` + agent judgment is sufficient.

## Session Checklist

At the end of any session that touches durable wiki pages:

1. `python3 scripts/wiki_tool.py orphan-notes` — fix any new orphans
2. `python3 scripts/wiki_tool.py build` — rebuild catalog
3. `python3 scripts/wiki_tool.py lint` — verify clean
4. Append to `wiki/log.md` if pages were materially added or changed
