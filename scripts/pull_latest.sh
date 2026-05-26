#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REMOTE="${1:-origin}"
BRANCH="${2:-main}"
LOG_FILE="${LOG_FILE:-/tmp/llm-wiki-sync.log}"
LOCK_DIR="${LOCK_DIR:-/tmp/llm-wiki-sync.lock}"
PID_FILE="$LOCK_DIR/pid"
EXCLUDED_PATHS=(':(exclude)wiki/.obsidian/**')

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

has_meaningful_changes() {
  if ! git diff --quiet -- . "${EXCLUDED_PATHS[@]}"; then
    return 0
  fi

  if ! git diff --cached --quiet -- . "${EXCLUDED_PATHS[@]}"; then
    return 0
  fi

  if [[ -n "$(git ls-files --others --exclude-standard -- . "${EXCLUDED_PATHS[@]}")" ]]; then
    return 0
  fi

  return 1
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  if [[ -f "$PID_FILE" ]]; then
    STALE_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [[ -n "$STALE_PID" ]] && kill -0 "$STALE_PID" 2>/dev/null; then
      log "skip: another sync process is already running"
      exit 0
    fi
  fi
  rm -f "$PID_FILE" >/dev/null 2>&1 || true
  if rmdir "$LOCK_DIR" 2>/dev/null && mkdir "$LOCK_DIR" 2>/dev/null; then
    log "info: cleared stale sync lock"
  else
    log "skip: unable to clear stale sync lock"
    exit 0
  fi
fi

printf "%s\n" "$$" >"$PID_FILE"

trap cleanup EXIT

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "error: $REPO_DIR is not a git repository"
  exit 1
fi

if has_meaningful_changes; then
  log "skip: worktree is dirty; not pulling"
  exit 0
fi

git fetch "$REMOTE" "$BRANCH" >>"$LOG_FILE" 2>&1

LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_SHA="$(git rev-parse "$REMOTE/$BRANCH")"
BASE_SHA="$(git merge-base HEAD "$REMOTE/$BRANCH")"

if [[ "$LOCAL_SHA" == "$REMOTE_SHA" ]]; then
  log "ok: already up to date"
  exit 0
fi

if [[ "$LOCAL_SHA" == "$BASE_SHA" ]]; then
  git pull --ff-only "$REMOTE" "$BRANCH" >>"$LOG_FILE" 2>&1
  log "ok: fast-forwarded to $REMOTE/$BRANCH"
  exit 0
fi

if [[ "$REMOTE_SHA" == "$BASE_SHA" ]]; then
  log "skip: local branch is ahead of $REMOTE/$BRANCH"
  exit 0
fi

log "skip: local branch has diverged from $REMOTE/$BRANCH"
exit 0
