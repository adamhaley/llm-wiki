#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REMOTE="${1:-origin}"
BRANCH="${2:-main}"
LOG_FILE="${LOG_FILE:-/tmp/llm-wiki-sync.log}"
LOCK_DIR="${LOCK_DIR:-/tmp/llm-wiki-sync.lock}"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  printf "[%s] %s\n" "$(timestamp)" "$1" >>"$LOG_FILE"
}

cleanup() {
  rmdir "$LOCK_DIR" >/dev/null 2>&1 || true
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "skip: another sync process is already running"
  exit 0
fi

trap cleanup EXIT

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "error: $REPO_DIR is not a git repository"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
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
