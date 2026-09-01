# Journal

Use this directory for Adam's own dated personal reflections, dictated thoughts, and daily
notes — his voice, not agent-authored work summaries. Agent session-log content (what was
actually done on a project) belongs in `wiki/projects/{project}/session-logs/` instead — see
`wiki/projects/README.md` — specifically so this directory doesn't fill up with agent output.

A typical pattern is one markdown file per day or per session, grounded in related wiki pages when relevant.

## Filename Convention

- Use `YYYY-MM-DD.md` with zero-padded month and day, directly in this directory. No nested per-source subdirectories (e.g. No `telegram/YYYY/`). That pattern was tried and abandoned as over-engineered relative to the actual sync-collision risk.
- Telegram (or other automated) captures should land as a timestamped section appended to the day's file, the same shape as a hand-written multi-entry day: a `H:MM AM/PM` header line followed by the entry text. Use `source: telegram-voice` in frontmatter when the whole file originated from a single automated capture; for mixed days, a body-level note is enough.
- If automation cannot safely append to a shared daily file directly (e.g. It cannot read-modify-write without risking a collision with a live Obsidian Sync edit), it may land a standalone `YYYY-MM-DDTHH-MM-SS.md` capture file flat in this directory instead. Never nested. Fold same-day capture files into the canonical `YYYY-MM-DD.md` during routine review and delete the capture file once folded.
- Keep non-journal experiments, import debris, and agent session-log content out of this directory — the latter goes to `wiki/projects/{project}/session-logs/`.

## Light Frontmatter Convention

Frontmatter is optional for imported legacy entries, but recommended for new automated captures such as Telegram voice notes.

```yaml
---
title: 2026-05-24 Journal
type: journal
created: 2026-05-24
updated: 2026-05-24
source: telegram-voice
tags:
  - journal
---
```

## Body Convention

- Start with the actual note content, not placeholder text.
- Preserve timestamps when they carry meaning.
- Link to CRM or wiki pages only when the connection is durable.
