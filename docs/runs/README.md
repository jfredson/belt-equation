# Run notes

Each file here is the note for one run of the tree: what was run, the numbers it gave, and how they read against the run before. The numbers themselves are also kept, whole, in the run's snapshot under data/snapshots/.

There are two kinds of note.

## Tree runs

Named `YYYY-MM-DD-<slug>.md`, for example `2026-09-19-first-run.md`. Written when the tree changes (a review lands, a structural ruling, a scan that moved something) to record the headline and tiers before and after.

## Choice runs

Adopted 2026-09-25. Every run of the tree made to compare real options, where the answer could change what John actually does, is saved as its own note:

    docs/runs/YYYY-MM-DD-choice-<slug>.md

`<slug>` names the choice in a few plain words, for example `2027-06-01-choice-next-training-role.md`. The date is the day the run was made. A choice that is run again later gets a new file with the new date, and the old one is left as it was, so the record shows how the answer moved.

A choice run is written before the decision is taken, and finished after. It holds five things:

1. **The options**, in plain words, one line each, with which one is the current plan.
2. **How it was run**: the command, the number of runs per scenario, the seed and the world spread, and the snapshot the tree stood at. For a choice point already in the tree, `python3 scripts/compute.py compare` runs the whole tree once per option. For options not in the tree, say what was changed on a scratch copy to model each one.
3. **The headline per option**: A2 (working off Earth on rotation) under each of the five longevity scenarios, and the second number (A2 at Tier 1) beside it, with the gap between options stated against the run's noise band. A gap inside the noise is written down as "cannot be told apart", not as a finding.
4. **The decision taken**, dated, and who took it.
5. **A dated note** on how much the number weighed in the decision against everything else, in one to three sentences. "The number did not decide this" is a good answer when it is true.

Filled in over time, a choice run is also the evidence for whether the project is a decision tool and not only a forecast, which was the reason given for building it (docs/roadmap.md, step 11).
