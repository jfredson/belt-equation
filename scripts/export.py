#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ and the changelog into JSON for the website.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, snapshots.json
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else
    python3 scripts/export.py --data DIR       read a different data folder (for tests)

The tree is read with the same loader and validator as compute.py, so the site can never show
a tree that fails the schema: if validation fails, nothing is written and the build stops.
The site (site/) reads the JSON at build time. Nothing in the browser touches TOML.

What the JSON holds, beyond a copy of each record:
- each node's dependencies resolved to names, the nodes that depend on it, and the tiers
  that require it directly (tier membership lives only in tiers.toml; this is the derived view);
- the changelog, split into dated days and their bullet lines;
- the headline numbers when the tree is complete enough for compute.py to run, and a plain
  reason when it is not (website step 23 puts them on the page);
- the committed run snapshots in data/snapshots/, as the series the history charts are drawn
  from and the difference between the last two runs (ledger step 28).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import compute  # noqa: E402  (the loader and validator, shared on purpose)

# The eight factors and the Contact Clause, in equation order, with the one-line meanings
# from README.md. The slug is the folder each factor gets on the site.
FACTORS = [
    {"letter": "W", "slug": "window", "name": "Window",
     "meaning": "That I am alive on the date in question."},
    {"letter": "L", "slug": "launch", "name": "Launch",
     "meaning": "That the cost of putting mass into orbit falls below the threshold that makes everything else affordable."},
    {"letter": "E", "slug": "energy", "name": "Energy",
     "meaning": "That cheap, abundant power exists off Earth, from fusion or an equivalent."},
    {"letter": "D", "slug": "drive", "name": "Drive",
     "meaning": "That propulsion puts the solar system within reach on human timescales."},
    {"letter": "B", "slug": "biology", "name": "Biology",
     "meaning": "That humans can live, and eventually reproduce, in partial gravity and deep-space radiation."},
    {"letter": "M", "slug": "motive", "name": "Motive",
     "meaning": "That there is an economic reason for large numbers of people to be out there."},
    {"letter": "R", "slug": "regime", "name": "Regime",
     "meaning": "That the political and legal conditions let a multi-decade build survive elections, downturns, and wars."},
    {"letter": "A", "slug": "access", "name": "Access",
     "meaning": "That I personally have a pathway in, given my training, health, and career."},
    {"letter": "C", "slug": "contact", "name": "Contact Clause",
     "meaning": "The dream underneath the project, published beside the equation and never multiplied into it."},
]
SLUG_BY_LETTER = {f["letter"]: f["slug"] for f in FACTORS}

DATE_HEADER = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")


# ------------------------------------------------------------------ helpers


def one_paragraph(text) -> str:
    """Collapse a multi-line TOML string into one line of ordinary spacing."""
    if text is None:
        return ""
    return " ".join(str(text).split())


# Three helpers moved into compute.py on 2026-09-19 (ledger step 28) so that the snapshot
# writer and this export share one copy of each rather than two that can drift.
plain = compute.plain
git_commit = compute.git_commit
chain_gates = compute.chain_gates


# --------------------------------------------------------------- the tree


def export_tree(tree: dict) -> dict:
    nodes = tree["nodes"]
    tiers = tree["tiers"]
    scenarios = tree["scenarios"]
    by_id = {n["id"]: n for n in nodes}
    tier_keys = {t["key"] for t in tiers}

    def ref(nid: str) -> dict:
        n = by_id[nid]
        return {"id": nid, "name": n["name"], "factor": n["factor"], "factor_slug": SLUG_BY_LETTER[n["factor"]]}

    # Derived views: who depends on whom, and which tiers require which nodes directly.
    dependents: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        for d in n.get("depends_on", []) or []:
            dependents[d].append(n["id"])
        for group in n.get("depends_on_any", []) or []:
            for d in group:
                dependents[d].append(n["id"])
    feeds: dict[str, list[str]] = defaultdict(list)
    for t in tiers:
        for r in t.get("requires", []) or []:
            if r not in tier_keys:
                feeds[r].append(t["key"])

    out_nodes = []
    for n in nodes:
        out_nodes.append({
            "id": n["id"],
            "name": n["name"],
            "factor": n["factor"],
            "factor_slug": SLUG_BY_LETTER[n["factor"]],
            "kind": n["kind"],
            "description": one_paragraph(n.get("description")),
            "resolution": one_paragraph(n.get("resolution")),
            "source": one_paragraph(n.get("source")),
            "horizon": n["horizon"],
            "status": n["status"],
            "long_shot": bool(n.get("long_shot")),
            "mechanism": one_paragraph(n.get("mechanism")) or None,
            "breaking_point": one_paragraph(n.get("breaking_point")) or None,
            "depends_on": [ref(d) for d in (n.get("depends_on", []) or [])],
            "depends_on_any": [[ref(d) for d in group] for group in (n.get("depends_on_any", []) or [])],
            "needed_by": [ref(d) for d in sorted(set(dependents[n["id"]]))],
            "feeds_tiers": feeds[n["id"]],
            "choice_group": n.get("choice_group"),
            "current_plan": bool(n.get("current_plan")) if n["kind"] == "choice" else None,
            "probability": plain(n.get("probability")),
            "estimated_on": plain(n.get("estimated_on")),
            "rationale": one_paragraph(n.get("rationale")) or None,
            "resolved_on": plain(n.get("resolved_on")),
            "resolved_by": one_paragraph(n.get("resolved_by")) or None,
            "superseded_by": n.get("superseded_by"),
            "revisions": plain(n.get("revisions", []) or []),
            "verify": list(n.get("verify", []) or []),
            "notes": one_paragraph(n.get("notes")) or None,
            "file": n["_file"],
            "path": f"/tree/{SLUG_BY_LETTER[n['factor']]}/{n['id']}/",
        })

    out_tiers = []
    for t in tiers:
        reqs = []
        for r in t.get("requires", []) or []:
            if r in tier_keys:
                other = next(x for x in tiers if x["key"] == r)
                reqs.append({"kind": "tier", "key": r, "name": other["name"]})
            else:
                reqs.append({"kind": "node", **ref(r)})
        out_tiers.append({
            "key": t["key"], "name": t["name"], "group": t["group"],
            "definition": one_paragraph(t.get("definition")), "requires": reqs,
        })

    out_factors = []
    for f in FACTORS:
        mine = [n for n in out_nodes if n["factor"] == f["letter"]]
        out_factors.append({
            **f,
            "path": f"/tree/{f['slug']}/",
            "node_count": len(mine),
            "with_probability": sum(1 for n in mine if n["probability"]),
            "resolved": sum(1 for n in mine if n["status"].startswith("resolved")),
        })

    counts = {
        "nodes": len(out_nodes),
        "with_probability": sum(1 for n in out_nodes if n["probability"]),
        "open_world_without_probability": len(compute.missing_probabilities(tree)),
        "resolved": sum(1 for n in out_nodes if n["status"].startswith("resolved")),
        "leaves": sum(1 for n in out_nodes if n["horizon"] == "leaf"),
        "long_shots": sum(1 for n in out_nodes if n["long_shot"]),
        "choice_points": sum(1 for n in out_nodes if n["kind"] == "choice"),
    }

    return {
        "exported_on": dt.date.today().isoformat(),
        "commit": git_commit(),
        "headline_tier": compute.HEADLINE_TIER,
        "scenarios": [plain(s) for s in scenarios],
        "factors": out_factors,
        "tiers": out_tiers,
        "nodes": out_nodes,
        "counts": counts,
        "numbers": export_numbers(tree),
    }


# Shown beside the headline until the outside-model review (roadmap step 27) is complete. Set to
# an empty string when the rulings have landed, and the label disappears.
NUMBERS_REVIEW_STATUS = ("First pass, 2026-09-19. Under review by outside models before publication "
                         "(roadmap step 27); every number may move.")


def export_numbers(tree: dict, runs: int = 20000, seed: int = 2026) -> dict:
    """The compute script's results when the tree is complete, or a plain reason when not."""
    missing = compute.missing_probabilities(tree)
    if missing:
        return {
            "available": False,
            "reason": (f"{len(missing)} open world node(s) have no probability yet, so the compute "
                       "script refuses to report numbers. They arrive at roadmap step 9."),
            "missing": missing,
        }
    rng = random.Random(seed)
    keys = [s["key"] for s in tree["scenarios"]]
    chain_nodes = chain_gates(tree)
    results = {k: compute.simulate(tree, k, runs, rng, joint=chain_nodes) for k in keys}
    return {
        "available": True,
        "runs": runs,
        "seed": seed,
        "computed_on": dt.date.today().isoformat(),
        "review_status": NUMBERS_REVIEW_STATUS,
        "tiers": {t["key"]: {k: results[k]["tiers"][t["key"]] for k in keys} for t in tree["tiers"]},
        "nodes": {n["id"]: {k: results[k]["nodes"][n["id"]] for k in keys} for n in tree["nodes"]},
        "chain": {f: {k: results[k]["joint"][f] for k in keys} for f in chain_nodes},
        "chain_nodes": chain_nodes,
    }


# ------------------------------------------------------------ the snapshots


def export_snapshots(folder: Path) -> dict:
    """The committed runs in data/snapshots/, turned into what the pages need.

    Each snapshot is the complete output of one run (scripts/compute.py, ledger step 28). The
    site never recomputes history: the chart on the ledger page, the gate-rate chart on each
    factor page and the "since the last run" arrows on the home page all read this and nothing
    else. The per-node table of every past run stays in the repository rather than the site's
    JSON, which would grow without limit; only the latest run carries its full node table."""
    snapshots = compute.load_snapshots(folder)
    summaries = []
    for s in snapshots:
        summaries.append({k: s.get(k) for k in (
            "key", "date", "label", "note", "review_status", "headline_tier",
            "run", "tiers", "chain", "chain_nodes", "contact", "decisions",
        )})

    def series(pick) -> dict:
        """One point per snapshot, oldest first, for whatever `pick` reads off a snapshot."""
        out: dict[str, list[dict]] = {}
        for s in snapshots:
            for scenario, value in (pick(s) or {}).items():
                out.setdefault(scenario, []).append({"key": s["key"], "date": s["date"], "value": value})
        return out

    tier_keys = sorted({k for s in snapshots for k in s.get("tiers", {})})
    chain_keys = sorted({k for s in snapshots for k in s.get("chain", {})})
    latest = snapshots[-1] if snapshots else None
    previous = snapshots[-2] if len(snapshots) > 1 else None

    def difference(field: str, key: str) -> dict:
        """How far one number moved between the last two runs, per scenario."""
        now = (latest or {}).get(field, {}).get(key, {})
        before = (previous or {}).get(field, {}).get(key, {})
        return {s: round(now[s] - before[s], 6) for s in now if s in before}

    change = None
    if latest and previous:
        change = {
            "from": previous["key"], "from_date": previous["date"],
            "to": latest["key"], "to_date": latest["date"],
            "tiers": {k: difference("tiers", k) for k in tier_keys},
            "chain": {k: difference("chain", k) for k in chain_keys},
        }

    return {
        "count": len(snapshots),
        "headline_tier": compute.HEADLINE_TIER,
        "latest_key": latest["key"] if latest else None,
        "snapshots": summaries,
        "latest": latest,
        "series": {
            "tiers": {k: series(lambda s, k=k: s.get("tiers", {}).get(k)) for k in tier_keys},
            "chain": {k: series(lambda s, k=k: s.get("chain", {}).get(k)) for k in chain_keys},
        },
        "change": change,
    }


# ----------------------------------------------------------- the changelog


def export_changelog(path: Path) -> dict:
    """Split CHANGELOG.md into its dated days, each a list of bullet lines (newest first)."""
    days: list[dict] = []
    intro: list[str] = []
    current: dict | None = None
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        m = DATE_HEADER.match(line)
        if m:
            current = {"date": m.group(1), "items": []}
            days.append(current)
            continue
        if current is None:
            if line and not line.startswith("# "):
                intro.append(line)
            continue
        if line.startswith("- "):
            current["items"].append(line[2:].strip())
        elif line.strip() and current["items"]:
            current["items"][-1] += " " + line.strip()
    return {"source": path.name, "intro": " ".join(intro), "days": days}


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    parser.add_argument("--changelog", type=Path, default=ROOT / "CHANGELOG.md")
    parser.add_argument("--snapshots", type=Path, default=ROOT / "data" / "snapshots")
    parser.add_argument("--out", type=Path, default=ROOT / "site" / "src" / "data")
    parser.add_argument("--check", action="store_true", help="validate and count, write nothing")
    args = parser.parse_args(argv)

    try:
        tree = compute.load_tree(args.data)
        problems = compute.validate(tree)
        if problems:
            print(f"Nothing exported: the tree in {args.data} breaks the schema in {len(problems)} place(s):")
            for p in problems:
                print("  -", p)
            return 1
        exported = export_tree(tree)
        changelog = export_changelog(args.changelog)
        snapshots = export_snapshots(args.snapshots)
    except (compute.TreeError, OSError) as e:
        print(f"Nothing exported: {e}")
        return 1

    c = exported["counts"]
    summary = (f"{c['nodes']} nodes ({c['with_probability']} with probabilities, {c['resolved']} resolved), "
               f"{len(exported['tiers'])} tiers, {len(exported['scenarios'])} scenarios, "
               f"{len(changelog['days'])} changelog day(s), {snapshots['count']} snapshot(s)")
    if args.check:
        print(f"The tree validates. Export would write: {summary}.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "tree.json").write_text(json.dumps(exported, indent=2, ensure_ascii=False) + "\n")
    (args.out / "changelog.json").write_text(json.dumps(changelog, indent=2, ensure_ascii=False) + "\n")
    (args.out / "snapshots.json").write_text(json.dumps(snapshots, indent=2, ensure_ascii=False) + "\n")
    print(f"Exported {summary} to {args.out}.")
    if not exported["numbers"]["available"]:
        print("Headline numbers not exported: " + exported["numbers"]["reason"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
