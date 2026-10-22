# Content

The content pipeline: the three stages a piece of Adam's own published output moves through,
each a sibling directory, joined by a shared **slug** rather than by nesting.

```
wiki/content/
  ideas/
    pricing-by-outcome.md
  drafts/
    pricing-by-outcome.md
  output/
    pricing-by-outcome--newsletter.md
    pricing-by-outcome--x-thread.md
```

Kept separate from `wiki/pages/` (compiled knowledge *in*) because this is Adam's own
production *out* — material whose value is that it eventually ships, not that it's retrievable.
A page is done when it's accurate; a content item is done when it's published.

## The Slug Is the Join Key

One slug per content item, kebab-case, **stable forever**. The same slug names the file at every
stage, so `ideas/X.md`, `drafts/X.md`, and `output/X--*.md` are the same item by convention — no
index, no backlink bookkeeping required to walk a piece from idea to publication.

Rules that keep the join reliable:

- **No dates in filenames.** A `2026-10-21-` prefix breaks the join the moment a draft slips a
  week. Dates live in `created`/`updated`/`published` frontmatter.
- **No version suffixes.** `--v2` is git's job, not the filename's. A draft is edited in place.
- **Never rename a slug** once a later stage exists. If the framing genuinely changes, that's a
  new idea with a new slug; link the two in the body.
- **Keep `slug:` in frontmatter too**, matching the filename. The redundancy is deliberate — a
  rename or typo shows up as a mismatch `content status` can catch, instead of silently
  orphaning a draft.

### Fan-out: one idea, many outputs

Outputs use `{slug}--{channel}.md`. Everything before the first `--` is the slug; everything
after is the channel (`newsletter`, `x-thread`, `blog`, `video`, `talk`). A single-output item
can just be `output/{slug}.md` with no suffix.

Ideas and drafts stay strictly one file per slug. If an idea needs two genuinely different
drafts, it's two ideas.

## Files Don't Move

Promoting to the next stage **creates** the next file; it does not move or delete the previous
one. An idea that got drafted keeps its idea note — the bank of ideas is worth mining later,
including the ones that stalled, and the stage files answer different questions (what was the
spark, what's the argument, what shipped).

The corollary: the idea file is **not** maintained to mirror the draft. Once a draft exists, the
idea note is a historical record of the spark. Don't sync them.

## Frontmatter

```yaml
---
title: Pricing by Outcome
type: idea            # idea | draft | output
slug: pricing-by-outcome
status: raw
created: 2026-10-21
updated: 2026-10-21
tags:
  - content
---
```

Outputs add `channel:` (matching the filename suffix) and, once live, `published:` and `url:`.
Any stage may carry `project:` when the content is about a tracked project.

`status` is a **closed set per type**, because `wiki_tool.py content status` reads it:

| type     | statuses                                        |
|----------|-------------------------------------------------|
| `idea`   | `raw`, `developing`, `drafted`, `shelved`       |
| `draft`  | `in-progress`, `ready`, `shelved`               |
| `output` | `scheduled`, `published`, `shelved`             |

`shelved` is the honest end state for anything abandoned — use it rather than deleting, so the
idea bank keeps its misses. Don't invent new values; extend the set in `wiki_tool.py` and here
together if one is genuinely missing.

Status describes **vault pipeline stage only** — never whether something reached an external
site. For ideas: `raw` is banked (may sit indefinitely), `developing` is actively being worked,
`drafted` means a `drafts/{slug}.md` file exists (set by `content promote`, nothing else). Sync
state with adamhaley.com lives in its own fields (`source_external_id`, an output's `url`).

## Who Owns Each Stage

For adamhaley.com blog content, the vault owns writing and Laravel owns publishing:

- **`ideas/`** — the single idea bank, vault-only. Ideas are not sent to adamhaley.com. (Until
  2026-10-21 `scripts/import_content_ideas.py` pushed ideas as `Post` rows and set them to
  `drafted`; it was retired once adamhaley.com stopped being a dependency of the pipeline. The 36
  ideas it pushed keep their `source_external_id` so a later push can match those rows.)
- **`drafts/`** — the draft text itself, written (or dictated) in Obsidian. Deliberately not a
  Filament form field: prose is easier to write in the editor than in a web textarea.
- **`output/`** — the publication record once live: `channel`, `published`, `url`. For blog
  posts the canonical published copy is the `Post` row, so the output note points at it rather
  than holding a second copy of the text.

Two identifiers coexist on the 36 previously-pushed ideas, on purpose (new ideas have only
`slug`):

| field                | what it is                                                                 |
|----------------------|----------------------------------------------------------------------------|
| `slug`               | the vault's join key — short, readable, matches the filename                |
| `source_external_id` | adamhaley.com's dedupe key for the `Post` row (`source` + this, unique)     |

They are *not* the same string. The external id is slugify-of-the-60-char-truncated-title, the
shape the first 36 ideas were imported under on 2026-09-06; the slug is a short readable name.
Never recompute an external id for an idea that already has one — that would create a duplicate
`Post` instead of matching the existing one.

**The last hop is manual for now (2026-10-21)**: nothing pushes finished `drafts/` text into the
matching `Post` row's `body` — you paste it. A push script is on the rolling todo, deliberately
not built yet: this whole three-stage shape is still an experiment in what fits Adam's writing
habit, and automating the hop before the workflow around it settles would lock in a guess. When
it is built, it should upsert on the idea's `source_external_id` where one exists, so the 36
existing `Post` rows get filled in rather than duplicated.

## Creating Files

Use the commands — they are the canonical path, because this vault is mostly written by agents
rather than by hand in Obsidian:

```bash
python3 scripts/wiki_tool.py content new --slug pricing-by-outcome \
    --title "Pricing by Outcome" --spark "What prompted this." [--project adamhaley-com]
python3 scripts/wiki_tool.py content promote --slug pricing-by-outcome --to draft
python3 scripts/wiki_tool.py content promote --slug pricing-by-outcome --to output --channel newsletter
```

`promote` inherits the previous stage's `title` and `project`, writes the back-link, and advances
the previous stage's status (idea → `drafted`, draft → `ready`) without ever walking a status
backwards — a `shelved` idea stays shelved. It refuses to create a stage whose previous stage
doesn't exist, which is what keeps the chain honest, and refuses to overwrite an existing file.

`content_note_text()` in `scripts/wiki_tool.py` is the single definition of a content note's
shape. The `wiki/templates/content-*-template.md` files mirror it for the Obsidian-side human
path; `content status` validates whichever route produced a file, so the two can't drift
silently. If you change one, change both.

## Checking the Convention

A naming convention nobody checks silently rots. Run:

```bash
python3 scripts/wiki_tool.py content status
```

It prints every slug with the stages that exist for it, and flags:

- drafts or outputs whose slug has no idea (broken join)
- `slug:` frontmatter that doesn't match the filename
- unknown `status` values for the note's type
- ideas at `status: drafted` with no draft file
- ideas sitting in `developing` past `--stale-days` (default 30) with no draft — `raw` ideas
  are the bank and are never nagged

## Core Value: Earn Your Keep

Same principle as [Patterns](/wiki/patterns/README.md) and
[Projects](/wiki/projects/README.md) — see [Use-Led Simplicity](/WIKI_SCHEMA.md). Ideas are
meant to be cheap and numerous, so `ideas/` can hold plenty that never progress. The caution
applies to the *structure*: don't add a fourth stage, per-channel subdirectories, or an
editorial-calendar layer until the three-stage shape has actually been in daily use and visibly
fallen short.
