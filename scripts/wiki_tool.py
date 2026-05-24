#!/usr/bin/env python3
"""Deterministic maintenance tooling for the local LLM wiki."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"
RAW_PROCESSED_DIR = RAW_DIR / "processed"
RAW_ASSETS_DIR = RAW_DIR / "assets"
WIKI_DIR = ROOT / "wiki"
SCHEMA_DIR = ROOT / "Schema"
CATALOG_PATH = WIKI_DIR / "catalog.jsonl"
MANIFEST_PATH = SCHEMA_DIR / "source-manifest.jsonl"
LOG_PATH = WIKI_DIR / "log.md"

TODAY = date.today().isoformat()

CATALOG_DIRS = {
    "sources": "source",
    "topics": "topic",
    "entities": "entity",
    "syntheses": "synthesis",
    "crm": "crm",
    "journal": "journal",
}
SECTION_LABELS = {
    "sources": "Sources",
    "topics": "Topics",
    "entities": "Entities",
    "syntheses": "Syntheses",
    "crm": "CRM",
    "journal": "Journal",
    "inbox-clips": "Inbox Clips",
}
EMPTY_MESSAGES = {
    "sources": "No source pages yet.",
    "topics": "No topic pages yet.",
    "entities": "No entity pages yet.",
    "syntheses": "No synthesis pages yet.",
    "crm": "No CRM pages yet.",
    "journal": "No journal pages yet.",
}
STRICT_NOTE_TYPES = {"source", "topic", "entity", "synthesis", "crm"}
ALLOWED_TYPES = set(CATALOG_DIRS.values())
SKIP_FILENAMES = {"README.md", "index.md"}
STOPWORDS = {
    "a", "about", "after", "all", "also", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "but", "by", "can", "could", "day", "did",
    "do", "does", "doing", "down", "even", "every", "for", "from", "get", "got", "had",
    "has", "have", "he", "her", "here", "him", "his", "how", "i", "if", "in", "into", "is",
    "it", "its", "itself", "just", "like", "lot", "me", "more", "most", "my", "no", "not",
    "now", "of", "on", "one", "or", "other", "our", "out", "over", "really", "so", "some",
    "still", "than", "that", "the", "their", "them", "then", "there", "these", "they",
    "thing", "this", "those", "through", "to", "today", "up", "very", "was", "we", "well",
    "went", "were", "what", "when", "which", "while", "with", "would", "yesterday", "you",
    "your",
}
PROMOTION_NOTE_TYPES = {"journal", "topic", "entity", "synthesis", "crm", "source"}


class WikiError(Exception):
    """User-facing command failure."""


@dataclass
class Note:
    path: Path
    rel_path: str
    title: str
    note_type: str
    frontmatter: dict[str, Any]
    summary: str


@dataclass
class PromotionCandidate:
    label: str
    count: int
    note_paths: list[str]
    examples: list[str]


def parse_scalar(value: str) -> Any:
    text = value.strip()
    if not text:
        return ""
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    lowered = text.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",")]
    return text


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    lines = text.splitlines()
    frontmatter: dict[str, Any] = {}
    current_key: str | None = None
    in_frontmatter = True
    body_start = 0

    for index in range(1, len(lines)):
        line = lines[index]
        if line == "---":
            body_start = index + 1
            in_frontmatter = False
            break
        if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if value:
                frontmatter[key] = parse_scalar(value)
                current_key = None
            else:
                frontmatter[key] = []
                current_key = key
            continue
        if current_key and re.match(r"^\s*-\s+", line):
            item = re.sub(r"^\s*-\s+", "", line)
            current_value = frontmatter.get(current_key)
            if not isinstance(current_value, list):
                current_value = []
            current_value.append(parse_scalar(item))
            frontmatter[current_key] = current_value
            continue
        if current_key and line.strip():
            frontmatter[current_key] = parse_scalar(line.strip())
            current_key = None

    if in_frontmatter:
        return {}, text
    body = "\n".join(lines[body_start:]).strip()
    return frontmatter, body


def first_heading_or_stem(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def extract_summary(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped
    return ""


def clean_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", text)


def note_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)
    return body or text


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def wiki_relative(path: Path) -> str:
    return path.relative_to(WIKI_DIR).as_posix()


def load_note(path: Path, default_type: str) -> Note:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    title = str(frontmatter.get("title") or first_heading_or_stem(path, body or text))
    note_type = str(frontmatter.get("type") or default_type)
    summary = extract_summary(body)
    return Note(
        path=path,
        rel_path=repo_relative(path),
        title=title,
        note_type=note_type,
        frontmatter=frontmatter,
        summary=summary,
    )


def iter_note_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    files = []
    for path in sorted(folder.glob("*.md")):
        if path.name in SKIP_FILENAMES:
            continue
        files.append(path)
    return files


def load_catalog_notes() -> list[Note]:
    notes: list[Note] = []
    for folder_name, default_type in CATALOG_DIRS.items():
        folder = WIKI_DIR / folder_name
        for path in iter_note_files(folder):
            notes.append(load_note(path, default_type))
    return sorted(notes, key=lambda note: note.rel_path)


def promotion_notes(note_types: set[str] | None = None) -> list[Note]:
    notes = load_catalog_notes()
    if note_types is None:
        note_types = PROMOTION_NOTE_TYPES
    return [note for note in notes if note.note_type in note_types]


def list_source_files() -> list[Path]:
    files: list[Path] = []
    for base in (RAW_DIR, RAW_PROCESSED_DIR):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.name in {"README.md", ".gitkeep"}:
                continue
            if RAW_ASSETS_DIR in path.parents:
                continue
            files.append(path)
    unique = sorted({path.resolve(): path for path in files}.values(), key=lambda item: repo_relative(item))
    return unique


def raw_source_title(path: Path) -> str:
    if path.suffix.lower() != ".md":
        return path.stem.replace("-", " ").replace("_", " ").title()
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if frontmatter.get("title"):
        return str(frontmatter["title"])
    if frontmatter.get("Title"):
        return str(frontmatter["Title"])
    return first_heading_or_stem(path, body or text)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        rows.append(json.loads(stripped))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, sort_keys=True) for row in rows)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def normalize_sources(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def validate_source_path(source_path: str) -> bool:
    path = ROOT / source_path
    if not path.exists():
        return False
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        return False
    return relative.startswith("raw/")


def coverage_map(notes: list[Note]) -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = defaultdict(list)
    for note in notes:
        sources = normalize_sources(note.frontmatter.get("sources"))
        for source in sources:
            coverage[source].append(note.rel_path)
        if note.note_type == "source":
            raw_source = note.frontmatter.get("raw_source")
            if isinstance(raw_source, str) and raw_source.strip():
                coverage[raw_source.strip()].append(note.rel_path)
    return {key: sorted(set(value)) for key, value in coverage.items()}


def generate_catalog() -> list[dict[str, Any]]:
    rows = []
    for note in load_catalog_notes():
        row = {
            "path": note.rel_path,
            "title": note.title,
            "type": note.note_type,
            "status": note.frontmatter.get("status", ""),
            "tags": note.frontmatter.get("tags", []),
            "sources": normalize_sources(note.frontmatter.get("sources")),
            "source_count": int(note.frontmatter.get("source_count", 0) or 0),
            "updated": note.frontmatter.get("updated", ""),
            "summary": note.summary,
        }
        rows.append(row)
    return rows


def generate_manifest(accept_covered: bool) -> list[dict[str, Any]]:
    notes = load_catalog_notes()
    coverage = coverage_map(notes)
    existing = {row["path"]: row for row in load_jsonl(MANIFEST_PATH) if "path" in row}
    rows = []
    for path in list_source_files():
        rel_path = repo_relative(path)
        covered_by = coverage.get(rel_path, [])
        was_processed = bool(existing.get(rel_path, {}).get("processed", False))
        is_processed_path = rel_path.startswith("raw/processed/")
        processed = was_processed or is_processed_path or (accept_covered and bool(covered_by))
        rows.append(
            {
                "path": rel_path,
                "title": raw_source_title(path),
                "processed": processed,
                "covered_by": covered_by,
                "updated": TODAY,
            }
        )
    return sorted(rows, key=lambda row: row["path"])


def top_phrase_candidates(
    notes: list[Note],
    min_count: int,
    max_results: int,
    phrase_lengths: range,
) -> list[PromotionCandidate]:
    phrase_hits: dict[str, set[str]] = defaultdict(set)
    examples: dict[str, list[str]] = defaultdict(list)

    for note in notes:
        words = [word.lower() for word in clean_words(note_body(note.path))]
        seen_in_note: set[str] = set()
        for length in phrase_lengths:
            if len(words) < length:
                continue
            for index in range(len(words) - length + 1):
                phrase_words = words[index:index + length]
                if any(word in STOPWORDS for word in phrase_words):
                    continue
                phrase = " ".join(phrase_words)
                if phrase in seen_in_note:
                    continue
                seen_in_note.add(phrase)
                phrase_hits[phrase].add(note.rel_path)
                if len(examples[phrase]) < 2:
                    examples[phrase].append(note.title)

    candidates = []
    for phrase, note_paths in phrase_hits.items():
        if len(note_paths) < min_count:
            continue
        candidates.append(
            PromotionCandidate(
                label=phrase,
                count=len(note_paths),
                note_paths=sorted(note_paths),
                examples=examples[phrase],
            )
        )
    candidates.sort(key=lambda candidate: (-candidate.count, candidate.label))
    return candidates[:max_results]


def top_name_candidates(notes: list[Note], min_count: int, max_results: int) -> list[PromotionCandidate]:
    name_hits: dict[str, set[str]] = defaultdict(set)
    examples: dict[str, list[str]] = defaultdict(list)
    pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b")

    for note in notes:
        body = note_body(note.path)
        seen_in_note: set[str] = set()
        for match in pattern.findall(body):
            candidate = match.strip()
            if candidate.lower() in STOPWORDS:
                continue
            if candidate in {"Los Angeles", "Today", "Good Morning"}:
                continue
            if candidate in seen_in_note:
                continue
            seen_in_note.add(candidate)
            name_hits[candidate].add(note.rel_path)
            if len(examples[candidate]) < 2:
                examples[candidate].append(note.title)

    candidates = []
    for name, note_paths in name_hits.items():
        if len(note_paths) < min_count:
            continue
        candidates.append(
            PromotionCandidate(
                label=name,
                count=len(note_paths),
                note_paths=sorted(note_paths),
                examples=examples[name],
            )
        )
    candidates.sort(key=lambda candidate: (-candidate.count, candidate.label))
    return candidates[:max_results]


def orphan_candidates() -> list[dict[str, str]]:
    notes = [note for note in load_catalog_notes() if note.note_type != "journal"]
    all_targets = {note.path.relative_to(WIKI_DIR).as_posix(): note for note in notes}
    inbound_counts = {target: 0 for target in all_targets}
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for note in notes:
        body = note_body(note.path)
        base = note.path.parent
        for _, target in link_pattern.findall(body):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (base / target).resolve()
            try:
                relative = resolved.relative_to(WIKI_DIR).as_posix()
            except ValueError:
                continue
            if relative in inbound_counts:
                inbound_counts[relative] += 1

    results = []
    for relative, count in sorted(inbound_counts.items()):
        if count == 0:
            note = all_targets[relative]
            results.append({"path": note.rel_path, "title": note.title, "type": note.note_type})
    return results


def build_folder_index(folder_name: str, notes: list[Note]) -> None:
    folder = WIKI_DIR / folder_name
    index_path = folder / "index.md"
    title = SECTION_LABELS.get(folder_name, folder_name.replace("-", " ").title())
    lines = [
        f"# {title} Index",
        "",
        f"Generated on {TODAY}.",
        "",
    ]
    if not notes:
        lines.extend(["No notes yet.", ""])
    else:
        for note in notes:
            relative_link = note.path.name
            summary = note.summary or "No summary yet."
            lines.append(f"- [{note.title}]({relative_link}): {summary}")
        lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")


def build_root_index(notes: list[Note]) -> None:
    grouped: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        folder_name = Path(note.rel_path).parts[1]
        grouped[folder_name].append(note)

    lines = [
        "# Vault Index",
        "",
        "This is the root catalog for the vault.",
        "",
        "## Core",
        "",
        "- [Overview](overview.md): top-level map of the knowledge base, current scope, and open questions.",
        "- [Log](log.md): append-only record of meaningful vault operations.",
        "- [Catalog](catalog.jsonl): machine-readable note catalog generated by `scripts/wiki_tool.py build`.",
        "",
        "## Wiki",
        "",
    ]

    ordered_sections = [
        ("sources", SECTION_LABELS["sources"]),
        ("topics", SECTION_LABELS["topics"]),
        ("entities", SECTION_LABELS["entities"]),
        ("syntheses", SECTION_LABELS["syntheses"]),
        ("crm", SECTION_LABELS["crm"]),
        ("journal", SECTION_LABELS["journal"]),
        ("inbox-clips", SECTION_LABELS["inbox-clips"]),
    ]

    for folder_name, label in ordered_sections:
        lines.append(f"### {label}")
        lines.append("")
        if folder_name == "inbox-clips":
            lines.append("- [Inbox Clips](inbox-clips/README.md): staging area for Obsidian Web Clipper captures before normalization or promotion.")
            lines.append("")
            continue
        lines.append(f"- [{label} Index]({folder_name}/index.md)")
        entries = grouped.get(folder_name, [])
        if not entries:
            lines.append(f"- {EMPTY_MESSAGES.get(folder_name, f'No {label.lower()} pages yet.')}")
        else:
            for note in entries:
                relative = note.path.relative_to(WIKI_DIR).as_posix()
                summary = note.summary or "No summary yet."
                lines.append(f"- [{note.title}]({relative}): {summary}")
        lines.append("")

    lines.extend(
        [
            "## Maintenance",
            "",
            f"- Source manifest: [`Schema/source-manifest.jsonl`](../Schema/source-manifest.jsonl)",
            "",
        ]
    )
    (WIKI_DIR / "index.md").write_text("\n".join(lines), encoding="utf-8")


def command_doctor(_: argparse.Namespace) -> int:
    required = [
        RAW_DIR,
        RAW_PROCESSED_DIR,
        WIKI_DIR,
        SCHEMA_DIR,
        WIKI_DIR / "sources",
        WIKI_DIR / "topics",
        WIKI_DIR / "entities",
        WIKI_DIR / "syntheses",
        WIKI_DIR / "crm",
        WIKI_DIR / "journal",
    ]
    missing = [repo_relative(path) for path in required if not path.exists()]
    if missing:
        raise WikiError(f"Missing required paths: {', '.join(missing)}")
    print(f"python={sys.version.split()[0]}")
    print(f"catalog_exists={CATALOG_PATH.exists()}")
    print(f"manifest_exists={MANIFEST_PATH.exists()}")
    print(f"raw_source_count={len(list_source_files())}")
    print(f"wiki_note_count={len(load_catalog_notes())}")
    return 0


def command_build(_: argparse.Namespace) -> int:
    notes = load_catalog_notes()
    rows = generate_catalog()
    write_jsonl(CATALOG_PATH, rows)
    grouped: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        folder_name = Path(note.rel_path).parts[1]
        grouped[folder_name].append(note)
    for folder_name, default_type in CATALOG_DIRS.items():
        if folder_name == "inbox-clips":
            continue
        build_folder_index(folder_name, grouped.get(folder_name, []))
    build_root_index(notes)
    print(f"built catalog={repo_relative(CATALOG_PATH)} notes={len(rows)}")
    return 0


def validate_common_frontmatter(note: Note, errors: list[str]) -> None:
    required = ["title", "type", "status", "created", "updated", "tags"]
    for key in required:
        if key not in note.frontmatter:
            errors.append(f"{note.rel_path}: missing frontmatter field `{key}`")
    tags = note.frontmatter.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append(f"{note.rel_path}: `tags` must be a list")


def command_lint(_: argparse.Namespace) -> int:
    errors: list[str] = []
    for note in load_catalog_notes():
        if note.note_type not in ALLOWED_TYPES:
            errors.append(f"{note.rel_path}: unsupported type `{note.note_type}`")
            continue
        if note.note_type in STRICT_NOTE_TYPES:
            validate_common_frontmatter(note, errors)
        if note.note_type == "source":
            raw_source = note.frontmatter.get("raw_source")
            if not isinstance(raw_source, str) or not raw_source.strip():
                errors.append(f"{note.rel_path}: source notes require `raw_source`")
            elif not validate_source_path(raw_source.strip()):
                errors.append(f"{note.rel_path}: raw_source does not exist: {raw_source}")
        if note.note_type in {"topic", "entity", "synthesis", "crm"}:
            sources = normalize_sources(note.frontmatter.get("sources"))
            source_count = note.frontmatter.get("source_count")
            if not isinstance(source_count, int):
                errors.append(f"{note.rel_path}: `source_count` must be an integer")
            elif source_count != len(sources):
                errors.append(f"{note.rel_path}: source_count={source_count} but sources={len(sources)}")
            for source in sources:
                if not validate_source_path(source):
                    errors.append(f"{note.rel_path}: missing source path `{source}`")
        if note.note_type == "source":
            tags = note.frontmatter.get("tags", [])
            if isinstance(tags, list) and "source" not in tags:
                errors.append(f"{note.rel_path}: source notes should include the `source` tag")

    if errors:
        raise WikiError("\n".join(errors))
    print("lint=ok")
    return 0


def command_source_scan(args: argparse.Namespace) -> int:
    rows = generate_manifest(accept_covered=args.accept_covered)
    if args.update:
        write_jsonl(MANIFEST_PATH, rows)
        print(f"manifest_updated={repo_relative(MANIFEST_PATH)} entries={len(rows)}")
        return 0
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    return 0


def command_source_lint(_: argparse.Namespace) -> int:
    errors: list[str] = []
    rows = load_jsonl(MANIFEST_PATH)
    manifest_paths = set()
    for row in rows:
        path = row.get("path")
        if not isinstance(path, str) or not path:
            errors.append("Schema/source-manifest.jsonl: every row needs a `path`")
            continue
        manifest_paths.add(path)
        absolute = ROOT / path
        if not absolute.exists():
            errors.append(f"{path}: manifest path does not exist")
        covered_by = row.get("covered_by", [])
        if not isinstance(covered_by, list):
            errors.append(f"{path}: `covered_by` must be a list")
            covered_by = []
        for wiki_path in covered_by:
            if not (ROOT / str(wiki_path)).exists():
                errors.append(f"{path}: covered_by target missing: {wiki_path}")
        if bool(row.get("processed")) and not covered_by:
            errors.append(f"{path}: processed source has no wiki coverage")
    actual_paths = {repo_relative(path) for path in list_source_files()}
    for missing in sorted(actual_paths - manifest_paths):
        errors.append(f"{missing}: missing from source manifest")
    if errors:
        raise WikiError("\n".join(errors))
    print("source_lint=ok")
    return 0


def command_source_delta(_: argparse.Namespace) -> int:
    manifest_paths = {row.get("path") for row in load_jsonl(MANIFEST_PATH)}
    actual_paths = [repo_relative(path) for path in list_source_files()]
    missing = [path for path in actual_paths if path not in manifest_paths]
    if not missing:
        print("source_delta=clean")
        return 0
    for path in missing:
        print(path)
    return 0


def command_source_coverage(_: argparse.Namespace) -> int:
    manifest = load_jsonl(MANIFEST_PATH)
    if not manifest:
        rows = generate_manifest(accept_covered=False)
    else:
        rows = manifest
    for row in rows:
        covered_by = row.get("covered_by", [])
        print(f"{row['path']}: {len(covered_by)} coverage -> {', '.join(covered_by) if covered_by else 'none'}")
    return 0


def command_search_catalog(args: argparse.Namespace) -> int:
    query = args.query.strip().lower()
    if not query:
        raise WikiError("query cannot be empty")
    rows = load_jsonl(CATALOG_PATH)
    matches = []
    for row in rows:
        haystack = " ".join(
            [
                str(row.get("title", "")),
                str(row.get("path", "")),
                " ".join(str(item) for item in row.get("tags", [])),
                " ".join(str(item) for item in row.get("sources", [])),
                str(row.get("summary", "")),
            ]
        ).lower()
        if query in haystack:
            matches.append(row)
    for row in matches:
        print(json.dumps(row, sort_keys=True))
    print(f"matches={len(matches)}")
    return 0


def command_promotion_candidates(args: argparse.Namespace) -> int:
    note_types = {item.strip() for item in args.note_types.split(",") if item.strip()}
    notes = promotion_notes(note_types=note_types)
    if args.mode == "phrases":
        candidates = top_phrase_candidates(notes, args.min_count, args.limit, range(2, 4))
    elif args.mode == "names":
        candidates = top_name_candidates(notes, args.min_count, args.limit)
    else:
        raise WikiError(f"unsupported mode: {args.mode}")
    for candidate in candidates:
        print(
            json.dumps(
                {
                    "label": candidate.label,
                    "count": candidate.count,
                    "note_paths": candidate.note_paths,
                    "examples": candidate.examples,
                },
                sort_keys=True,
            )
        )
    print(f"candidates={len(candidates)}")
    return 0


def command_orphan_notes(_: argparse.Namespace) -> int:
    results = orphan_candidates()
    for row in results:
        print(json.dumps(row, sort_keys=True))
    print(f"orphans={len(results)}")
    return 0


def command_log(args: argparse.Namespace) -> int:
    title = args.title.strip()
    details = args.details.strip()
    if not title or not details:
        raise WikiError("title and details are required")
    if not LOG_PATH.exists():
        raise WikiError("wiki/log.md does not exist")
    entry = f"\n## [{TODAY}] tool | {title}\n\n{details}\n"
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    print(f"log_appended={repo_relative(LOG_PATH)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LLM wiki maintenance tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = {
        "doctor": command_doctor,
        "build": command_build,
        "lint": command_lint,
        "source-scan": command_source_scan,
        "source-lint": command_source_lint,
        "source-delta": command_source_delta,
        "source-coverage": command_source_coverage,
        "search-catalog": command_search_catalog,
        "promotion-candidates": command_promotion_candidates,
        "orphan-notes": command_orphan_notes,
        "log": command_log,
    }

    subparsers.add_parser("doctor")
    subparsers.add_parser("build")
    subparsers.add_parser("lint")
    scan_parser = subparsers.add_parser("source-scan")
    scan_parser.add_argument("--update", action="store_true")
    scan_parser.add_argument("--accept-covered", action="store_true")
    subparsers.add_parser("source-lint")
    subparsers.add_parser("source-delta")
    subparsers.add_parser("source-coverage")
    search_parser = subparsers.add_parser("search-catalog")
    search_parser.add_argument("--query", required=True)
    promotion_parser = subparsers.add_parser("promotion-candidates")
    promotion_parser.add_argument("--mode", choices=["phrases", "names"], required=True)
    promotion_parser.add_argument("--min-count", type=int, default=2)
    promotion_parser.add_argument("--limit", type=int, default=20)
    promotion_parser.add_argument(
        "--note-types",
        default="journal,topic,entity,synthesis,crm,source",
        help="comma-separated note types to scan",
    )
    subparsers.add_parser("orphan-notes")
    log_parser = subparsers.add_parser("log")
    log_parser.add_argument("--title", required=True)
    log_parser.add_argument("--details", required=True)

    parser.set_defaults(func=lambda args: commands[args.command](args))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except WikiError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
