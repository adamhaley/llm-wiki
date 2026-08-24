#!/usr/bin/env python3
"""Deterministic maintenance tooling for the local LLM wiki."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
INBOX_DIR = WIKI_DIR / "inbox"
INBOX_ASSETS_DIR = INBOX_DIR / "assets"
SCHEMA_DIR = ROOT / "Schema"
CATALOG_PATH = WIKI_DIR / "catalog.jsonl"
MANIFEST_PATH = SCHEMA_DIR / "source-manifest.jsonl"
LOG_PATH = WIKI_DIR / "log.md"

TODAY = date.today().isoformat()

# Folder -> default note type. entity/source/synthesis notes now live inside
# pages/ (see ALLOWED_TYPES) and carry an explicit `type:` frontmatter value
# instead of getting their type from a dedicated folder.
CATALOG_DIRS = {
    "topics": "topic",
    "pages": "page",
    "crm": "crm",
    "journal": "journal",
    "field-reports": "field-report",
    "patterns": "pattern",
}
SECTION_LABELS = {
    "topics": "Topics",
    "pages": "Pages",
    "crm": "CRM",
    "journal": "Journal",
    "field-reports": "Field Reports",
    "patterns": "Patterns",
}
EMPTY_MESSAGES = {
    "topics": "No topic pages yet.",
    "pages": "No page notes yet.",
    "crm": "No CRM pages yet.",
    "journal": "No journal pages yet.",
    "field-reports": "No field reports yet.",
    "patterns": "No patterns yet.",
}
# field-report/pattern notes don't carry the full common-frontmatter contract
# (no status/created/updated requirement) - only require what they already use.
STRICT_NOTE_TYPES = {"source", "topic", "page", "entity", "synthesis", "crm", "plan"}
ALLOWED_TYPES = {"topic", "page", "crm", "journal", "entity", "source", "synthesis", "plan", "field-report", "pattern", "reference"}
SKIP_FILENAMES = {"README.md", "index.md"}
WIKI_ROOT_CORE_FILES = {"index.md", "log.md", "overview.md", "catalog.jsonl"}
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
PROMOTION_NOTE_TYPES = {"journal", "topic", "page", "entity", "synthesis", "crm", "source"}


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
    if INBOX_DIR.exists():
        for path in INBOX_DIR.rglob("*"):
            if not path.is_file():
                continue
            if path.name in {"README.md", ".gitkeep"}:
                continue
            if INBOX_ASSETS_DIR in path.parents:
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
    return relative.startswith("wiki/inbox/")


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


def inbox_status(path: Path) -> str:
    if path.suffix.lower() != ".md":
        return ""
    frontmatter, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
    return str(frontmatter.get("status") or "")


def generate_manifest(accept_covered: bool) -> list[dict[str, Any]]:
    notes = load_catalog_notes()
    coverage = coverage_map(notes)
    existing = {row["path"]: row for row in load_jsonl(MANIFEST_PATH) if "path" in row}
    rows = []
    for path in list_source_files():
        rel_path = repo_relative(path)
        covered_by = coverage.get(rel_path, [])
        was_processed = bool(existing.get(rel_path, {}).get("processed", False))
        is_archived = inbox_status(path) in {"archived", "processed"}
        processed = was_processed or is_archived or (accept_covered and bool(covered_by))
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


CROSS_LINK_TARGET_TYPES = {"topic", "page", "entity", "synthesis", "source", "crm"}
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")
EXISTING_LINK_PATTERN = re.compile(r"\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)")


def cross_link_candidates(max_per_file: int = 25) -> list[dict[str, str]]:
    """Find plain-text mentions of other notes' titles/aliases that aren't linked yet.

    Mirrors Obsidian's per-note "Unlinked mentions" panel, but vault-wide.
    Deliberately surfaces candidates only -- a text match isn't always a real
    reference, so linking is a judgment call for the reader (or an agent
    reviewing the output), not an automatic rewrite.
    """
    notes = load_catalog_notes()
    targets: dict[str, tuple[Note, str]] = {}
    for note in notes:
        if note.note_type not in CROSS_LINK_TARGET_TYPES:
            continue
        names = [note.title] + [
            str(alias) for alias in note.frontmatter.get("aliases", []) if str(alias).strip()
        ]
        for name in names:
            name = name.strip()
            if len(name) < 4 or name.lower() in STOPWORDS:
                continue
            targets.setdefault(name.lower(), (note, name))

    if not targets:
        return []

    name_pattern = re.compile(
        r"\b(" + "|".join(re.escape(name) for _, name in targets.values()) + r")\b",
        re.IGNORECASE,
    )

    results: list[dict[str, str]] = []
    for source in notes:
        body = note_body(source.path)
        found_targets: set[str] = set()
        per_file = 0
        in_fence = False
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or stripped.startswith("#"):
                continue
            cleaned = INLINE_CODE_PATTERN.sub("", line)
            cleaned = EXISTING_LINK_PATTERN.sub("", cleaned)
            for match in name_pattern.finditer(cleaned):
                matched_text = match.group(1)
                target_note, canonical_name = targets[matched_text.lower()]
                if target_note.rel_path == source.rel_path:
                    continue
                dedup_key = target_note.rel_path
                if dedup_key in found_targets:
                    continue
                if per_file >= max_per_file:
                    break
                found_targets.add(dedup_key)
                per_file += 1
                results.append(
                    {
                        "source": source.rel_path,
                        "target": target_note.rel_path,
                        "target_title": canonical_name,
                        "matched": matched_text,
                        "excerpt": stripped[:160],
                    }
                )
    return results


MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
WIKILINK_TARGET_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def wiki_markdown_index() -> dict[str, Path]:
    """basename (lowercased, no extension) -> path, for every markdown file in wiki/.

    Used to resolve [[wikilinks]], which Obsidian matches by filename across
    the whole vault rather than by relative path.
    """
    index: dict[str, Path] = {}
    for path in WIKI_DIR.rglob("*.md"):
        index.setdefault(path.stem.lower(), path)
    return index


def wiki_attachment_index() -> dict[str, Path]:
    """basename (lowercased, with extension) -> path, for non-markdown files in wiki/.

    Used to resolve [[image.jpg]]-style embed wikilinks, which (unlike note
    wikilinks) keep their extension and aren't covered by wiki_markdown_index().
    """
    index: dict[str, Path] = {}
    for path in WIKI_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() != ".md":
            index.setdefault(path.name.lower(), path)
    return index


def dead_link_candidates() -> list[dict[str, str]]:
    """Find [text](target) and [[wikilink]] targets that don't resolve to a real file.

    wiki_tool.py lint validates frontmatter and source/raw_source paths, but
    not that every in-body link target actually exists -- this fills that gap.
    """
    notes = load_catalog_notes()
    name_index = wiki_markdown_index()
    attachment_index = wiki_attachment_index()
    results: list[dict[str, str]] = []

    for note in notes:
        body = note_body(note.path)
        base = note.path.parent
        in_fence = False
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            cleaned = INLINE_CODE_PATTERN.sub("", line)

            for _, target in MARKDOWN_LINK_PATTERN.findall(cleaned):
                target = target.strip()
                if not target or "://" in target or target.startswith("#") or target.lower().startswith("mailto:"):
                    continue
                target_path = target.split("#", 1)[0].strip()
                if not target_path or not target_path.lower().endswith(".md"):
                    continue
                resolved = (base / target_path).resolve()
                if resolved.exists():
                    continue
                suggestions = difflib.get_close_matches(Path(target_path).stem.lower(), name_index.keys(), n=3)
                results.append(
                    {
                        "source": note.rel_path,
                        "link_type": "markdown",
                        "target": target_path,
                        "excerpt": stripped[:160],
                        "suggestions": ", ".join(wiki_relative(name_index[s]) for s in suggestions),
                    }
                )

            for wikitarget in WIKILINK_TARGET_PATTERN.findall(cleaned):
                key = wikitarget.strip().lower()
                if not key:
                    continue
                is_attachment = Path(key).suffix not in ("", ".md")
                if is_attachment:
                    if key in attachment_index:
                        continue
                    suggestions = difflib.get_close_matches(key, attachment_index.keys(), n=3)
                    suggestion_paths = [attachment_index[s] for s in suggestions]
                else:
                    if key in name_index:
                        continue
                    suggestions = difflib.get_close_matches(key, name_index.keys(), n=3)
                    suggestion_paths = [name_index[s] for s in suggestions]
                results.append(
                    {
                        "source": note.rel_path,
                        "link_type": "wikilink",
                        "target": wikitarget.strip(),
                        "excerpt": stripped[:160],
                        "suggestions": ", ".join(wiki_relative(p) for p in suggestion_paths),
                    }
                )
    return results


def root_inbox_files() -> list[Path]:
    """Loose .md files dropped directly in wiki/ root, awaiting triage.

    Distinct from wiki/inbox/: this catches files mistakenly dropped at the
    vault root rather than the intentional capture zone. Files land here by
    hand and are expected to be promoted into the correct subdirectory,
    moved into wiki/inbox/, or deleted, not to accumulate indefinitely. No
    frontmatter or naming convention is required here.
    """
    if not WIKI_DIR.exists():
        return []
    files = []
    for path in sorted(WIKI_DIR.glob("*.md")):
        if path.name in WIKI_ROOT_CORE_FILES:
            continue
        files.append(path)
    return files


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
        ("topics", SECTION_LABELS["topics"]),
        ("pages", SECTION_LABELS["pages"]),
        ("crm", SECTION_LABELS["crm"]),
        ("journal", SECTION_LABELS["journal"]),
        ("field-reports", SECTION_LABELS["field-reports"]),
        ("patterns", SECTION_LABELS["patterns"]),
    ]

    lines.append("### Inbox")
    lines.append("")
    lines.append("- [Inbox](inbox/README.md): staging area for raw captures and Web Clipper clips before triage. Not catalog-indexed; not linted.")
    lines.append("")

    for folder_name, label in ordered_sections:
        lines.append(f"### {label}")
        lines.append("")
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
        WIKI_DIR,
        INBOX_DIR,
        SCHEMA_DIR,
        WIKI_DIR / "topics",
        WIKI_DIR / "pages",
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
    print(f"root_inbox_count={len(root_inbox_files())}")
    return 0


def command_build(_: argparse.Namespace) -> int:
    notes = load_catalog_notes()
    rows = generate_catalog()
    write_jsonl(CATALOG_PATH, rows)
    grouped: dict[str, list[Note]] = defaultdict(list)
    for note in notes:
        folder_name = Path(note.rel_path).parts[1]
        grouped[folder_name].append(note)
    for folder_name in CATALOG_DIRS:
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
        if note.note_type in {"topic", "page", "entity", "synthesis", "crm"}:
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


def command_cross_link_candidates(args: argparse.Namespace) -> int:
    results = cross_link_candidates(max_per_file=args.max_per_file)
    for row in results:
        print(json.dumps(row, sort_keys=True))
    print(f"candidates={len(results)}")
    return 0


def command_dead_links(_: argparse.Namespace) -> int:
    results = dead_link_candidates()
    for row in results:
        print(json.dumps(row, sort_keys=True))
    print(f"dead_links={len(results)}")
    return 0


def command_root_inbox(_: argparse.Namespace) -> int:
    files = root_inbox_files()
    for path in files:
        size = path.stat().st_size
        print(
            json.dumps(
                {"path": repo_relative(path), "bytes": size, "empty": size == 0},
                sort_keys=True,
            )
        )
    print(f"root_inbox_files={len(files)}")
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
        "cross-link-candidates": command_cross_link_candidates,
        "dead-links": command_dead_links,
        "root-inbox": command_root_inbox,
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
    cross_link_parser = subparsers.add_parser("cross-link-candidates")
    cross_link_parser.add_argument("--max-per-file", type=int, default=25)
    subparsers.add_parser("dead-links")
    subparsers.add_parser("root-inbox")
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
