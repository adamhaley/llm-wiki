#!/usr/bin/env python3
"""Manual sync: import wiki/field-reports/*.md tagged `prospect` into adamhaley-com's /api/prospects.

Only field reports with `prospect` in their frontmatter `tags` list are synced - most field
reports are general captures, not leads. Tag a report `prospect` in Obsidian to make it
importable.

Reads SECOND_BRAIN_PROSPECT_API_URL and SECOND_BRAIN_API_TOKEN from .env in this repo's
root (gitignored) - .env points at production by default, so a bare run hits the live site.
When testing a change to this script itself (not just a routine sync), pass a local
URL/token explicitly as arguments to avoid writing to prod:
`import_prospects.py <local-token> <local-url>`.

SECOND_BRAIN_API_TOKEN is shared with import_crm_clients.py - one Sanctum token with both
clients:manage and prospects:manage abilities, rather than a separate token per endpoint.

Run by hand when field reports get tagged `prospect` - not scheduled.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIELD_REPORTS_DIR = REPO_ROOT / "wiki" / "field-reports"
SKIP = {"index.md", "README.md"}


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip()
    return env


env = load_env(REPO_ROOT / ".env")
TOKEN = sys.argv[1] if len(sys.argv) > 1 else env.get("SECOND_BRAIN_API_TOKEN")
API_URL = sys.argv[2] if len(sys.argv) > 2 else env.get("SECOND_BRAIN_PROSPECT_API_URL", "https://adamhaley-com.test/api/prospects")

if not TOKEN:
    print("No token found. Set SECOND_BRAIN_API_TOKEN in .env, or pass one as an argument.", file=sys.stderr)
    sys.exit(1)


def parse_frontmatter(text: str) -> dict:
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not fm_match:
        return {}
    fm_text, body = fm_match.group(1), fm_match.group(2)
    data: dict = {"_body": body}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "" and i + 1 < len(lines) and lines[i + 1].strip().startswith("- "):
                items = []
                i += 1
                while i < len(lines) and lines[i].strip().startswith("- "):
                    items.append(lines[i].strip()[2:].strip())
                    i += 1
                data[key] = items
                continue
            elif val == "" and i + 1 < len(lines) and re.match(r"^  \w+:", lines[i + 1]):
                nested = {}
                i += 1
                while i < len(lines) and re.match(r"^  \w+:", lines[i]):
                    nm = re.match(r"^  (\w+):\s*(.*)$", lines[i])
                    nested[nm.group(1)] = nm.group(2).strip()
                    i += 1
                data[key] = nested
                continue
            elif val == "[]":
                data[key] = []
            else:
                data[key] = val
        i += 1
    return data


def strip_image_embeds(text: str) -> str:
    return re.sub(r"!\[\[[^\]]+\]\]\n?", "", text).strip()


def as_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


results = []
for path in sorted(FIELD_REPORTS_DIR.glob("*.md")):
    if path.name in SKIP:
        continue
    fm = parse_frontmatter(path.read_text())
    if "prospect" not in fm.get("tags", []):
        continue

    slug = path.stem
    location = fm.get("location", {}) if isinstance(fm.get("location"), dict) else {}

    payload = {
        "source": "second_brain_field_report",
        "source_external_id": slug,
        "latitude": as_float(location.get("latitude")),
        "longitude": as_float(location.get("longitude")),
        "summary": strip_image_embeds(fm.get("_body", "")) or None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    proc = subprocess.run(
        [
            "curl", "-s", "-w", "\n%{http_code}",
            "-X", "POST", API_URL,
            "-H", f"Authorization: Bearer {TOKEN}",
            "-H", "Accept: application/json",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ],
        capture_output=True, text=True,
    )
    *body_lines, status = proc.stdout.rsplit("\n", 1)
    body_text = "\n".join(body_lines)
    try:
        body = json.loads(body_text)
        info = body.get("data", {}).get("id", body)
    except json.JSONDecodeError:
        info = body_text
    results.append((slug, status, info))

if not results:
    print("No field reports tagged `prospect` found.")
for slug, status, info in results:
    print(f"{status}  {slug}  {info}")
