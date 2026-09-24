#!/usr/bin/env python3
"""Tests for the agent-facing todo/plan editing commands in wiki_tool.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
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
        self.todo.write_text(TODO, encoding="utf-8")
        self.plan = self.wiki / "projects" / "demo" / "plans" / "2020-01-01.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        for name, value in {"ROOT": root, "WIKI_DIR": self.wiki, "TODO_PATH": self.todo}.items():
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
        self.assertIn("- [x] alpha: first thing — shipped", self.todo.read_text())

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


if __name__ == "__main__":
    unittest.main()
