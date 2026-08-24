#!/usr/bin/env python3
"""Manual sync: import wiki/crm/*.md client notes into adamhaley-com's /api/clients.

Reads SECOND_BRAIN_CLIENT_API_URL and SECOND_BRAIN_CLIENT_API_TOKEN from .env
in this repo's root (gitignored). Run by hand when new CRM notes are added -
not scheduled. See project_crm_import_automation_pin memory for the plan to
make this a durable, cron-scheduled step later.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CRM_DIR = REPO_ROOT / "wiki" / "crm"
SKIP = {"index.md", "README.md", "cassio.md"}  # cassio is a personal contact, not a business client


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
TOKEN = sys.argv[1] if len(sys.argv) > 1 else env.get("SECOND_BRAIN_CLIENT_API_TOKEN")
API_URL = sys.argv[2] if len(sys.argv) > 2 else env.get("SECOND_BRAIN_CLIENT_API_URL", "https://adamhaley-com.test/api/clients")

if not TOKEN:
    print("No token found. Set SECOND_BRAIN_CLIENT_API_TOKEN in .env, or pass one as an argument.", file=sys.stderr)
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
            elif val == "[]":
                data[key] = []
            else:
                data[key] = val
        i += 1
    return data


def extract_summary(body: str) -> str | None:
    m = re.search(r"## Summary\n\n(.*?)\n\n##", body, re.DOTALL)
    return m.group(1).strip() if m else None


def first_or_none(items):
    return items[0] if items else None


results = []
for path in sorted(CRM_DIR.glob("*.md")):
    if path.name in SKIP:
        continue
    fm = parse_frontmatter(path.read_text())
    slug = path.stem

    location = fm.get("location", "unknown")
    payload = {
        "source": "second_brain_crm",
        "source_external_id": slug,
        "name": fm.get("title") or slug,
        "description": extract_summary(fm.get("_body", "")),
        "email": first_or_none(fm.get("emails", [])),
        "phone": first_or_none(fm.get("phones", [])),
        "address": None if location in ("unknown", "") else location,
        "url": first_or_none(fm.get("websites", [])),
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

for slug, status, info in results:
    print(f"{status}  {slug}  {info}")
