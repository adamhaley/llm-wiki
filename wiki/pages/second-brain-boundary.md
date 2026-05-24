---
title: Second Brain Operating Boundary
type: page
status: active
created: 2026-05-24
updated: 2026-05-24
sources:
source_count: 0
aliases:
  - tool layer vs vault layer
  - operating boundary
tags:
  - page
  - second-brain
  - architecture
---

# Second Brain Operating Boundary

## Summary

The system has a practical split between a deterministic tool layer and a meaning-oriented vault layer.

## Key Points

- The tool layer is best for build, lint, source scanning, catalog generation, sync, and other repeatable maintenance work.
- The vault layer is best for synthesis, promotion, semantic cross-linking, and other note-centric reasoning tasks.
- The distinction is not only about files versus Obsidian. It is also about what should be safely automatable versus what should remain interpretive.

## Notes

### Tool Layer

- build
- lint
- source scanning
- catalog generation
- sync
- manifests
- non-semantic health checks

These operations are low-judgment and suitable for automation or scheduled jobs.

### Vault Layer

- reviewing recent journal entries
- deciding what deserves promotion
- creating or revising topic, entity, CRM, and synthesis notes
- adding selective cross-links that improve retrieval

These operations require judgment about meaning, relevance, and canonical structure, so they are better kept human-in-the-loop or agent-in-the-loop.

### Practical Usage

The likely steady-state workflow is that the tool layer runs quietly in the background, while the vault layer remains the place where interpretation and knowledge-shaping happen.

## Related Pages

- [Second Brain](../topics/second-brain.md)
- [Second Brain Workflow](second-brain-workflow.md)
- [Second Brain Sync Behavior](second-brain-sync-behavior.md)

## Open Questions

- Which vault tasks should stay fully interpretive even as the tooling layer grows?
