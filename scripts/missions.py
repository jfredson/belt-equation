#!/usr/bin/env python3
"""The Belt Equation: the missions I follow (data/missions.toml), checked and turned into what the
Missions page reads. Ruled by John on 2026-10-20 and 2026-10-21 (tracker pattern rule 4.20;
docs/proposal-missions-to-watch-2026-10-20.md).

Plain Python, standard library only. scripts/export.py calls `export_missions`; run on its own it
checks the file and prints what it would write:

    python3 scripts/missions.py                 check data/missions.toml and print the counts
    python3 scripts/missions.py --file FILE     check another file (for tests)

The missions never feed the number. Nothing here reads a probability, and nothing in compute.py
reads this file.

The check refuses a file where: a mission lacks a name, an https address, a group, a line of what
it is for or a "why I follow it" line; a mission id repeats; a step it names is not in the tree; a
milestone has no plain description, no date or two kinds of date, a date in a form other than the
ones the file's header lists, a span that runs backwards, a state other than done, plan or failed,
or no source with an https address; a moved milestone (`was`) has no `moved_on` day, or a
`moved_on` with no `was`; or a milestone marked done or failed starts after the day the file was
checked. A planned milestone whose day has passed is not refused, since the page says how fresh
its dates are, but it is listed as a note so the next reading catches it.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import datetime as dt
import io
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GROUPS = [
    ("moon", "The Moon"),
    ("mars", "Mars and its moons"),
    ("asteroids", "Asteroids and comets"),
    ("outer", "Jupiter and beyond"),
    ("orbit", "Stations in Earth orbit"),
]
GROUP_KEYS = {k for k, _ in GROUPS}
STATES = {"done", "plan", "failed"}
STATUSES = {"watching", "ended"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# How far ahead the page's "coming up" list looks, and the daily check's window.
COMING_UP_DAYS = 60
PART = {"early": (1, 4), "mid": (5, 8), "late": (9, 12)}
MONTHS = [calendar.month_name[i] for i in range(13)]


class MissionError(Exception):
    pass


def parse_when(s: str) -> dict:
    """One date as the file writes it -> its first and last day, its precision and its words."""
    s = str(s).strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        d = dt.date(int(m[1]), int(m[2]), int(m[3]))
        return {"start": d, "end": d, "precision": "day", "words": f"{d.day} {MONTHS[d.month]} {d.year}"}
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m:
        y, mo = int(m[1]), int(m[2])
        if not 1 <= mo <= 12:
            raise ValueError(s)
        last = calendar.monthrange(y, mo)[1]
        return {"start": dt.date(y, mo, 1), "end": dt.date(y, mo, last), "precision": "month", "words": f"{MONTHS[mo]} {y}"}
    m = re.fullmatch(r"(early|mid|late) (\d{4})", s)
    if m:
        a, b = PART[m[1]]
        y = int(m[2])
        return {"start": dt.date(y, a, 1), "end": dt.date(y, b, calendar.monthrange(y, b)[1]), "precision": "part", "words": s}
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        y = int(m[1])
        return {"start": dt.date(y, 1, 1), "end": dt.date(y, 12, 31), "precision": "year", "words": s}
    raise ValueError(s)


def resolve_date(ms: dict) -> dict:
    """A milestone's date, single or a span, as first day, last day, mark and words."""
    if "when" in ms:
        w = parse_when(ms["when"])
        start, end, words = w["start"], w["end"], w["words"]
        span = w["precision"] in ("part", "year")
    else:
        a, b = parse_when(ms["from"]), parse_when(ms["to"])
        start, end = a["start"], b["end"]
        words = f"{a['words']} to {b['words']}"
        span = True
    if ms.get("net"):
        words = f"no earlier than {words}"
    words = ms.get("label") or words
    return {"start": start, "end": end, "span": span, "words": words}


def mark_of(ms: dict, span: bool) -> str:
    if ms["state"] == "failed":
        return "failed"
    if ms["state"] == "done":
        return "done"
    return "span" if span else "plan"


def validate(data: dict, node_ids: set[str]) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []
    try:
        checked = dt.date.fromisoformat(str(data.get("checked", "")))
    except ValueError:
        return [f"the file's `checked` date is missing or not YYYY-MM-DD: {data.get('checked')!r}"], []
    seen: set[str] = set()
    for i, m in enumerate(data.get("mission") or [], 1):
        where = f"mission {i} ({m.get('id', '?')})"
        mid = m.get("id", "")
        if not ID_RE.match(str(mid)):
            problems.append(f"{where}: id must be lowercase words joined by hyphens")
        if mid in seen:
            problems.append(f"{where}: the id {mid} is used twice")
        seen.add(mid)
        for f in ("name", "url", "operator", "group", "what", "why"):
            if not str(m.get(f, "")).strip():
                problems.append(f"{where}: no {f}")
        if not str(m.get("url", "")).startswith("https://"):
            problems.append(f"{where}: the mission's page must be an https address")
        if m.get("group") not in GROUP_KEYS:
            problems.append(f"{where}: group {m.get('group')!r} is not one of {sorted(GROUP_KEYS)}")
        if m.get("status", "watching") not in STATUSES:
            problems.append(f"{where}: status {m.get('status')!r} is not watching or ended")
        for sid in (m.get("steps") or []) + ([m["step_near"]] if m.get("step_near") else []):
            if sid not in node_ids:
                problems.append(f"{where}: names a step that is not in the tree: {sid}")
        if not m.get("steps") and not m.get("step_note"):
            problems.append(f"{where}: bears on no step, so it needs a `step_note` saying the nearest and why not")
        try:
            dt.date.fromisoformat(str(m.get("checked", "")))
        except ValueError:
            problems.append(f"{where}: `checked` is missing or not YYYY-MM-DD")
        stones = m.get("milestone") or []
        if not stones:
            problems.append(f"{where}: has no milestones")
        for j, ms in enumerate(stones, 1):
            w = f"{where}, milestone {j}"
            if not str(ms.get("what", "")).strip():
                problems.append(f"{w}: no plain description (`what`)")
            has_when, has_span = "when" in ms, ("from" in ms or "to" in ms)
            if has_when == has_span:
                problems.append(f"{w}: give either `when` or both `from` and `to`")
                continue
            if has_span and not ("from" in ms and "to" in ms):
                problems.append(f"{w}: a span needs both `from` and `to`")
                continue
            try:
                d = resolve_date(ms)
            except ValueError as e:
                problems.append(f"{w}: a date is not in a form the file allows: {e}")
                continue
            if d["start"] > d["end"]:
                problems.append(f"{w}: the span runs backwards")
            if ms.get("state") not in STATES:
                problems.append(f"{w}: state {ms.get('state')!r} is not done, plan or failed")
            elif ms["state"] in ("done", "failed") and d["start"] > checked:
                problems.append(f"{w}: marked {ms['state']} but dated after the file was checked ({checked})")
            elif ms["state"] == "plan" and d["end"] < checked:
                notes.append(f"{w}: planned for {d['words']}, which has passed; the next reading should mark it done, moved or failed")
            srcs = ms.get("sources") or []
            if not any(str(s.get("url", "")).startswith("https://") and str(s.get("label", "")).strip() for s in srcs):
                problems.append(f"{w}: cites no source with a label and an https address")
            if ("was" in ms) != ("moved_on" in ms):
                problems.append(f"{w}: a moved date needs both `was` (the old date) and `moved_on` (the day it moved)")
            if "was" in ms and "moved_on" in ms:
                try:
                    parse_when(ms["was"])
                    dt.date.fromisoformat(str(ms["moved_on"]))
                except ValueError as e:
                    problems.append(f"{w}: `was` or `moved_on` is not a date the file allows: {e}")
    watching = sum(1 for m in data.get("mission") or [] if m.get("status", "watching") == "watching")
    if watching > 18:
        notes.append(f"{watching} missions are being followed; the ruling is about fifteen at a time")
    for k in ("next", "left_out"):
        for n in data.get(k) or []:
            if not str(n.get("url", "")).startswith("https://") or not n.get("name") or not n.get("line"):
                problems.append(f"{k}: every entry needs a name, an https address and a line: {n.get('name')!r}")
    return problems, notes


SCAN_CHANGES = {"done", "moved", "failed", "checked"}


def validate_scan_items(scans_dir: Path, mission_ids: set[str]) -> list[str]:
    """The `[[mission]]` items of the weekly scan records (docs/scan-plan.md, "The scan record"):
    each names a mission on the page, the milestone, what changed, the searches, what was found, and
    a source for anything but `checked`; a moved date gives `was` and `now`."""
    problems: list[str] = []
    if not scans_dir.exists():
        return problems
    for path in sorted(scans_dir.glob("*.toml")):
        try:
            raw = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            continue  # the scan validator in export.py reports a broken file
        for i, it in enumerate(raw.get("mission") or [], 1):
            w = f"{path.name}, mission item {i}"
            if it.get("mission") not in mission_ids:
                problems.append(f"{w}: names a mission not in data/missions.toml: {it.get('mission')!r}")
            if it.get("change") not in SCAN_CHANGES:
                problems.append(f"{w}: change must be one of {sorted(SCAN_CHANGES)}")
            for f in ("milestone", "found"):
                if not str(it.get(f, "")).strip():
                    problems.append(f"{w}: no {f}")
            if not it.get("queries"):
                problems.append(f"{w}: names no search (queries)")
            if it.get("change") in ("done", "moved", "failed") and not any(str(s).startswith("https://") for s in it.get("sources") or []):
                problems.append(f"{w}: a milestone marked {it.get('change')} needs a source with an https address")
            if it.get("change") == "moved" and not (it.get("was") and it.get("now")):
                problems.append(f"{w}: a moved milestone gives the old date (was) and the new one (now)")
    return problems


def load(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except tomllib.TOMLDecodeError as e:
        raise MissionError(f"{path} is not valid TOML: {e}") from e


def export(data: dict, nodes: list[dict]) -> dict:
    """What the Missions page reads. `nodes` is the exported tree's node list (id, name, path)."""
    if not data:
        return {"available": False, "missions": [], "groups": [], "next": [], "left_out": [], "coming_up": [], "milestones": []}
    by_id = {n["id"]: n for n in nodes}
    checked = dt.date.fromisoformat(str(data["checked"]))
    step = lambda sid: {"id": sid, "name": by_id[sid]["name"], "path": by_id[sid]["path"]}
    out, flat = [], []
    for m in data.get("mission") or []:
        stones = []
        for ms in m.get("milestone") or []:
            d = resolve_date(ms)
            was = None
            if "was" in ms:
                w = parse_when(ms["was"])
                was = {"start": w["start"].isoformat(), "end": w["end"].isoformat(), "words": w["words"], "moved_on": str(ms["moved_on"])}
            row = {
                "what": ms["what"],
                "state": ms["state"],
                "mark": mark_of(ms, d["span"]),
                "start": d["start"].isoformat(),
                "end": d["end"].isoformat(),
                "words": d["words"],
                "net": bool(ms.get("net")),
                "main": bool(ms.get("main")),
                "note": ms.get("note"),
                "was": was,
                "sources": [{"label": s["label"], "url": s["url"]} for s in ms.get("sources") or []],
            }
            stones.append(row)
        stones.sort(key=lambda r: (r["start"], r["end"]))
        nxt = next((r for r in stones if r["state"] == "plan"), None)
        mission = {
            "id": m["id"],
            "name": m["name"],
            "short": m.get("short") or m["name"].split(",")[0].split(":")[0],
            "url": m["url"],
            "url_label": m.get("url_label") or "Official page",
            "operator": m["operator"],
            "group": m["group"],
            "what": m["what"],
            "why": m["why"],
            "why_draft": bool(m.get("why_draft")),
            "steps": [step(s) for s in m.get("steps") or []],
            "step_note": m.get("step_note"),
            "step_near": step(m["step_near"]) if m.get("step_near") else None,
            "notes": m.get("notes"),
            "status": m.get("status", "watching"),
            "checked": str(m["checked"]),
            "milestones": stones,
            "next": nxt,
        }
        out.append(mission)
        for r in stones:
            flat.append({**r, "mission": m["id"], "mission_name": mission["short"], "bears": bool(mission["steps"])})
    order = {k: i for i, (k, _) in enumerate(GROUPS)}
    out.sort(key=lambda x: order[x["group"]])
    flat.sort(key=lambda r: (r["start"], r["end"], r["mission"]))
    horizon = checked + dt.timedelta(days=COMING_UP_DAYS)
    coming = [r for r in flat if r["state"] == "plan" and r["end"] >= checked.isoformat() and r["start"] <= horizon.isoformat()]
    return {
        "available": True,
        "checked": checked.isoformat(),
        "coming_up_days": COMING_UP_DAYS,
        "groups": [{"key": k, "label": label} for k, label in GROUPS if any(x["group"] == k and x["status"] == "watching" for x in out)],
        "missions": out,
        "milestones": flat,
        "coming_up": coming,
        "next": data.get("next") or [],
        "left_out": data.get("left_out") or [],
    }


LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def plain(text: str) -> str:
    """Markdown links in the file's prose ([words](address)) reduced to their words."""
    return LINK_RE.sub(r"\1", text or "")


def to_csv(exported: dict) -> str:
    """Every milestone as a CSV row, for the link under the timeline (design standard, section 9)."""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["mission", "milestone", "date_as_given", "first_day", "last_day", "state", "earlier_date", "moved_on",
                "bears_on_a_step", "source", "source_address", "checked"])
    names = {m["id"]: m["name"] for m in exported["missions"]}
    for r in exported["milestones"]:
        s = r["sources"][0] if r["sources"] else {"label": "", "url": ""}
        w.writerow([plain(names[r["mission"]]), plain(r["what"]), r["words"], r["start"], r["end"], r["state"],
                    (r["was"] or {}).get("words", ""), (r["was"] or {}).get("moved_on", ""),
                    "yes" if r["bears"] else "no", s["label"], s["url"], exported["checked"]])
    return buf.getvalue()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=Path, default=ROOT / "data" / "missions.toml")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(ROOT / "scripts"))
    import compute  # noqa: E402
    tree = compute.load_tree(ROOT / "data")
    data = load(a.file)
    problems, notes = validate(data, {n["id"] for n in tree["nodes"]})
    for n in notes:
        print("Note:", n)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"{len(problems)} problem(s) in {a.file}", file=sys.stderr)
        return 1
    n = len(data.get("mission") or [])
    k = sum(len(m.get("milestone") or []) for m in data.get("mission") or [])
    print(f"OK: {n} missions, {k} milestones, checked {data.get('checked')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
