#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="${LOG_FILE:-/tmp/llm-wiki-synthesis-report.log}"
LOCK_DIR="${LOCK_DIR:-/tmp/llm-wiki-synthesis-report.lock}"
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
      log "skip: synthesis report already running"
      exit 0
    fi
  fi
  rm -f "$PID_FILE" >/dev/null 2>&1 || true
  if rmdir "$LOCK_DIR" 2>/dev/null && mkdir "$LOCK_DIR" 2>/dev/null; then
    log "info: cleared stale synthesis lock"
  else
    log "skip: unable to clear stale synthesis lock"
    exit 0
  fi
fi

printf "%s\n" "$$" >"$PID_FILE"
trap cleanup EXIT

cd "$REPO_DIR"

OUTPUT="$(python3 scripts/synthesis_report.py --skip-empty 2>&1)"
log "$OUTPUT"
