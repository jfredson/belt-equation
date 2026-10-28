#!/usr/bin/env python3
"""Checks for scripts/check_news.py (the news posts; tracker pattern, rule 4.16).

    python3 scripts/test_news.py
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


class NewsPosts(unittest.TestCase):
    """scripts/check_news.py refuses a post that cannot be trusted (tracker pattern, rule 4.16)."""

    RECORDS = {"nodes": [{"id": "a-leaf", "revisions": [{"date": "2026-10-17"}], "resolved_on": None}], "entries": [], "scans": []}
    GOOD = ("---\ntitle: A leaf moves\ndate: 2026-10-18\nkind: rung-reached\nsummary: It moved.\nrecords: [a-leaf]\n"
            "sources:\n  - label: The paper\n    url: https://example.org/paper\n---\n\n## What happened\n\n"
            "On 27 April 2026 the centre [published it](https://example.org/paper).\n")

    def run_check(self, text, name="2026-10-18-a-leaf-moves.md"):
        import check_news
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp); (d / name).write_text(text, encoding="utf-8")
            problems, n = check_news.check(d, self.RECORDS)
        return problems

    def test_a_good_post_passes(self):
        self.assertEqual(self.run_check(self.GOOD), [])

    def test_a_figure_without_a_link_is_refused(self):
        bad = self.GOOD.replace("[published it](https://example.org/paper)", "published it")
        self.assertTrue(any("states a figure with no link" in p for p in self.run_check(bad)))

    def test_a_missing_record_is_refused(self):
        self.assertTrue(any("does not exist" in p for p in self.run_check(self.GOOD.replace("[a-leaf]", "[no-such-leaf]"))))

    def test_a_date_mismatch_is_refused(self):
        self.assertTrue(any("differs from the file name" in p for p in self.run_check(self.GOOD, name="2026-10-01-a-leaf-moves.md")))

    def test_a_record_with_no_change_near_the_date_is_refused(self):
        far = self.GOOD.replace("date: 2026-10-18", "date: 2026-12-30")
        self.assertTrue(any("shows no dated change" in p for p in self.run_check(far, name="2026-12-30-a-leaf-moves.md")))

    def test_no_source_is_refused(self):
        bad = self.GOOD.replace("sources:\n  - label: The paper\n    url: https://example.org/paper\n", "")
        self.assertTrue(any("cites no source" in p for p in self.run_check(bad)))

    def test_the_opener_need_not_name_a_record(self):
        opener = self.GOOD.replace("kind: rung-reached", "kind: start-here").replace("records: [a-leaf]\n", "")
        self.assertEqual(self.run_check(opener, name="2026-10-18-start-here.md"), [])



class MissionNews(unittest.TestCase):
    """Mission news, the eighth kind (tracker pattern rule 4.20, ruled by John 2026-10-21)."""

    MISSIONS = [{"id": "hera", "milestones": [
        {"state": "plan", "start": "2026-11-01", "end": "2026-11-30"},
        {"state": "done", "start": "2026-10-07", "end": "2026-10-07"},
    ]}]
    RECORDS = {"nodes": [], "entries": [], "scans": [], "missions": MISSIONS}
    GOOD = ("---\ntitle: Hera sees its asteroids\ndate: 2026-10-08\nkind: mission-news\nsummary: It saw them.\n"
            "missions: [hera]\nsources:\n  - label: ESA\n    url: https://example.org/esa\n---\n\n"
            "On 7 October Hera [saw Didymos](https://example.org/esa).\n\nThis doesn't change my odds.\n")

    def run_check(self, files):
        import check_news
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for name, text in files.items():
                (d / name).write_text(text, encoding="utf-8")
            problems, n = check_news.check(d, self.RECORDS)
        return problems

    def test_a_good_post_passes(self):
        self.assertEqual(self.run_check({"2026-10-08-hera-sees-its-asteroids.md": self.GOOD}), [])

    def test_no_mission_is_refused(self):
        bad = self.GOOD.replace("missions: [hera]\n", "")
        self.assertTrue(any("names no mission" in p for p in self.run_check({"2026-10-08-hera.md": bad})))

    def test_an_unknown_mission_is_refused(self):
        bad = self.GOOD.replace("[hera]", "[nope]")
        self.assertTrue(any("not on the Missions page" in p for p in self.run_check({"2026-10-08-hera.md": bad})))

    def test_nothing_marked_near_the_date_is_refused(self):
        far = self.GOOD.replace("2026-10-08", "2026-12-20")
        self.assertTrue(any("no milestone marked done" in p for p in self.run_check({"2026-12-20-hera.md": far})))

    def test_a_post_that_does_not_end_on_the_odds_is_refused(self):
        bad = self.GOOD.replace("This doesn't change my odds.", "Next it arrives.")
        self.assertTrue(any("ends on what the event" in p for p in self.run_check({"2026-10-08-hera.md": bad})))

    def test_a_third_post_in_one_week_is_refused(self):
        posts = {f"2026-10-0{d}-hera-{d}.md": self.GOOD.replace("2026-10-08", f"2026-10-0{d}") for d in (6, 7, 8)}
        self.assertTrue(any("the ceiling is 2 a week" in p for p in self.run_check(posts)))

    def test_only_mission_news_names_missions(self):
        bad = self.GOOD.replace("kind: mission-news", "kind: claim").replace("missions: [hera]\n", "missions: [hera]\nrecords: [x]\n")
        self.assertTrue(any("only a mission news post names missions" in p for p in self.run_check({"2026-10-08-hera.md": bad})))


class Discovery(unittest.TestCase):
    """A discovery, the ninth kind (asked for by John 2026-10-27): names no record or mission; ends on the odds."""

    RECORDS = {"nodes": [], "entries": [], "scans": [], "missions": []}
    GOOD = ("---\ntitle: A new dwarf planet candidate\ndate: 2026-10-27\nkind: discovery\nsummary: Found.\n"
            "sources:\n  - label: The release\n    url: https://example.org/release\n---\n\n"
            "On 13 October it was [found](https://example.org/release).\n\nIt moves none of my odds.\n")

    def run_check(self, text, name="2026-10-27-a-find.md"):
        import check_news
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp); (d / name).write_text(text, encoding="utf-8")
            problems, n = check_news.check(d, self.RECORDS)
        return problems

    def test_a_good_post_passes(self):
        self.assertEqual(self.run_check(self.GOOD), [])

    def test_it_need_not_name_a_record(self):
        self.assertFalse(any("names no record" in p for p in self.run_check(self.GOOD)))

    def test_a_post_that_does_not_end_on_the_odds_is_refused(self):
        bad = self.GOOD.replace("It moves none of my odds.", "Next comes the infrared.")
        self.assertTrue(any("a discovery post ends on what the event" in p for p in self.run_check(bad)))

    def test_it_may_not_name_a_mission(self):
        bad = self.GOOD.replace("sources:", "missions: [hera]\nsources:")
        self.assertTrue(any("only a mission news post names missions" in p for p in self.run_check(bad)))


class MissionsFile(unittest.TestCase):
    """scripts/missions.py refuses a missions file that cannot be trusted (rule 4.20)."""

    def base(self):
        return {"checked": "2026-10-21", "mission": [{
            "id": "hera", "name": "Hera", "url": "https://example.org", "operator": "ESA", "group": "asteroids",
            "what": "w", "why": "y", "steps": [], "step_note": "none", "checked": "2026-10-21",
            "milestone": [{"what": "Arrives", "when": "2026-11", "state": "plan",
                           "sources": [{"label": "ESA", "url": "https://example.org"}]}]}]}

    def problems(self, data):
        import missions
        return missions.validate(data, {"a-step"})[0]

    def test_the_real_file_passes(self):
        import missions, compute
        root = Path(__file__).resolve().parent.parent
        tree = compute.load_tree(root / "data")
        data = missions.load(root / "data" / "missions.toml")
        self.assertEqual(missions.validate(data, {n["id"] for n in tree["nodes"]})[0], [])

    def test_a_good_file_passes(self):
        self.assertEqual(self.problems(self.base()), [])

    def test_a_milestone_with_no_source_is_refused(self):
        d = self.base(); d["mission"][0]["milestone"][0]["sources"] = []
        self.assertTrue(any("cites no source" in p for p in self.problems(d)))

    def test_a_sharpened_or_unknown_date_form_is_refused(self):
        d = self.base(); d["mission"][0]["milestone"][0]["when"] = "November-ish 2026"
        self.assertTrue(any("not in a form" in p for p in self.problems(d)))

    def test_done_in_the_future_is_refused(self):
        d = self.base(); d["mission"][0]["milestone"][0]["state"] = "done"
        self.assertTrue(any("dated after the file was checked" in p for p in self.problems(d)))

    def test_a_moved_date_keeps_its_old_date_and_day(self):
        d = self.base(); d["mission"][0]["milestone"][0]["was"] = "2026-10"
        self.assertTrue(any("needs both `was`" in p for p in self.problems(d)))

    def test_an_unknown_step_is_refused(self):
        d = self.base(); d["mission"][0]["steps"] = ["no-such-step"]
        self.assertTrue(any("not in the tree" in p for p in self.problems(d)))

    def test_a_span_is_drawn_across_the_whole_span(self):
        import missions
        r = missions.resolve_date({"from": "late 2028", "to": "early 2029"})
        self.assertEqual((r["start"].isoformat(), r["end"].isoformat(), r["span"]), ("2028-09-01", "2029-04-30", True))


if __name__ == "__main__":
    unittest.main()
