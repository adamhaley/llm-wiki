# Lint Checklist

The deterministic maintenance gate should catch these cases before commit:

- required root folders are missing
- `wiki/catalog.jsonl` is stale or absent
- `Schema/source-manifest.jsonl` is stale or absent
- strict wiki notes are missing required frontmatter
- compiled notes have broken or missing raw source paths
- `source_count` does not match `sources`
- a manifest entry points to a missing raw source
- a processed raw source has no wiki coverage
- tracked files contain obvious secrets or machine-local path leaks

Manual health checks still matter for:

- duplicate concepts
- weak summaries
- orphan notes that are technically valid but poorly linked
- journal insights worth promoting into curated wiki pages
