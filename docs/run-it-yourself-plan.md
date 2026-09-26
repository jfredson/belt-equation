# Website step 39: run it for yourself

Written 2026-09-20. This is the plan document for the page that lets a visitor put in their own
birth year, pick one of the five longevity scenarios and a route, and see what the tree says for
them. The step existed only as a line in TimeAssembler ("Website step 27"); the number 27 is
already the outside-model review in docs/roadmap.md, and the ledger plan took 28 to 33 and the
scan plan 34 to 38, so this is step 39 everywhere from now on and the TimeAssembler task has
been renamed to match.

The build brief this came from is docs/run-it-yourself-brief.md, written the same day.

**What is John's to decide.** The three decisions below are recorded in the form the ground rule
of 2026-09-08 requires: for each one, how confident Claude is, whether it is standard practice
or a judgment call, and the strongest alternative with what choosing it would cost. The page has
been built against the recommended option in every case, so that there is something to look at
rather than a description of something. None of the three is settled: John accepts them, or
moves one, and the page changes to match. The page goes live when he merges the pull request,
and not before.

**What the page does not do.** It reads the tree. It does not write to it. No stored probability,
no committed run, no snapshot and no headline number changes because this page exists, and none
of them is computed differently than before. The ledger and the Radar are untouched.

---

## Decision 1. The reader's deadline

**Recommended: shift John's five windows by the difference in birth years, and read each event's
probability at the shifted year by drawing a line between the two neighbouring windows on the
log-odds scale.**

The five windows are not calendar years that happen to be interesting. They are John's ages: 85,
94, 109 and 150, for a man born in January 1986, plus the case where the deadline drops out
entirely. So a reader born in 2000 who picks the baseline scenario is asking about their own 85th
year, 2085, and the tree has no numbers for 2085. Shifting keeps a scenario meaning the same
thing for everybody: the same age, under the same assumption about what medicine does. Reading a
number at the shifted year is then a piece of arithmetic between two estimates the tree already
has.

The rule, in full, is written into docs/methodology.md under "Running the tree for somebody
else", because it is a method and belongs where the rest of the method is rather than buried in a
script. In short: a straight line on the log-odds scale between the two neighbouring windows; a
floor at the baseline number for any deadline at or before 2071, because the tree was never
estimated for a shorter wait; and beyond 2136 a move toward the no-deadline number that closes
half the remaining distance every 41 years, which is the gap between the last two named windows.
It reaches the no-deadline number only in the limit and never passes it.

**Confidence: moderate.** The shift is the part worth being confident about; it is the only
reading of the five scenarios that means anything for a stranger. The line between the windows is
the part that is a judgment, and the methodology section says so in the plainest words available:
the five numbers were estimated as five separate answers to five separate questions, not as
points on a curve, and drawing a line between them assumes they lie on one. That assumption is
the method's, not the estimator's. The further a reader's deadline falls from one of John's five
windows, the more of their answer is the line and the less is the estimate.

**Judgment call, on a standard footing.** Interpolating on the log-odds scale is ordinary
practice wherever probabilities are interpolated, and it is the scale the world draw already uses
(docs/methodology.md, "The world draw"), so the page introduces no new scale. What is a judgment
is interpolating these five points at all, and the two end rules.

**The strongest alternative: snap the reader to whichever of John's five windows is nearest.**
It costs nothing to build, introduces no new arithmetic, and needs no new section in the
methodology document. What it costs is the page's point. A reader born in 2000 would be shown
John's 2071 number for their own baseline, which is their 71st year rather than their 85th, and
the page would then have to spend a paragraph explaining why the number it just gave them is not
really theirs. Two readers fourteen years apart in age would get identical answers. The whole
reason to build the page is that a reader's deadline is different from John's; snapping throws
away exactly that.

**A second alternative worth naming: estimate the tree at more windows.** The honest fix for
"five points are not a curve" is more points, estimated rather than interpolated. That is a large
piece of work (sixty-nine events, each re-estimated at each new window) and it belongs to an
annual review, not to a website step. If John ever wants the curve to be real rather than read,
this is how it happens, and the interpolation can be retired the day it does.

---

## Decision 2. The reader's route

**Recommended: three routes, each a list of world events already in the tree, plus at most one
number the reader supplies. The reader's number is shown separately and labelled as theirs.**

The access branch of the tree is John's: his current training, the six-year fork of his current
contract, his current career turning into commercial crew training. None of that is a stranger's path, and a
stranger's odds must not be run through it. So a route is defined from world events only:

| Route | What the tree is asked | The reader's own part |
|---|---|---|
| **Buy a seat** | A seat to orbit is sold to a private person for under a million dollars. | Their chance of affording it, and passing the medical, once seats sell at that price. |
| **Work a rotation** | An industry selling services to spaceflight crews exists, and a hundred people are paid to work off Earth at the same time. | Their chance of getting one of those jobs, once the industry and the jobs exist. |
| **Contribute from Earth** | An industry selling services to spaceflight crews exists. | None. This route asks for no number of the reader's own. |

The reader's number defaults to 10 percent, is theirs to change, and is never mixed into the
tree's figure. The page shows the world's part, then their part with the input sitting beside it,
then the two multiplied, last and smallest, because that combined figure is the least reliable
thing on the page.

**Confidence: moderate on the shape, lower on the third route.** Splitting the world's part from
the person's part is the right shape and the one the page most needs: it is what keeps a visitor
from reading their own guess as the project's estimate. Two of the three routes map cleanly onto
events the tree already has. The third does not, and this is the place where the build had to
make a reading rather than follow an instruction, so it is flagged here rather than buried.

**Where the third route needed a reading.** "Contribute from Earth" is the A0 tier, and A0
requires one event: working in or for the off-world industry. That event's own requirements are
John's two route events, which are gated on his choice at the six-year fork. Strip John out and
one world event is left underneath it: that an industry selling survival and contingency services
to spaceflight crews exists. That is what the page uses. It is narrow. A0 means working in or for
the off-world industry in any capacity, and the event the page leans on is about one Earth-side
service industry in particular. The number the page shows for this route should be read as a
proxy for "Earth-side work for the off-world industry has grown into a thing a person can join",
which is close to what a reader means but not the same as what the event says.

Two ways to improve it, both John's call, neither taken here: add a second event to the route
(a commercial customer paying for work done in orbit is the obvious candidate, and would make the
route stricter and better defined), or add an event to the tree that says plainly that the
off-world industry employs people on Earth at scale. The second is a change to the tree, which
this step is explicitly not allowed to make.

**Judgment call.** There is no standard practice for "turn one person's decision tree into a
stranger's". The defensible part is the discipline: every route is a list of events that already
exist, with their own written tests, and the reader's guess is quarantined from all of them.

**The strongest alternative: the world tiers only, with no personal number at all.** Show a
reader the chance of an outpost, a settlement, a Belt and a full Expanse by their deadline, and
stop. It is more honest, because every figure on the page would then come from the tree and
nothing from a stranger's guess about themselves, and it removes the risk that someone screenshots
"my odds: 5 percent" when four of those five points were a number they typed themselves. What it
costs is the question the page is named after. "Run it for yourself" that never mentions you is a
world forecast with a date picker. The mitigation chosen instead is order and labelling: the
world-tier view is the first thing shown and the largest, the reader's own number is labelled as
theirs everywhere it appears, and the combined figure is last and smallest. Note that the
world-tier view is on the page under either decision, so choosing this alternative is a matter of
deleting the route section, not rebuilding the page.

---

## Decision 3. Where the numbers come from

**Recommended: the export script precomputes a grid in Python; the page reads between grid years
and multiplies in the reader's number. No probability is ever computed in the browser.**

`scripts/export.py` writes `site/src/data/reader.json` on every build, as it already writes the
tree, the changelog, the snapshots, the ledger, the scan records and the story. The grid holds
one cell per five-year deadline across the whole range a shifted window can land in, plus one
cell for no deadline at all: 31 cells, each the whole tree played out 5,000 times with the
standard seed and the standard world spread. Each cell records every tier's rate and, per route,
how often all of that route's events came true in the same play-through. The page finds the two
grid years either side of a reader's deadline, reads between them in a straight line, and
multiplies in the reader's own number. That is arithmetic on two numbers, not a simulation.

This keeps website-plan decision 3 intact: Python is the only place a number is worked out, and
every figure the page can show is reproducible from a committed export. `compute.py reader
--birth YEAR --scenario KEY --route KEY` prints one cell so any figure on the page can be checked
by hand against the tree.

**Two things that differ from the brief, both deliberate, both cheap to reverse.**

*The grid runs 2025 to 2170, not 2035 to 2140.* The done condition for this step is that a reader
born in any year from 1940 to 2020 gets an answer that matches the script. A reader born in 1940
has a baseline deadline of 2025; a reader born in 2020 has a radical-extension deadline of 2170.
The brief's range would have left both ends off the grid. The range is now derived from the birth
years the page offers rather than written down as two numbers, so the two cannot drift apart, and
a test checks that every birth year in range lands inside the grid.

*A deadline in the past is possible and the page says so.* A reader born in 1940 asking the
baseline question is asking about 2025, which has gone. Under decision 1's floor the tree answers
with its baseline numbers, which is the lowest it can see. That is not a real answer for 2025 and
the page says as much in plain words when the deadline is in the past.

**Confidence: high.** This is the same pattern every other number on the site already follows,
and it is the pattern the website plan settled in decision 3.

**Standard practice**, for a static site that must not duplicate its own maths.

**What it costs.** Two things. Export time: the grid adds about eleven seconds to a build, which
runs on every push through the deploy workflow. Acceptable, and far below the several minutes a
snapshot's node-worth table takes. And coarseness: at 5,000 play-throughs a cell's figures carry
roughly a point of run-to-run noise on a rate near a half, so two adjacent grid years can differ
by a point in the wrong direction in the far tail, where the real curve is nearly flat. A reader
who nudges their birth year by one may see a figure tick the wrong way. Raising the cell count to
20,000 would fix it and add about forty seconds to every build; that trade is worth revisiting if
anyone notices, and it is one number in the script (`READER_RUNS`).

**The strongest alternative: port the play-through loop to the browser and run it live on
tree.json.** It is about sixty lines; `tree.json` already carries the dependencies, the tiers and
every event's five probabilities. What it would buy is real: no grid, no reading between grid
years, an exact answer at any deadline, and the door open to letting a reader move an individual
event's probability and watch the headline respond, which is the most interesting thing this site
could eventually do. What it costs is the rule that has kept the site honest so far. There would
be two implementations of how the tree is played out, in two languages, and the day they disagree
the website would be showing a number the repository cannot reproduce. The site's whole claim is
that every figure on it comes out of the committed tree by the committed script.

**When the alternative becomes the right choice:** when a reader is to be given control of
individual events rather than a deadline and a route. A grid cannot precompute that, because the
number of combinations is not finite in any useful sense. At that point the honest way to do it
is to compile one implementation to both places, or to accept the browser copy and test it
against the Python on every build. That is version two of this page, and it is not this step.

---

## What was built

- `scripts/compute.py`: the reading of a deadline (`deadline_probability`, beside `shifted`,
  which is the other function that works on the log-odds scale), the shifted windows
  (`reader_deadline`), one cell (`reader_cell`), the whole grid (`reader_grid`), and a `reader`
  command that prints one cell for checking by hand.
- `scripts/test_reader.py`: thirteen checks, run with `python3 scripts/test_reader.py`. The one
  that matters plays the tree out at John's own five windows with the committed snapshot's own
  dice and requires every system tier's rate to come out *exactly* equal to the snapshot's.
  Because the reading hands back the stored numbers untouched at those years, the dice fall the
  same way and the rates must match to the last digit; anything else means the reading has
  changed what the tree says. A second check does the same with the grid's own smaller number of
  play-throughs and its own dice, within the run-to-run noise both runs carry.
- `scripts/export.py`: `export_reader()`, writing `site/src/data/reader.json`.
- `site/src/pages/run/index.astro`: the page, in the house style, with an inline script like the
  home page's dial. No framework, no external requests, no probability computed in the browser.
- `docs/methodology.md`: the new section, "Running the tree for somebody else".
- The page is in the site navigation and is pointed at from the home page.

## What this step deliberately leaves alone

- The tree. No event added, cut, reworded or re-estimated.
- The headline, the snapshots, the ledger, the Radar, and every number already on the site.
- John's own path. No route touches his current training, the six-year fork, the two route events
  under it, or the chain from his current career into crew training.
- The five scenarios and the world spread, which are fixed until an annual review
  (docs/methodology.md, "What is fixed and what moves").
