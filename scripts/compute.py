#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ into headline numbers.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/compute.py validate            check the tree against docs/node-schema.md
    python3 scripts/compute.py shape               print the tree's shape (counts, tiers, leaves)
    python3 scripts/compute.py run [--runs N]      simulate the tree once per longevity scenario
    python3 scripts/compute.py run --world-spread 0   the same with nodes rolled independently
    python3 scripts/compute.py run --snapshot [LABEL]  the same, and write the run to data/snapshots/
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time
    python3 scripts/compute.py worth               what each open world node would be worth to the headline
    python3 scripts/compute.py attribute ENTRY     how much of a run's move came from one ledger entry
    python3 scripts/compute.py --data DIR ...      use a different data folder (for tests)

What "run" does: for each scenario, it plays the tree out many thousands of times. In each
play-through, nodes are visited in dependency order. A world node whose dependencies all came
true comes true with its probability for that scenario; otherwise it stays false. Nodes already
resolved in the real world are fixed at their outcome. Choice points are never sampled: each
choice group is set to its current-plan option. A tier is reached when everything it requires
came true. The number reported for a tier is the fraction of play-throughs that reached it.
Contact Clause nodes are reported in their own section and never feed a tier.

Nodes are not rolled independently. Each play-through first draws one number for how favourable
the world turned out (the "world draw", added 2026-09-19 after the first run): a normal draw with
mean zero and a spread set by --world-spread, applied to every open world node's probability on
the log-odds scale, so a good world lifts every node together and a bad one sinks them together.
With the default spread of 1.0, one standard deviation up turns 0.50 into 0.73 and 0.20 into 0.40.
A spread of 0 restores independent rolls. "run" prints both, so the gap between them is visible.

"compare" repeats "run" for each option in each choice group, one group at a time, and reports
how far each option moves the headline (A2) from the current plan.

"run --snapshot" writes the whole run to data/snapshots/YYYY-MM-DD[-label].json and commits
nothing: the parameters, every tier's rate per scenario, every node's rate, the chain's gate
rates, the Contact Clause rungs, the decision comparison, and what each open world node is
worth. Snapshots are the ledger's memory (docs/ledger-plan.md); the history charts on the
website are drawn from nothing else. Working out every node's worth means playing the whole
tree out twice more per node, which takes several minutes; "--no-worth" leaves it out.

"worth" asks, of every open world node: if this came true tomorrow, where would the headline
go, and where would it go if it turned out no? "attribute" asks the question backwards, of one
ledger entry: how much lower would the headline be if this one change had not been made?

The script refuses to report numbers until every open world node has a probability for every
scenario, but "validate" and "shape" work on a tree with no numbers at all.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import random
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FACTORS = ["W", "L", "E", "D", "B", "M", "R", "A", "C"]
KINDS = {"world", "choice"}
HORIZONS = {"leaf", "mid", "root"}
STATUSES = {"open", "resolved-yes", "resolved-no", "superseded"}
REQUIRED = ["id", "name", "factor", "kind", "description", "resolution", "source", "horizon", "status"]
HEADLINE_TIER = "A2"

# Written onto every snapshot and kept there. Until the outside-model review (roadmap step 27)
# has been ruled in full, every number the tree produces is a first pass and the site says so.
# Change this to "reviewed" when the last of step 27's rulings lands: snapshots taken before
# then keep the label they were written with, which is the point of writing it into the file.
REVIEW_STATUS = "pre-review"


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

    # Everything in data/ that is not one of these is read as a factor file of nodes. The
    # ledger is a record of what changed rather than a part of the tree, so it is skipped here
    # and read by its own loader (load_ledger, below).
    NOT_FACTOR_FILES = ("scenarios.toml", "tiers.toml", "ledger.toml")

    nodes = []
    for path in sorted(data_dir.glob("*.toml")):
        if path.name in NOT_FACTOR_FILES:
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
        # Rule 9 (2026-09-19): an event marked as having happened links to the record that settled it.
        if str(n.get("status", "")).startswith("resolved"):
            if not str(n.get("resolved_by", "")).strip():
                problems.append(f"{where}: is resolved but has no 'resolved_by'")
            links = n.get("resolved_links") or []
            if not isinstance(links, list) or not any(str(u).startswith("http") for u in links):
                problems.append(f"{where}: is resolved but 'resolved_links' has no URL; a reader must be able to check the claim")
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


def shifted(p: float, w: float) -> float:
    """Move a probability by w on the log-odds scale. 0 and 1 stay where they are."""
    if p <= 0.0 or p >= 1.0:
        return p
    z = math.log(p / (1.0 - p)) + w
    return 1.0 / (1.0 + math.exp(-z))


def simulate(tree: dict, scenario_key: str, runs: int, rng: random.Random,
             forced: dict[str, bool] | None = None, world_spread: float = 1.0,
             joint: dict[str, list[str]] | None = None) -> dict:
    """Play the tree out `runs` times for one scenario. Returns yes-rates per node and per tier.

    `joint` maps a name to a list of node ids; the result's "joint" gives, per name, how often
    every one of those nodes held in the same play-through (the site's chain links use this).
    `forced` holds node ids set to True or False. A choice node in it overrides the current plan;
    an open world node in it is held at that outcome whatever its probability and its dependencies
    said, which is how node worth and entry contribution are worked out. A world node is still
    given its ordinary roll of the dice before being overridden, so that a run with nothing forced
    draws exactly the numbers it always did and every published figure stays reproducible.
    """
    order = topological_order(tree["nodes"])
    tiers = tier_order(tree["tiers"])
    forced = forced or {}
    node_yes = defaultdict(int)
    tier_yes = defaultdict(int)
    joint = joint or {}
    joint_yes = defaultdict(int)

    for _ in range(runs):
        state: dict[str, bool] = {}
        w = rng.gauss(0.0, world_spread) if world_spread > 0 else 0.0
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
                value = deps_ok and any_ok and rng.random() < shifted(n["probability"][scenario_key], w)
                if nid in forced:
                    value = forced[nid]
            state[nid] = value
            if value:
                node_yes[nid] += 1
        for t in tiers:
            reached = all(state.get(r, False) for r in t.get("requires", []) or [])
            state[t["key"]] = reached
            if reached:
                tier_yes[t["key"]] += 1
        for name, ids in joint.items():
            if all(state.get(i, False) for i in ids):
                joint_yes[name] += 1

    return {
        "nodes": {n["id"]: node_yes[n["id"]] / runs for n in order},
        "tiers": {t["key"]: tier_yes[t["key"]] / runs for t in tiers},
        "joint": {name: joint_yes[name] / runs for name in joint},
    }


def report_run(tree: dict, runs: int, seed: int, world_spread: float = 1.0) -> str:
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError(
            "cannot report numbers: these open world nodes have no probability for every scenario:\n  "
            + "\n  ".join(missing)
        )
    rng = random.Random(seed)
    keys = [s["key"] for s in tree["scenarios"]]
    results = {k: simulate(tree, k, runs, rng, world_spread=world_spread) for k in keys}
    lines = [f"Runs per scenario: {runs} (seed {seed}), world spread {world_spread:g}"
             + (" (nodes rolled independently)" if world_spread <= 0 else " on the log-odds scale"), ""]
    lines.append("Tier reached, by scenario:")
    lines.append("  tier  " + "".join(f"{k:>10}" for k in keys))
    for t in tree["tiers"]:
        mark = "  <- headline" if t["key"] == HEADLINE_TIER else ""
        lines.append(f"  {t['key']:<5} " + "".join(f"{results[k]['tiers'][t['key']]:>10.3f}" for k in keys) + mark)
    if world_spread > 0:
        rng0 = random.Random(seed)
        indep = {k: simulate(tree, k, runs, rng0, world_spread=0.0) for k in keys}
        lines.append("")
        lines.append("The same tiers with nodes rolled independently (world spread 0), for comparison:")
        for t in tree["tiers"]:
            lines.append(f"  {t['key']:<5} " + "".join(f"{indep[k]['tiers'][t['key']]:>10.3f}" for k in keys))
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


def report_compare(tree: dict, runs: int, seed: int, world_spread: float = 1.0) -> str:
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
    lines = [f"Decision comparison: headline is {HEADLINE_TIER}, runs per case {runs} (seed {seed}), world spread {world_spread:g}", ""]
    for g, options in groups.items():
        lines.append(f"Choice group '{g}':")
        for opt in options:
            rng = random.Random(seed)
            forced = {o["id"]: (o["id"] == opt["id"]) for o in options}
            row = []
            for k in keys:
                row.append(simulate(tree, k, runs, rng, forced, world_spread)["tiers"][HEADLINE_TIER])
            tag = " (current plan)" if opt.get("current_plan") else ""
            lines.append(f"  {opt['name']}{tag}")
            lines.append("      " + "".join(f"{k}: {v:.3f}   " for k, v in zip(keys, row)))
        lines.append("")
    return "\n".join(lines).rstrip()


# -------------------------------------------------------- worth and contribution
#
# Two questions the ledger asks of the tree (docs/ledger-plan.md, decisions 3 and 4).
#
# Worth, forwards: if this node came true tomorrow, where would the headline go? The node is
# forced to yes and the tree re-run, then forced to no and re-run, and both are reported against
# the headline as it stands. That is a one-at-a-time sensitivity analysis, the standard way to
# ask this, and it is what the site's watch lists are built from.
#
# Contribution, backwards: how much of this run's move came from this one entry? The tree as it
# stands at the entry's snapshot has that entry's changes reverted, and only those, and is re-run.
# Leaving one out this way does not add up exactly when several entries land in the same run,
# because the changes interact; what is left over is reported as its own line rather than hidden.


def force_run(tree: dict, forced: dict[str, bool], runs: int, seed: int,
              world_spread: float) -> dict[str, float]:
    """The headline under every scenario, with some nodes held at an outcome.

    Every forced run starts from the same seed, so the world draws line up run to run and the
    difference between two runs is mostly the change being asked about rather than dice."""
    keys = [s["key"] for s in tree["scenarios"]]
    rng = random.Random(seed)
    return {k: simulate(tree, k, runs, rng, forced, world_spread)["tiers"][HEADLINE_TIER] for k in keys}


def headline_rests_on(tree: dict) -> set[str]:
    """Every node the headline tier rests on, at any remove: the nodes it requires, the nodes
    those depend on, and so on down. A node outside this set cannot change the headline by any
    amount, whatever it does, so its worth is exactly nothing and no amount of playing the tree
    out will show otherwise. The window's own nodes are outside it (the window is the scenario,
    not a link in the chain) and so is the Contact Clause, which is never multiplied in."""
    tiers = {t["key"]: t for t in tree["tiers"]}
    by_id = {n["id"]: n for n in tree["nodes"]}
    seen_tiers: set[str] = set()
    nodes: set[str] = set()
    stack = [HEADLINE_TIER]
    while stack:
        key = stack.pop()
        if key in seen_tiers:
            continue
        seen_tiers.add(key)
        for r in tiers[key].get("requires", []) or []:
            if r in tiers:
                stack.append(r)
            elif r in by_id:
                nodes.add(r)
    pending = list(nodes)
    while pending:
        n = by_id[pending.pop()]
        parents = list(n.get("depends_on", []) or [])
        parents += [r for g in (n.get("depends_on_any", []) or []) for r in g]
        for p in parents:
            if p in by_id and p not in nodes:
                nodes.add(p)
                pending.append(p)
    return nodes


def run_noise(headline: dict[str, float], runs: int) -> dict[str, float]:
    """Roughly how far a figure can move between two runs for no reason but the dice.

    Two standard errors of one run's rate, which is a rough guide rather than a proper interval:
    the runs being compared share a seed, so they move together more than two unrelated runs
    would, and this overstates the noise rather than understating it. It is here so that the site
    can say plainly when a contribution is too small to tell apart from chance, instead of
    printing a confident figure that a second run would contradict."""
    return {k: round(2.0 * math.sqrt(max(p * (1.0 - p), 0.0) / runs), 6) for k, p in headline.items()}


def node_worth(tree: dict, runs: int, seed: int, world_spread: float) -> dict:
    """What each open world node would be worth to the headline if it resolved now.

    For every open world node the headline rests on: force it to yes and re-run, force it to no
    and re-run. Worth-if-yes is the first minus the headline as it stands, worth-if-no the second
    minus the same. A node the headline cannot rest on is worth nothing and is recorded as nothing
    rather than played out, which is both exact and much faster. Choice points are left out; the
    decision comparison already answers this question for them."""
    baseline = force_run(tree, {}, runs, seed, world_spread)
    nothing = {k: 0.0 for k in baseline}
    reachable = headline_rests_on(tree)
    out: dict[str, dict] = {}
    for n in tree["nodes"]:
        if n["kind"] != "world" or n["status"] != "open":
            continue
        if n["id"] not in reachable:
            out[n["id"]] = {
                "reaches_headline": False,
                "headline": baseline,
                "headline_if_yes": baseline,
                "headline_if_no": baseline,
                "if_yes": nothing,
                "if_no": nothing,
            }
            continue
        yes = force_run(tree, {n["id"]: True}, runs, seed, world_spread)
        no = force_run(tree, {n["id"]: False}, runs, seed, world_spread)
        out[n["id"]] = {
            "reaches_headline": True,
            "headline": baseline,
            "headline_if_yes": yes,
            "headline_if_no": no,
            "if_yes": {k: round(yes[k] - baseline[k], 6) for k in baseline},
            "if_no": {k: round(no[k] - baseline[k], 6) for k in baseline},
        }
    return {
        "headline": baseline,
        "reaches_headline": sorted(reachable),
        "nodes": out,
    }


def report_worth(tree: dict, runs: int, seed: int, world_spread: float) -> str:
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError("cannot work out what a node is worth until every open world node has probabilities")
    worth = node_worth(tree, runs, seed, world_spread)
    keys = [s["key"] for s in tree["scenarios"]]
    lines = [f"What each open world node is worth to the headline ({HEADLINE_TIER}): runs per case "
             f"{runs} (seed {seed}), world spread {world_spread:g}", ""]
    lines.append("The headline as it stands:")
    lines.append("      " + "".join(f"{k:>10}" for k in keys))
    lines.append("      " + "".join(f"{worth['headline'][k]:>10.3f}" for k in keys))
    lines.append("")
    lines.append("Change in the headline if the node resolved yes now, and if it resolved no,")
    lines.append(f"ranked by what a yes is worth under the {keys[0]} scenario:")
    reaching = {k: v for k, v in worth["nodes"].items() if v["reaches_headline"]}
    ranked = sorted(reaching.items(), key=lambda kv: -kv[1]["if_yes"][keys[0]])
    for nid, w in ranked:
        lines.append(f"  {nid}")
        lines.append("    yes " + "".join(f"{w['if_yes'][k]:>+10.4f}" for k in keys))
        lines.append("    no  " + "".join(f"{w['if_no'][k]:>+10.4f}" for k in keys))
    resting = len(worth["nodes"]) - len(reaching)
    if resting:
        lines.append("")
        lines.append(f"{resting} open world node(s) are worth nothing to the headline, because the "
                     "headline does not rest")
        lines.append("on them at any remove: the window's own nodes, which the scenario covers, and "
                     "the Contact")
        lines.append("Clause, which sits beside the equation and is never multiplied in.")
    return "\n".join(lines)


def probability_from_revision(old, scen_keys: list[str]) -> dict[str, float] | None:
    """Read a probability out of a revision's `old` field, or return None when it cannot be read.

    Revisions are written for people, so the old value is prose. Both forms in the record are
    understood: "0.60 flat across scenarios", the same number everywhere, and
    "0.75 / 0.80 / 0.85 / 0.90 / 0.92", one number per scenario in the order scenarios.toml lists
    them. A table or a bare number works too. Anything else is refused rather than guessed at, and
    the entry that rests on it is reported as one whose contribution cannot be separated."""
    if isinstance(old, dict):
        return {k: float(old[k]) for k in scen_keys} if all(k in old for k in scen_keys) else None
    if isinstance(old, (int, float)):
        return {k: float(old) for k in scen_keys}
    if not isinstance(old, str):
        return None
    numbers = re.findall(r"\d*\.\d+|\d+", old)
    if len(numbers) == 1:
        return {k: float(numbers[0]) for k in scen_keys}
    if len(numbers) == len(scen_keys):
        return dict(zip(scen_keys, (float(v) for v in numbers)))
    return None


def revert_entry(tree: dict, node_ids: list[str], since: str | None,
                 until: str) -> tuple[dict, list[str]]:
    """A copy of the tree with one entry's changes undone, and a plain list of what could not be.

    The window an entry's changes must fall in runs from the previous run up to the entry itself.
    Every date in this project is a day, and two runs can happen on one day, so the start of the
    window counts as inside it: a revision dated the same day as the previous run is still one this
    entry made. The changes an entry made are the revisions on the nodes it names that fall in that
    window, plus a resolution recorded in the same window. A probability revision is undone by
    putting the old numbers back, a resolution by opening the node again. Anything else on a node
    (a reworded criterion, a corrected source) moves no number and is left alone."""
    scen_keys = [s["key"] for s in tree["scenarios"]]
    by_id = {n["id"]: n for n in tree["nodes"]}
    reverted = {"scenarios": tree["scenarios"], "tiers": tree["tiers"], "nodes": []}
    cannot: list[str] = []
    undone: set[str] = set()
    refused: set[str] = set()

    def in_window(value) -> bool:
        day = plain(value)
        return isinstance(day, str) and (since is None or day >= since) and day <= until

    for nid in node_ids:
        if nid not in by_id:
            cannot.append(f"the entry names '{nid}', which is not a node in the tree")
            refused.add(nid)

    for n in tree["nodes"]:
        node = dict(n)
        if n["id"] in node_ids:
            for rev in n.get("revisions", []) or []:
                if rev.get("field") != "probability" or not in_window(rev.get("date")):
                    continue
                old = probability_from_revision(rev.get("old"), scen_keys)
                if old is None:
                    cannot.append(f"{n['id']}: the probability before this entry is written as "
                                  f"{rev.get('old')!r}, which cannot be read back as numbers")
                    refused.add(n["id"])
                    continue
                node["probability"] = old
                undone.add(n["id"])
            if n["status"].startswith("resolved") and in_window(n.get("resolved_on")):
                node["status"] = "open"
                node.pop("resolved_on", None)
                undone.add(n["id"])
                if not node.get("probability"):
                    cannot.append(f"{n['id']}: opening it again leaves it with no probability, so the "
                                  "tree cannot be played out with this entry undone")
                    refused.add(n["id"])
        reverted["nodes"].append(node)

    for nid in node_ids:
        if nid in by_id and nid not in undone and nid not in refused:
            cannot.append(f"{nid}: this entry names it, but no probability revision or resolution of "
                          "its date is on the node's record, so there is nothing to undo")
    return reverted, cannot


def attribute_entry(tree: dict, entry: dict, since: str | None, runs: int, seed: int,
                    world_spread: float, headline: dict[str, float] | None = None) -> dict:
    """How much of a run's move came from one ledger entry, by leaving that entry out.

    The headline is worked out twice: once with the tree as it stands at the entry's snapshot, and
    once with the entry's changes, and only those, undone. The difference is what the entry was
    worth: a positive contribution means the headline is that much higher than it would be with
    this entry undone. An entry whose changes cannot be undone from the record — a node added or
    cut, a tier requirement moved, a change to how the tree is played out — is reported as one
    that cannot be separated, and the run's unattributed remainder carries it instead."""
    node_ids = list(entry.get("nodes", []) or [])
    with_it = headline if headline is not None else force_run(tree, {}, runs, seed, world_spread)
    if entry.get("kind") == "held-steady":
        # Written precisely because nothing moved: the event was read against the criteria the tree
        # had already written down and none of them counted. Its contribution is nothing, exactly,
        # and there is nothing to play out to find that out.
        return {
            "id": entry["id"], "separable": True, "nodes": [], "moved_nothing": True,
            "headline": with_it, "headline_without": with_it,
            "contribution": {k: 0.0 for k in with_it},
        }
    if not node_ids:
        return {
            "id": entry["id"], "separable": False, "headline": with_it,
            "why": "This entry changed the shape of the tree, or the way the tree is played out, "
                   "rather than any node's number, so there is no one change to undo. Its share of "
                   "the run's move is reported with the rest that could not be separated.",
        }
    reverted, cannot = revert_entry(tree, node_ids, since, plain(entry["date"]))
    if cannot:
        return {
            "id": entry["id"], "separable": False, "headline": with_it,
            "why": "This entry cannot be undone from the record: " + "; ".join(cannot) + ".",
        }
    without_it = force_run(reverted, {}, runs, seed, world_spread)
    return {
        "id": entry["id"],
        "separable": True,
        "nodes": node_ids,
        "headline": with_it,
        "headline_without": without_it,
        "contribution": {k: round(with_it[k] - without_it[k], 6) for k in with_it},
    }


def load_ledger(path: Path) -> list[dict]:
    """The ledger entries in data/ledger.toml, oldest first, or an empty list when there is none.

    This reads; it does not check. The rules an entry must follow are enforced by the export
    script (scripts/export.py), which refuses to build the site when one is broken."""
    if not path.exists():
        return []
    try:
        return list(tomllib.loads(path.read_text()).get("entry", []) or [])
    except tomllib.TOMLDecodeError as e:
        raise TreeError(f"{path.name}: cannot be read as TOML: {e}") from e


def previous_snapshot(snapshots: list[dict], key: str) -> dict | None:
    """The run before the one named, in the order the folder sorts, or None for the first run."""
    keys = [s["key"] for s in snapshots]
    if key not in keys:
        raise TreeError(f"no snapshot named '{key}' in the snapshot folder")
    i = keys.index(key)
    return snapshots[i - 1] if i > 0 else None


def attribute_snapshot(tree: dict, entries: list[dict], snapshots: list[dict], key: str,
                       runs: int, seed: int, world_spread: float) -> dict:
    """Every ledger entry that landed in one run, what each was worth, and what is left over.

    Contributions do not add up to the run's whole move, because changes made in the same run
    interact and because some changes cannot be undone one at a time. The difference is reported
    as its own line rather than spread quietly over the entries (docs/ledger-plan.md, decision 3)."""
    snapshot = next((s for s in snapshots if s["key"] == key), None)
    if snapshot is None:
        raise TreeError(f"no snapshot named '{key}' in the snapshot folder")
    before = previous_snapshot(snapshots, key)
    since = before["date"] if before else None
    scen_keys = [s["key"] for s in tree["scenarios"]]

    headline = force_run(tree, {}, runs, seed, world_spread)
    recorded = snapshot.get("tiers", {}).get(HEADLINE_TIER, {})
    matches = all(abs(headline[k] - recorded.get(k, headline[k])) < 1e-9 for k in headline)

    mine = [e for e in entries if plain(e.get("snapshot")) == key]
    rows = [attribute_entry(tree, e, since, runs, seed, world_spread, headline=headline) for e in mine]

    total = None
    if before:
        was = before.get("tiers", {}).get(HEADLINE_TIER, {})
        total = {k: round(recorded[k] - was[k], 6) for k in scen_keys if k in recorded and k in was}
    separable = [r for r in rows if r["separable"]]
    attributed = {k: round(sum(r["contribution"].get(k, 0.0) for r in separable), 6) for k in scen_keys}
    remainder = None
    if total is not None:
        remainder = {k: round(total[k] - attributed[k], 6) for k in total}

    return {
        "snapshot": key,
        "previous_snapshot": before["key"] if before else None,
        "tree_matches_snapshot": matches,
        "runs": runs,
        "noise": run_noise(headline, runs),
        "headline": headline,
        "headline_recorded": recorded,
        "total_move": total,
        "attributed": attributed,
        "remainder": remainder,
        "unseparated": [r["id"] for r in rows if not r["separable"]],
        "entries": rows,
    }


def attribution_target(entries: list[dict], snapshots: list[dict], target: str) -> str:
    """The run a name points at: a run of its own, or the run one ledger entry landed in."""
    if any(s["key"] == target for s in snapshots):
        return target
    by_id = {plain(e["id"]): e for e in entries}
    if target not in by_id:
        raise TreeError(f"no ledger entry and no run named '{target}'")
    return plain(by_id[target]["snapshot"])


def write_attribution(result: dict, folder: Path) -> Path:
    """Write one run's attribution to data/attribution/<run>.json, beside the run it belongs to.

    Unlike a snapshot this may be written again: a snapshot records what a run produced and is
    fixed, while an attribution is an answer about that run which a later entry, or a better way
    of separating a structural change, can improve."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{result['snapshot']}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return path


def report_attribution(tree: dict, entries: list[dict], snapshots: list[dict], target: str,
                       runs: int, seed: int, world_spread: float) -> tuple[str, dict]:
    """The attribution for one entry, or for a whole run when a run's key is named."""
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError("cannot attribute anything until every open world node has probabilities")
    if not entries:
        raise TreeError(
            "there is no ledger to attribute: data/ledger.toml does not exist yet, or holds no "
            "entries. It is written at ledger step 30 (docs/ledger-plan.md)."
        )
    by_id = {plain(e["id"]): e for e in entries}
    key = attribution_target(entries, snapshots, target)
    result = attribute_snapshot(tree, entries, snapshots, key, runs, seed, world_spread)
    keys = [s["key"] for s in tree["scenarios"]]

    def row(label: str, values: dict | None) -> str:
        if values is None:
            return f"  {label:<28} (no earlier run to compare with)"
        return f"  {label:<28}" + "".join(f"{values.get(k, 0.0):>+10.4f}" for k in keys)

    lines = [f"Run {result['snapshot']}, read against {result['previous_snapshot'] or 'nothing earlier'}: "
             f"what moved the headline ({HEADLINE_TIER})",
             f"Runs per case {runs} (seed {seed}), world spread {world_spread:g}", ""]
    if not result["tree_matches_snapshot"]:
        lines.append("Careful: the tree as it stands no longer produces this run's recorded numbers, so")
        lines.append("these contributions are worked out against the tree in data/, not against that run.")
        lines.append("")
    lines.append("      " + " " * 28 + "".join(f"{k:>10}" for k in keys))
    lines.append(row("The whole run moved", result["total_move"]))
    lines.append("")
    for entry in result["entries"]:
        if entry["separable"]:
            lines.append(row(entry["id"], entry["contribution"]))
        else:
            lines.append(f"  {entry['id']:<28} cannot be separated")
            lines.append(f"      {entry['why']}")
    lines.append("")
    lines.append(row("Attributed to entries", result["attributed"]))
    lines.append(row("Interaction and the rest", result["remainder"]))
    lines.append(row("Within this much is noise", result["noise"]))
    if result["unseparated"]:
        lines.append("  The rest carries the entries above that could not be separated: "
                     + ", ".join(result["unseparated"]) + ".")
    if target in by_id:
        one = next((r for r in result["entries"] if r["id"] == target), None)
        if one and one["separable"]:
            lines.append("")
            lines.append(f"Asked about {target} alone: the headline is higher by")
            lines.append(row("", one["contribution"]))
            lines.append("than it would be with that entry undone.")
    return "\n".join(lines), result


# ---------------------------------------------------------------- snapshots
#
# A snapshot is the complete output of one run, written to data/snapshots/ and committed.
# It is the ledger's memory: the history charts on the site are drawn from nothing else, so
# the history a reader sees is exactly the history in the repository (docs/ledger-plan.md,
# decision 2). One is taken at every quarterly scan, every annual review, and whenever a
# ruling changes the tree in between.


def plain(value):
    """Make a TOML value JSON-safe: dates become ISO strings, tables and lists recurse."""
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    return value


def git_commit() -> str | None:
    """The short commit this ran from, read out of .git without running git."""
    try:
        dot_git = ROOT / ".git"
        if dot_git.is_file():  # a worktree: .git is a one-line pointer to the real folder
            gitdir = Path(dot_git.read_text().split(":", 1)[1].strip())
            common = gitdir.parent.parent if gitdir.parent.name == "worktrees" else gitdir
        else:
            gitdir = common = dot_git
        ref = (gitdir / "HEAD").read_text().strip()
        if not ref.startswith("ref: "):
            return ref[:7]
        ref_name = ref[5:]
        ref_path = common / ref_name
        if ref_path.exists():
            return ref_path.read_text().strip()[:7]
        packed = common / "packed-refs"
        if packed.exists():
            for line in packed.read_text().splitlines():
                if line.endswith(" " + ref_name):
                    return line.split()[0][:7]
    except (OSError, IndexError):
        pass
    return None


def chain_gates(tree: dict) -> dict[str, list[str]]:
    """The home page's chain: per factor, the nodes the headline tier requires, directly or
    through the tiers it rests on (T3 under A2, T2 under T3, and so on). A link "holds" when
    every gate node of its factor holds in the same play-through; because each gate node
    already waits on its own dependencies, the link's rate counts those too. Factors with no
    gate node (W, whose job is done by the scenario, and C, never multiplied in) are left out.
    Moved here from export.py on 2026-09-19 (ledger step 28) so a snapshot can record it too."""
    tiers = {t["key"]: t for t in tree["tiers"]}
    by_id = {n["id"]: n for n in tree["nodes"]}
    seen: set[str] = set()
    stack = [HEADLINE_TIER]
    gates: dict[str, list[str]] = {}
    while stack:
        key = stack.pop()
        if key in seen:
            continue
        seen.add(key)
        for r in tiers[key].get("requires", []) or []:
            if r in tiers:
                stack.append(r)
            elif r in by_id:
                gates.setdefault(by_id[r]["factor"], [])
                if r not in gates[by_id[r]["factor"]]:
                    gates[by_id[r]["factor"]].append(r)
    return {f: sorted(gates[f]) for f in FACTORS if f in gates}


def decision_comparison(tree: dict, runs: int, seed: int, world_spread: float) -> dict:
    """The decision comparison as data rather than a printed table: for every open choice
    group, each option's headline number per scenario, and which option is the current plan."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for n in tree["nodes"]:
        if n["kind"] == "choice" and n["status"] == "open":
            groups[n["choice_group"]].append(n)
    keys = [s["key"] for s in tree["scenarios"]]
    out: dict[str, dict] = {}
    for group, options in groups.items():
        rows = []
        for opt in options:
            rng = random.Random(seed)
            forced = {o["id"]: (o["id"] == opt["id"]) for o in options}
            headline = {}
            for k in keys:
                headline[k] = simulate(tree, k, runs, rng, forced, world_spread)["tiers"][HEADLINE_TIER]
            rows.append({
                "id": opt["id"],
                "name": opt["name"],
                "current_plan": bool(opt.get("current_plan")),
                "headline": headline,
            })
        out[group] = {"options": rows}
    return out


def take_snapshot(tree: dict, runs: int, seed: int, world_spread: float, date: str,
                  label: str | None = None, note: str | None = None,
                  review_status: str = REVIEW_STATUS, commit: str | None = None,
                  with_worth: bool = True) -> dict:
    """Run the whole tree and return one snapshot: every number a later run can be read against.

    `date` is the date the snapshot is recorded under (the run's own date for an ordinary run,
    the date the numbers were produced for a backfill). `label` tells two snapshots on the same
    date apart; the key is the file name without its extension, date first so the folder sorts."""
    missing = missing_probabilities(tree)
    if missing:
        raise TreeError(
            "cannot take a snapshot: these open world nodes have no probability for every scenario:\n  "
            + "\n  ".join(missing)
        )
    keys = [s["key"] for s in tree["scenarios"]]
    gates = chain_gates(tree)
    rng = random.Random(seed)
    results = {k: simulate(tree, k, runs, rng, world_spread=world_spread, joint=gates) for k in keys}

    def per_scenario(pick):
        return {k: pick(results[k]) for k in keys}

    return {
        "key": f"{date}-{label}" if label else date,
        "date": date,
        "label": label,
        "note": note,
        "review_status": review_status,
        "headline_tier": HEADLINE_TIER,
        "run": {
            "runs": runs,
            "seed": seed,
            "world_spread": world_spread,
            "commit": commit if commit is not None else git_commit(),
            "taken_on": dt.date.today().isoformat(),
        },
        "scenarios": [plain(s) for s in tree["scenarios"]],
        "tiers": {t["key"]: per_scenario(lambda r, key=t["key"]: r["tiers"][key]) for t in tree["tiers"]},
        "nodes": {n["id"]: per_scenario(lambda r, nid=n["id"]: r["nodes"][nid]) for n in tree["nodes"]},
        "chain": {f: per_scenario(lambda r, f=f: r["joint"][f]) for f in gates},
        "chain_nodes": gates,
        "contact": {n["id"]: per_scenario(lambda r, nid=n["id"]: r["nodes"][nid])
                    for n in tree["nodes"] if n["factor"] == "C"},
        "decisions": decision_comparison(tree, runs, seed, world_spread),
        "worth": node_worth(tree, runs, seed, world_spread) if with_worth else None,
    }


def write_snapshot(snapshot: dict, folder: Path) -> Path:
    """Write a snapshot to data/snapshots/<key>.json. It refuses to overwrite one that exists:
    a snapshot records a run that happened, and a second run gets a label of its own."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{snapshot['key']}.json"
    if path.exists():
        raise TreeError(
            f"{path.name} already exists. A snapshot records a run that happened and is never "
            "rewritten; give this one a label of its own (--snapshot LABEL)."
        )
    path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    return path


def load_snapshots(folder: Path) -> list[dict]:
    """Every snapshot in the folder, oldest first, with any malformed one named plainly.

    Runs are ordered by date and then by key, so two runs taken on one day are put in order by
    their labels. Give a same-day label that sorts the way the runs happened."""
    if not folder.exists():
        return []
    out: list[dict] = []
    problems: list[str] = []
    for path in sorted(folder.glob("*.json")):
        try:
            snap = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{path.name}: cannot be read as JSON: {e}")
            continue
        missing = [f for f in ("key", "date", "run", "tiers", "nodes") if f not in snap]
        if missing:
            problems.append(f"{path.name}: missing the field(s) a snapshot must carry: {', '.join(missing)}")
            continue
        if snap["key"] != path.stem:
            problems.append(f"{path.name}: its key '{snap['key']}' is not its file name")
            continue
        out.append(snap)
    if problems:
        raise TreeError("\n".join(problems))
    return sorted(out, key=lambda s: (s["date"], s["key"]))


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="validate",
                        choices=["validate", "shape", "run", "compare", "worth", "attribute"])
    parser.add_argument("target", nargs="?", default=None,
                        help="with 'attribute': the ledger entry id, or a snapshot key for the whole run")
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent.parent / "data")
    parser.add_argument("--runs", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--world-spread", type=float, default=1.0,
                        help="standard deviation of the per-run world draw on the log-odds scale; 0 = independent rolls")
    parser.add_argument("--snapshot", nargs="?", const="", default=None, metavar="LABEL",
                        help="with 'run': write the whole run to data/snapshots/, under an optional label")
    parser.add_argument("--snapshot-date", default=None, metavar="YYYY-MM-DD",
                        help="the date the snapshot is recorded under (default today; for backfilling a past run)")
    parser.add_argument("--snapshot-note", default=None,
                        help="one plain sentence kept with the snapshot saying what run it was")
    parser.add_argument("--snapshot-commit", default=None, metavar="SHORT-SHA",
                        help="the commit the numbers came from (default: the commit this ran from; "
                             "set it when backfilling a run that happened at an older commit)")
    parser.add_argument("--snapshots", type=Path, default=ROOT / "data" / "snapshots",
                        help="the snapshot folder (for tests)")
    parser.add_argument("--ledger", type=Path, default=ROOT / "data" / "ledger.toml",
                        help="the ledger file (for tests)")
    parser.add_argument("--attribution", type=Path, default=ROOT / "data" / "attribution",
                        help="where a written attribution goes (for tests)")
    parser.add_argument("--write", action="store_true",
                        help="with 'attribute': commit the answer to data/attribution/, which is "
                             "what the website reads rather than working it out on every build")
    parser.add_argument("--no-worth", dest="with_worth", action="store_false",
                        help="leave the node worth table out of a snapshot; it is the slow part")
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
            print(report_run(tree, args.runs, args.seed, args.world_spread))
            if args.snapshot is not None:
                snapshot = take_snapshot(
                    tree, args.runs, args.seed, args.world_spread,
                    date=args.snapshot_date or dt.date.today().isoformat(),
                    label=args.snapshot or None, note=args.snapshot_note,
                    commit=args.snapshot_commit, with_worth=args.with_worth,
                )
                path = write_snapshot(snapshot, args.snapshots)
                print(f"\nSnapshot {snapshot['key']} written to {path}, marked {snapshot['review_status']}.")
            return 0
        if args.command == "compare":
            print(report_compare(tree, args.runs, args.seed, args.world_spread))
            return 0
        if args.command == "worth":
            print(report_worth(tree, args.runs, args.seed, args.world_spread))
            return 0
        if args.command == "attribute":
            if not args.target:
                print("attribute needs the id of a ledger entry, or the key of a snapshot "
                      "to attribute the whole of that run.")
                return 1
            text, result = report_attribution(
                tree, load_ledger(args.ledger), load_snapshots(args.snapshots),
                args.target, args.runs, args.seed, args.world_spread)
            print(text)
            if args.write:
                path = write_attribution(result, args.attribution)
                print(f"\nAttribution for {result['snapshot']} written to {path}.")
            return 0
    except TreeError as e:
        print(str(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
