# Projects

Per-project grouping for the three kinds of content that pile up around an actively-worked
project: plans, session logs, and takeaways. Kept separate from the flat `wiki/pages/` and
`wiki/journal/` layers because once a project has enough of this content, reading it back by
project (not by date or by note type) is the more useful retrieval shape.

## Core Value: Earn Your Keep

Same principle as [Patterns](/wiki/patterns/README.md) — see
[Use-Led Simplicity](/WIKI_SCHEMA.md), with one adjustment for `session-logs/` specifically:
`wiki/journal/` is Adam's own personal space, not a fallback for agent work summaries (see
`wiki/journal/README.md`), so a `session-logs/` entry for a real, nameable project is fine to
create on its very first entry — there's no other home for that content to wait in. The
"don't create too early" caution still applies to `plans/` and `takeaways/`, and to creating a
`wiki/projects/{project}/` folder at all for something that isn't really a distinct tracked
project (a one-off errand, a single unrelated task) — a single `wiki/pages/` page still covers
that case. A project folder that never grows past its first dated file in more than one of the
three subdirectories was probably created too early; fold it back rather than leaving stale
subdirectories around.

## Directory Shape

```
wiki/projects/{project-slug}/
  plans/
    YYYY-MM-DD.md
  session-logs/
    YYYY-MM-DD.md
  takeaways/
    YYYY-MM-DD.md
```

- `{project-slug}`: kebab-case, matching the `project:` frontmatter value already used
  elsewhere in the vault (e.g. `deh-faq-autoresponder`, `site-screenshots`,
  `risk-fast-check-static-quiz`) so the two stay in sync. Check existing `project:` values
  across `wiki/pages/*.md` before inventing a new slug for the same project.
- All three subdirectories hold dated, journal-style files — one file per date, appended to
  through the day rather than one file per topic. This matches `wiki/journal/`'s
  `YYYY-MM-DD.md` convention (see `wiki/journal/README.md`), scoped to a single project.
- `plans/`: forward-looking build/implementation plans for this project. Use `type: plan`
  frontmatter with the same closed `status` enum (`planned`/`in-progress`/`done`) documented
  in `WIKI_SCHEMA.md`, plus `project: {project-slug}`.
- `session-logs/`: what actually happened, dated — agent-authored work summaries live here now,
  not in `wiki/journal/` (kept out specifically so Adam's personal journal doesn't fill up with
  agent content). When a day's work touches multiple projects, file each project's bullets
  under that project's own `session-logs/YYYY-MM-DD.md` rather than one mixed file — keeps
  retrieval-by-project clean at the cost of the single-narrative-day view. Genuinely
  project-less agent work (rare) has no default home here — ask rather than defaulting it into
  `wiki/journal/`.
- `takeaways/`: durable knowledge worth pulling out of the day-to-day session-log narrative —
  learnings, trade-offs made (and why), discoveries along the way, and anything meant to
  inform future decisions on this project rather than just record what happened. Distinct
  from `wiki/patterns/`, which only holds a technique after it has proven reusable *across*
  projects; a takeaway can and often should stay project-local forever.

## Frontmatter

Light, matching the journal convention:

```yaml
---
title: 2026-08-28 Risk Fast Check Session Log
type: journal
project: risk-fast-check-static-quiz
created: 2026-08-28
updated: 2026-08-28
tags:
  - journal
  - session-log
---
```

Plans use `type: plan` instead of `type: journal`, per `WIKI_SCHEMA.md`. Takeaways use
`type: takeaway` — no closed `status` enum, since a takeaway isn't a workflow item with a
planned/in-progress/done lifecycle, just a dated record of what was learned.

## Known Gap

`scripts/wiki_tool.py`'s catalog builder (`CATALOG_DIRS`) does not yet walk
`wiki/projects/**` — it only scans flat top-level folders. Until that's extended, files here
won't appear in `wiki/catalog.jsonl`, `wiki/index.md`, or link-check/promotion tooling. The
`SessionStart` hook (`dotclaude/hooks/session-start-brief.py`) was updated separately to scan
`wiki/projects/*/plans/*.md` directly so unexecuted plans keep surfacing regardless. Extending
the catalog builder itself is a follow-up, tracked in `wiki/todo.md`.
