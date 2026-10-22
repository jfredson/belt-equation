#!/usr/bin/env python3
"""The Belt Equation: the daily launch-day check for the Missions page (tracker pattern rule 4.20).

Ruled by John on 2026-10-21: "Launch days: a small daily job that checks only the next seven days'
milestones, paid from the monthly API credits", set up so it proposes a post or a date change and
never publishes on its own. It edits no file, commits nothing and posts nothing. What it finds goes
to John as a TimeAssembler task in the Belt Equation project, and a session writes the post or the
date change only after he says yes.

    python3 scripts/missions_watch.py --list 60          the milestones the weekly scan should read
                                                         (step 3c), from the local data/missions.toml;
                                                         no network, no cost
    python3 scripts/missions_watch.py --due              what today's check would look at; no cost
    python3 scripts/missions_watch.py --daily            the daily check: reads data/missions.toml from
                                                         the repository's main branch on GitHub, and
                                                         only if a milestone is due makes one call to
                                                         the Claude API with web search, then files a
                                                         task when something happened or moved
    ... --daily --dry-run                                everything but the API call and the task
    ... --daily --local                                  read the local file, not main (a test run)

What counts as due: a planned milestone dated to a day or a month (not a season, a year or a span,
which the weekly scan reads) that falls between three days ago and seven days ahead. Most days
nothing is due, and the job ends without calling the API.

The API key is the `weekly-readings` key (timeassembler/docs/session-routing.md: the trackers'
readings run as scripts on that workspace), read from
~/.config/sentient-horizons/anthropic-weekly-readings.env and never printed. Each run that calls the
API appends one line to ~/Library/Logs/belt-missions-watch.csv with its tokens, searches and cost,
which the month-end credits sweep adds up for the spending record (docs/spending-record.md).

Needs the `anthropic` package for --daily (the daily job runs it from its own virtual environment,
scripts/launchd/README.md); --list and --due need only the standard library.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tomllib
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import missions as missions_mod  # noqa: E402

RAW_MAIN = "https://raw.githubusercontent.com/jfredson/belt-equation/main/data/missions.toml"
KEY_FILE = Path.home() / ".config" / "sentient-horizons" / "anthropic-weekly-readings.env"
TA_FILE = Path.home() / "Documents" / ".timeassembler" / "credentials.env"
LOG = Path.home() / "Library" / "Logs" / "belt-missions-watch.csv"
TA_PROJECT = "Belt Equation"
MODEL = "claude-opus-5-5"
# Prices per million tokens and per search, read 2026-10-21 from
# https://platform.claude.com/docs/en/about-claude/pricing.md (Opus 5.5: $4 in, $20 out; web search
# $10 per 1,000 searches; web fetch has no charge beyond tokens). Used only to log what a run cost.
PRICE_IN, PRICE_OUT, PRICE_SEARCH = 4.0, 20.0, 0.01
LOOK_BACK, LOOK_AHEAD = 3, 7
MAX_SEARCHES = 10
POST_EVENTS = ("a launch; an arrival in orbit, or a flyby that returns pictures; a first picture of somewhere "
               "never seen; a landing; a sample or crew coming home; a crew flying; a failure or loss; a "
               "cancellation; a slip of more than a year in a main milestone")


def today_pacific() -> dt.date:
    return dt.datetime.now(ZoneInfo("America/Los_Angeles")).date()


def read_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        m = re.match(r"^\s*(?:export\s+)?([A-Z_][A-Z0-9_]*)=(.*)$", line)
        if m:
            out[m[1]] = m[2].strip().strip('"').strip("'")
    return out


def milestones(data: dict) -> list[dict]:
    rows = []
    for m in data.get("mission") or []:
        if m.get("status", "watching") != "watching":
            continue
        for ms in m.get("milestone") or []:
            d = missions_mod.resolve_date(ms)
            precise = "when" in ms and re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", str(ms["when"]))
            rows.append({"mission": m["id"], "name": missions_mod.plain(m["name"]), "url": m["url"],
                         "what": missions_mod.plain(ms["what"]), "state": ms["state"], "words": d["words"],
                         "start": d["start"], "end": d["end"], "precise": bool(precise), "main": bool(ms.get("main")),
                         "sources": [s["url"] for s in ms.get("sources") or []]})
    return sorted(rows, key=lambda r: r["start"])


def for_scan(data: dict, today: dt.date, ahead: int) -> list[dict]:
    """Step 3c of the scan procedure: planned milestones in the next `ahead` days, or in the past 30."""
    lo, hi = today - dt.timedelta(days=30), today + dt.timedelta(days=ahead)
    return [r for r in milestones(data) if r["state"] == "plan" and r["end"] >= lo and r["start"] <= hi]


def due(data: dict, today: dt.date) -> list[dict]:
    lo, hi = today - dt.timedelta(days=LOOK_BACK), today + dt.timedelta(days=LOOK_AHEAD)
    return [r for r in milestones(data) if r["state"] == "plan" and r["precise"] and r["end"] >= lo and r["start"] <= hi]


def fetch_main() -> dict | None:
    try:
        with urllib.request.urlopen(RAW_MAIN, timeout=30) as resp:
            return tomllib.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # the Missions page is not on main yet
        raise


PROMPT = """Today is {today}. You check space mission milestones for a public tracker. Read only pages you open with your tools; never answer from memory, since these events are newer than your training.

For each milestone below, search the operator's own pages first, then mainstream reporting. Decide:
- "happened": it happened (give the date as the source gives it, no more precise),
- "moved": the operator or a mainstream report gives a new date (give it as the source gives it),
- "failed": it failed or was lost,
- "no news": nothing new, or nothing you could confirm on a page you opened.
Give at least one source address you opened for anything but "no news". Say whether the event is one that earns a post, which is only: {events}.

Milestones:
{items}

Answer with one JSON object and nothing else:
{{"milestones": [{{"mission": "<id>", "milestone": "<as given>", "finding": "happened|moved|failed|no news", "date": "<as the source gives it, or empty>", "summary": "<one or two plain sentences with absolute dates>", "sources": ["https://..."], "earns_post": true|false}}]}}"""


def call_api(rows: list[dict], today: dt.date) -> tuple[list[dict], dict]:
    import anthropic  # the daily job's own environment has it; --list and --due do not need it

    key = read_env(KEY_FILE).get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit(f"No ANTHROPIC_API_KEY in {KEY_FILE}")
    client = anthropic.Anthropic(api_key=key)
    items = "\n".join(f"- mission {r['mission']} ({r['name']}, official page {r['url']}): {r['what']}; planned {r['words']}; "
                      f"current sources {', '.join(r['sources'])}" for r in rows)
    messages = [{"role": "user", "content": PROMPT.format(today=today.isoformat(), events=POST_EVENTS, items=items)}]
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": min(MAX_SEARCHES, 4 * len(rows))},
             {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 6}]
    usage = {"input": 0, "output": 0, "cache_read": 0, "searches": 0}
    text = ""
    for _ in range(4):  # a long server-tool turn may pause; continue it a few times at most
        resp = client.beta.messages.create(
            model=MODEL, max_tokens=16000, tools=tools, messages=messages,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"], extra_body={"fallbacks": "default"},
        )
        u = resp.usage
        usage["input"] += (u.input_tokens or 0) + (getattr(u, "cache_creation_input_tokens", 0) or 0)
        usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        usage["output"] += u.output_tokens or 0
        stu = getattr(u, "server_tool_use", None)
        usage["searches"] += (getattr(stu, "web_search_requests", 0) or 0) if stu else 0
        if resp.stop_reason == "refusal":
            raise SystemExit("The API declined the request; nothing filed.")
        text += "".join(b.text for b in resp.content if b.type == "text")
        if resp.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": resp.content})
    m = re.search(r"\{.*\}", text, re.S)
    found = json.loads(m.group(0)).get("milestones", []) if m else []
    usage["cost"] = round(usage["input"] / 1e6 * PRICE_IN + usage["cache_read"] / 1e6 * PRICE_IN * 0.1
                          + usage["output"] / 1e6 * PRICE_OUT + usage["searches"] * PRICE_SEARCH, 4)
    return found, usage


def log_run(today: dt.date, n: int, usage: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    new = not LOG.exists()
    with LOG.open("a") as f:
        if new:
            f.write("date,milestones_checked,input_tokens,cache_read_tokens,output_tokens,searches,cost_usd,vendor\n")
        f.write(f"{today},{n},{usage['input']},{usage['cache_read']},{usage['output']},{usage['searches']},{usage['cost']},Anthropic credits\n")


def file_task(today: dt.date, findings: list[dict]) -> str | None:
    """One TimeAssembler task for John, only when something happened, moved or failed."""
    news = [f for f in findings if f.get("finding") in ("happened", "moved", "failed")]
    if not news:
        return None
    env = read_env(TA_FILE)
    url, key = env.get("TIMEASSEMBLER_API_URL"), env.get("TIMEASSEMBLER_API_KEY")
    if not url or not key:
        print(f"No TimeAssembler credentials in {TA_FILE}; the proposal is printed above only.")
        return None
    posts = [f for f in news if f.get("earns_post")]
    head = (f"Mission news to approve: {posts[0]['mission']}" if posts else f"Mission date check: {news[0]['mission']}")
    lines = ["The daily launch-day check found the following. Nothing has been published or changed.",
             "Say yes and a session writes the mission news post (with its share kit) or the date change in data/missions.toml.", ""]
    for f in news:
        lines.append(f"- {f['mission']}: {f['milestone']}. {f['finding'].upper()}"
                     + (f", {f['date']}" if f.get("date") else "") + f". {f.get('summary', '')}"
                     + (" Earns a mission news post." if f.get("earns_post") else " A date change only, no post.")
                     + " Sources: " + ", ".join(f.get("sources") or []))
    lines += ["", f"Checked {today} by scripts/missions_watch.py. The ceiling is two mission news posts a week (tracker pattern rule 4.20)."]
    body = json.dumps({"title": f"{head} ({today})", "project": TA_PROJECT, "notes": "\n".join(lines),
                       "priority": "high" if posts else "medium", "source": "api"}).encode()
    req = urllib.request.Request(url.rstrip("/") + "/api/v1/tasks", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read()).get("id")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", type=int, metavar="DAYS", help="planned milestones in the next DAYS days or the past 30")
    ap.add_argument("--due", action="store_true", help="what today's daily check would look at")
    ap.add_argument("--daily", action="store_true", help="the daily check")
    ap.add_argument("--dry-run", action="store_true", help="with --daily: no API call, no task")
    ap.add_argument("--local", action="store_true", help="with --daily: read --file instead of main on GitHub (for a test run)")
    ap.add_argument("--file", type=Path, default=ROOT / "data" / "missions.toml")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=None)
    a = ap.parse_args(argv)
    today = a.today or today_pacific()
    if a.list is not None or a.due:
        data = missions_mod.load(a.file)
        rows = for_scan(data, today, a.list) if a.list is not None else due(data, today)
        for r in rows:
            print(f"{r['words']:<40} {r['mission']:<16} {r['what']}")
        print(f"{len(rows)} milestone(s)")
        return 0
    if not a.daily:
        ap.print_help()
        return 2
    data = missions_mod.load(a.file) if a.local else fetch_main()
    if not data:
        print(f"{today}: data/missions.toml is not on main yet; nothing to check.")
        return 0
    rows = due(data, today)
    if not rows:
        print(f"{today}: no milestone due between {today - dt.timedelta(days=LOOK_BACK)} and {today + dt.timedelta(days=LOOK_AHEAD)}; no API call.")
        return 0
    print(f"{today}: {len(rows)} milestone(s) due: " + "; ".join(f"{r['mission']} ({r['words']})" for r in rows))
    if a.dry_run:
        return 0
    findings, usage = call_api(rows, today)
    log_run(today, len(rows), usage)
    for f in findings:
        print(f"  {f.get('mission')}: {f.get('finding')} {f.get('date', '')} {f.get('summary', '')}")
    print(f"  cost ${usage['cost']:.2f} ({usage['input']} in, {usage['output']} out, {usage['searches']} searches)")
    task = file_task(today, findings)
    print(f"  filed TimeAssembler task {task}" if task else "  nothing to file")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
