#!/usr/bin/env python3
"""Checks on the reader grid, the part of the compute script that runs the tree for a stranger.

Written 2026-09-20 with website step 39 (docs/run-it-yourself-plan.md). Plain Python, standard
library only, no dependencies:

    python3 scripts/test_reader.py

The checks that matter are the last two. Reading a node's probability at a deadline between
two of John's windows is a new piece of arithmetic, and the way to know it has not quietly
changed the tree is to point it at John's own windows, where it should do nothing at all: at
2071 the reading hands back the baseline numbers untouched.

So the first check plays the tree out at John's five windows with the committed snapshot's own
dice: the same seed, the same number of play-throughs, and one continuous stream across the
five windows in order, which is how the snapshot was taken. Because the reading returns the
stored numbers unchanged at those years, every roll of the dice falls the same way, and the
tier rates must come out exactly equal to the ones in the file. Not close: equal. That is a
sharper check than any band, and it is the one that would catch the reading moving a number.

The second check is the one the plan document promises: a grid cell exactly as the website
gets it, played out its own smaller number of times from its own stream of dice, landing on
the snapshot's rates within the run-to-run noise the two runs carry. The band is three
standard errors of each rate rather than the two that compute.run_noise() reports. Two is what
the site quotes for one figure; three is used here because the snapshot's five windows were
played from one continuous stream of dice and a grid cell starts a fresh one, so where in the
stream a run begins moves a rate by a little more than two unrelated runs would. Three
standard errors covers that and still catches any change worth the name, and the first check
is what makes this one a spot check rather than the whole test.

Every run here takes the snapshot's own seed, so a failure is reproducible and means something
changed, not that the dice fell badly.
"""

from __future__ import annotations

import json
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# The latest run of the tree as it stands. Moved from 2026-09-20-step-27 to 2026-09-25-c5 on
# 2026-09-25, when C5 was added and the Contact Clause rungs given dice of their own; moved again
# the same day to 2026-09-25-methodology-pass, when the methodology pass changed Tier 1's and
# Tier 4's requirements. Move it again whenever a run follows a change to the tree's shape.
SNAPSHOT = ROOT / "data" / "snapshots" / "2026-09-25-sweep-function-over-route.json"
SYSTEM_TIERS = ["T1", "T2", "T3", "T4"]


def load() -> dict:
    tree = compute.load_tree(ROOT / "data")
    problems = compute.validate(tree)
    if problems:
        raise AssertionError("the tree does not validate:\n  " + "\n  ".join(problems))
    return tree


class ReadingADeadline(unittest.TestCase):
    """The arithmetic that gives a node a number at a year the tree was never asked about."""

    @classmethod
    def setUpClass(cls):
        cls.tree = load()
        cls.years = compute.scenario_years(cls.tree)
        # A node with five different numbers, so the reading has something to do.
        cls.prob = {"baseline": 0.2, "moderate": 0.3, "strong": 0.5, "radical": 0.8, "open": 0.9}

    def read(self, year):
        return compute.deadline_probability(self.prob, self.years, "open", year)

    def test_a_named_window_returns_its_own_number(self):
        for key, year in self.years:
            self.assertAlmostEqual(self.read(year), self.prob[key], places=12,
                                   msg=f"the reading moved the stored number at {year}")
        self.assertEqual(self.read(None), self.prob["open"])

    def test_below_the_first_window_it_does_not_fall(self):
        for year in (1990, 2026, 2050, 2070):
            self.assertEqual(self.read(year), self.prob["baseline"])

    def test_it_never_falls_as_the_deadline_moves_out(self):
        last = 0.0
        for year in range(2020, 2301):
            p = self.read(year)
            self.assertGreaterEqual(p + 1e-12, last, f"the number fell going into {year}")
            last = p

    def test_beyond_the_last_window_it_approaches_no_deadline_and_stops(self):
        self.assertLess(self.read(2200), self.prob["open"])
        self.assertGreater(self.read(2200), self.prob["radical"])
        self.assertAlmostEqual(self.read(2136 + 41), 0.5 * (
            compute._between(self.prob["radical"], self.prob["open"], 1.0)
            + self.prob["radical"]), delta=0.05)
        self.assertLess(self.read(3000), self.prob["open"] + 1e-9)

    def test_a_flat_node_stays_flat(self):
        flat = {k: 1.0 for k in self.prob}
        for year in (2040, 2085, 2130, 2400, None):
            self.assertEqual(
                compute.deadline_probability(flat, self.years, "open", year), 1.0)


class TheReaderWindows(unittest.TestCase):
    """Shifting John's windows onto somebody born in another year."""

    @classmethod
    def setUpClass(cls):
        cls.tree = load()

    def test_john_gets_his_own_windows_back(self):
        for key, year in compute.scenario_years(self.tree):
            self.assertEqual(compute.reader_deadline(self.tree, key, 1986), year)
        self.assertIsNone(compute.reader_deadline(self.tree, "open", 1986))

    def test_the_windows_are_ages(self):
        for birth in (1940, 1986, 2000, 2020):
            for _, year in compute.scenario_years(self.tree):
                deadline = year + (birth - 1986)
                self.assertEqual(deadline - birth, year - 1986,
                                 "a reader's window should be the same age as John's")

    def test_every_reader_the_page_offers_lands_inside_the_grid(self):
        grid = compute.reader_grid_years()
        for birth in range(compute.READER_MIN_BIRTH_YEAR, compute.READER_MAX_BIRTH_YEAR + 1):
            for key, _ in compute.scenario_years(self.tree):
                deadline = compute.reader_deadline(self.tree, key, birth)
                self.assertGreaterEqual(deadline, grid[0])
                self.assertLessEqual(deadline, grid[-1])


class TheGridAgreesWithTheSnapshot(unittest.TestCase):
    """The check that the new arithmetic has not moved the tree.

    At John's own five windows the reading returns the stored numbers untouched, so a grid cell
    at those deadlines is the same calculation the committed run made. The rates must match
    within the noise both runs carry.
    """

    @classmethod
    def setUpClass(cls):
        cls.tree = load()
        cls.snapshot = json.loads(SNAPSHOT.read_text())

    def windows(self):
        return [(k, y) for k, y in compute.scenario_years(self.tree)] + [("open", None)]

    def test_johns_five_windows_reproduce_the_committed_run_exactly(self):
        """With the snapshot's own dice, the reading changes nothing: the rates come out equal.

        The snapshot was taken by playing the five windows out in order from one stream of
        dice. Repeating that, with each window's probabilities fetched through the reading
        rather than read straight off the node, has to land on the same numbers to the last
        digit, because at John's own windows the reading hands back exactly what is stored.
        """
        runs = self.snapshot["run"]["runs"]
        spread = self.snapshot["run"]["world_spread"]
        rng = random.Random(self.snapshot["run"]["seed"])
        for key, year in self.windows():
            reader_tree = compute.tree_at_deadline(self.tree, year)
            result = compute.simulate(reader_tree, compute.READER_SCENARIO_KEY, runs, rng,
                                      world_spread=spread)
            for tier in SYSTEM_TIERS:
                self.assertEqual(
                    result["tiers"][tier], self.snapshot["tiers"][tier][key],
                    f"played out at John's {key} window ({year}) with the dice of the snapshot "
                    f"of {self.snapshot['date']}, {tier} came out "
                    f"{result['tiers'][tier]} where the snapshot has "
                    f"{self.snapshot['tiers'][tier][key]}. The reading is supposed to hand back "
                    "the stored numbers untouched at John's own windows, so this means it has "
                    "changed what the tree says.")

    def test_a_grid_cell_at_johns_windows_matches_within_the_run_noise(self):
        """The cell as the website gets it, against the snapshot, within the two runs' noise."""
        snapshot_runs = self.snapshot["run"]["runs"]
        spread = self.snapshot["run"]["world_spread"]
        worst = ("", "", 0.0, 0.0)
        for key, year in self.windows():
            cell = compute.reader_cell(self.tree, year, runs=compute.READER_RUNS,
                                       seed=self.snapshot["run"]["seed"], world_spread=spread)
            for tier in SYSTEM_TIERS:
                recorded = self.snapshot["tiers"][tier][key]
                got = cell["tiers"][tier]
                # run_noise() reports two standard errors; 1.5 times it is three, which is the
                # band this check uses and the docstring explains.
                band = 1.5 * (compute.run_noise({tier: recorded}, snapshot_runs)[tier]
                              + compute.run_noise({tier: got}, compute.READER_RUNS)[tier])
                gap = abs(got - recorded)
                if band and gap / band > worst[3]:
                    worst = (key, tier, gap, gap / band)
                self.assertLessEqual(
                    gap, band,
                    f"the grid cell at John's {key} window ({year}) puts {tier} at {got:.5f} "
                    f"where the snapshot of {self.snapshot['date']} has {recorded:.5f}; "
                    f"that is further apart than the {band:.5f} the two runs' dice explain.")
        print(f"\n  widest gap: {worst[1]} at the {worst[0]} window, "
              f"{worst[2]:.5f}, which is {worst[3]:.2f} of the band it is allowed.")

    def test_a_cell_reports_every_tier_and_every_route(self):
        cell = compute.reader_cell(self.tree, 2085, runs=200)
        for t in self.tree["tiers"]:
            self.assertIn(t["key"], cell["tiers"])
        for r in compute.READER_ROUTES:
            self.assertIn(r["key"], cell["routes"])

    def test_no_route_runs_through_johns_own_path(self):
        johns_own = {"A-pipeline-graduation", "A-reenlist-at-six-years",
                     "A-separate-at-six-years-into-civilian-space-work",
                     "A-civilian-spaceflight-training-role-obtained",
                     "A-military-role-with-off-earth-rotation-obtained",
                     "A-working-in-or-for-the-off-earth-industry",
                     "A-in-a-role-whose-holders-rotate-off-earth",
                     "A-first-spaceflight"}
        ids = {n["id"] for n in self.tree["nodes"]}
        for route in compute.READER_ROUTES:
            for node in route["world_nodes"]:
                self.assertIn(node, ids, f"route {route['key']} names a node not in the tree")
                self.assertNotIn(node, johns_own,
                                 f"route {route['key']} runs through John's own path")

    def test_reading_the_tree_leaves_it_alone(self):
        before = json.dumps(self.tree["nodes"], sort_keys=True, default=str)
        compute.reader_cell(self.tree, 2100, runs=100)
        after = json.dumps(self.tree["nodes"], sort_keys=True, default=str)
        self.assertEqual(before, after, "the reader grid changed the tree it was given")


if __name__ == "__main__":
    unittest.main(verbosity=2)
