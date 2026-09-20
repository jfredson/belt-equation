#!/usr/bin/env python3
"""The Belt Equation: turn the tree in data/ and the changelog into JSON for the website.

Plain Python, standard library only. Run from anywhere:

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, scans.json
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
- the weekly scan records in data/scans/ (the Radar, docs/scan-plan.md), newest scan first,
  each item's factor, chain link and node page resolved from the node it names. Every scan
  file is validated first, and a file that breaks the rules stops the build exactly as a
  broken tree does.
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
    {"letter": "W", "slug": "window", "chain_link": "how long I get", "name": "Window",
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
     "meaning": "The dream underneath the project, published beside the equation and never multiplied into it."},
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
    """The short commit the export ran from, read from .git without running git."""
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


def chain_gates(tree: dict) -> dict[str, list[str]]:
    """The home page's chain: per factor, the nodes the headline tier requires, directly or
    through the tiers it rests on (T3 under A2, T2 under T3, and so on). A link "holds" when
    every gate node of its factor holds in the same play-through; because each gate node
    already waits on its own dependencies, the link's rate counts those too. Factors with no
    gate node (W, whose job is done by the scenario, and C, never multiplied in) are left out."""
    tiers = {t["key"]: t for t in tree["tiers"]}
    by_id = {n["id"]: n for n in tree["nodes"]}
    seen: set[str] = set()
    stack = [compute.HEADLINE_TIER]
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
    return {f: sorted(gates[f]) for f in compute.FACTORS if f in gates}


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
    per scan; every verdict is one of the five; every verdict but `quiet` cites a source;
    a `flagged` item says what it would have done; and a ledger entry named by an item both
    reads like a ledger id and, once the ledger exists, is in it. A scan marked `test = true`
    is a fixture rather than a week of real work: its ledger references are allowed to point
    at entries that were never written, and that is reported as a note."""
    problems: list[str] = []
    notes: list[str] = []
    for raw in scans:
        where = raw["_where"]
        scan = raw.get("scan")
        if not isinstance(scan, dict):
            problems.append(f"{where}: no [scan] table, so the record says nothing about when it ran")
            continue
        is_test = bool(scan.get("test"))
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
            if not isinstance(queries, list) or not queries or any(not str(q).strip() for q in queries):
                problems.append(f"{iwhere}: 'queries' lists the searches that were run, at least one")
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
                message = f"{iwhere}: names the ledger entry '{led}', which is not in data/ledger.toml"
                if is_test:
                    notes.append(message + ". Allowed because this scan is marked a test.")
                else:
                    problems.append(message)
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
    parser.add_argument("--scans", type=Path, default=ROOT / "data" / "scans")
    parser.add_argument("--out", type=Path, default=ROOT / "site" / "src" / "data")
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
        scans, scan_problems, scan_notes = export_scans(tree, args.scans, args.data / "ledger.toml")
        if scan_problems:
            print(f"Nothing exported: the scan records in {args.scans} break the rules in "
                  f"{len(scan_problems)} place(s):")
            for p in scan_problems:
                print("  -", p)
            return 1
        exported = export_tree(tree)
        changelog = export_changelog(args.changelog)
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
               f"{len(changelog['days'])} changelog day(s), {scan_line}")
    for note in scan_notes:
        print("Note:", note)
    if args.check:
        print(f"The tree and the scan records validate. Export would write: {summary}.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "tree.json").write_text(json.dumps(exported, indent=2, ensure_ascii=False) + "\n")
    (args.out / "changelog.json").write_text(json.dumps(changelog, indent=2, ensure_ascii=False) + "\n")
    (args.out / "scans.json").write_text(json.dumps(scans, indent=2, ensure_ascii=False) + "\n")
    print(f"Exported {summary} to {args.out}.")
    if not exported["numbers"]["available"]:
        print("Headline numbers not exported: " + exported["numbers"]["reason"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
