#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="${LOG_FILE:-/tmp/llm-wiki-autonomous-promotion.log}"
LOCK_DIR="${LOCK_DIR:-/tmp/llm-wiki-autonomous-promotion.lock}"
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
      log "skip: autonomous promotion already running"
      exit 0
    fi
  fi
  rm -f "$PID_FILE" >/dev/null 2>&1 || true
  if rmdir "$LOCK_DIR" 2>/dev/null && mkdir "$LOCK_DIR" 2>/dev/null; then
    log "info: cleared stale autonomous promotion lock"
  else
    log "skip: unable to clear stale autonomous promotion lock"
    exit 0
  fi
fi

printf "%s\n" "$$" >"$PID_FILE"
trap cleanup EXIT

cd "$REPO_DIR"

REPORT_OUTPUT="$(python3 scripts/synthesis_report.py --skip-empty 2>&1)"
log "$REPORT_OUTPUT"

if grep -q "report_skipped=no_changed_items" <<<"$REPORT_OUTPUT"; then
  exit 0
fi

if [[ -z "${AUTOPROMOTE_COMMAND:-}" ]]; then
  log "skip: AUTOPROMOTE_COMMAND is not set"
  exit 0
fi

REPORT_PATH="$(grep -E "^report_written=" <<<"$REPORT_OUTPUT" | tail -n 1 | cut -d= -f2-)"
if [[ -z "$REPORT_PATH" ]]; then
  REPORT_PATH="$(ls -t wiki/pages/reports/synthesis-report-*.md 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "$REPORT_PATH" || ! -f "$REPORT_PATH" ]]; then
  log "error: unable to find synthesis report for promotion"
  exit 1
fi

PROMPT_FILE="$(mktemp "${TMPDIR:-/tmp}/llm-wiki-autopromote.XXXXXX.md")"
trap 'rm -f "$PROMPT_FILE"; cleanup' EXIT

cat >"$PROMPT_FILE" <<PROMPT
You are maintaining this local LLM wiki in autonomous promotion mode.

Read and follow AGENTS.md, WIKI_SCHEMA.md, Schema/promotion-workflow.md, and .agents/skills/llm-wiki-promote/SKILL.md.

Use this synthesis report as the starting point:

$REPORT_PATH

Autonomously promote high-confidence durable material into wiki/topics, wiki/pages, wiki/entities, wiki/crm, or wiki/syntheses. Promotion is based on durable future utility, not only recurrence. One-off but reference-grade, decision-relevant, project-relevant, rare, clarifying, or rediscovery-saving items may be promoted.

Prefer updating existing canonical pages over creating duplicates. Preserve provenance. Keep claims modest when grounded only in journal entries or clips. Add useful links, but avoid backlink spam.

Ask for human input only for sensitive CRM claims, destructive deletes/merges, major taxonomy changes, or unresolved contradictions. Otherwise proceed.

After changes, run:

python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/audit_public.py

Append to wiki/log.md if the promotion materially changed the vault.
PROMPT

log "running AUTOPROMOTE_COMMAND against $REPORT_PATH"
sh -c "$AUTOPROMOTE_COMMAND" <"$PROMPT_FILE" >>"$LOG_FILE" 2>&1
log "ok: autonomous promotion command completed"
