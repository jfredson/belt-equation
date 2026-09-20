# Scripts

`compute.py` turns the tree in `data/` into headline numbers. Plain Python, standard library only, written 2026-09-08 (roadmap step 5) against the schema in docs/node-schema.md.

    python3 scripts/compute.py validate            check the tree against the schema (the default)
    python3 scripts/compute.py shape               print the tree's shape: counts, leaves, tiers
    python3 scripts/compute.py run [--runs N]      play the tree out once per longevity scenario
    python3 scripts/compute.py run --snapshot [LABEL]  the same, and write the run to data/snapshots/
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time

`validate` and `shape` work on a tree with no probabilities. `run` and `compare` refuse until every open world node has a probability for every scenario, which is Phase 3. The rules the script enforces are listed in docs/node-schema.md under "Rules the compute script enforces".

## Snapshots

A snapshot is the complete output of one run, written to `data/snapshots/YYYY-MM-DD[-label].json`
and committed: the run's parameters and commit, every tier's rate per scenario, every node's
rate, the seven chain links' gate rates, the Contact Clause rungs, and the decision comparison.
Snapshots are the project's memory of its own numbers. The history charts on the website are
drawn from them and from nothing else, so the history a reader sees is exactly the history in
the repository. The plan and the reasoning are in docs/ledger-plan.md (the record, and decision 2).

One is taken at every quarterly scan, every annual review, and whenever a ruling changes the
tree in between. A snapshot is never rewritten: `--snapshot` refuses to overwrite a file that
exists, and a second run on the same day takes a label of its own. `--snapshot-date`,
`--snapshot-commit` and `--snapshot-note` exist for backfilling a run that already happened.

Two backfilled snapshots sit in the folder, both marked `pre-review` because the outside-model
review (roadmap step 27) has not been ruled in full:

- `2026-09-19-first-run`, the first run of the tree, replayed from the tree as it stood at
  commit `af01ac5` with nodes rolled independently, because the per-run world draw did not exist
  yet. Every tier figure it produces matches the ones written down in docs/runs/2026-09-19-first-run.md.
- `2026-09-19-second-run`, the run after John's four rulings of the same day. These are the
  numbers the site shows.

`export.py` turns the same tree, plus CHANGELOG.md, into the JSON the website reads (site/src/data/). Written 2026-09-19 (website step 21). It imports the loader and validator from `compute.py`, so it refuses to write anything for a tree that fails the schema, and the site can never show one.

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, snapshots.json
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else

Beyond a copy of each record it adds the derived views the pages need: each node's dependencies resolved to names, the nodes that depend on it, and the tiers that require it directly. When every open world node has a probability it also includes the run results; until then it says why not. The site's build runs it automatically (see site/README.md).

How a run works: for each scenario, the tree is played out many thousands of times. Nodes are visited in dependency order; a world node whose dependencies all came true comes true with its probability for that scenario, and otherwise stays false. Nodes already resolved in the real world are fixed. Choice points are set to their current-plan option. A tier is reached when everything it requires came true, and the number reported for a tier is the fraction of play-throughs that reached it. Contact Clause nodes are reported separately and never feed a tier.
