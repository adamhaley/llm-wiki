# Patterns

Use this directory for durable, reusable technical patterns: architectural conventions, UI paradigms, code shapes Adam has deliberately standardized on across projects — the kind of thing an AI agent building a new feature should check *before* inventing its own approach.

This is a first-class citizen, separate from `pages/`, because these notes are meant to be actively referenced by coding agents at the start of a build, not just narrative/compiled knowledge. See [[coding-standards]] in Adam's global Claude Code rules (`~/.claude/rules/coding-standards.md`) for the pointer that makes agents check here.

## Core Value: Earn Your Keep

A pattern belongs here only after it has actually been used more than once in real projects — not because it seems like good practice in the abstract. This directory should grow out of repeated implementation, never ahead of it. See [Use-Led Simplicity](/WIKI_SCHEMA.md) — same principle, applied to code conventions instead of vault structure.

**This is the default for shapes discovered bottom-up** — a UI convention, an admin-table setup, a code structure that happens to recur. A single instance there might just be coincidence or premature abstraction; waiting for a second, independent occurrence is what proves it's actually a reusable shape rather than one project's local choice.

It does **not** gate a shape Adam arrives at top-down: a deliberate architectural or technical decision, made once with the explicit intent that it become the standing approach going forward (e.g. "this is a standing default now, not a case-by-case call" — see [[push-reactivity-not-polling]], [[llm-free-faq-chatbot]]). There the decision itself is the durability signal, not the repetition — recording it after one real, working instance is correct, not premature. The giveaway is intent: did Adam converge on this shape by accident across projects, or explicitly decide "this is how I want to do X from now on"?

## Multiple Patterns Can Cover the Same Problem

This directory is not "one canonical answer per problem class." A whole family of legitimate, independently-recorded patterns can exist for the same kind of problem — e.g. chatbots: [[llm-free-faq-chatbot]] (deterministic TF-IDF, single-turn, cheap) sits alongside future notes for an LLM-backed conversational chatbot with real state, or something in between, each earning its own pattern note rather than being folded into one "the chatbot pattern" doc as variants or exceptions.

When recording a new pattern in a problem space that already has one:
- Don't treat the existing note as the default and the new one as the special case (or vice versa). Give each its own note, scoped to the shape it actually is.
- Each note's "When this pattern doesn't apply" section is where the *selection criteria* between siblings lives — state plainly what would make you reach for a different one instead, so a future agent (or Adam) can pick the right one for the actual requirements instead of assuming there's only one option.
- Cross-link siblings once more than one exists in the same space, so browsing one surfaces the others.

## One Note Per Pattern

Each note should:

- Name the pattern clearly (e.g. "Filament Slide-Over Processing Admin," not "Admin UI Ideas")
- Link to at least one **real reference implementation** — an actual file in an actual project, not just prose describing the idea. Patterns rot fast as descriptions; they stay accurate as pointers to working code.
- Note which project(s) currently use it, so "is this still the pattern?" has an answer grounded in reality, not just in this note's last-edited date.
- State the core reasoning/tradeoff briefly — why this shape over the obvious alternatives — so a future agent can judge when the pattern doesn't apply, not just copy it blindly.

## Filename Convention

`kebab-case-pattern-name.md`, flat in this directory. No nested subcategories until there's a real reason (per the core value above).
