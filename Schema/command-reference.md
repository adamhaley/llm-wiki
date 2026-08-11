# Command Reference

## Core Commands

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/wiki_tool.py source-delta
python3 scripts/wiki_tool.py source-coverage
python3 scripts/wiki_tool.py search-catalog --query "llm wiki"
python3 scripts/wiki_tool.py promotion-candidates --mode names --note-types journal
python3 scripts/wiki_tool.py promotion-candidates --mode phrases --note-types journal --min-count 2
python3 scripts/wiki_tool.py orphan-notes
python3 scripts/wiki_tool.py cross-link-candidates
python3 scripts/wiki_tool.py dead-links
python3 scripts/wiki_tool.py root-inbox
python3 scripts/synthesis_report.py
python3 scripts/synthesis_report.py --dry-run
scripts/run_synthesis_report.sh
scripts/run_autonomous_promotion.sh
scripts/run_weekly_grooming.sh
python3 scripts/wiki_tool.py log --title "title" --details "details"
python3 scripts/audit_public.py
```

## Expectations

- Run `build` before `search-catalog`.
- Run `lint`, `source-lint`, and `audit_public.py` before meaningful commits.
- Run `source-scan --update --accept-covered` after ingesting or triaging `wiki/inbox/` items.
- Use `doctor` as a quick non-mutating environment check.
- Use `promotion-candidates` and `orphan-notes` to surface likely promotion and cross-linking work, but keep semantic promotion decisions agent-driven.
- Use `cross-link-candidates` to surface plain-text mentions of other notes that aren't linked yet (vault-wide equivalent of Obsidian's "Unlinked mentions" panel). Candidates only — judge each one before linking.
- Use `dead-links` to find existing links that don't resolve to a real file — `lint` doesn't check this. Each result includes filename suggestions.
- Use `root-inbox` to list hand-dropped files sitting at the `wiki/` root awaiting triage — distinct from `wiki/inbox/`, which is the intentional capture zone.
- Use `synthesis_report.py` to generate a review brief from new or changed journal entries and `wiki/inbox/` items.
- Use `run_synthesis_report.sh` for cron-friendly report generation.
- Use `run_autonomous_promotion.sh` for headless agent promotion when `AUTOPROMOTE_COMMAND` is configured.
- Use `run_weekly_grooming.sh` on a VPS cron for the full weekly pass (lint fixes, orphan fixes, root-inbox triage, `wiki/inbox/` promotion, `overview.md` freshness) when `GROOMING_AGENT_COMMAND` is configured.
