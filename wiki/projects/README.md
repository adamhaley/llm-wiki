# Projects

Per-project grouping for the three kinds of content that pile up around an actively-worked
project: plans, session logs, and takeaways. Kept separate from the flat `wiki/pages/` and
`wiki/journal/` layers because once a project has enough of this content, reading it back by
project (not by date or by note type) is the more useful retrieval shape.

## Core Value: Earn Your Keep

Same principle as [Patterns](/wiki/patterns/README.md) — see
[Use-Led Simplicity](/WIKI_SCHEMA.md). Don't create a `wiki/projects/{project}/` folder just
because a project exists. Create it once a project has accumulated (or is clearly about to
accumulate) more than one or two plan/session-log entries — before that, a single
`wiki/pages/` page or a normal `wiki/journal/` entry is simpler and correct. A project folder
that never grows past its first dated file was created too early; fold it back rather than
leaving three mostly-empty subdirectories around.

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
- `session-logs/`: what actually happened, dated — the project-scoped equivalent of a
  `wiki/journal/` session-log entry. When a day's work touches multiple projects, file each
  project's bullets under that project's own `session-logs/YYYY-MM-DD.md` rather than one
  mixed file — keeps retrieval-by-project clean at the cost of the single-narrative-day view.
  General, non-project-specific reflection still belongs in `wiki/journal/`.
- `takeaways/`: lessons learned — what would have been done differently, patterns worth
  remembering, mistakes not to repeat on this project specifically. Distinct from
  `wiki/patterns/`, which only holds a technique after it has proven reusable *across*
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

Plans use `type: plan` instead of `type: journal`, per `WIKI_SCHEMA.md`.

## Known Gap

`scripts/wiki_tool.py`'s catalog builder (`CATALOG_DIRS`) does not yet walk
`wiki/projects/**` — it only scans flat top-level folders. Until that's extended, files here
won't appear in `wiki/catalog.jsonl`, `wiki/index.md`, or link-check/promotion tooling. The
`SessionStart` hook (`dotclaude/hooks/session-start-brief.py`) was updated separately to scan
`wiki/projects/*/plans/*.md` directly so unexecuted plans keep surfacing regardless. Extending
the catalog builder itself is a follow-up, tracked in `wiki/todo.md`.
