# Journal

Use this directory for dated journal entries.

A typical pattern is one markdown file per day or per session, grounded in related wiki pages when relevant.

## Filename Convention

- Use `YYYY-MM-DD.md` with zero-padded month and day.
- Keep non-journal experiments and import debris out of this top-level directory.

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
