# Tree data

This folder holds the tree: one record per breakthrough (a "node"), in TOML, one file per factor, plus `scenarios.toml` (the four longevity scenarios) and `tiers.toml` (what each system tier and access tier requires). `snapshots/` holds one JSON file per run of the tree, written by the compute script and never
rewritten; scripts/README.md says what is in one and why. `ledger.toml` is the record of what moved
the needle, one entry per thing that happened, appended and never edited; its own header says how an
entry is written. `attribution/` holds one file per run saying how much of that run's move came from
which entry, written by `compute.py attribute --write`. The record layout and the rules the
compute script enforces are in docs/node-schema.md. Nothing here has a probability until the tree is stable (end of Phase 2 in docs/roadmap.md).

`headline.json` (added 2026-10-17) is the one small file the family's other sites read to show this
project's headline, the way The Quiet Galaxy, The Upgrade Tree and Outrunning Ageing each publish
theirs, so that the Sentient Horizons Projects page needs one fetch, at
`https://raw.githubusercontent.com/jfredson/belt-equation/main/data/headline.json`, instead of
following the ledger to a snapshot. It is written by `compute.py headline` (and by `compute.py run
--snapshot`, and by `scripts/publish.py` on every run), from the newest snapshot and the newest scan
record, and plays nothing out: `computed_on` is the day that snapshot's run was taken, `snapshot`
names it, `last_reading` is the date of the newest weekly scan record (so it moves every week, even
a week in which nothing moved and no snapshot was taken), `method` carries the run's size, seed, commit
and review status, `headline` is the headline tier (A2, "Works off Earth on rotation") under the
baseline scenario with its deadline year, `second_number` is the station-or-lunar-base figure shown
beside it, and `by_scenario` and `tiers` hold the same for all five scenarios and every tier. It is
rewritten, never edited by hand; `scripts/test_headline.py` fails if it is missing or stale. Since
2026-10-17 the site serves a copy of it too, at `https://beltequation.com/data/headline.json`: the
export (`scripts/export.py`) copies it into `site/public/data/` on every build, so the two cannot
differ (ruled by John 2026-10-17 from the first cross-project lessons review, for every tracker).

`scans/` holds the weekly web scans (the Radar, docs/scan-plan.md): one TOML file per scan, named for the date it ran, saying for each node it checked what was searched, what was found and what verdict it reached. Scan files are appended and never edited. The export script (`scripts/export.py`) checks every one of them and refuses to build the site if a record breaks a rule, so a scan on the site is always a scan that adds up. The file dated 2026-09-19 is a hand-made test record, marked `test = true` and labelled as a test wherever the site shows it; it exists so the pages had something to render before the first real scan, and it goes away once one has run.
