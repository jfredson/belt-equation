# Scripts

`compute.py` turns the tree in `data/` into headline numbers. Plain Python, standard library only, written 2026-09-08 (roadmap step 5) against the schema in docs/node-schema.md.

    python3 scripts/compute.py validate            check the tree against the schema (the default)
    python3 scripts/compute.py shape               print the tree's shape: counts, leaves, tiers
    python3 scripts/compute.py run [--runs N]      play the tree out once per longevity scenario
    python3 scripts/compute.py run --snapshot [LABEL]  the same, and write the run to data/snapshots/
    python3 scripts/compute.py compare [--runs N]  the decision comparison, one choice group at a time
    python3 scripts/compute.py worth               what each open step would be worth to the headline
    python3 scripts/compute.py attribute ENTRY     how much of a run's move came from one ledger entry
    python3 scripts/compute.py reader --birth YEAR what the tree says for a reader born that year

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

Two backfilled snapshots sit in the folder, both marked `pre-review` because they were taken before
the outside-model review (roadmap step 27) was ruled in full; every snapshot from `2026-09-20-step-27`
on is marked `reviewed`:

- `2026-09-19-first-run`, the first run of the tree, replayed from the tree as it stood at
  commit `af01ac5` with nodes rolled independently, because the per-run world draw did not exist
  yet. Every tier figure it produces matches the ones written down in docs/runs/2026-09-19-first-run.md.
- `2026-09-19-second-run`, the run after John's four rulings of the same day.
- `2026-09-20-step-27`, the run after the outside-model review's 105 rulings landed (fifteen
  numbers moved, nine nodes added, forty-one criteria tightened). The first snapshot marked
  `reviewed`, the first to carry the second number (`second.a2_at_tier1`, a rotation at a
  station or lunar base, shown beside the headline under item 95), and the numbers the site shows.

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

## Running the tree for somebody other than John

`compute.py reader` answers the site's question for a visitor (website step 39,
docs/run-it-yourself-plan.md). The tree's probabilities are estimated at five deadlines, which
are John's own ages: 85, 94, 109, 150 and no deadline at all. A reader born in another year has
the same ages at different years, so each open step's number is read between the two neighbouring
windows on the log-odds scale and the whole tree is played out at that deadline. The reasoning
and its limits are in docs/methodology.md under "Running the tree for somebody else". It reads
the tree and never writes to it: no stored probability, snapshot or headline moves.

    python3 scripts/compute.py reader --birth 2000 --scenario baseline --route seat --personal 0.1

That prints one cell in two columns. "The website" is what a visitor sees, read between the two
nearest five-year steps of the grid; "this year exactly" is the tree played out at the reader's
own deadline with no reading between steps. The two are the same run when the deadline lands on a
five-year step, and the gap between them otherwise is what the grid's coarseness costs. The routes
are `seat` (buy one), `rotation` (hold a job whose holders go off Earth) and `earth` (work in or
for the industry without leaving, which asks for no number of the reader's own).

`export.py` writes the whole grid to `site/src/data/reader.json` on every build: one cell per
five-year deadline across the range a shifted window can land in, plus one for no deadline at all,
each the tree played out `READER_RUNS` times. The page reads between two cells and multiplies in
the reader's own guess, so no probability is ever worked out in the browser. The grid adds about
eleven seconds to a build; raising `READER_RUNS` is the one knob if its figures ever look too
coarse.

## Tests

    python3 scripts/test_reader.py

Standard library, no dependencies. Thirteen checks on the reader grid. The one that matters plays
the tree out at John's own five windows with the committed snapshot's own dice and requires every
system tier's rate to come out exactly equal to the snapshot's: at those years the reading hands
back the stored numbers untouched, so the dice fall the same way and anything but an exact match
means the reading has changed what the tree says. The others cover the reading itself (a named
window returns its own number, nothing falls as the deadline moves out, the floor below the first
window, the approach to the no-deadline number beyond the last), that every birth year the page
offers lands inside the grid, that no route runs through John's own path, and that playing the
tree out for a reader leaves the tree it was given alone.

    python3 scripts/test_publish.py

Standard library, plus the site's own packages (`cd site && npm ci` once). Seven checks on the
publish command, about five to seven minutes. The one that matters copies the working tree twice
into scratch folders, runs `publish.py` without `--push` in one and `export.py` plus `npm run build`
in the other, and requires every file the export writes and every page of the built site to come
out the same. The one exception is the decorative stars behind each page, which the site scatters
at random on every build, so the pages are compared with them taken out. It also checks that
nothing else in the tree changed, that no commit was made without `--push`, and that `--dry-run`
writes nothing at all.

`export.py` turns the same tree, plus CHANGELOG.md, the run snapshots, the ledger and the weekly scan records in data/scans/, into the JSON the website reads (site/src/data/). Written 2026-09-19 (website step 21; the scans added the same day, scan plan step 34). It imports the loader and validator from `compute.py`, so it refuses to write anything for a tree that fails the schema, and the site can never show one.

    python3 scripts/export.py                  write site/src/data/tree.json, changelog.json, snapshots.json, ledger.json, scans.json
    python3 scripts/export.py --check          validate and print the counts, write nothing
    python3 scripts/export.py --out DIR        write the JSON somewhere else
    python3 scripts/export.py --scans DIR      read a different folder of scan records (for tests)

Beyond a copy of each record it adds the derived views the pages need: each node's dependencies resolved to names, the nodes that depend on it, and the tiers that require it directly. When every open world node has a probability it also includes the run results; until then it says why not. The site's build runs it automatically (see site/README.md).

The scan records get the same treatment as the tree, and the same refusal: `export_scans()` checks every file in data/scans/ before anything is written (the file name is the scan's own date; the [scan] table carries its six fields; every item names a node that is in the tree, once per scan; every verdict is one of the five in docs/scan-plan.md; every item names at least one search it ran, unless it is `quiet` and `found` says why no search was run; every verdict but `quiet` cites a source and a resolution cites two; a flagged item says what it would have done; a ledger entry an item names must be in data/ledger.toml once that file exists). Then it writes each item out with its node's name, factor, chain link and page address, plus every node's own checks newest first and the flagged items nothing has picked up yet. A record may still carry `test = true` to mark a hand-made fixture rather than a week of real work, and the site labels one as a test wherever it appears; no record carries it now that the first real scan has run, and such a record gets no exemption from the rules above. `export.py` also checks the optional `watch` list on a node, which `compute.py` does not know about.

How a run works: for each scenario, the tree is played out many thousands of times. Nodes are visited in dependency order; a world node whose dependencies all came true comes true with its probability for that scenario, and otherwise stays false. Nodes already resolved in the real world are fixed. Choice points are set to their current-plan option. A tier is reached when everything it requires came true, and the number reported for a tier is the fraction of play-throughs that reached it. Contact Clause nodes are reported separately and never feed a tier.

## Publishing: one command

`publish.py` is the last step of every scan and every review (website step 26, written
2026-09-25). One command takes the tree in `data/` to the live site:

    python3 scripts/publish.py                          regenerate, build, and stop to show what changed
    python3 scripts/publish.py --snapshot LABEL         the same, taking a run snapshot first
    python3 scripts/publish.py --push                   the same, then commit everything and push main
    python3 scripts/publish.py --dry-run                all of it in a scratch copy; nothing here is written
    python3 scripts/publish.py --no-story               leave data/story/ as it is
    python3 scripts/publish.py --push --message "..."   your own commit message (repeat for more paragraphs)
    python3 scripts/publish.py --push --fallback-branch claude/scan-YYYY-MM-DD
                                                        if the push to main is refused, push once there instead

In order, stopping loudly at the first thing that fails: it checks the tree (`compute.py validate`);
with `--snapshot LABEL` it plays the tree out and writes `data/snapshots/<date>-<label>.json`; it draws
the tree picture and keeps a dated copy in docs/visual/ only when the picture changed since the newest
copy there; it refreshes data/story/ from TimeAssembler when the key is on this computer (see
data/story/README.md); it runs `export.py`, which also refuses a broken ledger or scan record; and it
builds the site in `site/` (installing the packages first if they are missing). Then it prints what
changed, as git sees it, and the headline before and after. "Before" is the tree as last committed,
played out with the export's own seed, so an unchanged tree shows the same figures to the last digit.

Without `--push` it stops there so the diff can be read; run it again with `--push` to publish. With
`--push`, on main only, it stages everything, makes one commit, and pushes. The site is deployed by
the GitHub Action (.github/workflows/deploy.yml) from that push, as it is for any push to main that
touches the site; the script never deploys by any other road. Every script it runs is run in John's
time zone (America/Los_Angeles), so the dated picture, the snapshot and the commit agree on the date.

Which label: the weekly scan takes `scan` when something moved (docs/scan-procedure.md, step 6); the
quarterly scan takes `quarterly` and the annual review `annual-review` (docs/roadmap.md, steps 17 and
18). They differ because the quarterly scan and the weekly scan fall on the same first Sundays, and a
snapshot is never overwritten.
