#!/usr/bin/env python3
"""The Belt Equation: how much a scan moved the headline, and which steps are high-stakes.

Plain Python, standard library only. Written 2026-10-03 for the article prompts in the weekly
scan (docs/scan-procedure.md, step 3b, ruled by John 2026-10-03):

    python3 scripts/headline.py save FILE      play the tree out and keep the headline in FILE
    python3 scripts/headline.py compare FILE   play it out again and compare with FILE
    python3 scripts/headline.py stakes         the steps worth 10% or more of the headline if
                                               they came true, from the newest saved run

The headline is tier A2 under each of the five longevity scenarios. Both thresholds are read
against the moderate scenario (the 2080 deadline): the baseline number is so small that a few
runs of the dice move it by several per cent of itself, and the moderate one is the first that
is large enough to read a five per cent change from.

`compare` ends with a line starting "BIG MOVER" when the moderate headline moved by 5% of itself
or more, in either direction, and "no big mover" otherwise. `save` and `compare` each take about
twenty seconds; they use the same runs and seed as compute.py, so the difference between them is
the change in the tree and not the dice.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = "moderate"
MOVE_CUTOFF = 0.05    # a scan's change to the headline, as a share of the headline
STAKES_CUTOFF = 0.10  # what a step coming true would add, as a share of the headline


def headline_now() -> dict[str, float]:
    tree = compute.load_tree(ROOT / "data")
    return compute.force_run(tree, {}, compute.DEFAULT_RUNS, 2026, 1.0)


def pct(x: float) -> str:
    return f"{100 * x:6.2f}%"


def save(path: Path) -> int:
    path.write_text(json.dumps(headline_now(), indent=1) + "\n")
    print(f"Headline saved to {path}.")
    return 0


def compare(path: Path) -> int:
    before = json.loads(path.read_text())
    after = headline_now()
    print("The headline (A2), before -> after, and the change as a share of where it was:")
    for key, b in before.items():
        a = after[key]
        share = "" if b == 0 else f"  {100 * (a - b) / b:+.1f}% of itself"
        print(f"  {key:<9} {pct(b)} -> {pct(a)}{share}")
    b, a = before[REFERENCE], after[REFERENCE]
    share = 0.0 if b == 0 else (a - b) / b
    if abs(share) >= MOVE_CUTOFF:
        print(f"BIG MOVER: the {REFERENCE} headline moved {100 * share:+.1f}% of itself "
              f"(cutoff {100 * MOVE_CUTOFF:.0f}%).")
    else:
        print(f"no big mover: the {REFERENCE} headline moved {100 * share:+.1f}% of itself "
              f"(cutoff {100 * MOVE_CUTOFF:.0f}%).")
    return 0


def stakes() -> int:
    snaps = [s for s in compute.load_snapshots(ROOT / "data" / "snapshots") if s.get("worth")]
    if not snaps:
        print("No saved run carries step worths; run `python3 scripts/compute.py run --snapshot` first.")
        return 1
    snap = snaps[-1]
    worth = snap["worth"]
    base = worth["headline"][REFERENCE]
    names = {n["id"]: n["name"] for n in compute.load_tree(ROOT / "data")["nodes"]}
    rows = []
    for nid, w in worth["nodes"].items():
        if not w.get("reaches_headline") or nid not in names:
            continue
        share = w["if_yes"][REFERENCE] / base if base else 0.0
        if share >= STAKES_CUTOFF:
            rows.append((share, nid))
    rows.sort(reverse=True)
    print(f"Steps that would raise the {REFERENCE} headline by {100 * STAKES_CUTOFF:.0f}% of itself "
          f"or more if they came true (saved run {snap['key']}):")
    for share, nid in rows:
        print(f"  {100 * share:+5.0f}%  {nid}  ({names[nid]})")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] in ("save", "compare"):
        return (save if argv[0] == "save" else compare)(Path(argv[1]))
    if argv == ["stakes"]:
        return stakes()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
