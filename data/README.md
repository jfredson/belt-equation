# Tree data

This folder holds the tree: one record per breakthrough (a "node"), in TOML, one file per factor, plus `scenarios.toml` (the four longevity scenarios) and `tiers.toml` (what each system tier and access tier requires). `snapshots/` holds one JSON file per run of the tree, written by the compute script and never
rewritten; scripts/README.md says what is in one and why. `ledger.toml` is the record of what moved
the needle, one entry per thing that happened, appended and never edited; its own header says how an
entry is written. `attribution/` holds one file per run saying how much of that run's move came from
which entry, written by `compute.py attribute --write`. The record layout and the rules the
compute script enforces are in docs/node-schema.md. Nothing here has a probability until the tree is stable (end of Phase 2 in docs/roadmap.md).
