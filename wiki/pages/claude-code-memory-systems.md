---
title: Claude Code Memory Systems
type: page
status: active
created: 2026-05-25
updated: 2026-05-25
sources:
source_count: 0
aliases:
  - agent memory systems
  - claude memory stack
tags:
  - page
  - claude-code
  - memory
  - agents
---

# Claude Code Memory Systems

## Summary

The recent clip cluster frames Claude Code memory as a stack of approaches rather than one tool, with the LLM wiki pattern serving as a higher-order compiled memory layer rather than a universal replacement for every other memory mechanism.

## Key Points

- Different memory systems solve different retrieval problems: always-loaded rules, indexed markdown, semantic lookup, or verbatim recall.
- The LLM wiki pattern is strongest when you want durable, cross-session, cross-agent markdown knowledge rather than only project-local memory.
- This vault is intentionally leaning toward the LLM wiki end of that spectrum, with deterministic maintenance and selective semantic promotion.
- The practical tradeoff is more setup and review discipline in exchange for portability, auditability, and cross-tool reuse.

## Notes

The most relevant current clip cluster is:

- [Every Claude Code Memory System Compared (So You Don't Have To)](../inbox-clips/Every%20Claude%20Code%20Memory%20System%20Compared%20%28So%20You%20Don%27t%20Have%20To%29.md)
- [Claude Code + Karpathy Autoresearch = The New Meta](../inbox-clips/Claude%20Code%20%2B%20Karpathy%20Autoresearch%20%3D%20The%20New%20Meta.md)
- [Karpathy's "autoresearch" broke the internet](../inbox-clips/Karpathy%27s%20%22autoresearch%22%20broke%20the%20internet.md)
- [I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases](../inbox-clips/I%20Built%20Self-Evolving%20Claude%20Code%20Memory%20w%20Karpathy%27s%20LLM%20Knowledge%20Bases.md)

This cluster is useful less for exact implementation details and more for clarifying the design space:

- project-local memory files
- searchable memory stores
- compiled markdown knowledge bases
- always-on versus manual retrieval strategies

## Related Pages

- [LLM Wiki](../topics/llm-wiki.md)
- [Second Brain](../topics/second-brain.md)
- [Second Brain Operating Boundary](second-brain-boundary.md)
- [Second Brain Workflow](second-brain-workflow.md)

## Open Questions

- Which lower-level memory mechanisms are worth adopting in addition to the wiki, if any?
- When should memory stay project-local rather than being promoted into the shared vault?
