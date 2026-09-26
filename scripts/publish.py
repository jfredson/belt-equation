#!/usr/bin/env python3
"""The Belt Equation: publish the site with one command (website step 26, 2026-09-25).

Plain Python, standard library only. Run from anywhere:

    python3 scripts/publish.py                      regenerate and build, then stop and show what changed
    python3 scripts/publish.py --snapshot scan      the same, and take a run snapshot first
    python3 scripts/publish.py --push               the same, then commit everything and push main
    python3 scripts/publish.py --dry-run            do all of it in a scratch copy; write nothing here

What it does, in order, stopping at the first thing that fails:

1. Checks the tree against the schema (compute.py validate).
2. With --snapshot LABEL, plays the tree out and writes data/snapshots/<date>-<label>.json
   (compute.py run --snapshot LABEL), which is what a scan or a review does when something moved.
3. Draws the tree picture (visual.py) and keeps a dated copy under docs/visual/, unless the newest
   copy there is the same picture apart from its date, in which case nothing is written.
4. Refreshes the story snapshots in data/story/ from TimeAssembler (see data/story/README.md),
   when the TimeAssembler key is on this computer. Without it, or with --no-story, it leaves them
   as they are and says so. A file is rewritten only when its entries or steps changed.
5. Writes the site's data (export.py), which also refuses a broken ledger or scan record.
6. Builds the site (astro build in site/), installing its packages first if they are missing.
   A failed build stops everything, with the builder's own output.
7. Shows what changed: git status, and the headline before (the tree as last committed) and after.
8. Only with --push: stages everything, commits with a dated message (or --message), and pushes
   main. The GitHub Action (.github/workflows/deploy.yml) then builds and deploys the site from
   that push, exactly as it does for any other push; this script never deploys by any other road.
   With --fallback-branch NAME, a push to main that is refused is tried once on that branch.

Without --push it stops after step 7 so the caller can read the diff before anything is committed.
--dry-run copies the working tree to a scratch folder, runs every step there, and reports what
would change here; it writes nothing in the repository and never commits or pushes.

Every script is run with the time zone set to John's (America/Los_Angeles), so the dated picture,
the snapshot and the commit message agree on the date wherever this runs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
TZ = "America/Los_Angeles"
PROJECT = "Belt Equation"
CREDENTIALS = Path.home() / "Documents" / ".timeassembler" / "credentials.env"
HEADLINE = "A2"   # compute.HEADLINE_TIER; repeated so reading the committed tree needs nothing new
WORKLOG_LIMIT = 500


class PublishError(Exception):
    """A step failed; the message says which and why, in plain words."""


def today() -> str:
    return dt.datetime.now(ZoneInfo(TZ)).date().isoformat()


def say(line: str = "") -> None:
    print(line, flush=True)


def run(cmd: list[str], cwd: Path, what: str, quiet: bool = False) -> str:
    """Run one command in John's time zone. On failure, print its output and stop everything."""
    env = dict(os.environ, TZ=TZ)
    p = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.returncode != 0:
        say(p.stdout.rstrip())
        raise PublishError(f"{what} failed (exit {p.returncode}): {' '.join(cmd)}")
    if not quiet and p.stdout.strip():
        for line in p.stdout.rstrip().splitlines():
            say("    " + line)
    return p.stdout


def git(root: Path, *args: str) -> str:
    return run(["git", *args], root, f"git {args[0]}", quiet=True)


# ------------------------------------------------------------ the scratch copy


def visible_files(root: Path) -> dict[str, Path]:
    """The files git would see in root (tracked, plus untracked files not ignored), by path."""
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         cwd=root, check=True, stdout=subprocess.PIPE).stdout
    return {rel: root / rel for rel in sorted(set(filter(None, out.decode().split("\0"))))
            if (root / rel).is_file()}


def copy_working_tree(src: Path, dst: Path) -> None:
    """Copy every file git would see in src to dst, and link site/node_modules rather than
    copying it. Used by --dry-run and by scripts/test_publish.py."""
    for rel, path in visible_files(src).items():
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    modules = src / "site" / "node_modules"
    if modules.is_dir():
        (dst / "site").mkdir(parents=True, exist_ok=True)
        (dst / "site" / "node_modules").symlink_to(modules, target_is_directory=True)


def walk_files(root: Path) -> dict[str, Path]:
    """Every file under root except the site's packages (for a scratch copy)."""
    return {str(p.relative_to(root)): p for p in sorted(root.rglob("*"))
            if p.is_file() and "node_modules" not in p.parts}


def ignored(root: Path, paths: list[str]) -> set[str]:
    """Which of these paths git ignores in root (the site's build output, the generated data)."""
    p = subprocess.run(["git", "check-ignore", "--stdin", "-z"], cwd=root,
                       input="\0".join(paths).encode(), stdout=subprocess.PIPE)
    return set(filter(None, p.stdout.decode().split("\0")))


def differences(here: dict[str, Path], there: dict[str, Path]) -> list[str]:
    """Lines in git's short-status style for how `there` differs from `here`."""
    lines = []
    for rel in sorted(set(here) | set(there)):
        if rel not in there:
            lines.append(f" D {rel}")
        elif rel not in here:
            lines.append(f"?? {rel}")
        elif not filecmp.cmp(here[rel], there[rel], shallow=False):
            lines.append(f" M {rel}")
    return lines


# ------------------------------------------------------------ the tree picture


def refresh_picture(root: Path, date: str) -> str:
    """Draw the tree and keep a dated copy under docs/visual/ when the picture has changed."""
    folder = root / "docs" / "visual"
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "tree.svg"
        run([sys.executable, "scripts/visual.py", "--out", str(fresh)], root,
            "Drawing the tree picture", quiet=True)
        svg = fresh.read_text()
    copies = sorted(folder.glob("????-??-??-tree.svg"))
    if copies:
        newest = copies[-1]
        # The date is drawn once, in the title (visual.render); other dates in the text are data.
        stamp = "The Belt Equation: the tree, {}</text>"
        if newest.read_text().replace(stamp.format(newest.name[:10]), stamp.format(date)) == svg:
            return f"unchanged since {newest.relative_to(root)}; no new copy written"
    target = folder / f"{date}-tree.svg"
    folder.mkdir(parents=True, exist_ok=True)
    target.write_text(svg)
    return f"wrote {target.relative_to(root)}"


# ------------------------------------------------------------ the story, from TimeAssembler


def credentials() -> tuple[str, str] | None:
    """The TimeAssembler address and key: from the environment, else the credentials file."""
    url, key = os.environ.get("TIMEASSEMBLER_API_URL"), os.environ.get("TIMEASSEMBLER_API_KEY")
    if not (url and key) and CREDENTIALS.exists():
        values = {}
        for line in CREDENTIALS.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                values[k.strip().removeprefix("export ").strip()] = v.strip().strip('"').strip("'")
        url = url or values.get("TIMEASSEMBLER_API_URL")
        key = key or values.get("TIMEASSEMBLER_API_KEY")
    return (url.rstrip("/"), key) if url and key else None


def fetch(base: str, key: str, path: str):
    # TimeAssembler's firewall turns away Python's default user agent, so name this script.
    req = urllib.request.Request(base + path, headers={"Authorization": f"Bearer {key}",
                                                       "User-Agent": "belt-equation-publish/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pacific_date(stamp: str) -> str:
    return dt.datetime.fromisoformat(stamp).astimezone(ZoneInfo(TZ)).date().isoformat()


def story_from_timeassembler(base: str, key: str, date: str) -> tuple[dict, dict]:
    """The worklog and roadmap snapshots, in the shape data/story/README.md describes."""
    projects = fetch(base, key, "/api/v1/projects")
    projects = projects if isinstance(projects, list) else projects.get("projects", [])
    match = [p for p in projects if p.get("name") == PROJECT]
    if len(match) != 1:
        raise PublishError(f"TimeAssembler has {len(match)} project(s) named '{PROJECT}', not one")
    pid = match[0]["id"]
    entries = fetch(base, key, f"/api/v1/worklog?projectId={pid}&limit={WORKLOG_LIMIT}")
    if len(entries) >= WORKLOG_LIMIT:
        raise PublishError(f"the worklog returned {len(entries)} entries, the most one request "
                           "asks for; raise WORKLOG_LIMIT in scripts/publish.py so none are dropped")
    worklog = {
        "project": PROJECT,
        "source": f"TimeAssembler worklog, read by scripts/publish.py on {date} (Pacific)",
        "fetched_on": date,
        "entries": [{"date": pacific_date(e["createdAt"]), "type": e["type"],
                     "decided_by": e.get("decidedBy"), "title": e["title"]} for e in entries],
    }
    roadmap_raw = fetch(base, key, f"/api/v1/projects/{pid}/roadmap")
    # Recurring tasks (the quarterly scan, the annual review) have no place in the order, so
    # they are not roadmap steps and are left out; the story page sorts by that order.
    roadmap = {
        "project": PROJECT,
        "source": f"TimeAssembler roadmap, read by scripts/publish.py on {date} (Pacific)",
        "fetched_on": date,
        "steps": [{"order": s["sortOrder"], "status": s["status"], "phase": s.get("phase"),
                   "title": s["title"]}
                  for s in roadmap_raw["steps"] if s.get("sortOrder") is not None],
    }
    return worklog, roadmap


def refresh_story(root: Path, date: str, skip: bool) -> list[str]:
    if skip:
        return ["left as it is (--no-story)"]
    creds = credentials()
    if not creds:
        return [f"left as it is: no TimeAssembler key here (looked in the environment and {CREDENTIALS})"]
    try:
        worklog, roadmap = story_from_timeassembler(*creds, date)
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
        raise PublishError(f"reading the story from TimeAssembler failed: {e}. Run again with "
                           "--no-story to publish without refreshing it.")
    notes = []
    for name, fresh, part in (("worklog.json", worklog, "entries"), ("roadmap.json", roadmap, "steps")):
        path = root / "data" / "story" / name
        old = json.loads(path.read_text()) if path.exists() else {}
        if old.get(part) == fresh[part]:
            notes.append(f"{name}: unchanged since {old.get('fetched_on')}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(fresh, indent=2, ensure_ascii=False) + "\n")
        notes.append(f"{name}: refreshed, {len(fresh[part])} {part} (was {len(old.get(part, []))})")
    return notes


# ------------------------------------------------------------ the headline, before and after


NUMBERS_AT = """
import json, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import compute, export
print(json.dumps(export.export_numbers(compute.load_tree(Path("data")))))
"""


def headline_at_head(root: Path) -> tuple[str, dict | None]:
    """The numbers the tree gave as last committed: the scripts and data at HEAD, played out with
    the export's own seed and count, so an unchanged tree gives exactly the same figures."""
    try:
        commit = git(root, "rev-parse", "--short", "HEAD").strip()
        archive = subprocess.run(["git", "archive", "HEAD", "data", "scripts"], cwd=root,
                                 check=True, stdout=subprocess.PIPE).stdout
    except (PublishError, subprocess.CalledProcessError):
        return "no commit to compare with", None
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive)) as t:
            t.extractall(tmp, filter="data")
        try:
            out = run([sys.executable, "-c", NUMBERS_AT], Path(tmp), "Playing out the committed tree", quiet=True)
            return commit, json.loads(out.strip().splitlines()[-1])
        except (PublishError, ValueError, IndexError):
            return commit, None


def headline_lines(scenarios: list[dict], before: dict | None, after: dict | None) -> list[str]:
    def pct(x):
        return "   -  " if x is None else f"{100 * x:5.2f}%"

    def usable(n):
        return n if n and n.get("available") else {}

    lines = []
    for label, pick in ((f"{HEADLINE}, working off Earth on rotation", lambda n: n.get("tiers", {}).get(HEADLINE) or {}),
                        (f"{HEADLINE} at Tier 1, a station or lunar base", lambda n: n.get("a2_at_tier1") or {})):
        lines.append(label)
        for s in scenarios:
            b = pick(usable(before)).get(s["key"])
            a = pick(usable(after)).get(s["key"])
            by = f"by {s['window_year']}" if s.get("window_year") else "no deadline"
            change = "" if a is None or b is None else ("  same" if a == b else f"  {100 * (a - b):+.2f} points")
            lines.append(f"    {by:<12} {s['key']:<9} {pct(b)} -> {pct(a)}{change}")
    return lines


# ------------------------------------------------------------ the whole thing


def pipeline(root: Path, date: str, snapshot: str | None, no_story: bool) -> None:
    say("1. Checking the tree against the schema")
    run([sys.executable, "scripts/compute.py", "validate"], root, "Validation")

    if snapshot is not None:
        say(f"2. Playing the tree out and taking snapshot '{snapshot}' (about ten minutes)")
        run([sys.executable, "scripts/compute.py", "run", "--snapshot", snapshot], root, "The snapshot run")
    else:
        say("2. No snapshot asked for (--snapshot LABEL takes one)")

    say("3. Drawing the tree picture")
    say("    " + refresh_picture(root, date))

    say("4. Refreshing the story from TimeAssembler")
    for note in refresh_story(root, date, skip=no_story):
        say("    " + note)

    say("5. Writing the site's data (export)")
    run([sys.executable, "scripts/export.py"], root, "The export")

    say("6. Building the site")
    site = root / "site"
    if not (site / "node_modules").exists():
        run(["npm", "ci"], site, "Installing the site's packages", quiet=True)
    # astro build directly: `npm run build` would run the export a second time (its prebuild).
    run(["npx", "--no-install", "astro", "build"], site, "The site build", quiet=True)
    pages = sum(1 for _ in (site / "dist").rglob("index.html"))
    say(f"    built {pages} pages into site/dist/")


def commit_and_push(root: Path, message: str, fallback: str | None) -> None:
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch != "main":
        raise PublishError(f"--push publishes main, and this checkout is on '{branch}'. "
                           "Switch to main, or commit here and open a pull request instead.")
    git(root, "add", "-A")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode == 0:
        say("Nothing to commit: the site already shows this tree. Nothing pushed.")
        return
    git(root, "commit", "-q", "-m", message)
    say(f"Committed {git(root, 'rev-parse', '--short', 'HEAD').strip()}.")
    push = subprocess.run(["git", "push", "origin", "main"], cwd=root, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if push.returncode == 0:
        say("Pushed main. The deploy action builds and deploys the site from this push; follow it "
            "with `gh run watch` or on the repository's Actions tab.")
        return
    say(push.stdout.rstrip())
    if not fallback:
        raise PublishError("The push to main was refused. The commit is here, not on GitHub.")
    again = subprocess.run(["git", "push", "origin", f"HEAD:refs/heads/{fallback}"], cwd=root, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    say(again.stdout.rstrip())
    if again.returncode != 0:
        raise PublishError(f"The push to main was refused, and so was the push to {fallback}.")
    raise PublishError(f"The push to main was refused; the commit is on branch {fallback} instead. "
                       "The site does not change until that branch is merged into main.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", metavar="LABEL", default=None,
                    help="take a run snapshot, data/snapshots/<date>-<label>.json (a scan uses 'scan')")
    ap.add_argument("--push", action="store_true", help="commit everything and push main after the summary")
    ap.add_argument("--dry-run", action="store_true",
                    help="run every step in a scratch copy and report what would change; write nothing")
    ap.add_argument("--no-story", action="store_true", help="do not refresh data/story/ from TimeAssembler")
    ap.add_argument("--message", action="append", default=None,
                    help="the commit message with --push (default: 'Publish <date>: ...'); give it more "
                         "than once for a subject and body paragraphs, as with git commit -m")
    ap.add_argument("--fallback-branch", default=None, metavar="NAME",
                    help="with --push: if the push to main is refused, push once to this branch instead")
    args = ap.parse_args(argv)

    date = today()
    say(f"Publishing the Belt Equation site, {date}"
        + (" (dry run: nothing here is written)" if args.dry_run else ""))
    before_commit, before = headline_at_head(ROOT)
    try:
        if args.dry_run:
            with tempfile.TemporaryDirectory() as tmp:
                scratch = Path(tmp) / "repo"
                copy_working_tree(ROOT, scratch)
                pipeline(scratch, date, args.snapshot, no_story=args.no_story)
                after = json.loads((scratch / "site" / "src" / "data" / "tree.json").read_text())
                built = walk_files(scratch)
                hidden = ignored(ROOT, list(built))
                changes = differences(visible_files(ROOT),
                                      {k: v for k, v in built.items() if k not in hidden})
        else:
            pipeline(ROOT, date, args.snapshot, no_story=args.no_story)
            after = json.loads((ROOT / "site" / "src" / "data" / "tree.json").read_text())
            changes = [line for line in git(ROOT, "status", "--short").splitlines() if line.strip()]
    except PublishError as e:
        say(f"\nStopped: {e}")
        return 1

    say("\n7. What changed" + (" (would change)" if args.dry_run else ""))
    say("    files, as git sees them:")
    for line in changes or ["(nothing)"]:
        say("      " + line)
    say(f"    the headline, as last committed ({before_commit}) -> now:")
    for line in headline_lines(after["scenarios"], before, after["numbers"]):
        say("      " + line)

    if args.dry_run:
        say("\nDry run: nothing was written, committed or pushed."
            + (" With --push it would now commit and push main." if args.push else ""))
        return 0
    if not args.push:
        say("\nStopped before committing. Read the diff (git diff), then run again with --push to publish.")
        return 0
    message = "\n\n".join(args.message) if args.message else (
        f"Publish {date}: site regenerated"
        + (f", snapshot {date}-{args.snapshot}" if args.snapshot is not None else "")
        + "\n\nRun by scripts/publish.py. The deploy action builds and deploys the site from this push.")
    try:
        commit_and_push(ROOT, message, args.fallback_branch)
    except PublishError as e:
        say(f"\nStopped: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
