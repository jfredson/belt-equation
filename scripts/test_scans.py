#!/usr/bin/env python3
"""Checks the export's rule for a search listed under one node but first run for another.

Written 2026-10-06. At the first audit of the weekly scan John ruled that a search counts toward
a node only if it was aimed at that node, and that a search first run for another node and listed
again carries a `reused` line with a reason (docs/scan-procedure.md, step 1). The export cannot
judge the reason, but it refuses a `reused` line that gives none, and one that names no search
the item lists. Plain Python, standard library only:

    python3 scripts/test_scans.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import export  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NODES = {"C1", "C5", "L-heavy-launcher-100-per-year"}
SEARCH = "machine originated proof idea peer reviewed 2026"
OTHER = "accepted test for an inside in machine minds 2026"


def record(item_extra: dict) -> dict:
    item = {"node": "C5", "verdict": "quiet", "queries": [SEARCH, OTHER],
            "found": "Nothing in the week bore on the criterion."}
    item.update(item_extra)
    return {
        "scan": {"date": "2026-10-11", "ran_at": "2026-10-12T01:00:00Z", "scope": "weekly",
                 "nodes_checked": 1, "searches": 2, "commit_before": "abc1234"},
        "item": [item],
        "_file": "2026-10-11.toml", "_where": "scans/2026-10-11.toml", "_name_date": "2026-10-11",
    }


def problems_for(item_extra: dict) -> list[str]:
    problems, _ = export.validate_scans([record(item_extra)], NODES, set(), False)
    return problems


class AReusedSearchNeedsAReason(unittest.TestCase):
    def test_no_reused_line_is_fine(self):
        self.assertEqual(problems_for({}), [])

    def test_a_reused_line_with_a_reason_passes(self):
        line = (f"'{SEARCH}', first run for C1: part (a) of this node is an idea that came from "
                "the machine, which is exactly what C1's search looks for")
        self.assertEqual(problems_for({"reused": [line]}), [])

    def test_a_reused_line_with_no_reason_is_refused(self):
        for line in (SEARCH, f"{SEARCH} (C1)", f"'{SEARCH}', first run for C1",
                     f"reused from C1: {SEARCH}"):
            with self.subTest(line=line):
                found = problems_for({"reused": [line]})
                self.assertEqual(len(found), 1, found)
                self.assertIn("marked reused without a reason", found[0])

    def test_a_reused_line_must_name_a_search_the_item_lists(self):
        found = problems_for({"reused": ["Navier-Stokes blow-up search, first run for C1, "
                                         "because a machine proof would bear on it"]})
        self.assertEqual(len(found), 1, found)
        self.assertIn("does not name any search", found[0])

    def test_reused_must_be_a_list_of_lines(self):
        for bad in (f"{SEARCH} because it bears on part (a)", [""], [3]):
            with self.subTest(reused=bad):
                found = problems_for({"reused": bad})
                self.assertEqual(len(found), 1, found)
                self.assertIn("'reused' lists the searches", found[0])

    def test_a_node_id_does_not_count_as_a_reason(self):
        line = f"{SEARCH} L-heavy-launcher-100-per-year C1"
        self.assertEqual(len(problems_for({"reused": [line]})), 1)

    def test_the_scan_records_on_file_still_pass(self):
        tree_ids = {n["id"] for n in export.compute.load_tree(ROOT / "data")["nodes"]}
        raw, load_problems = export.load_scans(ROOT / "data" / "scans")
        self.assertEqual(load_problems, [])
        problems, _ = export.validate_scans(raw, tree_ids, set(), False)
        self.assertEqual([p for p in problems if "reused" in p], [])


if __name__ == "__main__":
    unittest.main()
