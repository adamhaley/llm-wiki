---
title: Second Brain Sync Behavior
type: page
status: active
created: 2026-05-24
updated: 2026-05-24
sources:
source_count: 0
aliases:
  - sync behavior
  - idle vs active sync
tags:
  - page
  - second-brain
  - sync
---

# Second Brain Sync Behavior

## Summary

Scheduled pull automation is most useful during idle periods, not active editing periods.

## Key Points

- When the repo is clean and idle, scheduled pull can fast-forward journal updates automatically.
- When the repo is dirty or locally ahead because work is in progress, scheduled pull should skip safely.
- The automation behaves more like passive background refresh than live two-way sync.

## Notes

### Practical Behavior

During stretches where the repo is not being actively edited on the local machine, journal updates can land without attention. During active work, sync pauses rather than creating conflicts.

### Operational Implication

This makes scheduled pull worthwhile for passive periods even if it cannot solve the active-development case in the same working tree.

## Related Pages

- [Second Brain](../topics/second-brain.md)
- [Second Brain Operating Boundary](second-brain-boundary.md)

## Open Questions

- At what point would a dedicated clean sync clone be worth the extra operational complexity?
