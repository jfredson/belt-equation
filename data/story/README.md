# The story snapshots

Two files the website's story page reads (website step 24, 2026-09-20), both copied from
TimeAssembler, where the project's day-by-day record lives:

- `worklog.json`: the Belt Equation project's worklog, every entry's date, type (decision,
  progress, session summary, idea), who made a decision (John, or Claude with John's approval,
  or Claude alone), its title, and (since 2026-09-25) its TimeAssembler id. Bodies stay in
  TimeAssembler.
- `roadmap.json`: the project's roadmap as TimeAssembler orders it, each step with its status.

A third file, `exclude.toml`, is written by hand and never fetched. It lists worklog entries that
must not appear in public, each by its TimeAssembler id (whole, or its first eight characters)
with a `why` in plain words that does not repeat what the entry says. The publish command leaves
a listed entry out when it writes `worklog.json`, and the export script leaves it out again when
it builds the story page, so an entry on the list reaches neither even from an older snapshot. A
list the export cannot read, or a row with no id or no reason, stops the build. The entry stays in
TimeAssembler as it is. Added 2026-09-25 for John's ruling of that day that no public surface
describes his current career until May 2027; its first row is that ruling's own entry, whose title
names what the ruling withholds. Remove a row when its reason lapses.

The website plan (decision 5) had the export script fetch these at build time with a key kept on
the Mac. The build moved to GitHub Actions on 2026-09-19, where no key lives, so a snapshot is
committed here instead and the page shows the date it was taken (`fetched_on`). Whichever session
logs to TimeAssembler refreshes them with its tools and commits the result. Since 2026-09-25 the
publish command (`python3 scripts/publish.py`, website step 26) does it too, whenever the
TimeAssembler key is on the computer it runs on: it reads the Belt Equation project's worklog and
roadmap through TimeAssembler's API, dates each worklog entry in Pacific time, leaves out tasks with
no place in the roadmap's order (recurring tasks such as the quarterly scan), and rewrites a file
only when its entries or steps changed. Without the key (a cloud session) it leaves them alone. The
export script
(`scripts/export.py`) turns them into `site/src/data/story.json`. When TimeAssembler grows a
public read-only endpoint for one project's story, the alternative the plan named, the export can
fetch live and these files go away.
