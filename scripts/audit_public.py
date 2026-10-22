#!/usr/bin/env python3
"""Basic public-safety audit for the repository."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    ".git",
}
SKIP_FILES = {
    "workspace.json",
    "workspace-mobile.json",
    ".DS_Store",
}
FORBIDDEN_PATH_SNIPPETS = [
    ".obsidian/plugins/",
    ".obsidian/cache/",
]
FORBIDDEN_PATTERNS = [
    r"BEGIN [A-Z ]*PRIVATE KEY",
    r"/Users/[A-Za-z0-9._-]+/",
    r"sk-[A-Za-z0-9]{12,}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
]


def iter_files() -> list[Path]:
    """Git-tracked files only - "public" here means whatever git would publish.

    Deliberately not a filesystem walk. Most of wiki/ is gitignored by design
    (see .gitignore), so walking the disk audited notes that can never leave
    this machine, and flagged on-disk Obsidian plugin files that .gitignore
    already excludes - noise that made this check fail permanently. Secrets in
    untracked local notes are a real concern, but a different one.
    """
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True,
        text=True,
        check=True,
    )
    files = []
    for entry in result.stdout.split("\0"):
        if not entry:
            continue
        path = ROOT / entry
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        rel_path = path.relative_to(ROOT).as_posix()
        for snippet in FORBIDDEN_PATH_SNIPPETS:
            if snippet in rel_path:
                failures.append(f"forbidden tracked path: {rel_path}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, text):
                failures.append(f"forbidden content pattern `{pattern}` in {rel_path}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("audit_public=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
