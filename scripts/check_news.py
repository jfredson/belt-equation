#!/usr/bin/env python3
"""The Belt Equation: refuse a news post that cannot be trusted (tracker pattern, rule 4.16).

Plain Python, standard library only. Run from anywhere, after scripts/export.py has written
site/src/data/tree.json, ledger.json and scans.json (the build's prebuild does both, in that order):

    python3 scripts/check_news.py                 check site/src/content/news/, print the count
    python3 scripts/check_news.py --posts DIR     check another folder (for tests)
    python3 scripts/check_news.py --records FILE  read another records.json (for tests)

A post is one Markdown file, YYYY-MM-DD-slug.md, with a frontmatter block. The check refuses a
post that: has a file name not of that form, or a frontmatter date that differs from it; carries
a kind outside the seven; names no record, or one that does not exist (the opener, kind
"start-here", is the one post that need not name a record); cites no source with an https
address; states a figure (any digit) in a paragraph that carries no link (a Markdown link or a written-out https address) to a source or a record
(a table is covered by the record links the page draws under the post; the frontmatter is not
prose); or names a record that shows no dated change within fourteen days of the post's date
(a revision, a resolution, a ledger entry, or a scan item ruled or moved), so a post cannot announce
what the record does not show. The rules are John's of 2026-10-18.

Mission news (the eighth kind, "mission-news"; tracker pattern rule 4.20, ruled by John 2026-10-21)
names missions from data/missions.toml (`missions: [...]`) in place of records. The check refuses
one that names no mission or one not on the Missions page; names a mission with no milestone
marked done, moved or failed within fourteen days of the post's date; or is a third mission news
post in one week (Monday to Sunday), past the ceiling of two.

A discovery (the ninth kind, "discovery"; asked for by John 2026-10-27, on Rubin's first dwarf planet
candidate) is about something newly found in the solar system, whether or not it touches a step. It
names no record and no mission, so the check asks of it only what it asks of every post (a source, a
link beside every figure).

Until 2026-11-09 the check also required a mission news or discovery post to end on what the event
does and does not change for the odds. John dropped that on 2026-11-09: these posts stick to the
news, and speak of the odds only where the event bears on a step ("Not every article needs to
include the statement ... the article itself can stick to the news").

Pictures (tracker pattern, rule 4.23, in force since 2026-11-14). A post may show real photographs
of its event. The check refuses a post whose picture: is not written as a <figure> with an <img> and
a <figcaption>; is loaded from another site and not from /news/ here; has no description (alt); has
no entry under `photos:` in the frontmatter giving its file, source page, credit, licence, licence
link and the day the licence was read; has a caption that does not link to that source page; or is
listed under `photos:` and not shown. It also refuses a listed picture whose file is not in the
folder the site serves at /news/. The check cannot tell whether a licence really allows the use:
that is read on the source page by whoever adds the picture, and the entry records that it was.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"start-here", "rung-reached", "estimate-revised", "flagged-item-ruled", "claim", "headline-moved", "method-changed", "mission-news", "discovery"}
UNRECORDED = ("start-here", "mission-news", "discovery")  # the kinds that name no record
MISSION_POSTS_PER_WEEK = 2
WINDOW_DAYS = 14
NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")


def frontmatter(text: str) -> tuple[dict, str]:
    """A small reader for the frontmatter this site writes: scalars, lists of scalars, and lists of
    {label, url} tables written as `- label: ...` / `  url: ...`. Enough for the posts; nothing else."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    head, body = text[4:end], text[end + 4:]
    data: dict = {}
    key = None
    for raw in head.split("\n"):
        if not raw.strip():
            continue
        if raw.lstrip().startswith("- ") and key is not None:
            item = raw.lstrip()[2:].strip()
            if ":" in item and not item.startswith(("http:", "https:")):
                k, v = item.split(":", 1)
                data.setdefault(key, []).append({k.strip(): v.strip().strip('"')})
            else:
                data.setdefault(key, []).append(item.strip('"'))
            continue
        if raw.startswith("  ") and ":" in raw and key is not None and isinstance(data.get(key), list) and data[key] and isinstance(data[key][-1], dict):
            k, v = raw.strip().split(":", 1)
            data[key][-1][k.strip()] = v.strip().strip('"')
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            data[key] = []
        elif val.startswith("[") and val.endswith("]"):
            data[key] = [x.strip().strip('"') for x in val[1:-1].split(",") if x.strip()]
        elif val in ("true", "false"):
            data[key] = val == "true"
        else:
            data[key] = val.strip('"')
    return data, body


def paragraphs(body: str) -> list[str]:
    """The prose paragraphs of the body: not headings, not table rows, not blank."""
    out, cur = [], []
    for line in body.split("\n"):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            if cur:
                out.append(" ".join(cur)); cur = []
            continue
        cur.append(s)
    if cur:
        out.append(" ".join(cur))
    return out


def record_changed_near(rec: dict, when: date, readings: list[dict]) -> bool:
    lo, hi = when - timedelta(days=WINDOW_DAYS), when + timedelta(days=WINDOW_DAYS)
    dates: list[str] = []
    for rv in rec.get("revisions") or []:
        if rv.get("date"):
            dates.append(str(rv["date"]))
    for key in ("resolved_on", "estimated_on", "date"):
        if rec.get(key):
            dates.append(str(rec[key]))
    for rd in readings:
        for it in rd.get("items") or []:
            if it.get("node") == rec.get("id"):
                if it.get("picked_up"):
                    dates.append(str((it["picked_up"] or {}).get("on") or rd.get("date") or ""))
                if it.get("verdict") in ("moved", "resolved"):
                    dates.append(str(rd.get("date") or ""))
    for d in dates:
        try:
            if lo <= date.fromisoformat(d[:10]) <= hi:
                return True
        except ValueError:
            pass
    return False


def mission_changed_near(mission: dict, when: date) -> bool:
    """A milestone marked done or failed, or a date moved, within the window of the post's date."""
    lo, hi = when - timedelta(days=WINDOW_DAYS), when + timedelta(days=WINDOW_DAYS)
    for ms in mission.get("milestones") or []:
        try:
            if ms.get("state") in ("done", "failed"):
                if date.fromisoformat(ms["start"]) <= hi and date.fromisoformat(ms["end"]) >= lo:
                    return True
            if ms.get("was") and lo <= date.fromisoformat(ms["was"]["moved_on"]) <= hi:
                return True
        except (KeyError, ValueError):
            pass
    return False


PHOTO_FIELDS = ("source", "credit", "licence", "licence_url", "read_on")
FIGURE_RE = re.compile(r"<figure\b.*?</figure>", re.S | re.I)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)


def _attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', tag, re.I)
    return m.group(1) if m else None


def check_photos(name: str, fm: dict, body: str, pictures_dir: Path | None) -> list[str]:
    """The pictures in one post (tracker pattern, rule 4.23, in force since 2026-11-14). Every picture
    the post shows is written as a <figure> holding an <img> and a <figcaption>, is kept on this site,
    carries a description for readers who cannot see it, and has an entry under `photos:` in the
    frontmatter naming its file, its source page, its credit, its licence with a link, and the day the
    licence was read. The caption links to the source page. Every entry is a picture the post shows."""
    problems: list[str] = []
    listed: dict[str, dict] = {}
    for ph in fm.get("photos") or []:
        if not isinstance(ph, dict) or not ph.get("file"):
            problems.append(f"{name}: an entry under photos names no file"); continue
        f = ph["file"]
        listed[f] = ph
        for field in PHOTO_FIELDS:
            if not str(ph.get(field) or "").strip():
                problems.append(f"{name}: the picture {f} has no {field} under photos")
        for field in ("source", "licence_url"):
            v = str(ph.get(field) or "")
            if v and not v.startswith("https://"):
                problems.append(f"{name}: the picture {f} gives a {field} that is not an https address")
        if ph.get("read_on"):
            try:
                date.fromisoformat(str(ph["read_on"]))
            except ValueError:
                problems.append(f"{name}: the picture {f} gives a read_on that is not a date (YYYY-MM-DD)")
        if pictures_dir is not None and not (pictures_dir / f).is_file():
            problems.append(f"{name}: the picture file {f} is not in {pictures_dir.name}/; a picture is kept on this site")
    if re.search(r"!\[[^\]]*\]\(", body):
        problems.append(f"{name}: a picture is written as ![...](...); write it as a <figure> with a <figcaption>")
    outside = FIGURE_RE.sub("", body)
    if IMG_RE.search(outside):
        problems.append(f"{name}: a picture stands outside a <figure>; every picture needs a caption")
    shown: set[str] = set()
    for fig in FIGURE_RE.findall(body):
        caption = re.search(r"<figcaption\b.*?</figcaption>", fig, re.S | re.I)
        for tag in IMG_RE.findall(fig):
            src = _attr(tag, "src") or ""
            f = src.rsplit("/", 1)[-1]
            shown.add(f)
            if not src.startswith("/news/"):
                problems.append(f"{name}: the picture {src or '(no address)'} is not served from /news/ on this site")
            if not (_attr(tag, "alt") or "").strip():
                problems.append(f"{name}: the picture {f} has no description (alt) for readers who cannot see it")
            if not caption:
                problems.append(f"{name}: the picture {f} has no caption")
            if f not in listed:
                problems.append(f"{name}: the picture {f} has no entry under photos (file, source, credit, licence, licence_url, read_on)")
            elif caption and listed[f].get("source") and str(listed[f]["source"]) not in caption.group(0):
                problems.append(f"{name}: the caption of {f} does not link to its source page")
    for f in listed:
        if f not in shown:
            problems.append(f"{name}: photos lists {f}, which the post does not show")
    return problems


def check(posts_dir: Path, records: dict, pictures_dir: Path | None = None) -> tuple[list[str], int]:
    problems: list[str] = []
    by_id: dict[str, dict] = {}
    for r in records.get("nodes") or []:
        by_id[r["id"]] = r
    for r in records.get("entries") or []:
        by_id[r["id"]] = r
    readings = records.get("scans") or []
    missions = {m["id"]: m for m in records.get("missions") or []}
    mission_weeks: dict[tuple[int, int], list[str]] = {}
    files = sorted(p for p in posts_dir.glob("*.md")) if posts_dir.exists() else []
    openers = 0
    for path in files:
        name = path.name
        m = NAME_RE.match(name)
        if not m:
            problems.append(f"{name}: the file name must be YYYY-MM-DD-slug.md")
            continue
        fm, body = frontmatter(path.read_text(encoding="utf-8"))
        if not fm:
            problems.append(f"{name}: no frontmatter"); continue
        for field in ("title", "date", "kind", "summary"):
            if not fm.get(field):
                problems.append(f"{name}: frontmatter has no {field}")
        if fm.get("date") and fm["date"] != m.group(1):
            problems.append(f"{name}: the frontmatter date {fm['date']} differs from the file name's {m.group(1)}")
        kind = fm.get("kind")
        if kind not in KINDS:
            problems.append(f"{name}: kind {kind!r} is not one of the nine")
        if kind == "start-here":
            openers += 1
        recs = fm.get("records") or []
        named = fm.get("missions") or []
        if kind == "mission-news":
            if not named:
                problems.append(f"{name}: a mission news post names no mission (missions: [...])")
            for mid in named:
                if mid not in missions:
                    problems.append(f"{name}: names a mission that is not on the Missions page: {mid}")
        elif named:
            problems.append(f"{name}: only a mission news post names missions")
        if kind not in UNRECORDED and not recs:
            problems.append(f"{name}: names no record (records: [...])")
        for rid in recs:
            if rid not in by_id:
                problems.append(f"{name}: names a record that does not exist: {rid}")
        sources = fm.get("sources") or []
        if not any(isinstance(s, dict) and str(s.get("url", "")).startswith("https://") for s in sources):
            problems.append(f"{name}: cites no source with an https address")
        problems.extend(check_photos(name, fm, body, pictures_dir))
        try:
            when = date.fromisoformat(fm.get("date") or m.group(1))
        except ValueError:
            when = None
        if when and kind == "mission-news":
            for mid in named:
                if mid in missions and not mission_changed_near(missions[mid], when):
                    problems.append(f"{name}: {mid} has no milestone marked done, moved or failed within {WINDOW_DAYS} days of {when}; a post cannot announce what the Missions page does not show")
            iso = when.isocalendar()
            mission_weeks.setdefault((iso[0], iso[1]), []).append(name)
        if when and kind not in UNRECORDED:
            for rid in recs:
                if rid in by_id and not record_changed_near(by_id[rid], when, readings):
                    problems.append(f"{name}: {rid} shows no dated change within {WINDOW_DAYS} days of {when}; a post cannot announce what the record does not show")
        for i, para in enumerate(paragraphs(body), 1):
            if re.search(r"\d", para) and "](" not in para and "https://" not in para:
                problems.append(f"{name}: paragraph {i} states a figure with no link to a source or a record: {para[:70]!r}")
    for (y, wk), names in sorted(mission_weeks.items()):
        if len(names) > MISSION_POSTS_PER_WEEK:
            problems.append(f"week {wk} of {y}: {len(names)} mission news posts ({', '.join(names)}); the ceiling is {MISSION_POSTS_PER_WEEK} a week")
    if openers > 1:
        problems.append(f"{posts_dir}: {openers} posts of kind start-here; there is one per site")
    return problems, len(files)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts", default=str(ROOT / "site" / "src" / "content" / "news"))
    ap.add_argument("--records", default=None, help="one JSON file holding nodes, entries and scans (for tests)")
    ap.add_argument("--pictures", default=str(ROOT / "site" / "public" / "news"), help="the folder the site serves at /news/, where a post's pictures are kept")
    a = ap.parse_args(argv)
    data_dir = ROOT / "site" / "src" / "data"
    if a.records:
        records = json.loads(Path(a.records).read_text(encoding="utf-8"))
    else:
        try:
            tree = json.loads((data_dir / "tree.json").read_text(encoding="utf-8"))
            ledger = json.loads((data_dir / "ledger.json").read_text(encoding="utf-8"))
            scans = json.loads((data_dir / "scans.json").read_text(encoding="utf-8"))
        except FileNotFoundError as e:
            print(f"{e.filename} is missing; run scripts/export.py first", file=sys.stderr)
            return 2
        try:
            missions = json.loads((data_dir / "missions.json").read_text(encoding="utf-8")).get("missions") or []
        except FileNotFoundError:
            missions = []
        records = {"nodes": tree.get("nodes") or [], "entries": ledger.get("entries") or [], "scans": scans.get("scans") or [], "missions": missions}
    problems, n = check(Path(a.posts), records, pictures_dir=Path(a.pictures) if a.pictures else None)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"{len(problems)} problem(s) in {n} post(s)", file=sys.stderr)
        return 1
    print(f"OK: {n} news post(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
