# Scripts

`compute.py` turns the tree in `data/` into headline numbers. Plain Python, standard library only, written 2026-09-08 (roadmap step 5) against the schema in docs/node-schema.md.

    python3 scripts/compute.py validate            check the tree against the schema (the default)
    python3 scripts/compute.py shape               print the tree's shape: counts, leaves, tiers
    python3 scripts/compute.py run [--runs N]      play the tree out once per longevity scenario
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time

`validate` and `shape` work on a tree with no probabilities. `run` and `compare` refuse until every open world node has a probability for every scenario, which is Phase 3. The rules the script enforces are listed in docs/node-schema.md under "Rules the compute script enforces".

`export.py` turns the same tree, plus CHANGELOG.md and the weekly scan records in data/scans/, into the JSON the website reads (site/src/data/). Written 2026-09-19 (website step 21; the scans added the same day, scan plan step 34). It imports the loader and validator from `compute.py`, so it refuses to write anything for a tree that fails the schema, and the site can never show one.

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, scans.json
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else
    python3 scripts/export.py --scans DIR      read a different folder of scan records (for tests)

Beyond a copy of each record it adds the derived views the pages need: each node's dependencies resolved to names, the nodes that depend on it, and the tiers that require it directly. When every open world node has a probability it also includes the run results; until then it says why not. The site's build runs it automatically (see site/README.md).

The scan records get the same treatment as the tree, and the same refusal: `export_scans()` checks every file in data/scans/ before anything is written (the file name is the scan's own date; the [scan] table carries its six fields; every item names a node that is in the tree, once per scan; every verdict is one of the five in docs/scan-plan.md; every verdict but `quiet` cites a source and a resolution cites two; a flagged item says what it would have done; a ledger entry an item names must be in data/ledger.toml once that file exists). Then it writes each item out with its node's name, factor, chain link and page address, plus every node's own checks newest first and the flagged items nothing has picked up yet. A record marked `test = true` is a hand-made fixture rather than a week of real work: it may name a ledger entry that was never written, and the site labels it a test wherever it appears. `export.py` also checks the optional `watch` list on a node, which `compute.py` does not know about.

How a run works: for each scenario, the tree is played out many thousands of times. Nodes are visited in dependency order; a world node whose dependencies all came true comes true with its probability for that scenario, and otherwise stays false. Nodes already resolved in the real world are fixed. Choice points are set to their current-plan option. A tier is reached when everything it requires came true, and the number reported for a tier is the fraction of play-throughs that reached it. Contact Clause nodes are reported separately and never feed a tier.
