#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ into headline numbers.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/compute.py validate            check the tree against docs/node-schema.md
    python3 scripts/compute.py shape               print the tree's shape (counts, tiers, leaves)
    python3 scripts/compute.py run [--runs N]      simulate the tree once per longevity scenario
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time
    python3 scripts/compute.py --data DIR ...      use a different data folder (for tests)

What "run" does: for each scenario, it plays the tree out many thousands of times. In each
play-through, nodes are visited in dependency order. A world node whose dependencies all came
true comes true with its probability for that scenario; otherwise it stays false. Nodes already
resolved in the real world are fixed at their outcome. Choice points are never sampled: each
choice group is set to its current-plan option. A tier is reached when everything it requires
came true. The number reported for a tier is the fraction of play-throughs that reached it.
Contact Clause nodes are reported in their own section and never feed a tier.

"compare" repeats "run" for each option in each choice group, one group at a time, and reports
how far each option moves the headline (A2) from the current plan.

The script refuses to report numbers until every open world node has a probability for every
scenario, but "validate" and "shape" work on a tree with no numbers at all.
"""

from __future__ import annotations

import argparse
import random
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

FACTORS = ["W", "L", "E", "D", "B", "M", "R", "A", "C"]
KINDS = {"world", "choice"}
HORIZONS = {"leaf", "mid", "root"}
STATUSES = {"open", "resolved-yes", "resolved-no", "superseded"}
REQUIRED = ["id", "name", "factor", "kind", "description", "resolution", "source", "horizon", "status"]
HEADLINE_TIER = "A2"


class TreeError(Exception):
    """Raised with a plain-language list of everything wrong with the tree."""


# ---------------------------------------------------------------- loading


def load_tree(data_dir: Path) -> dict:
    """Read scenarios, tiers and every factor file. Returns a dict with plain lists."""
    problems = []

    def read(path: Path) -> dict:
        try:
            return tomllib.loads(path.read_text())
        except tomllib.TOMLDecodeError as e:
            problems.append(f"{path.name}: cannot be read as TOML: {e}")
            return {}

    scen_path = data_dir / "scenarios.toml"
    tier_path = data_dir / "tiers.toml"
    for p in (scen_path, tier_path):
        if not p.exists():
            problems.append(f"{p.name} is missing from {data_dir}")
    if problems:
        raise TreeError("\n".join(problems))

    scenarios = read(scen_path).get("scenario", [])
    tiers_raw = read(tier_path)
    tiers = [dict(t, group="system") for t in tiers_raw.get("system_tier", [])]
    tiers += [dict(t, group="access") for t in tiers_raw.get("access_tier", [])]

    nodes = []
    for path in sorted(data_dir.glob("*.toml")):
        if path.name in ("scenarios.toml", "tiers.toml"):
            continue
        letter = path.name.split("-", 1)[0]
        if letter not in FACTORS:
            problems.append(f"{path.name}: file name must start with a factor letter and a dash")
            continue
        for n in read(path).get("node", []):
            n = dict(n)
            n["_file"] = path.name
            n["_file_factor"] = letter
            nodes.append(n)

    if problems:
        raise TreeError("\n".join(problems))
    return {"scenarios": scenarios, "tiers": tiers, "nodes": nodes}


# ------------------------------------------------------------- validating


def validate(tree: dict) -> list[str]:
    """Return a list of problems, empty when the tree follows the schema."""
    problems: list[str] = []
    scenarios = tree["scenarios"]
    tiers = tree["tiers"]
    nodes = tree["nodes"]

    scen_keys = [s.get("key") for s in scenarios]
    if not scen_keys or any(not k for k in scen_keys):
        problems.append("scenarios.toml: every scenario needs a key")
    if len(set(scen_keys)) != len(scen_keys):
        problems.append("scenarios.toml: scenario keys must be unique")

    tier_keys = [t.get("key") for t in tiers]
    if len(set(tier_keys)) != len(tier_keys):
        problems.append("tiers.toml: tier keys must be unique")

    # Rule 1 and 2: required fields, allowed values, unique ids.
    ids: dict[str, dict] = {}
    for n in nodes:
        where = f"{n['_file']} node {n.get('id', '(no id)')}"
        for f in REQUIRED:
            if f not in n or n[f] in ("", None):
                problems.append(f"{where}: missing required field '{f}'")
        nid = n.get("id")
        if nid:
            if nid in ids:
                problems.append(f"{where}: id is used more than once")
            ids[nid] = n
            if nid in tier_keys:
                problems.append(f"{where}: id clashes with a tier key")
        if n.get("factor") not in FACTORS:
            problems.append(f"{where}: factor must be one of {', '.join(FACTORS)}")
        elif n["factor"] != n["_file_factor"]:
            problems.append(f"{where}: factor {n['factor']} does not match its file")
        if n.get("kind") not in KINDS:
            problems.append(f"{where}: kind must be 'world' or 'choice'")
        if n.get("horizon") not in HORIZONS:
            problems.append(f"{where}: horizon must be leaf, mid, or root")
        if n.get("status") not in STATUSES:
            problems.append(f"{where}: status must be one of {', '.join(sorted(STATUSES))}")
        # Rule 4: a resolution criterion that is actually there.
        if not str(n.get("resolution", "")).strip():
            problems.append(f"{where}: has no resolution criterion; a node without one is not a node")
        # Rule 8: long shots name their mechanism and breaking point.
        if n.get("long_shot"):
            for f in ("mechanism", "breaking_point"):
                if not str(n.get(f, "")).strip():
                    problems.append(
                        f"{where}: is a long shot without a '{f}'; the second founding rule says it "
                        "has not earned its place"
                    )

    # Rule 2 continued: every referenced id exists.
    def check_ref(where: str, field: str, ref: str, allow_tiers: bool = False) -> None:
        if ref in ids:
            return
        if allow_tiers and ref in tier_keys:
            return
        problems.append(f"{where}: {field} names '{ref}', which does not exist")

    for n in nodes:
        where = f"{n['_file']} node {n.get('id', '(no id)')}"
        for ref in n.get("depends_on", []) or []:
            check_ref(where, "depends_on", ref)
        for group in n.get("depends_on_any", []) or []:
            if not isinstance(group, list) or not group:
                problems.append(f"{where}: depends_on_any must be a list of non-empty lists")
                continue
            for ref in group:
                check_ref(where, "depends_on_any", ref)
        if n.get("superseded_by"):
            check_ref(where, "superseded_by", n["superseded_by"])
        if n.get("status") == "superseded" and not n.get("superseded_by"):
            problems.append(f"{where}: is superseded but does not say by what")
    for t in tiers:
        where = f"tiers.toml tier {t.get('key')}"
        for ref in t.get("requires", []) or []:
            check_ref(where, "requires", ref, allow_tiers=True)
        if "requires_any" in t:
            problems.append(f"{where}: requires_any is not part of the schema; put 'either route' logic on a node")

    # Rule 3: no cycles, counting both kinds of dependency.
    if not problems:
        try:
            topological_order(nodes)
        except TreeError as e:
            problems.append(str(e))
        try:
            tier_order(tiers)
        except TreeError as e:
            problems.append(str(e))

    # Rules 6 and 7: probabilities, and choice groups.
    groups: dict[str, list[dict]] = defaultdict(list)
    for n in nodes:
        where = f"{n['_file']} node {n.get('id', '(no id)')}"
        prob = n.get("probability")
        if n.get("kind") == "choice":
            if not n.get("choice_group"):
                problems.append(f"{where}: a choice node needs a choice_group")
            else:
                groups[n["choice_group"]].append(n)
            if prob is not None:
                problems.append(f"{where}: choice nodes do not carry a probability")
            continue
        if prob is None:
            continue
        if not isinstance(prob, dict):
            problems.append(f"{where}: probability must be a table with one entry per scenario key")
            continue
        missing = [k for k in scen_keys if k not in prob]
        extra = [k for k in prob if k not in scen_keys]
        if missing:
            problems.append(f"{where}: probability is missing scenario(s) {', '.join(missing)}")
        if extra:
            problems.append(f"{where}: probability names unknown scenario(s) {', '.join(extra)}")
        for k, v in prob.items():
            if not isinstance(v, (int, float)) or not 0 <= v <= 1:
                problems.append(f"{where}: probability for {k} must be a number between 0 and 1")
        if not missing and not extra:
            values = [prob[k] for k in scen_keys]
            if any(b < a for a, b in zip(values, values[1:])):
                problems.append(
                    f"{where}: probability falls as the window lengthens ({values}); "
                    "a longer window can only make a node more likely"
                )
        if not n.get("estimated_on"):
            problems.append(f"{where}: has a probability but no estimated_on date")
        if not str(n.get("rationale", "")).strip():
            problems.append(f"{where}: has a probability but no rationale")
    for g, members in groups.items():
        plans = [m for m in members if m.get("current_plan")]
        if len(plans) != 1:
            problems.append(
                f"choice group '{g}': exactly one option must have current_plan = true (found {len(plans)})"
            )
    return problems


def topological_order(nodes: list[dict]) -> list[dict]:
    """Nodes in an order where every dependency comes before what depends on it."""
    by_id = {n["id"]: n for n in nodes}
    parents = {
        n["id"]: set(n.get("depends_on", []) or [])
        | {r for g in (n.get("depends_on_any", []) or []) for r in g}
        for n in nodes
    }
    done: list[dict] = []
    state: dict[str, int] = {}  # 1 = visiting, 2 = finished

    def visit(nid: str, path: list[str]) -> None:
        if state.get(nid) == 2:
            return
        if state.get(nid) == 1:
            cycle = " -> ".join(path[path.index(nid):] + [nid])
            raise TreeError(f"dependency cycle: {cycle}")
        state[nid] = 1
        for p in sorted(parents[nid]):
            if p in by_id:
                visit(p, path + [nid])
        state[nid] = 2
        done.append(by_id[nid])

    for nid in sorted(by_id):
        visit(nid, [])
    return done


def tier_order(tiers: list[dict]) -> list[dict]:
    """Tiers in an order where a tier that requires another comes after it."""
    by_key = {t["key"]: t for t in tiers}
    done: list[dict] = []
    state: dict[str, int] = {}

    def visit(key: str, path: list[str]) -> None:
        if state.get(key) == 2:
            return
        if state.get(key) == 1:
            raise TreeError("tier requirement cycle: " + " -> ".join(path + [key]))
        state[key] = 1
        for r in by_key[key].get("requires", []) or []:
            if r in by_key:
                visit(r, path + [key])
        state[key] = 2
        done.append(by_key[key])

    for key in by_key:
        visit(key, [])
    return done


# ---------------------------------------------------------------- shape


def describe_shape(tree: dict) -> str:
    nodes = tree["nodes"]
    lines = []
    lines.append(f"Nodes: {len(nodes)}")
    by_factor = defaultdict(int)
    by_kind = defaultdict(int)
    by_horizon = defaultdict(int)
    by_status = defaultdict(int)
    long_shots = 0
    with_prob = 0
    for n in nodes:
        by_factor[n["factor"]] += 1
        by_kind[n["kind"]] += 1
        by_horizon[n["horizon"]] += 1
        by_status[n["status"]] += 1
        long_shots += 1 if n.get("long_shot") else 0
        with_prob += 1 if n.get("probability") else 0
    lines.append("By factor:  " + ", ".join(f"{f} {by_factor[f]}" for f in FACTORS if by_factor[f]))
    lines.append("By kind:    " + ", ".join(f"{k} {v}" for k, v in sorted(by_kind.items())))
    lines.append("By horizon: " + ", ".join(f"{k} {v}" for k, v in sorted(by_horizon.items())))
    lines.append("By status:  " + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())))
    if nodes:
        share = by_horizon["leaf"] / len(nodes)
        verdict = "meets" if share >= 1 / 3 else "below"
        lines.append(f"Leaves: {by_horizon['leaf']} of {len(nodes)} ({share:.0%}), {verdict} the one-third rule")
    lines.append(f"Long shots: {long_shots}")
    lines.append(f"With probabilities: {with_prob} of {len(nodes)}")
    unverified = [(n["id"], c) for n in nodes for c in (n.get("verify") or [])]
    lines.append(f"Claims awaiting verification: {len(unverified)}")
    for nid, claim in unverified:
        lines.append(f"  {nid}: {claim}")
    lines.append("")
    lines.append("Scenarios: " + ", ".join(
        f"{s['key']} ({s.get('window_year', 'open')})" for s in tree["scenarios"]))
    lines.append("")
    lines.append("Tiers and what they require:")
    for t in tree["tiers"]:
        req = t.get("requires", []) or []
        lines.append(f"  {t['key']} {t['name']}: " + (", ".join(req) if req else "(nothing listed yet)"))
    feeds = defaultdict(list)
    for t in tree["tiers"]:
        for r in t.get("requires", []) or []:
            feeds[r].append(t["key"])
    node_feeds = {k: v for k, v in feeds.items() if k not in {t["key"] for t in tree["tiers"]}}
    if node_feeds:
        lines.append("")
        lines.append("Which tiers each node feeds directly:")
        for nid, ts in sorted(node_feeds.items()):
            lines.append(f"  {nid}: {', '.join(ts)}")
    return "\n".join(lines)


# ------------------------------------------------------------- simulating


def missing_probabilities(tree: dict) -> list[str]:
    keys = [s["key"] for s in tree["scenarios"]]
    out = []
    for n in tree["nodes"]:
        if n["kind"] != "world" or n["status"] != "open":
            continue
        prob = n.get("probability") or {}
        if any(k not in prob for k in keys):
            out.append(n["id"])
    return out


def simulate(tree: dict, scenario_key: str, runs: int, rng: random.Random,
             forced: dict[str, bool] | None = None) -> dict:
    """Play the tree out `runs` times for one scenario. Returns yes-rates per node and per tier.

    `forced` maps choice-node ids to True/False and overrides the current plan; any choice node
    not mentioned keeps its current-plan setting.
    """
    order = topological_order(tree["nodes"])
    tiers = tier_order(tree["tiers"])
    forced = forced or {}
    node_yes = defaultdict(int)
    tier_yes = defaultdict(int)

    for _ in range(runs):
        state: dict[str, bool] = {}
        for n in order:
            nid = n["id"]
            status = n["status"]
            if status == "resolved-yes":
                value = True
            elif status in ("resolved-no", "superseded"):
                value = False
            elif n["kind"] == "choice":
                value = forced.get(nid, bool(n.get("current_plan")))
            else:
                deps_ok = all(state.get(d, False) for d in n.get("depends_on", []) or [])
                any_ok = all(any(state.get(d, False) for d in g)
                             for g in n.get("depends_on_any", []) or [])
                value = deps_ok and any_ok and rng.random() < n["probability"][scenario_key]
            state[nid] = value
            if value:
                node_yes[nid] += 1
        for t in tiers:
            reached = all(state.get(r, False) for r in t.get("requires", []) or [])
            state[t["key"]] = reached
            if reached:
                tier_yes[t["key"]] += 1

    return {
        "nodes": {n["id"]: node_yes[n["id"]] / runs for n in order},
        "tiers": {t["key"]: tier_yes[t["key"]] / runs for t in tiers},
    }


def report_run(tree: dict, runs: int, seed: int) -> str:
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError(
            "cannot report numbers: these open world nodes have no probability for every scenario:\n  "
            + "\n  ".join(missing)
        )
    rng = random.Random(seed)
    keys = [s["key"] for s in tree["scenarios"]]
    results = {k: simulate(tree, k, runs, rng) for k in keys}
    lines = [f"Runs per scenario: {runs} (seed {seed})", ""]
    lines.append("Tier reached, by scenario:")
    lines.append("  tier  " + "".join(f"{k:>10}" for k in keys))
    for t in tree["tiers"]:
        mark = "  <- headline" if t["key"] == HEADLINE_TIER else ""
        lines.append(f"  {t['key']:<5} " + "".join(f"{results[k]['tiers'][t['key']]:>10.3f}" for k in keys) + mark)
    contact = [n for n in tree["nodes"] if n["factor"] == "C"]
    if contact:
        lines.append("")
        lines.append("Contact Clause, beside the equation and never multiplied into it:")
        for n in contact:
            lines.append(f"  {n['id']:<6} " + "".join(f"{results[k]['nodes'][n['id']]:>10.3f}" for k in keys)
                         + f"  {n['name']}")
    lines.append("")
    lines.append("Every node, by scenario:")
    for n in topological_order(tree["nodes"]):
        lines.append(f"  {n['id']:<45} " + "".join(f"{results[k]['nodes'][n['id']]:>10.3f}" for k in keys))
    return "\n".join(lines)


def report_compare(tree: dict, runs: int, seed: int) -> str:
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError("cannot compare decisions until every open world node has probabilities")
    groups: dict[str, list[dict]] = defaultdict(list)
    for n in tree["nodes"]:
        if n["kind"] == "choice" and n["status"] == "open":
            groups[n["choice_group"]].append(n)
    if not groups:
        return "No open choice points in the tree; nothing to compare."
    keys = [s["key"] for s in tree["scenarios"]]
    lines = [f"Decision comparison: headline is {HEADLINE_TIER}, runs per case {runs} (seed {seed})", ""]
    for g, options in groups.items():
        lines.append(f"Choice group '{g}':")
        for opt in options:
            rng = random.Random(seed)
            forced = {o["id"]: (o["id"] == opt["id"]) for o in options}
            row = []
            for k in keys:
                row.append(simulate(tree, k, runs, rng, forced)["tiers"][HEADLINE_TIER])
            tag = " (current plan)" if opt.get("current_plan") else ""
            lines.append(f"  {opt['name']}{tag}")
            lines.append("      " + "".join(f"{k}: {v:.3f}   " for k, v in zip(keys, row)))
        lines.append("")
    return "\n".join(lines).rstrip()


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="validate",
                        choices=["validate", "shape", "run", "compare"])
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent.parent / "data")
    parser.add_argument("--runs", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args(argv)

    try:
        tree = load_tree(args.data)
        problems = validate(tree)
        if problems:
            print(f"The tree in {args.data} breaks the schema in {len(problems)} place(s):")
            for p in problems:
                print("  -", p)
            return 1
        if args.command == "validate":
            print(f"The tree in {args.data} follows the schema: {len(tree['nodes'])} node(s), "
                  f"{len(tree['tiers'])} tier(s), {len(tree['scenarios'])} scenario(s).")
            missing = missing_probabilities(tree)
            if missing:
                print(f"{len(missing)} open world node(s) have no probabilities yet, so 'run' will refuse.")
            return 0
        if args.command == "shape":
            print(describe_shape(tree))
            return 0
        if args.command == "run":
            print(report_run(tree, args.runs, args.seed))
            return 0
        if args.command == "compare":
            print(report_compare(tree, args.runs, args.seed))
            return 0
    except TreeError as e:
        print(str(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
