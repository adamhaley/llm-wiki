#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="${LOG_FILE:-/tmp/llm-wiki-weekly-grooming.log}"
LOCK_DIR="${LOCK_DIR:-/tmp/llm-wiki-weekly-grooming.lock}"
PID_FILE="$LOCK_DIR/pid"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  printf "[%s] %s\n" "$(timestamp)" "$1" >>"$LOG_FILE"
}

cleanup() {
  rm -f "$PID_FILE" >/dev/null 2>&1 || true
  rmdir "$LOCK_DIR" >/dev/null 2>&1 || true
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  if [[ -f "$PID_FILE" ]]; then
    STALE_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [[ -n "$STALE_PID" ]] && kill -0 "$STALE_PID" 2>/dev/null; then
      log "skip: weekly grooming already running"
      exit 0
    fi
  fi
  rm -f "$PID_FILE" >/dev/null 2>&1 || true
  if rmdir "$LOCK_DIR" 2>/dev/null && mkdir "$LOCK_DIR" 2>/dev/null; then
    log "info: cleared stale grooming lock"
  else
    log "skip: unable to clear stale grooming lock"
    exit 0
  fi
fi

printf "%s\n" "$$" >"$PID_FILE"
trap cleanup EXIT

cd "$REPO_DIR"

if [[ -z "${GROOMING_AGENT_COMMAND:-}" ]]; then
  log "skip: GROOMING_AGENT_COMMAND is not set"
  exit 0
fi

PROMPT_FILE="$(mktemp "${TMPDIR:-/tmp}/llm-wiki-weekly-grooming.XXXXXX.md")"
trap 'rm -f "$PROMPT_FILE"; cleanup' EXIT

cat >"$PROMPT_FILE" <<'PROMPT'
Working directory: this repo (the llm-wiki vault).

Read and follow AGENTS.md, WIKI_SCHEMA.md, Schema/promotion-workflow.md, and the SKILL.md files under .agents/skills/.

Run the weekly grooming pass:

1. Deterministic baseline: python3 scripts/wiki_tool.py doctor, build, lint, source-lint, and python3 scripts/audit_public.py. Fix any lint failures you can fix mechanically (e.g. missing/mismatched source_count, missing required frontmatter fields).
2. python3 scripts/wiki_tool.py orphan-notes — add at least one inbound link (from a real content page, not an auto-generated index.md/README.md, which don't count) for any orphan found.
3. python3 scripts/wiki_tool.py cross-link-candidates — for each candidate, judge whether it's a genuine reference (per Schema/cross-linking-workflow.md's guidance) or a coincidental word match. Convert genuine matches to real links in place. Skip coincidental matches; don't force a link where the mention isn't actually about that entity. This is the main lever for turning journal prose into real cross-links, so give it real attention, not a rubber stamp.
4. python3 scripts/wiki_tool.py root-inbox — triage any loose files at the wiki/ root: promote, move into wiki/inbox/, or delete if debris (empty files can be deleted without asking).
5. Triage wiki/inbox/: read items older than ~2 weeks. For each, per WIKI_SCHEMA.md's Autonomous Promotion Workflow, promote high-confidence durable material into wiki/topics/, wiki/pages/ (type: page, entity, source, or synthesis as appropriate), or wiki/crm/ without asking first. Prefer updating existing canonical pages over creating duplicates, and prefer processing related items in one themed pass over handling each in isolation. Ask for input only before destructive deletes/merges, sensitive CRM claims, major taxonomy changes, or resolving substantive contradictions. Once an item is fully promoted: delete it, or mark it status: archived if a source page's raw_source still needs it for provenance. Link newly promoted pages to related existing pages as you create them, not just via a later cross-link-candidates pass.
6. Check wiki/overview.md's Current State section against reality (entity/synthesis/topic counts, inbox backlog size) and update it if it's gone stale.
7. Re-run the deterministic baseline to confirm everything is still clean.
8. Append one entry to wiki/log.md summarizing what changed: items promoted, items deleted, orphans fixed, cross-links added, lint issues fixed, and anything left pending that needs human judgment.

Keep diffs minimal, factual, and heavily cross-linked. Do not touch the n8n/Telegram journal capture pipeline — it's a separate, working system.
PROMPT

log "running GROOMING_AGENT_COMMAND"
sh -c "$GROOMING_AGENT_COMMAND" <"$PROMPT_FILE" >>"$LOG_FILE" 2>&1
log "ok: weekly grooming command completed"
