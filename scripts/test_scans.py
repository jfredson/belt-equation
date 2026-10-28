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


class ARulingOnTheNodeClearsAFlag(unittest.TestCase):
    """Added 2026-10-12: a flagged item is picked up when the node carries a revision, dated on
    or after the scan, whose reason names the scan's date (docs/scan-plan.md, the Radar page)."""

    def test_a_later_revision_naming_the_scan_counts(self):
        node = {"revisions": [{"date": "2026-10-12", "field": "verify", "old": "a claim", "new": "cleared",
                               "why": "Checked by the scan of 2026-10-11 and settled; ruled by John."}]}
        self.assertTrue(export.ruled_on_the_node(node, "2026-10-11"))

    def test_a_same_day_revision_naming_the_scan_counts(self):
        node = {"revisions": [{"date": "2026-10-11", "field": "verify", "old": "a", "new": "b",
                               "why": "Ruled the same evening as the 2026-10-11 scan."}]}
        self.assertTrue(export.ruled_on_the_node(node, "2026-10-11"))

    def test_an_earlier_revision_does_not_count(self):
        node = {"revisions": [{"date": "2026-10-10", "field": "verify", "old": "a", "new": "b",
                               "why": "Mentions 2026-10-11 as a future date, oddly."}]}
        self.assertFalse(export.ruled_on_the_node(node, "2026-10-11"))

    def test_a_later_revision_about_something_else_does_not_count(self):
        node = {"revisions": [{"date": "2026-10-12", "field": "probability", "old": "0.5", "new": "0.6",
                               "why": "Moved at the annual review."}]}
        self.assertFalse(export.ruled_on_the_node(node, "2026-10-11"))

    def test_a_node_with_no_revisions_does_not_count(self):
        self.assertFalse(export.ruled_on_the_node({}, "2026-10-11"))

    def test_the_staple_crop_flag_of_2026_10_11_is_no_longer_waiting(self):
        tree = export.compute.load_tree(ROOT / "data")
        scans, problems, _ = export.export_scans(tree, ROOT / "data" / "scans", ROOT / "data" / "ledger.toml")
        self.assertEqual(problems, [])
        still = [(w["scan_date"], w["node"]) for w in scans["waiting_on_john"]]
        self.assertNotIn(("2026-10-11", "B-staple-crop-grown-from-seed-to-harvest-off-earth"), still)


class ADiscoveryItemIsChecked(unittest.TestCase):
    """Added 2026-10-27 with the discovery watch (docs/discovery-sources.md; scan procedure step 3d):
    a `[[discovery]]` item carries a title, a date, an https source, one sentence and a node or
    "none", the record says how many sources the pass read, and a record holding only the pass
    may leave out its [[item]] list when it says it read no nodes."""

    GOOD = {"title": "The Rubin Observatory's first dwarf planet candidate, 2026 ED138", "date": "2026-10-27",
            "source": "https://rubinobservatory.org/news/rubin-first-dwarf-planet-candidate",
            "found": "On 2026-10-27 the Rubin Observatory announced 2026 ED138.", "node": "none"}

    def with_discoveries(self, discoveries, scan_extra=None, items=True) -> list[str]:
        raw = record({})
        raw["discovery"] = discoveries
        raw["scan"].update(scan_extra or {})
        if not items:
            raw["item"] = []
        problems, _ = export.validate_scans([raw], NODES, set(), False)
        return problems

    def test_a_good_item_passes(self):
        self.assertEqual(self.with_discoveries([self.GOOD], {"discovery_sources": 7}), [])

    def test_an_item_touching_a_step_names_a_node_in_the_tree(self):
        self.assertEqual(self.with_discoveries([{**self.GOOD, "node": "C5"}], {"discovery_sources": 7}), [])
        found = self.with_discoveries([{**self.GOOD, "node": "Z9"}], {"discovery_sources": 7})
        self.assertEqual(len(found), 1, found)
        self.assertIn("no node has the id 'Z9'", found[0])

    def test_items_need_the_count_of_sources_read(self):
        found = self.with_discoveries([self.GOOD])
        self.assertEqual(len(found), 1, found)
        self.assertIn("discovery_sources", found[0])

    def test_each_field_is_required_and_the_source_is_an_https_address(self):
        for field in ("title", "date", "source", "found", "node"):
            with self.subTest(missing=field):
                item = {k: v for k, v in self.GOOD.items() if k != field}
                found = self.with_discoveries([item], {"discovery_sources": 7})
                self.assertTrue(any(f"missing '{field}'" in p for p in found), found)
        found = self.with_discoveries([{**self.GOOD, "source": "a search result"}], {"discovery_sources": 7})
        self.assertEqual(len(found), 1, found)
        self.assertIn("https address", found[0])

    def test_the_date_is_a_day(self):
        found = self.with_discoveries([{**self.GOOD, "date": "October 2026"}], {"discovery_sources": 7})
        self.assertEqual(len(found), 1, found)
        self.assertIn("YYYY-MM-DD", found[0])

    def test_a_pass_that_found_nothing_is_fine(self):
        self.assertEqual(self.with_discoveries([], {"discovery_sources": 7}), [])

    def test_a_record_holding_only_the_pass_says_it_read_no_nodes(self):
        self.assertEqual(self.with_discoveries([self.GOOD], {"discovery_sources": 7, "nodes_checked": 0}, items=False), [])
        found = self.with_discoveries([self.GOOD], {"discovery_sources": 7}, items=False)
        self.assertEqual(len(found), 1, found)
        self.assertIn("at least one [[item]]", found[0])

    def test_the_export_lists_every_discovery_newest_first_with_its_record(self):
        tree = export.compute.load_tree(ROOT / "data")
        scans, problems, _ = export.export_scans(tree, ROOT / "data" / "scans", ROOT / "data" / "ledger.toml")
        self.assertEqual(problems, [])
        dates = [d["date"] for d in scans["discoveries"]]
        self.assertEqual(dates, sorted(dates, reverse=True))
        self.assertIn("2026-10-27", [d["scan_date"] for d in scans["discoveries"]])
        self.assertIsNotNone(scans["last_discovery_pass"])
        self.assertEqual(scans["counts"]["discoveries"], len(scans["discoveries"]))


if __name__ == "__main__":
    unittest.main()
