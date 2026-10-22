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
differ (decided 2026-10-17 from the first cross-project lessons review, for every tracker).

`scans/` holds the weekly web scans (the Radar, docs/scan-plan.md): one TOML file per scan, named for the date it ran, saying for each node it checked what was searched, what was found and what verdict it reached. Scan files are appended and never edited. The export script (`scripts/export.py`) checks every one of them and refuses to build the site if a record breaks a rule, so a scan on the site is always a scan that adds up. The file dated 2026-09-19 is a hand-made test record, marked `test = true` and labelled as a test wherever the site shows it; it exists so the pages had something to render before the first real scan, and it goes away once one has run.

## The missions: `missions.toml`

Added 2026-10-21 (tracker pattern rule 4.20; docs/proposal-missions-to-watch-2026-10-20.md). The missions on the Missions page, with their milestones. **This file never feeds the number**: `scripts/compute.py` skips it, as it skips the ledger.

- The file: `checked` (the day every date was last read), then one `[[mission]]` per mission, then `[[next]]` (next in line) and `[[left_out]]` (considered and left out, with why), each a name, an https address and a line.
- A mission: `id` (lowercase words joined by hyphens, never renamed; it is the page anchor and what a mission news post names), `name`, `url` (the official page, or Wikipedia where the operator's pages give no text, said in `url_label`), `operator`, `group` (`moon`, `mars`, `asteroids`, `outer` or `orbit`), `what` (one line of what it is for), `why` ("why I follow it", in John's first person; `why_draft = true` while it is a session's draft for him to rewrite), `steps` (the ids of tree steps it bears on; a mission is marked with a diamond when this is not empty), `step_note` (when `steps` is empty: the nearest step and why it does not bear on it), optionally `step_near` (that nearest step's id), `notes`, `status` (`watching`, the default, or `ended`) and `checked`.
- A milestone, `[[mission.milestone]]`: `what` (plain words), a date as `when` or as a span `from` and `to`, `state` (`done`, `plan` or `failed`), `sources` (a list of `{ label, url }`), and optionally `net = true` (no earlier than), `main = true` (the mission's main milestones, where a slip of more than a year earns a post), `label` (words to show in place of the written-out date, only where the plain form would mislead), `note`, and for a moved date `was` (the old date) and `moved_on` (the day it moved).
- Dates are written as precisely as the source gives them and never sharpened: a day (`2027-08-11`), a month (`2027-08`), a part of a year (`early 2028`, `mid 2027`, `late 2027`) or a year (`2027`).
- Prose fields may carry Markdown links (`[words](https://...)`), which the page keeps and the CSV drops to their words.

The check (`scripts/missions.py`, run by `scripts/export.py`) refuses a file where a mission lacks a name, an https address, a group, a line of what it is for, or a "why I follow it" line; an id repeats; a named step is not in the tree; a mission with no steps has no `step_note`; a milestone has no description, no date, a date in another form, a span that runs backwards, a state other than the three, or no source with an https address; a moved date lacks either `was` or `moved_on`; or a milestone marked done or failed starts after the file's `checked` day. A planned milestone whose date has passed is printed as a note for the next reading. It also checks the `[[mission]]` items of the scan records (docs/scan-plan.md).
