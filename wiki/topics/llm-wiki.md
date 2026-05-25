---
title: LLM Wiki
type: topic
status: active
created: 2026-05-25
updated: 2026-05-25
sources:
source_count: 0
aliases:
  - llm knowledge base
  - memory layer for agents
tags:
  - topic
  - llm-wiki
  - knowledge-base
  - obsidian
---

# LLM Wiki

## Summary

An LLM wiki is a compiled markdown knowledge layer that sits between raw captured material and future agent queries, with deterministic maintenance around indexing, provenance, and linting.

## Key Points

- The core pattern separates raw source capture, compiled wiki notes, and schema/tooling rules.
- The durable value comes from compiling reusable notes, not from re-reading raw material every time.
- Deterministic maintenance keeps the system queryable as it scales.
- In this repo, the pattern has been adapted so `raw/` lives outside the Obsidian vault while the compiled wiki stays inside it.

## Evidence

- [How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI](../inbox-clips/How%20To%20Build%20LLM%20Wiki%20In%20Obsidian%3F%20%F0%9F%A7%A0%20A%20Memory%20Layer%20For%20Any%20Agentic%20AI.md): three-layer model of sources, wiki, and schema/tooling.
- [I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases](../inbox-clips/I%20Built%20Self-Evolving%20Claude%20Code%20Memory%20w%20Karpathy%27s%20LLM%20Knowledge%20Bases.md): reinforces the compiler-style memory pattern.
- [Every Claude Code Memory System Compared (So You Don't Have To)](../inbox-clips/Every%20Claude%20Code%20Memory%20System%20Compared%20%28So%20You%20Don%27t%20Have%20To%29.md): positions the LLM wiki as one memory-system layer among other approaches.

## Related Pages

- [Second Brain](second-brain.md)
- [Claude Code Memory Systems](../pages/claude-code-memory-systems.md)
- [Second Brain Workflow](../pages/second-brain-workflow.md)
- [Overview](../overview.md)

## Open Questions

- Which parts of the memory-compiler pattern should stay deterministic versus agentic in this vault?
- Should a future ingest workflow compile selected clips into `wiki/sources/` automatically or only on explicit request?
