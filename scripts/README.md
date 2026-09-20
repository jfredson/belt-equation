# Scripts

`compute.py` turns the tree in `data/` into headline numbers. Plain Python, standard library only, written 2026-09-08 (roadmap step 5) against the schema in docs/node-schema.md.

    python3 scripts/compute.py validate            check the tree against the schema (the default)
    python3 scripts/compute.py shape               print the tree's shape: counts, leaves, tiers
    python3 scripts/compute.py run [--runs N]      play the tree out once per longevity scenario
    python3 scripts/compute.py run --snapshot [LABEL]  the same, and write the run to data/snapshots/
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time
    python3 scripts/compute.py worth               what each open step would be worth to the headline
    python3 scripts/compute.py attribute ENTRY     how much of a run's move came from one ledger entry

`validate` and `shape` work on a tree with no probabilities. `run` and `compare` refuse until every open world node has a probability for every scenario, which is Phase 3. The rules the script enforces are listed in docs/node-schema.md under "Rules the compute script enforces".

## Snapshots

A snapshot is the complete output of one run, written to `data/snapshots/YYYY-MM-DD[-label].json`
and committed: the run's parameters and commit, every tier's rate per scenario, every node's
rate, the seven chain links' gate rates, the Contact Clause rungs, the decision comparison, and
what each open step would be worth to the headline if it settled now.
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

## What a step is worth, and what an entry was worth

Two questions the ledger asks of the tree, one facing forwards and one facing back.

**Worth, forwards.** `compute.py worth` takes every open step the headline rests on, holds it at
yes and plays the whole tree out again, then holds it at no and plays it out again. The difference
from the headline as it stands is what that step is worth. This is a one-at-a-time sensitivity
analysis, which is the ordinary way to ask the question, and it is what the site's "what would move
this" lists and each step's worth line are built from — so those figures can never drift from the
tree, because they are the tree. A step the headline does not rest on at any remove is recorded as
worth nothing without being played out at all: that answer is exact, and skipping it roughly halves
the work. Every forced run starts from the same seed, so the world draws line up and the difference
between two runs is mostly the change being asked about rather than dice.

This is the slow part of taking a snapshot — about ten minutes at twenty thousand play-throughs per
scenario, because the tree is played out twice more for every step. `--no-worth` leaves it out.

**Contribution, backwards.** `compute.py attribute <entry or run>` takes the tree as it stood at a
run, undoes one ledger entry's changes and only those — putting the old numbers back from the
`revisions` on the steps the entry names, or opening a step that the entry resolved — and plays the
tree out again. How far the headline falls is what that entry was worth. `--write` commits the
answer to `data/attribution/<run>.json`, which is what the website reads; it is stored rather than
recomputed for the same reason a run is, so that a page renders in a second instead of in minutes
of playing the tree out.

Contributions do not add up to a run's whole move, and the leftover is reported as its own line
rather than hidden. Two reasons: changes made in the same run interact with each other, and some
changes cannot be undone one at a time at all. Moving a requirement from one tier to another, or
changing how the tree is played out, has no "old number" on any step's record to put back. Those
entries are reported as ones that cannot be separated, with the reason in plain words, and the
leftover carries them. Version one goes no further than that, on purpose (docs/ledger-plan.md,
decision 3 and "Deferred, and why").

## The ledger

`data/ledger.toml` is the record of what moved the needle: one entry per thing that happened,
appended and never edited, with six kinds so that a reader can tell the world moving from John
changing his mind. The record layout is in docs/ledger-plan.md and the file's own header.

The export script checks it on every build and refuses to write anything when a rule is broken.
The rule that matters most is the cross-check: every step an entry says it changed must carry, on
its own record, a revision or a resolution dated between the previous run and the entry. That is
what stops the story and the tree drifting apart, which was the real risk in keeping the story in a
file of its own.

An entry carries words, not numbers. Everything numeric beside it on the site — each step's rate
before and after, where the headline stood on either side, and the entry's own contribution — is
filled in by the export from the committed runs. An entry therefore cannot claim a change the tree
did not produce.

`export.py` turns the same tree, plus CHANGELOG.md, the run snapshots, the ledger and the weekly scan records in data/scans/, into the JSON the website reads (site/src/data/). Written 2026-09-19 (website step 21; the scans added the same day, scan plan step 34). It imports the loader and validator from `compute.py`, so it refuses to write anything for a tree that fails the schema, and the site can never show one.

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, snapshots.json, ledger.json, scans.json
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else
    python3 scripts/export.py --scans DIR      read a different folder of scan records (for tests)

Beyond a copy of each record it adds the derived views the pages need: each node's dependencies resolved to names, the nodes that depend on it, and the tiers that require it directly. When every open world node has a probability it also includes the run results; until then it says why not. The site's build runs it automatically (see site/README.md).

The scan records get the same treatment as the tree, and the same refusal: `export_scans()` checks every file in data/scans/ before anything is written (the file name is the scan's own date; the [scan] table carries its six fields; every item names a node that is in the tree, once per scan; every verdict is one of the five in docs/scan-plan.md; every item names at least one search it ran, unless it is `quiet` and `found` says why no search was run; every verdict but `quiet` cites a source and a resolution cites two; a flagged item says what it would have done; a ledger entry an item names must be in data/ledger.toml once that file exists). Then it writes each item out with its node's name, factor, chain link and page address, plus every node's own checks newest first and the flagged items nothing has picked up yet. A record may still carry `test = true` to mark a hand-made fixture rather than a week of real work, and the site labels one as a test wherever it appears; no record carries it now that the first real scan has run, and such a record gets no exemption from the rules above. `export.py` also checks the optional `watch` list on a node, which `compute.py` does not know about.

How a run works: for each scenario, the tree is played out many thousands of times. Nodes are visited in dependency order; a world node whose dependencies all came true comes true with its probability for that scenario, and otherwise stays false. Nodes already resolved in the real world are fixed. Choice points are set to their current-plan option. A tier is reached when everything it requires came true, and the number reported for a tier is the fraction of play-throughs that reached it. Contact Clause nodes are reported separately and never feed a tier.
