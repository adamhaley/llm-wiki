---
name: llm-wiki-query
description: Use this skill when answering questions from the existing wiki, prioritizing compiled notes before raw source material.
---

# LLM Wiki Query

Use this skill when answering questions from the existing wiki.

## Workflow

1. Open `wiki/index.md`.
2. Run `python3 scripts/wiki_tool.py search-catalog --query "topic"`.
3. Read the most relevant compiled notes first.
4. Open raw sources only when compiled notes are insufficient or source-level verification is requested.
5. If the answer creates durable value, file it into `wiki/syntheses/` and run the maintenance commands.
