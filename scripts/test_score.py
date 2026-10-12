#!/usr/bin/env python3
"""Checks on the calibration score (methodology.md, "The calibration score"; built 2026-10-12).

Plain Python, standard library only, no dependencies; runs in well under a second:

    python3 scripts/test_score.py

The rule being checked: a resolved step is scored only if its record holds a probability dated
before its resolution date, either as its current number (under `estimated_on`) or as a
probability revision's new value (under the revision's date); the number scored is the latest
such one, under the baseline scenario; the score is the Brier score, averaged over the year's
scored steps and over every scored step ever. A small made-up tree stands in for the real one,
so the checks say what the rule does in each case rather than what the tree happens to hold.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compute  # noqa: E402

SCENARIOS = [{"key": k, "window_year": y} for k, y in
             (("baseline", 2071), ("moderate", 2080), ("strong", 2095), ("radical", 2136), ("open", None))]


def flat(p: float) -> dict[str, float]:
    return {s["key"]: p for s in SCENARIOS}


def text(p: float) -> str:
    return " / ".join(f"{p:.2f}" for _ in SCENARIOS)


def node(id: str, status: str, resolved_on: str | None = None, probability: dict | None = None,
         estimated_on: str | None = None, revisions: list | None = None) -> dict:
    n = {"id": id, "name": id.replace("-", " "), "factor": id[0], "kind": "world", "status": status}
    if resolved_on:
        n["resolved_on"] = resolved_on
    if probability is not None:
        n["probability"] = probability
    if estimated_on:
        n["estimated_on"] = estimated_on
    if revisions:
        n["revisions"] = revisions
    return n


def tree(*nodes: dict) -> dict:
    return {"scenarios": SCENARIOS, "tiers": [], "nodes": list(nodes)}


def snapshot(key: str, date: str, baseline: float, review_status: str = "reviewed") -> dict:
    return {"key": key, "date": date, "review_status": review_status, "headline_tier": "A2",
            "scenarios": SCENARIOS, "tiers": {"A2": flat(baseline)}, "run": {}, "nodes": {}}


class ScoringRule(unittest.TestCase):

    def rows(self, *nodes: dict) -> dict[str, dict]:
        return {r["id"]: r for r in compute.scored_resolutions(tree(*nodes))}

    def test_a_step_resolved_before_its_first_estimate_is_not_scored(self):
        r = self.rows(node("W-early", "resolved-yes", "2026-06-09"))["W-early"]
        self.assertFalse(r["scored"])
        self.assertIn("no probability on the record before 2026-06-09", r["reason"])

    def test_a_step_estimated_then_resolved_is_scored_on_its_current_number(self):
        r = self.rows(node("L-yes", "resolved-yes", "2026-12-01", flat(0.70), "2026-09-20"))["L-yes"]
        self.assertTrue(r["scored"])
        self.assertEqual(r["recorded_on"], "2026-09-20")
        self.assertAlmostEqual(r["brier"], (0.70 - 1.0) ** 2)

    def test_a_step_that_did_not_happen_scores_against_zero(self):
        r = self.rows(node("R-no", "resolved-no", "2026-12-01", flat(0.30), "2026-09-20"))["R-no"]
        self.assertTrue(r["scored"])
        self.assertAlmostEqual(r["brier"], 0.30 ** 2)

    def test_the_number_in_force_at_resolution_is_the_latest_dated_before_it(self):
        revisions = [{"date": "2026-10-15", "field": "probability", "old": text(0.70), "new": text(0.90),
                      "why": "[scan 2026-10-15] moved up"}]
        n = node("E-moved", "resolved-yes", "2026-11-01", flat(0.90), "2026-10-15", revisions)
        r = self.rows(n)["E-moved"]
        self.assertTrue(r["scored"])
        self.assertEqual(r["recorded_on"], "2026-10-15")
        self.assertAlmostEqual(r["brier"], (0.90 - 1.0) ** 2)

    def test_a_revision_dated_on_the_resolution_day_does_not_count_as_before_it(self):
        revisions = [{"date": "2026-11-01", "field": "probability", "old": text(0.70), "new": text(0.90),
                      "why": "same day"}]
        n = node("E-same-day", "resolved-yes", "2026-11-01", flat(0.90), "2026-11-01", revisions)
        r = self.rows(n)["E-same-day"]
        self.assertFalse(r["scored"])
        self.assertIn("earliest dated probability, 2026-11-01, is after it resolved", r["reason"])

    def test_a_re_estimate_after_the_world_date_leaves_the_step_unscored(self):
        # The number that was in force when it happened is the revision's old value, which the
        # record does not date; the rule is mechanical, so the step is listed as unscored with
        # that reason rather than scored on a guess.
        revisions = [{"date": "2026-10-20", "field": "probability", "old": text(0.50), "new": text(0.60),
                      "why": "[scan 2026-10-20] moved before the resolution was caught"}]
        n = node("B-late", "resolved-yes", "2026-10-01", flat(0.60), "2026-10-20", revisions)
        r = self.rows(n)["B-late"]
        self.assertFalse(r["scored"])
        self.assertIn("2026-10-20", r["reason"])

    def test_superseded_and_open_steps_are_not_rows(self):
        rows = self.rows(node("D-old", "superseded"), node("D-open", "open", probability=flat(0.5), estimated_on="2026-09-20"))
        self.assertEqual(rows, {})

    def test_the_year_and_cumulative_scores_average_only_scored_steps(self):
        t = tree(node("W-early", "resolved-yes", "2025-06-09"),
                 node("L-yes", "resolved-yes", "2026-12-01", flat(0.70), "2026-09-20"),
                 node("R-no", "resolved-no", "2026-12-02", flat(0.30), "2026-09-20"),
                 node("M-last-year", "resolved-yes", "2025-12-31", flat(0.80), "2025-01-01"))
        cal = compute.calibration(t, 2026)
        self.assertEqual([r["id"] for r in cal["rows_in_year"]], ["L-yes", "R-no"])
        self.assertAlmostEqual(cal["year_score"]["brier"], (0.09 + 0.09) / 2)
        self.assertEqual(cal["year_score"], {"count": 2, "unscored": 0, "brier": cal["year_score"]["brier"]})
        self.assertAlmostEqual(cal["cumulative_score"]["brier"], (0.09 + 0.09 + 0.04) / 3)
        self.assertEqual(cal["cumulative_score"]["count"], 3)
        self.assertEqual(cal["cumulative_score"]["unscored"], 1)

    def test_a_year_with_nothing_scored_says_so(self):
        cal = compute.calibration(tree(node("W-early", "resolved-yes", "2026-06-09")), 2026)
        self.assertIsNone(cal["year_score"]["brier"])
        self.assertEqual(cal["year_score"]["unscored"], 1)


class HeadlineMovement(unittest.TestCase):

    def test_from_the_last_run_of_the_year_before_when_there_is_one(self):
        snaps = [snapshot("2025-12-20-x", "2025-12-20", 0.004), snapshot("2026-03-01-x", "2026-03-01", 0.005),
                 snapshot("2026-10-11-scan", "2026-10-11", 0.0047)]
        m = compute.headline_movement(snaps, 2026)
        self.assertEqual((m["from"]["key"], m["to"]["key"]), ("2025-12-20-x", "2026-10-11-scan"))
        self.assertTrue(m["from_previous_year"])
        self.assertAlmostEqual(m["to"]["headline"]["baseline"] - m["from"]["headline"]["baseline"], 0.0007)

    def test_from_the_years_first_run_otherwise(self):
        snaps = [snapshot("2026-03-01-x", "2026-03-01", 0.005), snapshot("2026-10-11-scan", "2026-10-11", 0.0047)]
        m = compute.headline_movement(snaps, 2026)
        self.assertEqual(m["from"]["key"], "2026-03-01-x")
        self.assertFalse(m["from_previous_year"])

    def test_pre_review_runs_are_left_out(self):
        snaps = [snapshot("2026-09-19-first-run", "2026-09-19", 0.0, "pre-review"),
                 snapshot("2026-09-20-step-27", "2026-09-20", 0.0047), snapshot("2026-10-11-scan", "2026-10-11", 0.0046)]
        self.assertEqual(compute.headline_movement(snaps, 2026)["from"]["key"], "2026-09-20-step-27")

    def test_a_year_without_a_run_is_none(self):
        self.assertIsNone(compute.headline_movement([snapshot("2026-10-11-scan", "2026-10-11", 0.0046)], 2027))


class ReportText(unittest.TestCase):

    def test_the_report_names_both_scores_and_the_unscored_reason(self):
        t = tree(node("W-early", "resolved-yes", "2026-06-09"),
                 node("L-yes", "resolved-yes", "2026-12-01", flat(0.70), "2026-09-20"))
        out = compute.report_score(t, [snapshot("2026-10-11-scan", "2026-10-11", 0.0046)], 2026)
        self.assertIn("Brier score for 2026: 0.0900 over 1 scored step(s), 1 unscored", out)
        self.assertIn("Cumulative Brier score, every year: 0.0900 over 1 scored step(s), 1 unscored", out)
        self.assertIn("not scored: no probability on the record before 2026-06-09", out)
        self.assertIn("on the record since 2026-09-20: 0.70 under the baseline scenario; Brier 0.0900", out)
        self.assertIn("reviewed runs only", out)

    def test_the_real_tree_scores_without_error(self):
        t = compute.load_tree(compute.ROOT / "data")
        out = compute.report_score(t, compute.load_snapshots(compute.ROOT / "data" / "snapshots"), 2026)
        self.assertIn("Calibration score for 2026", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
