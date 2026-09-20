# The story snapshots

Two files the website's story page reads (website step 24, 2026-09-20), both copied from
TimeAssembler, where the project's day-by-day record lives:

- `worklog.json`: the Belt Equation project's worklog, every entry's date, type (decision,
  progress, session summary, idea), who made a decision (John, or Claude with John's approval,
  or Claude alone), and its title. Bodies stay in TimeAssembler.
- `roadmap.json`: the project's roadmap as TimeAssembler orders it, each step with its status.

The website plan (decision 5) had the export script fetch these at build time with a key kept on
the Mac. The build moved to GitHub Actions on 2026-09-19, where no key lives, so a snapshot is
committed here instead and the page shows the date it was taken (`fetched_on`). Whichever session
logs to TimeAssembler refreshes them with its tools and commits the result; the export script
(`scripts/export.py`) turns them into `site/src/data/story.json`. When TimeAssembler grows a
public read-only endpoint for one project's story, the alternative the plan named, the export can
fetch live and these files go away.
