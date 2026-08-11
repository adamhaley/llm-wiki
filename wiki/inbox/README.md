# Inbox

Single landing zone for everything not yet triaged: Web Clipper captures, raw source material, anything dropped in ad hoc. Inside the vault on purpose, so Obsidian Sync carries it to every device — including a headless VPS instance — without a separate transport.

This folder is for fast collection, not curation.

- Expect noisy or partial captures. No frontmatter or naming convention required to add something here.
- Mark `status: inbox` in frontmatter when practical; leave it off if the capture is plain text.
- Not catalog-indexed and not linted (`wiki_tool.py` deliberately skips this folder in `build`/`lint`) — it's pre-processing material, not a wiki note yet.
- Promote durable material into `wiki/topics/`, `wiki/pages/`, or `wiki/crm/` after review; delete what turns out to have no durable signal.
- If a source page's `raw_source` needs to point at something here for provenance, mark that file `status: archived` (not `inbox`) once promoted, rather than deleting it.
- `assets/` holds images/attachments referenced by inbox or promoted material.
