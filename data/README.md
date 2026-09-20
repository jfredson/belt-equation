# Tree data

This folder holds the tree: one record per breakthrough (a "node"), in TOML, one file per factor, plus `scenarios.toml` (the four longevity scenarios) and `tiers.toml` (what each system tier and access tier requires). `snapshots/` holds one JSON file per run of the tree, written by the compute script and never
rewritten; scripts/README.md says what is in one and why. `ledger.toml` is the record of what moved
the needle, one entry per thing that happened, appended and never edited; its own header says how an
entry is written. `attribution/` holds one file per run saying how much of that run's move came from
which entry, written by `compute.py attribute --write`. The record layout and the rules the
compute script enforces are in docs/node-schema.md. Nothing here has a probability until the tree is stable (end of Phase 2 in docs/roadmap.md).

`scans/` holds the weekly web scans (the Radar, docs/scan-plan.md): one TOML file per scan, named for the date it ran, saying for each node it checked what was searched, what was found and what verdict it reached. Scan files are appended and never edited. The export script (`scripts/export.py`) checks every one of them and refuses to build the site if a record breaks a rule, so a scan on the site is always a scan that adds up. The file dated 2026-09-19 is a hand-made test record, marked `test = true` and labelled as a test wherever the site shows it; it exists so the pages had something to render before the first real scan, and it goes away once one has run.
