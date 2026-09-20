#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ into headline numbers.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/compute.py validate            check the tree against docs/node-schema.md
    python3 scripts/compute.py shape               print the tree's shape (counts, tiers, leaves)
    python3 scripts/compute.py run [--runs N]      simulate the tree once per longevity scenario
    python3 scripts/compute.py run --world-spread 0   the same with nodes rolled independently
    python3 scripts/compute.py run --snapshot [LABEL]  the same, and write the run to data/snapshots/
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time
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
rates, the Contact Clause rungs and the decision comparison. Snapshots are the ledger's memory
(docs/ledger-plan.md); the history charts on the website are drawn from nothing else.

The script refuses to report numbers until every open world node has a probability for every
scenario, but "validate" and "shape" work on a tree with no numbers at all.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import random
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
    `forced` maps choice-node ids to True/False and overrides the current plan; any choice node
    not mentioned keeps its current-plan setting.
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
                  review_status: str = REVIEW_STATUS, commit: str | None = None) -> dict:
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
    """Every snapshot in the folder, oldest first, with any malformed one named plainly."""
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
                        choices=["validate", "shape", "run", "compare"])
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
                    commit=args.snapshot_commit,
                )
                path = write_snapshot(snapshot, args.snapshots)
                print(f"\nSnapshot {snapshot['key']} written to {path}, marked {snapshot['review_status']}.")
            return 0
        if args.command == "compare":
            print(report_compare(tree, args.runs, args.seed, args.world_spread))
            return 0
    except TreeError as e:
        print(str(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
