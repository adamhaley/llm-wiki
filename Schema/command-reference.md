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
python3 scripts/synthesis_report.py
python3 scripts/synthesis_report.py --dry-run
scripts/run_synthesis_report.sh
scripts/run_autonomous_promotion.sh
python3 scripts/wiki_tool.py log --title "title" --details "details"
python3 scripts/audit_public.py
```

## Expectations

- Run `build` before `search-catalog`.
- Run `lint`, `source-lint`, and `audit_public.py` before meaningful commits.
- Run `source-scan --update --accept-covered` after ingesting or moving raw sources.
- Use `doctor` as a quick non-mutating environment check.
- Use `promotion-candidates` and `orphan-notes` to surface likely promotion and cross-linking work, but keep semantic promotion decisions agent-driven.
- Use `synthesis_report.py` to generate a review brief from new or changed journal entries and inbox clips.
- Use `run_synthesis_report.sh` for cron-friendly report generation.
- Use `run_autonomous_promotion.sh` for headless agent promotion when `AUTOPROMOTE_COMMAND` is configured.
