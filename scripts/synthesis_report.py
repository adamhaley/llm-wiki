#!/usr/bin/env python3
"""Generate a deterministic synthesis-prep report from new journal entries and inbox clips."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from wiki_tool import (
    ROOT,
    WIKI_DIR,
    clean_words,
    load_catalog_notes,
    load_note,
    note_body,
    orphan_candidates,
)

STATE_PATH = ROOT / "scripts" / "state.json"
REPORTS_DIR = WIKI_DIR / "pages" / "reports"
JOURNAL_DIR = WIKI_DIR / "journal"
INBOX_CLIPS_DIR = WIKI_DIR / "inbox-clips"
SKIP_FILENAMES = {"README.md", "index.md"}
ANALYSIS_STOPWORDS = {
    "http",
    "https",
    "www",
    "com",
    "watch",
    "youtube",
    "transcript",
    "okay",
    "yeah",
    "gonna",
    "wanna",
    "just",
    "that",
    "this",
    "have",
    "it's",
    "im",
    "i'm",
    "lets",
    "let",
}


@dataclass
class ChangedItem:
    rel_path: str
    title: str
    note_type: str
    summary: str
    path: Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"synthesis_report": {"items": {}, "last_report": ""}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_markdown(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    paths = []
    for path in sorted(folder.rglob("*.md")):
        if path.name in SKIP_FILENAMES:
            continue
        if "quarantine" in path.parts:
            continue
        paths.append(path)
    return paths


def load_changed_items(state: dict[str, Any]) -> tuple[list[ChangedItem], dict[str, str]]:
    previous = state.get("synthesis_report", {}).get("items", {})
    current_hashes: dict[str, str] = {}
    changed: list[ChangedItem] = []

    for path in iter_markdown(JOURNAL_DIR):
        note = load_note(path, "journal")
        rel_path = path.relative_to(ROOT).as_posix()
        digest = sha256_text(path.read_text(encoding="utf-8"))
        current_hashes[rel_path] = digest
        if previous.get(rel_path) != digest:
            changed.append(
                ChangedItem(
                    rel_path=rel_path,
                    title=note.title,
                    note_type="journal",
                    summary=note.summary,
                    path=path,
                )
            )

    for path in iter_markdown(INBOX_CLIPS_DIR):
        note = load_note(path, "clip")
        rel_path = path.relative_to(ROOT).as_posix()
        digest = sha256_text(path.read_text(encoding="utf-8"))
        current_hashes[rel_path] = digest
        if previous.get(rel_path) != digest:
            changed.append(
                ChangedItem(
                    rel_path=rel_path,
                    title=note.title,
                    note_type="clip",
                    summary=note.summary,
                    path=path,
                )
            )

    changed.sort(key=lambda item: item.rel_path)
    return changed, current_hashes


def report_name_candidates(items: list[ChangedItem], min_count: int, limit: int) -> list[dict[str, Any]]:
    hits: dict[str, set[str]] = defaultdict(set)
    pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b")
    for item in items:
        text = sanitize_analysis_text(note_body(item.path))
        seen: set[str] = set()
        for match in pattern.findall(text):
            candidate = match.strip()
            lowered = candidate.lower()
            if lowered in ANALYSIS_STOPWORDS:
                continue
            if candidate in {"Los Angeles", "Today", "Good Morning"}:
                continue
            if candidate in seen:
                continue
            seen.add(candidate)
            hits[candidate].add(item.rel_path)
    rows = []
    for label, paths in hits.items():
        if len(paths) < min_count:
            continue
        rows.append({"label": label, "count": len(paths), "note_paths": sorted(paths)})
    rows.sort(key=lambda row: (-row["count"], row["label"]))
    return rows[:limit]


def report_phrase_candidates(items: list[ChangedItem], min_count: int, limit: int) -> list[dict[str, Any]]:
    hits: dict[str, set[str]] = defaultdict(set)
    for item in items:
        words = [word.lower() for word in clean_words(sanitize_analysis_text(note_body(item.path)))]
        seen: set[str] = set()
        for length in range(2, 4):
            if len(words) < length:
                continue
            for index in range(len(words) - length + 1):
                phrase_words = words[index:index + length]
                if any(word in ANALYSIS_STOPWORDS for word in phrase_words):
                    continue
                phrase = " ".join(phrase_words)
                if phrase in seen:
                    continue
                seen.add(phrase)
                hits[phrase].add(item.rel_path)
    rows = []
    for label, paths in hits.items():
        if len(paths) < min_count:
            continue
        rows.append({"label": label, "count": len(paths), "note_paths": sorted(paths)})
    rows.sort(key=lambda row: (-row["count"], row["label"]))
    return rows[:limit]


def top_keywords(text: str, limit: int = 8) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for word in clean_words(sanitize_analysis_text(text)):
        token = word.lower()
        if len(token) < 4:
            continue
        if token in ANALYSIS_STOPWORDS:
            continue
        counts[token] += 1
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return [word for word, _ in ranked[:limit]]


def sanitize_analysis_text(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    return text


def connection_candidates(items: list[ChangedItem], limit: int = 8) -> list[dict[str, Any]]:
    keywords = {item.rel_path: set(top_keywords(note_body(item.path), 10)) for item in items}
    candidates: list[dict[str, Any]] = []
    for left_index in range(len(items)):
        for right_index in range(left_index + 1, len(items)):
            left = items[left_index]
            right = items[right_index]
            overlap = sorted(keywords[left.rel_path] & keywords[right.rel_path])
            if len(overlap) < 2:
                continue
            candidates.append(
                {
                    "left": left,
                    "right": right,
                    "overlap": overlap,
                }
            )
    candidates.sort(key=lambda row: (-len(row["overlap"]), row["left"].title, row["right"].title))
    return candidates[:limit]


def catalog_note_map() -> dict[str, str]:
    result = {}
    for note in load_catalog_notes():
        result[note.rel_path] = note.title
    return result


def report_path(now: datetime) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR / f"synthesis-report-{now.strftime('%Y-%m-%d-%H%M')}.md"


def render_report(
    changed: list[ChangedItem],
    name_candidates: list[Any],
    phrase_candidates: list[Any],
    connections: list[dict[str, Any]],
    orphans: list[dict[str, str]],
    now: datetime,
) -> str:
    journal_items = [item for item in changed if item.note_type == "journal"]
    clip_items = [item for item in changed if item.note_type == "clip"]

    lines = [
        f"# Synthesis Report {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "Deterministic review brief for new or changed journal entries and inbox clips.",
        "",
        "## Summary",
        "",
        f"- Changed journal entries: {len(journal_items)}",
        f"- Changed inbox clips: {len(clip_items)}",
        f"- Repeated names surfaced: {len(name_candidates)}",
        f"- Repeated phrases surfaced: {len(phrase_candidates)}",
        f"- Potential cross-note connections: {len(connections)}",
        f"- Current orphan durable notes: {len(orphans)}",
        "",
        "## New Or Changed Journal Entries",
        "",
    ]

    if not journal_items:
        lines.append("- None")
    else:
        for item in journal_items:
            summary = item.summary or "No summary extracted."
            lines.append(f"- [{item.title}]({Path(item.rel_path).relative_to('wiki').as_posix()}): {summary}")
    lines.append("")
    lines.append("## New Or Changed Inbox Clips")
    lines.append("")
    if not clip_items:
        lines.append("- None")
    else:
        for item in clip_items:
            summary = item.summary or "No summary extracted."
            lines.append(f"- [{item.title}]({Path(item.rel_path).relative_to('wiki').as_posix()}): {summary}")

    lines.extend(["", "## Candidate Names", ""])
    if not name_candidates:
        lines.append("- None")
    else:
        for candidate in name_candidates:
            note_refs = ", ".join(Path(path).name for path in candidate["note_paths"][:4])
            lines.append(f"- `{candidate['label']}` appears in {candidate['count']} notes: {note_refs}")

    lines.extend(["", "## Candidate Phrases", ""])
    if not phrase_candidates:
        lines.append("- None")
    else:
        for candidate in phrase_candidates:
            note_refs = ", ".join(Path(path).name for path in candidate["note_paths"][:4])
            lines.append(f"- `{candidate['label']}` appears in {candidate['count']} notes: {note_refs}")

    lines.extend(["", "## Potential Connections", ""])
    if not connections:
        lines.append("- None")
    else:
        for row in connections:
            left = row["left"]
            right = row["right"]
            overlap = ", ".join(row["overlap"][:6])
            lines.append(f"- {left.title} <-> {right.title}: shared keywords `{overlap}`")

    lines.extend(["", "## Orphan Durable Notes", ""])
    if not orphans:
        lines.append("- None")
    else:
        for row in orphans:
            path = Path(row["path"]).relative_to("wiki").as_posix()
            lines.append(f"- [{row['title']}]({path}) (`{row['type']}`)")

    lines.extend(
        [
            "",
            "## Suggested Next Actions",
            "",
            "- Review the changed journal entries and clips first.",
            "- Choose only durable concepts, people, or cross-note insights worth promoting.",
            "- Create or update canonical hub notes in `wiki/topics/`.",
            "- Create supporting durable notes in `wiki/pages/` when a note belongs under a hub rather than as a peer topic.",
            "- File higher-order conclusions into `wiki/syntheses/` when a genuine synthesis emerges.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a synthesis-prep report")
    parser.add_argument("--dry-run", action="store_true", help="Print report instead of writing it")
    parser.add_argument("--no-state-update", action="store_true", help="Do not update scripts/state.json")
    parser.add_argument("--limit", type=int, default=10, help="Max candidates per section")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    now = datetime.now()
    state = read_state()
    changed, current_hashes = load_changed_items(state)

    name_candidates = report_name_candidates(changed, min_count=2, limit=args.limit)
    phrase_candidates = report_phrase_candidates(changed, min_count=2, limit=args.limit)
    connections = connection_candidates(changed, limit=args.limit)
    orphans = orphan_candidates()

    content = render_report(changed, name_candidates, phrase_candidates, connections, orphans, now)

    if args.dry_run:
        print(content)
        return 0

    target = report_path(now)
    target.write_text(content, encoding="utf-8")
    print(f"report_written={target.relative_to(ROOT).as_posix()}")

    if not args.no_state_update:
        state.setdefault("synthesis_report", {})
        state["synthesis_report"]["items"] = current_hashes
        state["synthesis_report"]["last_report"] = target.relative_to(ROOT).as_posix()
        state["synthesis_report"]["updated"] = now.isoformat()
        write_state(state)
        print(f"state_updated={STATE_PATH.relative_to(ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
