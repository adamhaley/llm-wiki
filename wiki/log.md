# Vault Log

Append-only chronological log of vault operations.

## [2026-05-23] init | repository scaffold

Created the initial LLM wiki structure with shared schema, cross-agent instructions, root index and log, raw source directories, wiki directories, journal and CRM directories, starter templates, and overview files.

## [2026-05-23] refactor | obsidian-friendly layout

Adjusted the scaffold to better match the Obsidian-friendly pattern described by MindStudio: root `index.md` and `log.md`, `raw/processed/`, plus first-class `journal/` and `crm/` directories.

## [2026-05-23] policy | direct journal capture

Updated the schema and agent instructions to allow normalized Telegram voice-note captures to write directly into `journal/`, while reserving `raw/` for external source material.

## [2026-05-23] refactor | wiki as vault

Moved the Obsidian vault boundary to `wiki/`, relocated `index.md`, `log.md`, `journal/`, `crm/`, and `.obsidian/` under `wiki/`, and updated the repo docs so the repository root remains agent-facing infrastructure.

## [2026-05-24] policy | raw ignored and inbox clips

Updated the repository so `raw/` is git-ignored except for tracked skeleton files, and added `wiki/inbox-clips/` as the Obsidian-visible landing zone for Web Clipper captures.

## [2026-05-24] tool | deterministic tooling baseline

Added deterministic wiki maintenance tooling, schema docs, generated indexes, and repo-local agent skills while keeping raw/ outside the Obsidian vault.

## [2026-05-24] tool | journal import cleanup

Normalized legacy journal filenames to zero-padded dates, quarantined non-journal test files, removed obvious placeholder text, and added journal capture conventions and a template.

## [2026-05-24] tool | promotion workflow baseline

Added agent-driven promotion workflow docs, a promotion skill, and deterministic helper commands for repeated names, repeated phrases, and orphan-note discovery without automating semantic page creation.

## [2026-05-24] tool | second brain topic

Added a canonical topic page for the practical second-brain workflow, including capture, promotion, review rhythm, and web clipper handling guidance.

## [2026-05-24] tool | second brain boundary

Expanded the Second Brain topic with the practical boundary between the deterministic tool layer and the meaning-oriented vault layer, including what is appropriate to automate versus keep human or agent in the loop.

## [2026-05-24] tool | second brain sync behavior

Expanded the Second Brain topic to clarify that scheduled pull automation is most useful during idle clean periods and should safely skip during active local editing or when the branch is ahead.

## [2026-05-24] tool | second brain note cluster

Split the large Second Brain topic into a hub note plus smaller glanceable notes for workflow, operating boundary, review rhythm, and sync behavior.

## [2026-05-24] tool | pages note class

Added wiki/pages as a general durable note area, clarified topics as canonical hubs, and moved Second Brain supporting notes from topics into pages.

## [2026-05-24] tool | pages typing fix

Corrected the Second Brain supporting notes under wiki/pages to use type page so canonical topics and supporting pages stay distinct in the catalog and indexes.

## [2026-05-25] tool | synthesis prep workflow

Added a stateful synthesis-prep report script, documented the report-driven review workflow, and ignored generated report/state artifacts so scheduled runs can stay deterministic without dirtying the repo.

## [2026-05-25] promotion | first durable clusters

Promoted the first synthesis-driven clusters into durable notes by adding canonical pages for LLM Wiki and Upwork plus a supporting page for Claude Code memory systems, and linked them back into the Second Brain hub.
