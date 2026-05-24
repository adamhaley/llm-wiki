---
title: Second Brain
type: topic
status: active
created: 2026-05-24
updated: 2026-05-24
sources:
source_count: 0
aliases:
  - llm second brain
  - personal knowledge workflow
tags:
  - topic
  - second-brain
  - workflow
---

# Second Brain

## Summary

A practical second-brain workflow keeps capture cheap, preserves raw material, and promotes only the ideas that become durable enough to deserve canonical wiki pages.

## Key Points

- Let `wiki/journal/` stay low-friction for thoughts, experiments, progress notes, names, and loose ideas.
- Let `wiki/inbox-clips/` act as an intake lane for clipped external material before deciding what is worth curating.
- Use periodic promotion passes to move recurring or durable material into `wiki/topics/`, `wiki/entities/`, `wiki/crm/`, and `wiki/syntheses/`.
- Treat `wiki/sources/` as the curated summary layer for important external source material.
- The value of the system comes more from review cadence than from capture volume alone.

## Notes

### Practical Workflow

1. `journal/` stays cheap:
   - capture thoughts, experiments, progress notes, names, and loose ideas
   - do not over-organize at entry time
2. `inbox-clips/` stays as inbox:
   - clip articles, docs, threads, and references into `wiki/inbox-clips/`
   - do not treat clipped pages as curated knowledge yet
3. Periodic promotion passes create structure:
   - promote recurring ideas from journal into [Topics Index](index.md)
   - promote recurring people, orgs, and tools into [Entities Index](../entities/index.md)
   - promote relationship-relevant people into [CRM Index](../crm/index.md)
   - promote multi-note conclusions into [Syntheses Index](../syntheses/index.md)

### Working Model

- `journal/` = raw lived stream
- `inbox-clips/` = raw external stream
- `sources/` = curated source summaries
- `topics/` = stable concepts
- `entities/` = stable nouns
- `syntheses/` = higher-order thinking
- `crm/` = people with relationship context

### Operating Boundary

The system has a practical split between a deterministic tool layer and a meaning-oriented vault layer.

- Tool layer:
  - best for build, lint, source scanning, catalog generation, sync, and other repeatable maintenance work
  - suitable for automation and scheduled jobs because the operations are low-judgment and deterministic
- Vault layer:
  - best for synthesis, promotion, semantic cross-linking, and other note-centric reasoning tasks
  - better kept human-in-the-loop or agent-in-the-loop because these tasks require judgment about meaning, relevance, and canonical structure

This boundary is not only about files versus Obsidian. It is also about what should be safely automatable versus what should remain interpretive.

### Review Rhythm

- Daily:
  - add journal notes
  - clip useful things
  - optionally ingest one important source
- Weekly:
  - review recent journal entries
  - run promotion helpers
  - create or update a few topic or entity pages
  - summarize notable patterns into one synthesis note
- Monthly:
  - merge duplicates
  - tighten cross-links
  - update overview pages
  - turn clusters of notes into stronger syntheses

### Promotion Heuristics

- Create a topic page when an idea recurs and future retrieval will be easier with a canonical page.
- Create an entity page when a person, org, or tool keeps appearing across notes.
- Create a synthesis page when there is a conclusion, comparison, or decision worth preserving.
- Leave material in the journal when it is purely situational, emotional, or one-off.

### Web Clipper Workflow

1. Clip into [Inbox Clips](../inbox-clips/README.md).
2. During review, decide whether to ignore it, move it into `raw/`, or summarize it into `wiki/sources/`.
3. Connect the material to an existing topic or entity page when possible.
4. Create a new durable page only when the clipped item adds a genuinely reusable idea.

### Practical Usage

- Use the tool layer for system operations:
  - sync
  - indexing
  - manifests
  - linting
  - non-semantic health checks
- Use the vault layer for meaning work:
  - reviewing recent journal entries
  - deciding what deserves promotion
  - creating or revising topic, entity, CRM, and synthesis notes
  - adding selective cross-links that improve retrieval

The likely steady-state workflow is that the tool layer runs quietly in the background, while the vault layer remains the place where interpretation and knowledge-shaping happen.

## Related Pages

- [Overview](../overview.md)
- [Vault Index](../index.md)
- [Promotion Workflow](../../Schema/promotion-workflow.md)
- [Journal](../journal/README.md)

## Open Questions

- What review cadence will be sustainable enough to keep promotion current without turning the system into overhead?
- Which recurring themes from the journal should become the first durable topic, entity, and synthesis pages after this one?
