#!/usr/bin/env python3
"""Tests for the agent-facing todo/plan editing commands in wiki_tool.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wiki_tool  # noqa: E402

TODO = """---
title: Todo
type: todo
updated: 2020-01-01
---

# Todo

- [ ] alpha: first thing
- [x] beta: already done
- [ ] alpha: second thing
- [ ] loose item without a project
"""

PLAN = """---
title: Some plan
type: plan
status: planned
created: 2020-01-01
updated: 2020-01-01
tags:
  - x
---

# Some plan

**Status:** Not started.

Body text that must not change.
"""


class WikiToolEditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.wiki = root / "wiki"
        (self.wiki / "projects" / "demo" / "plans").mkdir(parents=True)
        self.todo = self.wiki / "todo.md"
        self.todo_archive = self.wiki / "todo-archive.md"
        self.todo.write_text(TODO, encoding="utf-8")
        self.plan = self.wiki / "projects" / "demo" / "plans" / "2020-01-01.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        for name, value in {"ROOT": root, "WIKI_DIR": self.wiki, "TODO_PATH": self.todo, "TODO_ARCHIVE_PATH": self.todo_archive}.items():
            patcher = mock.patch.object(wiki_tool, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_cli(self, *argv: str) -> int:
        args = wiki_tool.build_parser().parse_args(list(argv))
        return args.func(args)

    def test_todo_add_lands_after_the_last_item_for_the_same_project(self) -> None:
        self.run_cli("todo", "add", "--text", "alpha: third thing")
        lines = self.todo.read_text().split("\n")
        self.assertEqual(lines[lines.index("- [ ] alpha: second thing") + 1], "- [ ] alpha: third thing")

    def test_todo_add_for_a_new_project_goes_after_the_last_item(self) -> None:
        self.run_cli("todo", "add", "--text", "gamma: brand new")
        self.assertIn("- [ ] loose item without a project\n- [ ] gamma: brand new", self.todo.read_text())

    def test_todo_add_rejects_an_identical_item(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("todo", "add", "--text", "beta: already done")

    def test_todo_add_bumps_the_updated_date(self) -> None:
        self.run_cli("todo", "add", "--text", "gamma: x")
        self.assertIn(f"updated: {wiki_tool.TODAY}", self.todo.read_text())

    def test_todo_check_ticks_exactly_one_item_and_appends_the_note(self) -> None:
        self.run_cli("todo", "check", "--match", "first thing", "--note", "shipped")
        self.assertIn(f"- [x] alpha: first thing — shipped — completed: {wiki_tool.TODAY}", self.todo.read_text())

    def test_todo_archive_moves_only_completed_items_at_least_seven_days_old(self) -> None:
        as_of = date(2026, 10, 11)
        text = TODO + "- [x] old — completed: 2026-10-04\n- [x] recent — completed: 2026-10-05\n"

        remaining, archived, newly_dated = wiki_tool.archive_todo_items(text, as_of)

        self.assertEqual(archived, ["- [x] old — completed: 2026-10-04"])
        self.assertIn("- [x] recent — completed: 2026-10-05", remaining)
        self.assertIn("- [x] beta: already done — completed by: 2026-10-11", remaining)
        self.assertIn("- [ ] alpha: first thing", remaining)
        self.assertEqual(newly_dated, 1)

    def test_todo_archive_moves_undated_completed_items_only_when_requested(self) -> None:
        remaining, archived, newly_dated = wiki_tool.archive_todo_items(TODO, date(2026, 10, 11), include_undated=True)

        self.assertEqual(archived, ["- [x] beta: already done"])
        self.assertIn("- [ ] alpha: first thing", remaining)
        self.assertEqual(newly_dated, 0)

    def test_todo_archive_keeps_manually_checked_item_for_seven_days_after_first_seen(self) -> None:
        first_sweep, archived, _ = wiki_tool.archive_todo_items(TODO, date(2026, 10, 11))
        next_sweep, archived_next, _ = wiki_tool.archive_todo_items(first_sweep, date(2026, 10, 18))

        self.assertEqual(archived, [])
        self.assertEqual(archived_next, ["- [x] beta: already done — completed by: 2026-10-11"])
        self.assertIn("- [ ] alpha: first thing", next_sweep)

    def test_todo_archive_command_preserves_open_items_and_original_completed_text(self) -> None:
        self.run_cli("todo", "archive", "--include-undated")

        self.assertNotIn("- [x] beta: already done", self.todo.read_text())
        self.assertIn("- [ ] alpha: first thing", self.todo.read_text())
        self.assertIn("## Archived " + wiki_tool.TODAY, self.todo_archive.read_text())
        self.assertIn("- [x] beta: already done", self.todo_archive.read_text())

    def test_todo_check_refuses_an_ambiguous_match(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("todo", "check", "--match", "alpha:")

    def test_todo_check_refuses_when_nothing_matches(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("todo", "check", "--match", "does not exist")

    def test_todo_check_ignores_already_checked_items(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("todo", "check", "--match", "already done")

    def test_failed_edit_leaves_the_file_untouched(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("todo", "check", "--match", "alpha:")
        self.assertEqual(self.todo.read_text(), TODO)

    def test_plan_set_status_updates_frontmatter_only(self) -> None:
        self.run_cli("plan", "set-status", "--project", "demo", "--date", "2020-01-01", "--status", "done")
        expected = PLAN.replace("status: planned", "status: done").replace(
            "updated: 2020-01-01", f"updated: {wiki_tool.TODAY}"
        )
        self.assertEqual(self.plan.read_text(), expected)

    def test_plan_set_status_note_replaces_the_body_status_line(self) -> None:
        self.run_cli(
            "plan", "set-status", "--project", "demo", "--date", "2020-01-01",
            "--status", "in-progress", "--note", "Started.",
        )
        self.assertIn("**Status:** Started.\n\nBody text that must not change.", self.plan.read_text())

    def test_plan_set_status_rejects_an_unknown_status(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            wiki_tool.set_plan_status(PLAN, "finished", None)

    def test_plan_set_status_rejects_a_missing_plan(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("plan", "set-status", "--project", "demo", "--date", "1999-01-01", "--status", "done")


class ContentPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.wiki = root / "wiki"
        for folder in wiki_tool.CONTENT_DIRS.values():
            (self.wiki / folder).mkdir(parents=True)
        for name, value in {"ROOT": root, "WIKI_DIR": self.wiki}.items():
            patcher = mock.patch.object(wiki_tool, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_cli(self, *argv: str) -> int:
        args = wiki_tool.build_parser().parse_args(list(argv))
        return args.func(args)

    def frontmatter(self, stage: str, slug: str, channel: str = "") -> dict:
        path = wiki_tool.content_path(stage, slug, channel)
        return wiki_tool.parse_frontmatter(path.read_text(encoding="utf-8"))[0]

    def test_content_new_writes_an_idea_at_the_first_status(self) -> None:
        self.run_cli("content", "new", "--slug", "a-real-idea", "--title", "A Real Idea: With Colon")
        frontmatter = self.frontmatter("idea", "a-real-idea")
        self.assertEqual(frontmatter["type"], "idea")
        self.assertEqual(frontmatter["slug"], "a-real-idea")
        self.assertEqual(frontmatter["status"], "raw")
        self.assertEqual(frontmatter["title"], "A Real Idea: With Colon")

    def test_content_new_rejects_a_non_kebab_case_slug(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("content", "new", "--slug", "Not A Slug")

    def test_content_new_refuses_to_overwrite_an_existing_idea(self) -> None:
        self.run_cli("content", "new", "--slug", "taken")
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("content", "new", "--slug", "taken")

    def test_content_promote_requires_the_previous_stage(self) -> None:
        with self.assertRaises(wiki_tool.WikiError):
            self.run_cli("content", "promote", "--slug", "nothing-here", "--to", "draft")

    def test_content_promote_to_draft_advances_the_idea_and_inherits_its_title(self) -> None:
        self.run_cli("content", "new", "--slug", "chain", "--title", "Chain Title", "--project", "demo")
        self.run_cli("content", "promote", "--slug", "chain", "--to", "draft")
        self.assertEqual(self.frontmatter("idea", "chain")["status"], "drafted")
        draft = self.frontmatter("draft", "chain")
        self.assertEqual(draft["title"], "Chain Title")
        self.assertEqual(draft["project"], "demo")
        self.assertEqual(draft["status"], "in-progress")

    def test_content_promote_to_output_uses_the_channel_suffix_and_advances_the_draft(self) -> None:
        self.run_cli("content", "new", "--slug", "fanned")
        self.run_cli("content", "promote", "--slug", "fanned", "--to", "draft")
        self.run_cli("content", "promote", "--slug", "fanned", "--to", "output", "--channel", "x-thread")
        path = wiki_tool.content_path("output", "fanned", "x-thread")
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "fanned--x-thread.md")
        self.assertEqual(self.frontmatter("output", "fanned", "x-thread")["channel"], "x-thread")
        self.assertEqual(self.frontmatter("draft", "fanned")["status"], "ready")

    def test_content_promote_never_walks_a_status_backwards(self) -> None:
        self.run_cli("content", "new", "--slug", "shelved-one")
        idea_path = wiki_tool.content_path("idea", "shelved-one")
        idea_path.write_text(
            wiki_tool.set_frontmatter_value(idea_path.read_text(encoding="utf-8"), "status", "shelved"),
            encoding="utf-8",
        )
        self.run_cli("content", "promote", "--slug", "shelved-one", "--to", "draft")
        self.assertEqual(self.frontmatter("idea", "shelved-one")["status"], "shelved")

    def test_content_status_flags_a_draft_with_no_idea(self) -> None:
        wiki_tool.content_path("draft", "orphan").write_text(
            wiki_tool.content_note_text("draft", "orphan", "Orphan"), encoding="utf-8"
        )
        problems = wiki_tool.content_problems(wiki_tool.content_items(), stale_days=30)
        self.assertTrue(any("no idea for slug `orphan`" in problem for problem in problems))

    def write_idea(self, slug: str, status: str, updated: str = wiki_tool.TODAY) -> None:
        text = wiki_tool.content_note_text("idea", slug, slug)
        for key, value in {"status": status, "updated": updated}.items():
            text = wiki_tool.set_frontmatter_value(text, key, value)
        wiki_tool.content_path("idea", slug).write_text(text, encoding="utf-8")

    def test_content_status_flags_a_drafted_idea_with_no_draft(self) -> None:
        self.write_idea("claims-drafted", "drafted")
        problems = wiki_tool.content_problems(wiki_tool.content_items(), stale_days=30)
        self.assertTrue(any("status `drafted` but no draft" in problem for problem in problems))

    def test_content_status_leaves_an_old_raw_idea_alone(self) -> None:
        self.write_idea("banked", "raw", updated="2000-01-01")
        self.assertEqual(wiki_tool.content_problems(wiki_tool.content_items(), stale_days=30), [])

    def test_content_status_flags_an_old_developing_idea_with_no_draft(self) -> None:
        self.write_idea("stalled", "developing", updated="2000-01-01")
        problems = wiki_tool.content_problems(wiki_tool.content_items(), stale_days=30)
        self.assertTrue(any("idle since 2000-01-01" in problem for problem in problems))

    def test_content_status_accepts_everything_the_commands_produce(self) -> None:
        self.run_cli("content", "new", "--slug", "clean-one")
        self.run_cli("content", "promote", "--slug", "clean-one", "--to", "draft")
        self.run_cli("content", "promote", "--slug", "clean-one", "--to", "output", "--channel", "blog")
        self.assertEqual(wiki_tool.content_problems(wiki_tool.content_items(), stale_days=30), [])


if __name__ == "__main__":
    unittest.main()
