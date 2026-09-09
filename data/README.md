# Tree data

This folder holds the tree: one record per breakthrough (a "node"), in TOML, one file per factor, plus `scenarios.toml` (the four longevity scenarios) and `tiers.toml` (what each system tier and access tier requires). The record layout and the rules the compute script enforces are in docs/node-schema.md. Nothing here has a probability until the tree is stable (end of Phase 2 in docs/roadmap.md).
