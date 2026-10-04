#!/usr/bin/env python3
"""The Belt Equation: work out "what could happen next" for runs saved before it was recorded.

Plain Python, standard library only. Written 2026-10-03 with the site's /next/ page.

    python3 scripts/backfill_next_steps.py          write data/snapshots/backfill/next-steps.json

From 2026-10-03 every saved run carries its own `next_steps` (compute.py, take_snapshot). The
seven runs saved before then do not, and a saved run is never rewritten, so this works their
lists out once and keeps them in a file of their own. Each run's list is read from the tree as it
stood in the commit that added the run's file (the run was committed together with the tree it
measured), with the worth and the node rates the run itself saved. Nothing is played out again.
Run it again only if the rule for what counts as "next" changes; a run that already carries its
own list is skipped.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS = ROOT / "data" / "snapshots"
OUT = SNAPSHOTS / "backfill" / "next-steps.json"


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def tree_at(commit: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=BytesIO(git("archive", commit, "data")), mode="r:") as tar:
            tar.extractall(tmp, filter="data")
        return compute.load_tree(Path(tmp) / "data")


def main() -> int:
    runs = {}
    for path in sorted(SNAPSHOTS.glob("*.json")):
        snap = json.loads(path.read_text())
        if "next_steps" in snap or not snap.get("worth"):
            continue
        added = git("log", "--diff-filter=A", "--format=%h", "--", str(path.relative_to(ROOT))).decode().split()
        if not added:
            print(f"{path.name}: not committed yet, skipped")
            continue
        commit = added[-1]
        steps = compute.next_steps(tree_at(commit), snap["worth"], snap["nodes"])
        runs[snap["key"]] = {"tree_commit": commit, "next_steps": steps}
        print(f"{snap['key']}: {len(steps)} steps, tree as of {commit}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "note": "What could happen next, worked out on 2026-10-03 for runs saved before each run "
                "recorded its own list (scripts/backfill_next_steps.py). Ids are as they were at "
                "the time; data/snapshots/renamed-ids.toml maps any that changed.",
        "runs": runs,
    }, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
