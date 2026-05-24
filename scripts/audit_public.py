#!/usr/bin/env python3
"""Basic public-safety audit for the repository."""

from __future__ import annotations

import re
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
    files = []
    for path in ROOT.rglob("*"):
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
