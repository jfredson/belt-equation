#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ and the changelog into JSON for the website.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json,
                                               snapshots.json, ledger.json, scans.json, story.json,
                                               reader.json,
                                               and the tree picture at site/public/tree.svg
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else
    python3 scripts/export.py --data DIR       read a different data folder (for tests)
    python3 scripts/export.py --scans DIR      read a different folder of scan records (for tests)

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
  from and the difference between the last two runs (ledger step 28);
- the ledger in data/ledger.toml, checked against its own rules and against the node records,
  with every figure on an entry filled in from the runs rather than read off the entry (step 30);
- the weekly scan records in data/scans/ (the Radar, docs/scan-plan.md), newest scan first,
  each item's factor, chain link and node page resolved from the node it names. Every scan
  file is validated first, and a file that breaks the rules stops the build exactly as a
  broken tree does;
- the reader grid the "Run it for yourself" page reads (website step 39): the tree played out
  once per five-year deadline across the range a reader's shifted window can fall in, plus one
  cell for no deadline at all. It is worked out here, in Python, so the browser never computes
  a probability of its own (docs/website-plan.md, decision 3). It changes nothing: the stored
  probabilities, the snapshots and the headline are all untouched by it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import compute  # noqa: E402  (the loader and validator, shared on purpose)

# The eight factors and the Contact Clause, in equation order, with the one-line meanings
# from README.md. The slug is the folder each factor gets on the site. The chain link is the
# plain-English name the home page gives that factor ("cheap launch", "bodies that hold up");
# the home page and the Radar page both read it from here, so the two cannot drift apart.
# The window (W) and the Contact Clause (C) are not links in the chain, because the window is
# the dial and the Contact Clause is never multiplied in; they carry a plain name anyway, so
# that a scan item on one of their nodes has something readable to be grouped under.
FACTORS = [
    {"letter": "W", "slug": "window", "chain_link": "time window", "name": "Window",
     "meaning": "That I am alive on the date in question."},
    {"letter": "L", "slug": "launch", "chain_link": "cheap launch", "name": "Launch",
     "meaning": "That the cost of putting mass into orbit falls below the threshold that makes everything else affordable."},
    {"letter": "E", "slug": "energy", "chain_link": "power off Earth", "name": "Energy",
     "meaning": "That cheap, abundant power exists off Earth, from fusion or an equivalent."},
    {"letter": "D", "slug": "drive", "chain_link": "fast ships", "name": "Drive",
     "meaning": "That propulsion puts the solar system within reach on human timescales."},
    {"letter": "B", "slug": "biology", "chain_link": "bodies that hold up", "name": "Biology",
     "meaning": "That humans can live, and eventually reproduce, in partial gravity and deep-space radiation."},
    {"letter": "M", "slug": "motive", "chain_link": "a reason to go", "name": "Motive",
     "meaning": "That there is an economic reason for large numbers of people to be out there."},
    {"letter": "R", "slug": "regime", "chain_link": "governments", "name": "Regime",
     "meaning": "That the political and legal conditions let a multi-decade build survive elections, downturns, and wars."},
    {"letter": "A", "slug": "access", "chain_link": "a seat for me", "name": "Access",
     "meaning": "That I personally have a pathway in, given my training, health, and career."},
    {"letter": "C", "slug": "contact", "chain_link": "the Contact Clause", "name": "Contact Clause",
     "meaning": "That we meet a mind that is not ours, whether a machine that has outgrown us or something of non-human origin. The dream underneath the project, published beside the equation and never multiplied into it."},
]
CHAIN_LINK_BY_LETTER = {f["letter"]: f["chain_link"] for f in FACTORS}
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
            "resolved_links": [str(u) for u in (n.get("resolved_links", []) or [])],
            "superseded_by": n.get("superseded_by"),
            "revisions": plain(n.get("revisions", []) or []),
            "verify": list(n.get("verify", []) or []),
            "watch": [one_paragraph(t) for t in (n.get("watch", []) or [])],
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
        # The Contact Clause as its sibling branches (2026-09-25, when C5 was added): C4 above C3,
        # and C5 above C2 and C1. Each rung carries its depth on the branch so the page can indent
        # it under the rung it depends on. Beside the equation, never multiplied into it.
        "contact_branches": [
            {"top": b["top"], "name": b["name"],
             "rungs": [{**ref(r), "depth": i} for i, r in enumerate(b["rungs"])]}
            for b in compute.contact_branches(tree)
        ],
        "numbers": export_numbers(tree),
    }


# Was shown beside the headline until the outside-model review (roadmap step 27) was complete.
# Empty since 2026-09-20, when the rulings landed, so the label no longer appears.
NUMBERS_REVIEW_STATUS = ""


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
    joint = dict(chain_nodes)
    joint.update(compute.second_number_joint())
    results = {k: compute.simulate(tree, k, runs, rng, joint=joint) for k in keys}
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
        # The second number beside the headline (step 27, item 95): A2 at Tier 1, a rotation at a
        # station or lunar base, with the nodes it is computed from so the page can say so.
        "a2_at_tier1": {k: results[k]["joint"][compute.SECOND_NUMBER_KEY] for k in keys},
        "a2_at_tier1_nodes": list(compute.SECOND_NUMBER_NODES),
    }


def export_reader(tree: dict) -> dict:
    """The grid behind the "Run it for yourself" page (website step 39), or a plain reason why not.

    One cell per five-year deadline across the range a reader's shifted window can land in, plus
    a cell for no deadline at all. Each cell holds every tier's rate at that deadline and, per
    route, the world's part of a reader's odds. The page reads between the two cells either side
    of a reader's deadline and multiplies in whatever number the reader supplies for their own
    part; it never works out a probability of its own.
    """
    missing = compute.missing_probabilities(tree)
    if missing:
        return {
            "available": False,
            "reason": (f"{len(missing)} open world node(s) have no probability yet, so the tree "
                       "cannot be played out for a reader either."),
        }
    grid = compute.reader_grid(tree)
    grid["available"] = True
    grid["computed_on"] = dt.date.today().isoformat()
    grid["review_status"] = NUMBERS_REVIEW_STATUS
    return grid


# ------------------------------------------------------------ the story: worklog and roadmap


STORY_TYPES = {"decision": "Decision", "progress": "Progress", "session-summary": "Session",
               "idea": "Idea"}
STORY_STATUS = {"done": "done", "in_progress": "in progress", "todo": "to do", "waiting": "waiting"}


def export_story(folder: Path) -> dict:
    """The project's own story, from TimeAssembler, as the story page shows it (website step 24).

    TimeAssembler is where the project's day-by-day record lives: a worklog of decisions,
    progress and session summaries, and the roadmap as an ordered task list. The website plan
    (decision 5) had the export fetch both at build time with a key kept on the Mac; the build
    moved to GitHub Actions on 2026-09-19, so instead a snapshot of each is committed under
    data/story/ (worklog.json, roadmap.json) and refreshed by whichever session logs to
    TimeAssembler, using its tools, until TimeAssembler has a public read-only endpoint for one
    project's story (the alternative the plan named). The page shows the date the snapshot was
    taken. Either file may be absent, in which case its section is left off the page."""
    out: dict = {"worklog": None, "roadmap": None}
    wl = folder / "worklog.json"
    if wl.exists():
        data = json.loads(wl.read_text())
        entries = []
        for e in data.get("entries", []):
            entries.append({
                "date": e["date"],
                "type": e["type"],
                "type_label": STORY_TYPES.get(e["type"], e["type"]),
                "decided_by": e.get("decided_by"),
                "title": e["title"],
            })
        days: dict[str, list] = {}
        for e in entries:
            days.setdefault(e["date"], []).append(e)
        out["worklog"] = {
            "fetched_on": data.get("fetched_on"),
            "source": data.get("source"),
            "count": len(entries),
            "by_type": {t: sum(1 for e in entries if e["type"] == t) for t in STORY_TYPES},
            "days": [{"date": d, "entries": days[d]} for d in sorted(days, reverse=True)],
        }
    rm = folder / "roadmap.json"
    if rm.exists():
        data = json.loads(rm.read_text())
        steps = sorted(data.get("steps", []), key=lambda s: s["order"])
        for s_ in steps:
            s_["status_label"] = STORY_STATUS.get(s_["status"], s_["status"])
        done = sum(1 for s_ in steps if s_["status"] == "done")
        out["roadmap"] = {
            "fetched_on": data.get("fetched_on"),
            "source": data.get("source"),
            "count": len(steps),
            "done": done,
            "up_next": [s_ for s_ in steps if s_["status"] != "done"][:6],
            "steps": steps,
        }
    return out


# ------------------------------------------------------------ the tree picture


def write_tree_picture(tree: dict, numbers: dict, path: Path) -> None:
    """The whole tree as one SVG at site/public/tree.svg (website step 22, 2026-09-20).

    Drawn by scripts/visual.py from the same tree and the same run the site's numbers come from,
    so the picture on the site can never disagree with the pages beside it. Written on every
    export rather than committed, like the JSON; docs/visual/ keeps the dated copies that
    roadmap step 13 asks for. Skipped, with a line saying so, when the tree has no numbers yet."""
    if not numbers.get("available"):
        print(f"No tree picture written to {path}: {numbers.get('reason')}")
        return
    import visual  # beside this file; imported here so --check never needs it
    keys = [s["key"] for s in tree["scenarios"]]
    results = {k: {"tiers": {t: numbers["tiers"][t][k] for t in numbers["tiers"]}} for k in keys}
    svg = visual.render(tree, results, numbers["runs"], numbers["computed_on"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    print(f"Tree picture written to {path}: {len(tree['nodes'])} nodes.")


# ------------------------------------------------------------ the snapshots


def export_snapshots(snapshots: list[dict]) -> dict:
    """The committed runs from data/snapshots/, turned into what the pages need.

    Each snapshot is the complete output of one run (scripts/compute.py, ledger step 28). The
    site never recomputes history: the chart on the ledger page, the gate-rate chart on each
    factor page and the "since the last run" arrows on the home page all read this and nothing
    else. The per-node table of every past run stays in the repository rather than the site's
    JSON, which would grow without limit; only the latest run carries its full node table."""
    summaries = []
    for s in snapshots:
        summaries.append({k: s.get(k) for k in (
            "key", "date", "label", "note", "review_status", "headline_tier",
            "run", "tiers", "chain", "chain_nodes", "second", "contact", "decisions",
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

    # How far a figure from the latest run can move for no reason but the dice. The watch lists
    # and the worth lines are differences between runs of the same size, so this is the band below
    # which one of their figures is not worth reading.
    noise = None
    if latest:
        noise = compute.run_noise(latest.get("tiers", {}).get(compute.HEADLINE_TIER, {}),
                                  latest.get("run", {}).get("runs") or 1)

    return {
        "count": len(snapshots),
        "headline_tier": compute.HEADLINE_TIER,
        "latest_key": latest["key"] if latest else None,
        "noise": noise,
        "snapshots": summaries,
        "latest": latest,
        "series": {
            "tiers": {k: series(lambda s, k=k: s.get("tiers", {}).get(k)) for k in tier_keys},
            "chain": {k: series(lambda s, k=k: s.get("chain", {}).get(k)) for k in chain_keys},
        },
        "change": change,
    }


# ---------------------------------------------------------------- the ledger


# The six kinds an entry can have, with the plain meaning the site shows beside the filter.
# The table this comes from, and the reasoning for six rather than two, are in
# docs/ledger-plan.md ("The two rules that keep it honest", and decision 5).
LEDGER_KINDS = [
    {"key": "event", "label": "Something happened",
     "meaning": "Something happened in the world and a link of the chain moved because of it. "
                "It cites a public record."},
    {"key": "resolution", "label": "Settled",
     "meaning": "A step the tree was waiting on is now settled, one way or the other. These are "
                "what the project's own forecasting record is later scored against."},
    {"key": "revision", "label": "Changed my mind",
     "meaning": "A number or the reasoning behind it changed with no new event: an outside "
                "review, a reconsideration, or a correction."},
    {"key": "structure", "label": "The tree itself changed",
     "meaning": "The tree changed shape, or the way it is played out changed: a step added, cut "
                "or rewired, a requirement moved, a criterion reworded. Numbers either side of "
                "one of these are not a like-for-like comparison, and the site says so."},
    {"key": "decision", "label": "A choice made",
     "meaning": "John took or changed a choice of his own, or the plan at a fork changed."},
    {"key": "held-steady", "label": "Widely reported, moved nothing",
     "meaning": "Something widely reported happened and no number moved. It names the steps it "
                "was read against and says why none of them counted."},
]
KIND_KEYS = {k["key"] for k in LEDGER_KINDS}

# Which fields each kind must carry, beyond the ones every entry carries (id, date, kind, title,
# body, snapshot). `nodes` is not required of a structural entry: moving a tier requirement or
# changing how the tree is played out touches no node's record, and three of the four structural
# entries of 2026-09-19 are of exactly that sort.
REQUIRED_OF_EVERY = ["id", "date", "kind", "title", "body", "snapshot"]
NEEDS_SOURCE = {"event", "resolution", "held-steady"}
NEEDS_OCCURRED_ON = {"event", "resolution"}
NEEDS_NODES = {"event", "resolution", "revision", "decision"}


def validate_ledger(entries: list[dict], tree: dict, snapshots: list[dict]) -> list[str]:
    """Every way this ledger breaks its own rules, in plain language. Empty means it is sound.

    The rule that matters most is the last one: every node an entry names must carry, on its own
    record, a revision or a resolution dated in the stretch between the previous run and this
    entry. That is what stops the ledger and the node records drifting apart, and it was the real
    risk of keeping the story in a file of its own (docs/ledger-plan.md, decision 1)."""
    problems: list[str] = []
    node_ids = {n["id"] for n in tree["nodes"]}
    snapshot_dates = {s["key"]: s["date"] for s in snapshots}
    seen_ids: set[str] = set()
    last_date = ""
    last_snapshot_date = ""

    for i, e in enumerate(entries):
        eid = plain(e.get("id")) or f"(the entry in position {i + 1}, which has no id)"
        where = f"ledger entry {eid}"
        for f in REQUIRED_OF_EVERY:
            if f not in e or e[f] in ("", None):
                problems.append(f"{where}: missing the required field '{f}'")
        kind = e.get("kind")
        if kind not in KIND_KEYS:
            problems.append(f"{where}: kind must be one of {', '.join(sorted(KIND_KEYS))}")
        if "id" in e:
            if eid in seen_ids:
                problems.append(f"{where}: this id is used by more than one entry")
            seen_ids.add(eid)
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", eid):
                problems.append(f"{where}: an id is a date and a short dash-separated slug, "
                                "like 2026-09-27-the-ship-came-back")
        date = plain(e.get("date"))
        if date and eid.startswith("2") and not eid.startswith(str(date)):
            problems.append(f"{where}: its id begins with a different date from its 'date' field ({date})")
        if date and date < last_date:
            problems.append(f"{where}: entries are appended newest last, and this one is dated "
                            f"{date}, before the entry above it ({last_date})")
        last_date = date or last_date

        if kind in NEEDS_SOURCE and not str(e.get("source", "")).strip():
            problems.append(f"{where}: a '{kind}' entry has to name the public record that settles "
                            "what happened")
        if kind in NEEDS_OCCURRED_ON and not plain(e.get("occurred_on")):
            problems.append(f"{where}: a '{kind}' entry has to say when the thing happened in the "
                            "world, in its 'occurred_on' field")
        nodes = list(e.get("nodes", []) or [])
        checked = list(e.get("checked_against", []) or [])
        if kind in NEEDS_NODES and not nodes:
            problems.append(f"{where}: a '{kind}' entry has to list the steps of the tree it changed")
        if kind == "held-steady":
            if nodes:
                problems.append(f"{where}: a 'held-steady' entry changed nothing, so it lists the "
                                "steps it was read against in 'checked_against', not in 'nodes'")
            if not checked:
                problems.append(f"{where}: a 'held-steady' entry has to name the steps whose "
                                "criteria the event was read against")
        elif checked:
            problems.append(f"{where}: 'checked_against' belongs only on a 'held-steady' entry")
        for nid in nodes + checked:
            if nid not in node_ids:
                problems.append(f"{where}: names '{nid}', which is not a step in the tree")
        if e.get("watch_ref") and e["watch_ref"] not in node_ids:
            problems.append(f"{where}: its watch_ref names '{e['watch_ref']}', which is not a step "
                            "in the tree")
        if e.get("corrects"):
            if plain(e["corrects"]) not in seen_ids:
                problems.append(f"{where}: it corrects '{plain(e['corrects'])}', which is not an "
                                "earlier entry in this file")
        if e.get("author") is not None and not str(e["author"]).strip():
            problems.append(f"{where}: 'author' is either left out, meaning John wrote it, or says "
                            "who did; it cannot be empty")

        snap = plain(e.get("snapshot"))
        if snap and snap not in snapshot_dates:
            problems.append(f"{where}: it says it landed in the run '{snap}', and there is no such "
                            "run in data/snapshots/")
            continue
        if not snap:
            continue
        if snapshot_dates[snap] < last_snapshot_date:
            problems.append(f"{where}: it landed in the run '{snap}', which is older than the run "
                            "the entry above it landed in")
        last_snapshot_date = snapshot_dates[snap]

        # The cross-check: what the entry says it changed must be on the node's own record.
        before = compute.previous_snapshot(snapshots, snap)
        since = before["date"] if before else None
        until = date or snapshot_dates[snap]
        by_id = {n["id"]: n for n in tree["nodes"]}
        for nid in nodes:
            if nid not in by_id:
                continue
            node = by_id[nid]
            dates = [plain(r.get("date")) for r in (node.get("revisions", []) or [])]
            if node.get("resolved_on"):
                dates.append(plain(node["resolved_on"]))
            if not any(d and (since is None or d >= since) and d <= until for d in dates):
                problems.append(
                    f"{where}: it says it changed '{nid}', but that step's own record carries no "
                    f"revision and no resolution dated between the previous run and {until}. Either "
                    "the node record is missing the change or the entry names the wrong step."
                )
    return problems


def load_attribution(folder: Path) -> dict:
    """The stored answer to "how much of each run's move came from which entry", per run.

    Attribution is worked out by the compute script (`attribute <run> --write`) and committed
    beside the run it belongs to, for the same reason the run itself is: so the site never
    recomputes its own history at build time, and a page renders in a second rather than in
    minutes of playing the tree out (docs/ledger-plan.md, decision 2)."""
    if not folder.exists():
        return {}
    out = {}
    for path in sorted(folder.glob("*.json")):
        out[path.stem] = json.loads(path.read_text())
    return out


def export_ledger(entries: list[dict], tree: dict, snapshots: list[dict], attribution: dict) -> dict:
    """The ledger with every figure filled in from the runs and the node records.

    Nothing here is read off an entry: an entry says what happened in words and names the steps it
    touched, and the numbers beside it — each step's rate before and after, the headline on either
    side, and the entry's own contribution — come from the committed runs."""
    by_id = {n["id"]: n for n in tree["nodes"]}
    snapshot_by_key = {s["key"]: s for s in snapshots}
    gates = compute.chain_gates(tree)
    factor_name = {f["letter"]: f for f in FACTORS}

    def rates(snapshot: dict | None, nid: str):
        return (snapshot or {}).get("nodes", {}).get(nid)

    out_entries = []
    for e in entries:
        snap = snapshot_by_key.get(plain(e.get("snapshot")))
        before = compute.previous_snapshot(snapshots, snap["key"]) if snap else None
        nodes = list(e.get("nodes", []) or [])
        checked = list(e.get("checked_against", []) or [])
        touched = nodes or checked
        letters = sorted({by_id[n]["factor"] for n in touched if n in by_id})

        node_changes = []
        for nid in touched:
            n = by_id.get(nid)
            if not n:
                continue
            node_changes.append({
                "id": nid,
                "name": n["name"],
                "factor": n["factor"],
                "factor_slug": SLUG_BY_LETTER[n["factor"]],
                "path": f"/tree/{SLUG_BY_LETTER[n['factor']]}/{nid}/",
                "status": n["status"],
                "before": rates(before, nid),
                "after": rates(snap, nid),
            })

        headline_tier = compute.HEADLINE_TIER
        after = (snap or {}).get("tiers", {}).get(headline_tier)
        was = (before or {}).get("tiers", {}).get(headline_tier)
        change = {k: round(after[k] - was[k], 6) for k in after} if (after and was) else None

        stored = attribution.get(snap["key"], {}) if snap else {}
        mine = next((r for r in stored.get("entries", []) if r["id"] == plain(e["id"])), None)

        watch = None
        if e.get("watch_ref"):
            worth = ((before or {}).get("worth") or {}).get("nodes", {}).get(e["watch_ref"])
            watch = {
                "node": e["watch_ref"],
                "name": by_id[e["watch_ref"]]["name"] if e["watch_ref"] in by_id else e["watch_ref"],
                "path": (f"/tree/{SLUG_BY_LETTER[by_id[e['watch_ref']]['factor']]}/{e['watch_ref']}/"
                         if e["watch_ref"] in by_id else None),
                "predicted": (worth or {}).get("if_yes"),
                "predicted_at": before["key"] if before else None,
            }

        out_entries.append({
            "id": plain(e["id"]),
            "date": plain(e.get("date")),
            "occurred_on": plain(e.get("occurred_on")),
            "kind": e.get("kind"),
            "title": one_paragraph(e.get("title")),
            "body": one_paragraph(e.get("body")),
            "source": one_paragraph(e.get("source")) or None,
            "author": e.get("author"),
            "nodes": nodes,
            "checked_against": checked,
            "node_changes": node_changes,
            "factors": [{"letter": l, "name": factor_name[l]["name"], "slug": factor_name[l]["slug"]}
                        for l in letters],
            "links": [l for l in letters if l in gates],
            "snapshot": plain(e.get("snapshot")),
            "snapshot_date": snap["date"] if snap else None,
            "previous_snapshot": before["key"] if before else None,
            "headline_before": was,
            "headline_after": after,
            "headline_change": change,
            "contribution": mine.get("contribution") if mine and mine.get("separable") else None,
            "headline_without": mine.get("headline_without") if mine and mine.get("separable") else None,
            "separable": bool(mine and mine.get("separable")),
            "not_separable_why": None if not mine or mine.get("separable") else mine.get("why"),
            "attributed": mine is not None,
            "watch": watch,
            "run_note": e.get("run_note"),
            "corrects": plain(e.get("corrects")),
        })

    newest_first = list(reversed(out_entries))
    by_kind: dict[str, int] = defaultdict(int)
    by_author: dict[str, int] = defaultdict(int)
    for e in out_entries:
        by_kind[e["kind"]] += 1
        by_author[e["author"] or "john"] += 1

    return {
        "count": len(out_entries),
        "headline_tier": compute.HEADLINE_TIER,
        "kinds": LEDGER_KINDS,
        "entries": newest_first,
        "totals": {"by_kind": dict(by_kind), "by_author": dict(by_author)},
        "movers": ledger_movers(newest_first),
        "runs": ledger_runs(newest_first, snapshots, attribution),
    }


def ledger_movers(entries: list[dict]) -> list[dict]:
    """The year's biggest movers, and beside them the ones that changed nothing.

    Ranked under the headline's default scenario, which is the first one scenarios.toml lists.
    An entry whose contribution could not be worked out separately is listed with the reason
    rather than left out, and one that was written precisely because nothing moved is listed as
    what it is (docs/ledger-plan.md, "Movers")."""
    years: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        years[(e["date"] or "")[:4]].append(e)
    out = []
    for year in sorted(years, reverse=True):
        rows = []
        for e in years[year]:
            first = next(iter(e["contribution"]), None) if e["contribution"] else None
            rows.append({
                "id": e["id"], "title": e["title"], "kind": e["kind"], "date": e["date"],
                "author": e["author"], "links": e["links"],
                "contribution": e["contribution"],
                "sort_by": abs(e["contribution"][first]) if first else -1.0,
                "moved_nothing": e["kind"] == "held-steady",
                "not_separable_why": e["not_separable_why"],
            })
        rows.sort(key=lambda r: (-r["sort_by"], r["id"]))
        out.append({"year": year, "rows": rows})
    return out


def ledger_runs(entries: list[dict], snapshots: list[dict], attribution: dict) -> list[dict]:
    """One row per run that the ledger has entries for: what the run moved in total, how much of
    that was pinned on particular entries, and what was left over. The leftover is reported rather
    than hidden: changes made in the same run interact, and some cannot be undone one at a time."""
    out = []
    for snapshot in reversed(snapshots):
        mine = [e for e in entries if e["snapshot"] == snapshot["key"]]
        if not mine:
            continue
        stored = attribution.get(snapshot["key"], {})
        out.append({
            "key": snapshot["key"],
            "date": snapshot["date"],
            "label": snapshot.get("label"),
            "note": snapshot.get("note"),
            "review_status": snapshot.get("review_status"),
            "previous": stored.get("previous_snapshot"),
            "runs": stored.get("runs"),
            "noise": stored.get("noise"),
            "total_move": stored.get("total_move"),
            "attributed": stored.get("attributed"),
            "remainder": stored.get("remainder"),
            "unseparated": stored.get("unseparated", []),
            "entries": [e["id"] for e in mine],
        })
    return out


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


# --------------------------------------------------- the scans (the Radar)
#
# Every week a fresh session reads each open world node against the news and writes one record
# to data/scans/, one file per scan, appended and never edited (docs/scan-plan.md, step 34;
# the procedure the session follows is docs/scan-procedure.md). These functions are the gate
# between that folder and the website: a record that breaks a rule stops the build, exactly as
# a broken tree does, so the site can never show a scan that does not add up.

VERDICTS = ["quiet", "noted", "moved", "resolved", "flagged"]
SCAN_SCOPES = {"weekly", "monthly"}
SCAN_FIELDS = ["date", "ran_at", "scope", "nodes_checked", "searches", "commit_before"]
SCAN_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})(-\d+)?$")
LEDGER_ID = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")


def validate_watch_terms(tree: dict) -> list[str]:
    """Check the optional `watch` list on a node (docs/node-schema.md).

    A watch list is extra search terms the weekly scan adds to the ones it composes from the
    node's own name, criterion and source: a project name or a term of art that the plain
    reading would miss. The compute script does not know the field, so it is checked here."""
    problems: list[str] = []
    for n in tree["nodes"]:
        if "watch" not in n:
            continue
        where = f"{n['_file']} node {n.get('id', '(no id)')}"
        terms = n["watch"]
        if not isinstance(terms, list) or not terms:
            problems.append(f"{where}: 'watch' must be a list holding at least one search term")
            continue
        for t in terms:
            if not isinstance(t, str) or not t.strip():
                problems.append(f"{where}: every term in 'watch' must be a line of text with something in it")
    return problems


def load_ledger(ledger_path: Path) -> tuple[list[dict], list[str]]:
    """The ledger entries, when the ledger exists. Read only; this script never writes it.

    The ledger (docs/ledger-plan.md, steps 28 to 30) may not be built yet. An absent file is
    not a problem: a scan that moves a number before the ledger lands says so in its commit
    message and carries the verdict in its own record."""
    if not ledger_path.exists():
        return [], []
    try:
        return tomllib.loads(ledger_path.read_text()).get("entry", []), []
    except tomllib.TOMLDecodeError as e:
        return [], [f"{ledger_path.name}: cannot be read as TOML: {e}"]


def load_scans(scans_dir: Path) -> tuple[list[dict], list[str]]:
    """Read every scan record in the folder. Returns the raw records and what could not be read."""
    scans: list[dict] = []
    problems: list[str] = []
    if not scans_dir.exists():
        return scans, problems
    for path in sorted(scans_dir.glob("*.toml")):
        where = f"{scans_dir.name}/{path.name}"
        m = SCAN_NAME.match(path.stem)
        if not m:
            problems.append(f"{where}: the file name must be the scan's date, YYYY-MM-DD.toml, "
                            "with -2 on a second scan the same day")
            continue
        try:
            raw = dict(tomllib.loads(path.read_text()))
        except tomllib.TOMLDecodeError as e:
            problems.append(f"{where}: cannot be read as TOML: {e}")
            continue
        raw["_file"] = path.name
        raw["_where"] = where
        raw["_name_date"] = m.group(1)
        scans.append(raw)
    return scans, problems


def validate_scans(scans: list[dict], node_ids: set[str], ledger_ids: set[str],
                   ledger_exists: bool) -> tuple[list[str], list[str]]:
    """Check every scan record against the rules in docs/scan-plan.md.

    Returns the problems (which stop the build) and the notes (which are printed and do not).
    The rules: the file name is the scan's own date; the [scan] table carries its six fields
    and a scope of weekly or monthly; every item names a node that exists in the tree, once
    per scan; every verdict is one of the five; every item names at least one search it ran,
    unless it is `quiet` and `found` says why no search was run; every verdict but `quiet`
    cites a source;
    a `flagged` item says what it would have done; and a ledger entry named by an item both
    reads like a ledger id and, once the ledger exists, is in it."""
    problems: list[str] = []
    notes: list[str] = []
    for raw in scans:
        where = raw["_where"]
        scan = raw.get("scan")
        if not isinstance(scan, dict):
            problems.append(f"{where}: no [scan] table, so the record says nothing about when it ran")
            continue
        for field in SCAN_FIELDS:
            if scan.get(field) in (None, ""):
                problems.append(f"{where}: the [scan] table is missing '{field}'")
        if "date" in scan and str(plain(scan["date"])) != raw["_name_date"]:
            problems.append(f"{where}: the date in the record ({plain(scan['date'])}) is not the date "
                            f"in the file name ({raw['_name_date']})")
        if "scope" in scan and scan["scope"] not in SCAN_SCOPES:
            problems.append(f"{where}: scope must be 'weekly' (the leaves) or 'monthly' (every node), "
                            f"not {scan['scope']!r}")
        if "test" in scan and not isinstance(scan["test"], bool):
            problems.append(f"{where}: 'test' marks a made-up record and must be true or false")

        items = raw.get("item") or []
        if not items:
            problems.append(f"{where}: a scan record needs at least one [[item]]")
        if isinstance(scan.get("nodes_checked"), int) and items and scan["nodes_checked"] != len(items):
            problems.append(f"{where}: the [scan] table says {scan['nodes_checked']} nodes were checked "
                            f"and the record holds {len(items)} item(s)")

        seen: set[str] = set()
        for i, item in enumerate(items, 1):
            nid = item.get("node")
            iwhere = f"{where} item {i} ({nid or 'no node named'})"
            if not nid:
                problems.append(f"{iwhere}: every item names the node it checked")
            elif nid not in node_ids:
                problems.append(f"{iwhere}: no node in the tree has this id")
            elif nid in seen:
                problems.append(f"{iwhere}: this node is checked twice in the same scan")
            if nid:
                seen.add(nid)

            verdict = item.get("verdict")
            if verdict not in VERDICTS:
                problems.append(f"{iwhere}: the verdict must be one of {', '.join(VERDICTS)}, not {verdict!r}")
            if not one_paragraph(item.get("found")):
                problems.append(f"{iwhere}: 'found' says in plain English what the past week held, "
                                "and is required on every verdict")
            queries = item.get("queries")
            # Some nodes have nothing of their own to search for: they resolve only when one of
            # the nodes they depend on resolves, and those were checked as their own items in the
            # same scan. Such an item may leave 'queries' empty, but only when the verdict is
            # 'quiet' and 'found' says why no search was run. Every other verdict names a search.
            no_search_allowed = verdict == "quiet" and bool(one_paragraph(item.get("found")))
            if not isinstance(queries, list) or any(not str(q).strip() for q in queries):
                problems.append(f"{iwhere}: 'queries' lists the searches that were run, "
                                "each one a line of text")
            elif not queries and not no_search_allowed:
                problems.append(f"{iwhere}: 'queries' lists the searches that were run, at least one. "
                                "Only a 'quiet' item may leave it empty, and then 'found' has to say "
                                "why no search was run")
            sources = item.get("sources") or []
            if not isinstance(sources, list) or any(not str(s).strip() for s in sources):
                problems.append(f"{iwhere}: 'sources' must be a list of public records")
            elif verdict in ("noted", "moved", "resolved", "flagged") and not sources:
                problems.append(f"{iwhere}: a verdict of '{verdict}' has to cite the record it read; "
                                "only 'quiet' may go without a source")
            if verdict == "resolved" and len(sources) < 2:
                problems.append(f"{iwhere}: a node resolves only when two independent public records agree, "
                                "so 'sources' lists both")
            if verdict == "flagged" and not one_paragraph(item.get("for_john")):
                problems.append(f"{iwhere}: a flagged item needs 'for_john': the move it would have made, "
                                "and why it was not the scanner's to make")

            led = item.get("ledger")
            if led is None:
                if verdict in ("moved", "resolved") and ledger_exists:
                    notes.append(f"{iwhere}: a '{verdict}' item with no ledger entry named.")
            elif not isinstance(led, str) or not LEDGER_ID.match(led):
                problems.append(f"{iwhere}: a ledger entry id reads as a date and a short slug, "
                                f"like 2026-09-27-ship-caught, not {led!r}")
            elif not ledger_exists:
                notes.append(f"{iwhere}: names the ledger entry '{led}'. The ledger "
                             "(data/ledger.toml) does not exist yet, so it cannot be checked.")
            elif led not in ledger_ids:
                problems.append(f"{iwhere}: names the ledger entry '{led}', "
                                "which is not in data/ledger.toml")
    return problems, notes


def export_scans(tree: dict, scans_dir: Path, ledger_path: Path) -> tuple[dict, list[str], list[str]]:
    """Validate data/scans/ and turn it into what the site reads (site/src/data/scans.json).

    Newest scan first. Each item carries the node it checked with its name, its factor, the
    chain link that factor is on and the address of its page, so the Radar page can group the
    week's work the way the home page reads. Alongside the scans: `by_node`, every node's own
    checks newest first, which is what a node page shows above its revisions; and
    `waiting_on_john`, the flagged items nothing has picked up yet. A flagged item counts as
    picked up when a later scan checks that node again or a later ledger entry names it."""
    by_id = {n["id"]: n for n in tree["nodes"]}
    raw_scans, problems = load_scans(scans_dir)
    ledger_entries, ledger_problems = load_ledger(ledger_path)
    problems += ledger_problems
    ledger_ids = {e.get("id") for e in ledger_entries if e.get("id")}
    rule_problems, notes = validate_scans(raw_scans, set(by_id), ledger_ids, ledger_path.exists())
    problems += rule_problems
    if problems:
        return {}, problems, notes

    out_scans = []
    for raw in raw_scans:
        scan = raw["scan"]
        items = []
        for item in raw.get("item", []):
            node = by_id[item["node"]]
            slug = SLUG_BY_LETTER[node["factor"]]
            led = item.get("ledger")
            items.append({
                "node": node["id"],
                "node_name": node["name"],
                "factor": node["factor"],
                "factor_slug": slug,
                "chain_link": CHAIN_LINK_BY_LETTER[node["factor"]],
                "path": f"/tree/{slug}/{node['id']}/",
                "verdict": item["verdict"],
                "queries": [one_paragraph(q) for q in item.get("queries", []) or []],
                "found": one_paragraph(item.get("found")),
                "sources": [str(s).strip() for s in (item.get("sources") or [])],
                # The ledger page arrives with ledger plan step 31; until the entry exists there
                # is nothing to link to, and the site says so rather than offering a dead link.
                "ledger": None if led is None else {
                    "id": led,
                    "written": led in ledger_ids,
                    "path": f"/story/#{led}" if led in ledger_ids else None,
                },
                "for_john": one_paragraph(item.get("for_john")) or None,
            })
        out_scans.append({
            "date": plain(scan["date"]),
            "ran_at": plain(scan["ran_at"]),
            "scope": scan["scope"],
            "nodes_checked": scan["nodes_checked"],
            "searches": scan["searches"],
            "commit_before": scan["commit_before"],
            "test": bool(scan.get("test")),
            "file": raw["_file"],
            "counts": {v: sum(1 for it in items if it["verdict"] == v) for v in VERDICTS},
            "items": items,
        })
    out_scans.sort(key=lambda s: (s["date"], s["file"]), reverse=True)

    by_node: dict[str, list[dict]] = defaultdict(list)
    for s in out_scans:
        for it in s["items"]:
            by_node[it["node"]].append({
                "date": s["date"], "scope": s["scope"], "test": s["test"], "file": s["file"],
                "verdict": it["verdict"], "found": it["found"], "sources": it["sources"],
                "ledger": it["ledger"], "for_john": it["for_john"],
            })

    waiting = []
    for s in out_scans:
        for it in s["items"]:
            if it["verdict"] != "flagged":
                continue
            checked_again = any(
                later["date"] > s["date"] and any(x["node"] == it["node"] for x in later["items"])
                for later in out_scans)
            in_ledger = any(
                str(plain(e.get("date", ""))) > s["date"]
                and it["node"] in ((e.get("nodes") or []) + (e.get("checked_against") or []))
                for e in ledger_entries)
            if not (checked_again or in_ledger):
                waiting.append({"scan_date": s["date"], "scan_file": s["file"], "test": s["test"], **it})

    return {
        "exported_on": dt.date.today().isoformat(),
        "scans": out_scans,
        "waiting_on_john": waiting,
        "by_node": dict(by_node),
        "counts": {
            "scans": len(out_scans),
            "real_scans": sum(1 for s in out_scans if not s["test"]),
            "test_scans": sum(1 for s in out_scans if s["test"]),
            "items": sum(len(s["items"]) for s in out_scans),
            "waiting_on_john": len(waiting),
        },
    }, problems, notes


# ------------------------------------------------------------------ main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    parser.add_argument("--changelog", type=Path, default=ROOT / "CHANGELOG.md")
    parser.add_argument("--snapshots", type=Path, default=ROOT / "data" / "snapshots")
    parser.add_argument("--ledger", type=Path, default=ROOT / "data" / "ledger.toml")
    parser.add_argument("--attribution", type=Path, default=ROOT / "data" / "attribution")
    parser.add_argument("--scans", type=Path, default=ROOT / "data" / "scans")
    parser.add_argument("--out", type=Path, default=ROOT / "site" / "src" / "data")
    parser.add_argument("--story", type=Path, default=ROOT / "data" / "story",
                        help="the committed TimeAssembler snapshots the story page reads (website step 24)")
    parser.add_argument("--svg", type=Path, default=ROOT / "site" / "public" / "tree.svg",
                        help="where the tree picture is written (website step 22); the site serves it at /tree.svg")
    parser.add_argument("--check", action="store_true", help="validate and count, write nothing")
    args = parser.parse_args(argv)

    try:
        tree = compute.load_tree(args.data)
        problems = compute.validate(tree) + validate_watch_terms(tree)
        if problems:
            print(f"Nothing exported: the tree in {args.data} breaks the schema in {len(problems)} place(s):")
            for p in problems:
                print("  -", p)
            return 1
        scans, scan_problems, scan_notes = export_scans(tree, args.scans, args.ledger)
        if scan_problems:
            print(f"Nothing exported: the scan records in {args.scans} break the rules in "
                  f"{len(scan_problems)} place(s):")
            for p in scan_problems:
                print("  -", p)
            return 1
        exported = export_tree(tree)
        changelog = export_changelog(args.changelog)
        all_snapshots = compute.load_snapshots(args.snapshots)
        snapshots = export_snapshots(all_snapshots)
        entries = compute.load_ledger(args.ledger)
        broken = validate_ledger(entries, tree, all_snapshots)
        if broken:
            print(f"Nothing exported: the ledger in {args.ledger} breaks its own rules "
                  f"in {len(broken)} place(s):")
            for p in broken:
                print("  -", p)
            return 1
        ledger = export_ledger(entries, tree, all_snapshots, load_attribution(args.attribution))
        story = export_story(args.story)
        reader = export_reader(tree)
    except (compute.TreeError, OSError) as e:
        print(f"Nothing exported: {e}")
        return 1

    c = exported["counts"]
    s = scans["counts"]
    scan_line = (f"{s['scans']} scan record(s) holding {s['items']} node check(s)"
                 + (f", {s['test_scans']} of them test records" if s["test_scans"] else "")
                 + (f", {s['waiting_on_john']} item(s) waiting on John" if s["waiting_on_john"] else ""))
    summary = (f"{c['nodes']} nodes ({c['with_probability']} with probabilities, {c['resolved']} resolved), "
               f"{len(exported['tiers'])} tiers, {len(exported['scenarios'])} scenarios, "
               f"{len(changelog['days'])} changelog day(s), {snapshots['count']} snapshot(s), "
               f"{ledger['count']} ledger entr{'y' if ledger['count'] == 1 else 'ies'}, {scan_line}")
    for note in scan_notes:
        print("Note:", note)
    if args.check:
        print(f"The tree and the scan records validate. Export would write: {summary}.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "tree.json").write_text(json.dumps(exported, indent=2, ensure_ascii=False) + "\n")
    (args.out / "changelog.json").write_text(json.dumps(changelog, indent=2, ensure_ascii=False) + "\n")
    (args.out / "snapshots.json").write_text(json.dumps(snapshots, indent=2, ensure_ascii=False) + "\n")
    (args.out / "ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    (args.out / "scans.json").write_text(json.dumps(scans, indent=2, ensure_ascii=False) + "\n")
    (args.out / "story.json").write_text(json.dumps(story, indent=2, ensure_ascii=False) + "\n")
    (args.out / "reader.json").write_text(json.dumps(reader, indent=2, ensure_ascii=False) + "\n")
    print(f"Exported {summary} to {args.out}.")
    write_tree_picture(tree, exported["numbers"], args.svg)
    if not exported["numbers"]["available"]:
        print("Headline numbers not exported: " + exported["numbers"]["reason"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
