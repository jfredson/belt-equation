#!/usr/bin/env python3
"""Checks that the Contact Clause stays beside the equation and is never multiplied into it.

Written 2026-09-25 when rung C5, communion with a machine mind of another perspective, was
added (docs/proposal-contact-clause-null-rule-2026-09-19.md, adopted by John 2026-09-25).
Plain Python, standard library only, no dependencies:

    python3 scripts/test_contact.py

The check that matters is the first. The tree is played out twice from the same seed, once as
it stands and once with C5 taken out, and the headline and every tier rate must come out equal.
Not close: equal. That holds because the rungs roll their own dice (scripts/compute.py,
simulate()), so a rung's presence cannot shift the equation's dice by even one roll, and
because the validator refuses any tree where a tier or a node outside the clause depends on a
rung. The second check is the stronger form of the same claim: C5 held at certain and at
impossible leaves the tiers where they were too. The remaining checks cover the validator rule
and the shape of the two branches the run output and the site show.
"""

from __future__ import annotations

import copy
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RUNS = 4000      # enough play-throughs for every tier to be reached many times; the check is equality
SEED = 2026


def load() -> dict:
    tree = compute.load_tree(ROOT / "data")
    problems = compute.validate(tree)
    if problems:
        raise AssertionError("the tree does not validate:\n  " + "\n  ".join(problems))
    return tree


def play(tree: dict) -> dict:
    """The five scenarios in order from one stream of dice, the way a snapshot is taken."""
    rng = random.Random(SEED)
    joint = dict(compute.chain_gates(tree))
    joint.update(compute.second_number_joint())
    return {s["key"]: compute.simulate(tree, s["key"], RUNS, rng, joint=joint) for s in tree["scenarios"]}


def without(tree: dict, nid: str) -> dict:
    out = copy.deepcopy(tree)
    out["nodes"] = [n for n in out["nodes"] if n["id"] != nid]
    return out


def with_c5_at(tree: dict, p: float) -> dict:
    out = copy.deepcopy(tree)
    for n in out["nodes"]:
        if n["id"] == "C5":
            n["probability"] = {k: p for k in n["probability"]}
    return out


class TheContactClauseIsNeverMultipliedIn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = load()
        cls.with_c5 = play(cls.tree)

    def assertSameEquation(self, other: dict, what: str):
        for key, result in self.with_c5.items():
            self.assertEqual(result["tiers"], other[key]["tiers"],
                             f"{what} moved a tier rate in the {key} scenario")
            self.assertEqual(result["joint"], other[key]["joint"],
                             f"{what} moved a chain link or the second number in the {key} scenario")
            equation = {n: r for n, r in result["nodes"].items() if not n.startswith("C")}
            self.assertEqual(equation, {n: r for n, r in other[key]["nodes"].items() if not n.startswith("C")},
                             f"{what} moved a node outside the Contact Clause in the {key} scenario")

    def test_c5_is_in_the_tree(self):
        c5 = next((n for n in self.tree["nodes"] if n["id"] == "C5"), None)
        self.assertIsNotNone(c5, "rung C5 is not in data/C-contact.toml")
        self.assertEqual(c5["depends_on"], ["C2"])
        self.assertTrue(c5.get("long_shot"))

    def test_the_headline_and_every_tier_are_unchanged_by_c5s_presence(self):
        self.assertSameEquation(play(without(self.tree, "C5")), "taking C5 out")
        headline = compute.HEADLINE_TIER
        for key, result in self.with_c5.items():
            self.assertGreater(result["tiers"][headline], 0.0,
                               f"the headline never happened in the {key} scenario, so the check proved nothing")

    def test_c5_certain_or_impossible_moves_nothing_in_the_equation(self):
        self.assertSameEquation(play(with_c5_at(self.tree, 1.0)), "holding C5 at certain")
        self.assertSameEquation(play(with_c5_at(self.tree, 0.0)), "holding C5 at impossible")

    def test_no_tier_requires_a_rung_and_the_validator_says_so(self):
        for t in self.tree["tiers"]:
            self.assertFalse([r for r in t.get("requires", []) or [] if r.startswith("C")],
                             f"tier {t['key']} requires a Contact Clause rung")
        broken = copy.deepcopy(self.tree)
        broken["tiers"][0].setdefault("requires", []).append("C5")
        self.assertTrue(any("C5" in p for p in compute.validate(broken)),
                        "the validator let a tier require C5")
        broken = copy.deepcopy(self.tree)
        outside = next(n for n in broken["nodes"] if n["factor"] != "C" and n["kind"] == "world")
        outside.setdefault("depends_on", []).append("C5")
        self.assertTrue(any("C5" in p for p in compute.validate(broken)),
                        "the validator let a node outside the clause depend on C5")

    def test_c4_and_c5_are_sibling_branches(self):
        branches = {b["top"]: b["rungs"] for b in compute.contact_branches(self.tree)}
        self.assertEqual(branches, {"C4": ["C3", "C4"], "C5": ["C1", "C2", "C5"]})


if __name__ == "__main__":
    unittest.main(verbosity=2)
