# Field Reports

Use this directory for structured field captures: photos, GPS location, and notes sent from the field (currently via the Telegram multimodal capture bot). This is a first-class citizen, separate from `journal/`, because these captures are structured and repeatable rather than narrative — mixing them into the daily journal would bury reflective entries under location dumps.

**Why this exists:** Adam drives Lyft part-time across Los Angeles. This capture bot turns that driving time into business-development time — logging leads and observations from all over the city while on the road, not just earning per-ride income. These notes are the raw capture layer; the plan is to eventually promote them into a `prospects` table in `adamhaley-com`, alongside other lead sources (see [CRM Database Pipeline](../pages/crm-database-pipeline.md)).

One markdown file per capture session. Never merged into a shared daily file, so there is no read-modify-write collision risk with a live Obsidian Sync edit.

## Filename Convention

- `YYYY-MM-DDTHH-MM-SS.md`, flat in this directory. No nested per-source subdirectories.
- The timestamp is the capture session's start time (when the first message of the session arrived), not per-item timestamps.

## Frontmatter Convention

```yaml
---
title: 2026-08-19 14:32 Field Report
type: field-report
captured_at: 2026-08-19T14:32:00-07:00
location:
  latitude: 34.1478
  longitude: -118.1445
source: telegram-capture
tags:
  - field-report
---
```

Leave `location` absent (not zeroed) when no location was captured in the session. Do not invent coordinates.

## Body Convention

- Start with the synthesized report text, not placeholder text.
- Follow with image embeds (`![[filename.jpg]]`) for any photos captured in the session, in the order they were sent.
- Contact info, when present, is captured freeform in the body for now rather than as discrete frontmatter fields — promote to structured fields later only if repeated use shows a real pattern worth extracting (see [Use-Led Simplicity](/WIKI_SCHEMA.md)).

## Attachments

Images live in `attachments/`, flat, named `{captured_at-slug}-{n}.{ext}` (e.g. `2026-08-19T14-32-00-1.jpg`). Referenced from the report note by filename via wikilink embed.
