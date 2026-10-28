#!/usr/bin/env python3
"""Checks on data/headline.json, the small file the family's Projects page reads (added 2026-10-17).

Plain Python, standard library only:

    python3 scripts/test_headline.py

The file is made from the newest snapshot in data/snapshots/ and the newest scan record in
data/scans/, and plays nothing out, so the checks are quick. They fail, in plain words, when the
committed file is missing, names a snapshot that is not the newest, carries numbers that are not
that snapshot's, or gives a last-reading date that is not the newest scan's. That is the
failure to catch: a scan that moved something, took a snapshot, and forgot to publish the file
(scripts/publish.py writes it on every run). Since 2026-10-17 they also check that the export's
copy for the site (site/public/data/headline.json, served at /data/headline.json) is the file.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute  # noqa: E402
import export  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def copy_of_data(tmp: str) -> Path:
    """A scratch copy of data/ without the folders the headline file does not read."""
    dst = Path(tmp) / "data"
    shutil.copytree(DATA, dst, ignore=shutil.ignore_patterns("attribution", "story"))
    return dst


class CommittedHeadlineFile(unittest.TestCase):
    def test_exists_and_is_current(self):
        problems = compute.headline_file_problems(DATA, DATA / "snapshots")
        self.assertEqual(problems, [], "\n".join(problems))

    def test_carries_what_the_projects_page_reads(self):
        h = json.loads((DATA / "headline.json").read_text())
        for key in ("computed_on", "last_reading", "snapshot", "method", "headline", "by_scenario", "tiers"):
            self.assertIn(key, h)
        self.assertEqual(h["headline"]["tier"], compute.HEADLINE_TIER)
        self.assertEqual(h["headline"]["chance"], h["tiers"][compute.HEADLINE_TIER][h["headline"]["scenario"]])
        self.assertTrue(h["method"]["status"])

    def test_agrees_with_the_snapshot_the_ledger_names_last(self):
        """The Projects page used to read the ledger's last snapshot; the two routes must agree."""
        ledger = (DATA / "ledger.toml").read_text()
        last = re.findall(r'^snapshot\s*=\s*"([^"]+)"', ledger, re.M)[-1]
        snap = json.loads((DATA / "snapshots" / f"{last}.json").read_text())
        h = json.loads((DATA / "headline.json").read_text())
        self.assertEqual(h["headline"]["chance"], snap["tiers"][compute.HEADLINE_TIER]["baseline"])


class ServedWithTheSite(unittest.TestCase):
    """The export copies data/headline.json to site/public/data/ so the site serves it at
    /data/headline.json (2026-10-17). The copy is the file, byte for byte; a missing source is
    reported and skipped rather than stopping the build."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.data = copy_of_data(self._tmp.name)
        self.served = Path(self._tmp.name) / "public" / "data" / "headline.json"

    def test_the_served_copy_is_the_committed_file(self):
        self.assertTrue(export.serve_headline_file(self.data, self.data / "snapshots", self.served))
        self.assertEqual(self.served.read_bytes(), (DATA / "headline.json").read_bytes())

    def test_a_missing_source_is_skipped_not_fatal(self):
        (self.data / "headline.json").unlink()
        self.assertFalse(export.serve_headline_file(self.data, self.data / "snapshots", self.served))
        self.assertFalse(self.served.exists())


class StaleOrMissingIsRefused(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.data = copy_of_data(self._tmp.name)
        self.snaps = self.data / "snapshots"

    def test_a_missing_file_is_named(self):
        (self.data / "headline.json").unlink()
        problems = compute.headline_file_problems(self.data, self.snaps)
        self.assertTrue(any("missing" in p for p in problems), problems)

    def test_writing_it_twice_changes_nothing(self):
        compute.write_headline_file(self.data, self.snaps)
        first = (self.data / "headline.json").read_bytes()
        compute.write_headline_file(self.data, self.snaps)
        self.assertEqual(first, (self.data / "headline.json").read_bytes())
        self.assertEqual(first, (DATA / "headline.json").read_bytes())

    def test_a_newer_scan_makes_the_file_stale(self):
        scans = self.data / "scans"
        # The newest record that read the tree: a record holding only the discovery pass
        # (nodes_checked = 0) does not count as a reading, so it is not the one copied here.
        newest = [p for p in sorted(scans.glob("*.toml")) if "nodes_checked = 0" not in p.read_text()][-1]
        text = newest.read_text().replace(newest.stem, "2099-01-04", 1)
        (scans / "2099-01-04.toml").write_text(text)
        problems = compute.headline_file_problems(self.data, self.snaps)
        self.assertTrue(any("last_reading" in p for p in problems), problems)
        compute.write_headline_file(self.data, self.snaps)
        self.assertEqual(compute.headline_file_problems(self.data, self.snaps), [])

    def test_a_newer_snapshot_makes_the_file_stale(self):
        newest = sorted(self.snaps.glob("*.json"))[-1]
        snap = json.loads(newest.read_text())
        snap["key"], snap["date"] = "2099-01-04-scan", "2099-01-04"
        snap["tiers"][compute.HEADLINE_TIER]["baseline"] = 0.5
        (self.snaps / "2099-01-04-scan.json").write_text(json.dumps(snap))
        problems = compute.headline_file_problems(self.data, self.snaps)
        self.assertTrue(any("snapshot" in p for p in problems), problems)

    def test_doctored_numbers_are_caught_even_when_the_dates_agree(self):
        path = self.data / "headline.json"
        h = json.loads(path.read_text())
        h["headline"]["chance"] = 0.5
        path.write_text(json.dumps(h))
        problems = compute.headline_file_problems(self.data, self.snaps)
        self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
