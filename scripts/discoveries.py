#!/usr/bin/env python3
"""The Belt Equation: the weekly discovery watch's reader (docs/discovery-sources.md; scan
procedure step 3d, added 2026-10-27).

Once a week the scan reads a fixed list of primary sources for discoveries and firsts in our own
solar system: a new body, a first image, a first measurement, a mission arriving somewhere. This
script fetches those sources and prints what each one published in the past week, so the scan reads
one short list instead of composing web searches. It decides nothing: the scan reads the lines,
keeps the ones that are a discovery or a first, and writes each as a `[[discovery]]` item in the
scan record. It edits no file, commits nothing and posts nothing.

    python3 scripts/discoveries.py                           the seven days ending today (Pacific)
    python3 scripts/discoveries.py --week-ending 2026-10-27  the seven days ending on that date
    python3 scripts/discoveries.py --days 14                 a longer window
    python3 scripts/discoveries.py --check                   fetch each source and say whether it answered
    python3 scripts/discoveries.py --json                    the same items as JSON, for other scripts

The sources are the ones in docs/discovery-sources.md, in the same order, and the two files are kept
in step by hand: a source added to one is added to the other. Four of them are ordinary RSS feeds,
one (JAXA) is the older RDF form of RSS, and two have no feed at all, so the script reads their pages:
the Minor Planet Center's list of recent circulars, and arXiv's past-week listing for the planetary
science section (its RSS feed holds one day only). The arXiv listing runs to sixty or seventy papers a
week, so only titles with a discovery word in them are printed, and the count left out is said.

Standard library only, like the other scripts. A source that does not answer is reported as such and
the rest are still printed; the scan says in its record which sources it could not read.
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import html
import json
import re
import sys
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

PACIFIC = ZoneInfo("America/Los_Angeles")
# A browser-like user agent: some of these sites answer a plain Python fetch with a refusal.
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
TIMEOUT = 60

# The sources, as docs/discovery-sources.md lists them. `page` is the address a person opens; `feed`
# is what the script fetches; `kind` says how it is read.
SOURCES: list[dict] = [
    {"id": "mpc", "name": "Minor Planet Center, recent circulars",
     "page": "https://www.minorplanetcenter.net/mpec/RecentMPECs.html",
     "feed": "https://www.minorplanetcenter.net/mpec/RecentMPECs.html", "kind": "mpc"},
    {"id": "noirlab", "name": "NOIRLab news (the Rubin Observatory's releases appear here)",
     "page": "https://noirlab.edu/public/news/",
     "feed": "https://noirlab.edu/public/news/feed/", "kind": "rss"},
    {"id": "nasa", "name": "NASA Science, the solar system",
     "page": "https://science.nasa.gov/solar-system/",
     "feed": "https://science.nasa.gov/category/solar-system/feed/", "kind": "rss"},
    {"id": "jpl", "name": "NASA's Jet Propulsion Laboratory, news",
     "page": "https://www.jpl.nasa.gov/news/",
     "feed": "https://www.jpl.nasa.gov/feeds/news/", "kind": "rss"},
    {"id": "esa", "name": "ESA, space science news",
     "page": "https://www.esa.int/Science_Exploration/Space_Science",
     "feed": "https://www.esa.int/rssfeed/science", "kind": "rss"},
    {"id": "jaxa", "name": "JAXA, press releases",
     "page": "https://global.jaxa.jp/press/",
     "feed": "https://global.jaxa.jp/rss/press.rdf", "kind": "rss"},
    {"id": "arxiv", "name": "arXiv, planetary science papers of the past week (astro-ph.EP)",
     "page": "https://arxiv.org/list/astro-ph.EP/pastweek?skip=0&show=500",
     "feed": "https://arxiv.org/list/astro-ph.EP/pastweek?skip=0&show=500", "kind": "arxiv"},
]

# The Minor Planet Center's daily orbit updates are housekeeping, not discoveries.
MPC_SKIP = re.compile(r"daily orbit update", re.I)
# A provisional designation on its own: a year, a space, two letters and an optional number.
MPC_DESIGNATION = re.compile(r"\d{4} [A-Z]{2}\d*")
# A paper is printed only when its title carries one of these; the rest of the week's papers are
# counted and left out. The words are deliberately few: the scan reads what is printed, so a wide
# net costs reading time and a narrow one misses a find. Widen it when a scan shows it missed one.
ARXIV_WORDS = re.compile(
    r"\b(discover\w*|first (?:detection|image|images|observation|observations|measurement|direct|resolved|look)"
    r"|new (?:dwarf|moon|moons|satellite|satellites|comet|ring|rings|object|objects|member|members)|newly"
    r"|interstellar (?:object|comet|visitor)|candidate dwarf|dwarf planet|trans-neptunian|kuiper belt"
    r"|planet nine|planet x|occultation|3I/|2I/|1I/)",
    re.I)


class SourceError(Exception):
    pass


# ------------------------------------------------------------------ fetching

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raise SourceError(f"answered {e.code}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise SourceError(f"could not be reached ({e})") from e
    return raw.decode("utf-8", errors="replace")


# ------------------------------------------------------------------ parsing

def _text(block: str, tag: str) -> str:
    """The text inside the first <tag>...</tag> of a block, CDATA unwrapped, tags stripped, entities unescaped."""
    m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", block, re.S | re.I)
    if not m:
        return ""
    text = m.group(1)
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text, flags=re.S)
    # Tags are stripped twice: once as written, and once more after unescaping, because some feeds
    # (NOIRLab's) escape the HTML of their descriptions, so an <img> tag only appears after &lt; is undone.
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"<[^>]+>", "", html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def _when(block: str) -> dt.date | None:
    """The item's date as a Pacific calendar date, from <pubDate> (RFC 2822) or <dc:date> (ISO)."""
    for tag in ("pubDate", "dc:date", "published", "updated"):
        raw = _text(block, tag)
        if not raw:
            continue
        try:
            if tag == "pubDate":
                when = email.utils.parsedate_to_datetime(raw)
            else:
                when = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=dt.timezone.utc)
        return when.astimezone(PACIFIC).date()
    return None


def parse_rss(text: str) -> list[dict]:
    """Items of an RSS 2.0 or RSS 1.0 (RDF) feed: title, link, date, and the first line of the description."""
    items = []
    for m in re.finditer(r"<item\b[^>]*>(.*?)</item>", text, re.S | re.I):
        block = m.group(1)
        items.append({
            "title": _text(block, "title"),
            "url": _text(block, "link"),
            "date": _when(block),
            "line": _text(block, "description")[:240],
        })
    return items


MPC_ITEM = re.compile(
    r'<a href="(?P<path>/mpec/[^"]+)"><i>MPEC</i>\s*(?P<number>[\w-]+)</a>\s*\((?P<date>\d{4} \w+ \d{1,2})\)'
    r'\s*<ul>\s*(?P<titles>.*?)</ul>', re.S)


def parse_mpc(text: str) -> list[dict]:
    """The Minor Planet Center's list of recent circulars: one item per circular, its date and its subject
    line (a designation such as 2026 ED138, a comet, a recovery). Daily orbit updates are left out."""
    items = []
    for m in MPC_ITEM.finditer(text):
        titles = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()
                  for t in m.group("titles").split("<li>")]
        titles = [t for t in titles if t]
        title = "; ".join(titles)
        if not title or MPC_SKIP.search(title):
            continue
        try:
            when = dt.datetime.strptime(m.group("date"), "%Y %B %d").date()
        except ValueError:
            when = None
        items.append({
            "title": f"MPEC {m.group('number')}: {title}",
            "url": "https://www.minorplanetcenter.net" + m.group("path"),
            "date": when,
            "line": "",
            # A circular whose whole subject is one provisional designation (2026 UX1) is, nearly
            # always, a routine new near-Earth asteroid: a dozen or more a week. They are printed on
            # one line together, so the scan can match a designation it met elsewhere (2026 ED138
            # looked like any other) without reading each circular.
            "routine": bool(MPC_DESIGNATION.fullmatch(title)),
        })
    return items


ARXIV_DAY = re.compile(r"<h3>\s*(\w{3}, \d{1,2} \w{3} \d{4})")
ARXIV_ENTRY = re.compile(
    r'<a href ?="/abs/(?P<id>[^"]+)"[^>]*>.*?<div class=\'list-title[^>]*>\s*<span[^>]*>Title:</span>\s*(?P<title>.*?)\s*</div>', re.S)


def parse_arxiv(text: str) -> tuple[list[dict], int]:
    """arXiv's past-week listing: the papers whose titles carry a discovery word, each dated by the day
    heading it sits under, and the count of papers left out."""
    items: list[dict] = []
    left_out = 0
    # Split the page at the day headings; everything after a heading until the next belongs to that day.
    parts = ARXIV_DAY.split(text)
    for i in range(1, len(parts), 2):
        try:
            when = dt.datetime.strptime(parts[i], "%a, %d %b %Y").date()
        except ValueError:
            when = None
        for e in ARXIV_ENTRY.finditer(parts[i + 1]):
            title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", e.group("title")))).strip()
            if not ARXIV_WORDS.search(title):
                left_out += 1
                continue
            items.append({"title": title, "url": f"https://arxiv.org/abs/{e.group('id')}", "date": when, "line": ""})
    return items, left_out


def read_source(source: dict, text: str) -> tuple[list[dict], str]:
    """Every item the source's page or feed holds, and a note (what was left out), before the window is applied."""
    if source["kind"] == "rss":
        return parse_rss(text), ""
    if source["kind"] == "mpc":
        return parse_mpc(text), ""
    if source["kind"] == "arxiv":
        items, left_out = parse_arxiv(text)
        return items, f"{left_out} paper(s) with no discovery word in the title left out"
    raise SourceError(f"unknown kind {source['kind']!r}")


# ------------------------------------------------------------------ the window

def in_window(items: list[dict], start: dt.date, end: dt.date) -> list[dict]:
    """The items dated inside the window, inclusive at both ends. An item with no readable date is kept,
    marked, so a feed that drops dates does not silently drop its news."""
    kept = []
    for it in items:
        if it["date"] is None:
            kept.append({**it, "undated": True})
        elif start <= it["date"] <= end:
            kept.append({**it, "undated": False})
    return kept


def window(week_ending: dt.date, days: int) -> tuple[dt.date, dt.date]:
    return week_ending - dt.timedelta(days=days - 1), week_ending


# ------------------------------------------------------------------ main

def run(sources: list[dict], start: dt.date, end: dt.date, getter=fetch) -> list[dict]:
    """One result per source: its items in the window, or the error that stopped it."""
    results = []
    for s in sources:
        try:
            text = getter(s["feed"])
            items, note = read_source(s, text)
        except SourceError as e:
            results.append({**s, "error": str(e), "items": [], "note": "", "total": 0})
            continue
        results.append({**s, "error": None, "items": in_window(items, start, end), "note": note, "total": len(items)})
    return results


def print_report(results: list[dict], start: dt.date, end: dt.date) -> None:
    print(f"Discovery watch: {start} to {end} (seven days ending {end})" if (end - start).days == 6
          else f"Discovery watch: {start} to {end}")
    found = 0
    failed = []
    for r in results:
        print()
        print(f"## {r['name']}")
        print(f"   {r['page']}")
        if r["error"]:
            print(f"   COULD NOT READ: {r['error']}")
            failed.append(r["name"])
            continue
        if not r["items"]:
            print(f"   nothing in the window ({r['total']} item(s) on the feed, none dated inside it)")
        routine = [it for it in r["items"] if it.get("routine")]
        if routine:
            found += len(routine)
            names = ", ".join(it["title"].split(": ", 1)[1] for it in routine)
            print(f"   {len(routine)} circular(s) each on one new provisional designation, nearly always a routine "
                  f"near-Earth asteroid; read one only if the designation is named elsewhere this week: {names}")
        for it in r["items"]:
            if it.get("routine"):
                continue
            found += 1
            when = "undated " if it["undated"] else f"{it['date']}  "
            print(f"   {when}{it['title']}")
            print(f"              {it['url']}")
            if it["line"]:
                print(f"              {it['line']}")
        if r["note"]:
            print(f"   ({r['note']})")
    print()
    print(f"{found} item(s) in the window across {len(results) - len(failed)} source(s) read"
          + (f"; could not read {len(failed)}: {', '.join(failed)}" if failed else "") + ".")
    print("The scan keeps only the lines that are a discovery or a first in our own solar system "
          "(a new body, a first image, a first measurement, a mission arrival) and opens each one before writing it.")


def check(sources: list[dict]) -> int:
    bad = 0
    for s in sources:
        try:
            text = fetch(s["feed"])
            items, _ = read_source(s, text)
            dated = [it["date"] for it in items if it["date"]]
            span = f"{min(dated)} to {max(dated)}" if dated else "no dates read"
            print(f"ok    {s['name']}: {len(items)} item(s), {span}")
        except SourceError as e:
            bad += 1
            print(f"FAIL  {s['name']}: {e}")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--week-ending", type=dt.date.fromisoformat, default=dt.datetime.now(PACIFIC).date(),
                        help="the last day of the window, YYYY-MM-DD (default: today, Pacific)")
    parser.add_argument("--days", type=int, default=7, help="how many days the window holds (default 7)")
    parser.add_argument("--check", action="store_true", help="fetch each source and report whether it answered; print no items")
    parser.add_argument("--json", action="store_true", help="print the items as JSON instead of the report")
    args = parser.parse_args(argv)
    if args.days < 1:
        parser.error("--days must be at least 1")
    if args.check:
        return check(SOURCES)
    start, end = window(args.week_ending, args.days)
    results = run(SOURCES, start, end)
    if args.json:
        out = [{k: v for k, v in r.items() if k != "kind"} for r in results]
        for r in out:
            for it in r["items"]:
                it["date"] = it["date"].isoformat() if it["date"] else None
        print(json.dumps({"start": start.isoformat(), "end": end.isoformat(), "sources": out}, indent=2, ensure_ascii=False))
        return 0
    print_report(results, start, end)
    return 0


if __name__ == "__main__":
    sys.exit(main())
