#!/usr/bin/env python3
"""Manual sync: import `[idea]`-tagged lines from wiki/pages/adamhaley-com-content-ideas.md
into adamhaley-com's /api/posts, as draft-stage Post rows (title + raw only).

Only lines tagged `[idea]` in the page's "## Ideas" numbered list are synced. On a
successful import, the script rewrites that line's tag to `[drafted]` in place, so a
re-run only ever picks up genuinely new ideas - the API's own source/source_external_id
uniqueness is a second, independent safety net against duplicates, not the only one.

Reads SECOND_BRAIN_POST_API_URL and SECOND_BRAIN_API_TOKEN from .env in this repo's
root (gitignored) - .env points at production by default, so a bare run hits the live
site. When testing a change to this script itself (not just a routine sync), pass a
local URL/token explicitly as arguments to avoid writing to prod:
`import_content_ideas.py <local-token> <local-url>`.

SECOND_BRAIN_API_TOKEN is shared with import_crm_clients.py and import_prospects.py -
one Sanctum token with clients:manage, prospects:manage, and posts:manage abilities,
rather than a separate token per endpoint. The token needs posts:manage added before
this script can be run against production - see the [[adamhaley-com-content-ideas]]
page's Open Questions / the second brain's rolling todo.

Run by hand when new ideas are added to the page - not scheduled.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGE_PATH = REPO_ROOT / "wiki" / "pages" / "adamhaley-com-content-ideas.md"
IDEA_LINE = re.compile(r"^(\d+)\. `\[idea\]` (.+)$")


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
API_URL = sys.argv[2] if len(sys.argv) > 2 else env.get("SECOND_BRAIN_POST_API_URL", "https://adamhaley-com.test/api/posts")

if not TOKEN:
    print("No token found. Set SECOND_BRAIN_API_TOKEN in .env, or pass one as an argument.", file=sys.stderr)
    sys.exit(1)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "idea"


def make_title(text: str, limit: int = 60) -> str:
    if len(text) <= limit:
        return text
    truncated = text[:limit].rsplit(" ", 1)[0]
    return f"{truncated}…"


if not PAGE_PATH.exists():
    print(f"Page not found: {PAGE_PATH}", file=sys.stderr)
    sys.exit(1)

lines = PAGE_PATH.read_text().splitlines()
results = []

for i, line in enumerate(lines):
    m = IDEA_LINE.match(line)
    if not m:
        continue

    text = m.group(2)
    title = make_title(text)
    payload = {
        "source": "second_brain_content_ideas",
        "source_external_id": slugify(title),
        "title": title,
        "raw": text,
    }

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

    if status in ("200", "201"):
        lines[i] = line.replace("`[idea]`", "`[drafted]`", 1)

    results.append((payload["source_external_id"], status, info))

if results:
    PAGE_PATH.write_text("\n".join(lines) + "\n")

if not results:
    print("No `[idea]`-tagged lines found.")
for slug, status, info in results:
    print(f"{status}  {slug}  {info}")
