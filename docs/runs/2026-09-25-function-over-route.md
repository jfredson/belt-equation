# Sixth run of the tree: 2026-09-25, the function-over-route pass landed

While the introduction essay was being drafted, John asked why the Belt had to wait on a nuclear reactor on the Moon. It did not have to: what lunar mining needs is power through the lunar night, and a reactor is one way to get it. Claude wrote that up as a rule, that a link names the function a child needs and not one route to it, and swept every link in the tree against it (docs/proposal-function-over-route-2026-09-25.md). John approved the proposal in full on 2026-09-25 and counted the pass as the review that methodology.md requires before a tier changes, on the methodology-pass precedent. How each candidate was to land is recorded in docs/handoff-function-over-route-2026-09-25.md. This run follows the methodology pass earlier the same day (snapshot `2026-09-25-methodology-pass`), and is read against it.

What landed:

- **The rule.** A new section, "Function over route", in methodology.md, carrying the rule and the test, and two lines in node-schema.md: `depends_on_any` is now the default form whenever more than one route could satisfy a child, and this sweep is recorded under Known simplifications as the first application, with every later brainstorm applying the test to each new link.
- **Candidate 1, power through the lunar night.** Lunar material at scale now depends on a new step: a hundred kilowatts at one lunar site for ninety percent of a year, from any source (`E-power-through-the-lunar-night-at-a-surface-site`). Three routes sit under it: the lunar reactor, unchanged, and two new steps, polar solar with storage and power sent down from orbit, each written to the reactor's own forty-kilowatt, year-long test so the routes are like for like.
- **Candidate 3, the lunar programme.** The step lunar material waits on now counts a crewed lunar programme, government or commercial, that keeps flying across two changes of its principal backer. The old step had published numbers, so under methodology.md ("What is fixed and what moves") it was retired and replaced rather than renamed: `R-crewed-lunar-program-outlives-two-changes-of-president` is marked replaced by `R-crewed-lunar-program-outlives-two-changes-of-backer`.
- **Candidate 4, a light power source for the fast drive.** The fast-drive step now depends on a new step, a hundred megawatts of electricity from a system of no more than a hundred tonnes (`E-compact-power-source-at-fast-drive-scale`). The bar is one kilogram per kilowatt because that is the practical requirement the drive's own record gives, from agency fusion-rocket studies; a hundred megawatts covers the drive's fifty megawatts of exhaust power after conversion losses. The grid fusion plant and a new fission-electric route (a flight-built fission system reaching a hundred megawatts) sit under it. The drive's own conditional was re-estimated up, because the weight gap it used to price now sits in the new step.
- **Candidate 5, a crewed round trip beyond the Moon.** The crewed site beyond the Earth-Moon system now waits on any crewed round trip at least five million kilometres from Earth, with Mars named as the likeliest instance. The Mars step was retired and replaced the same way as candidate 3 (`D-crew-round-trip-to-mars` replaced by `D-crew-round-trip-beyond-the-earth-moon-system`).
- **Candidate 6, fast transit.** Tier 3 now requires `D-fast-transit-in-routine-use`, three missions in one year reaching the asteroid belt within twelve months of leaving Earth, crewed or cargo, instead of routine nuclear propulsion. Routine nuclear propulsion and a new step for megawatt solar-electric propulsion in routine use are its routes. The Tier 3 definition now reads "transit fast enough that people go out there to work", in data/tiers.toml and docs/definitions.md, with an entry in the definitions decision log.
- **Candidate 7, off-Earth material.** The profitable-product step now depends on an either-route step, a hundred tonnes a year from the Moon or from an asteroid (`L-off-earth-material-delivered-at-scale`), with a new asteroid route beside the lunar one.
- **Candidate 9, food made on site.** The year of closed-loop life support now counts "most of its food produced on site from raw inputs", so cultured or fermented food made from things that are not themselves food counts beside crops. The staple crop stays its parent, unchanged. No number moved.
- **Candidate 2, checked and left.** The link from lunar material at scale to the reusable crewed lunar lander was checked: a hundred tonnes a year almost certainly needs reusable landers, possibly uncrewed ones, but the proposal rated it weak and John ruled it left. The link stands.

Each changed candidate has its own commit and its own structure entry in data/ledger.toml, and every node whose fields changed carries a dated revision. The tree is now eighty-one nodes, two of them retired.

**The home page chain.** The energy link now rests on the new power step alone. `chain_gates` in scripts/compute.py finds it through lunar material at scale, which Tier 3 names, as the fallback approved on 2026-09-25 was written to do. The walk stops at the first energy step it meets, so the three routes under it are not ANDed into the link. The drive link now reads the fast-transit step in place of routine nuclear propulsion.

Command: `cd ~/Code/belt-equation && python3 scripts/compute.py run --snapshot sweep-function-over-route --snapshot-date 2026-09-25` (20,000 runs per scenario, seed 2026, world spread 1.0). The label is `sweep-function-over-route` rather than `function-over-route` because two runs taken on one day are ordered by label, and `function-over-route` would have sorted before `methodology-pass`, putting this run before the one it follows. Snapshot: data/snapshots/2026-09-25-sweep-function-over-route.json. Attribution: data/attribution/2026-09-25-sweep-function-over-route.json, from `python3 scripts/compute.py attribute 2026-09-25-sweep-function-over-route --write`.

## Headline and tiers

```
Runs per scenario: 20000 (seed 2026), world spread 1 on the log-odds scale

Tier reached, by scenario:
  tier    baseline  moderate    strong   radical      open
  T1         0.352     0.441     0.567     0.702     0.731
  T2         0.073     0.116     0.219     0.443     0.532
  T3         0.009     0.018     0.055     0.166     0.239
  T4         0.002     0.005     0.019     0.085     0.143
  A0         0.143     0.214     0.314     0.391     0.402
  A1         0.361     0.490     0.643     0.771     0.819
  A2         0.006     0.012     0.038     0.108     0.150  <- headline
  A3         0.006     0.011     0.036     0.105     0.148
```

The full per-node table is in the snapshot.

## Read against the run before

Against `2026-09-25-methodology-pass`, with the same seed. Unlike the last read, this one is not like for like even where nothing changed: the new steps take their own rolls of the dice, which shifts the draws every later step gets, so figures the pass did not touch move by a few tenths of a point in either direction. Tier 1, Tier 2, A0 and A1 moved that way and only that way. Percentages:

| | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| A2, the headline | 0.47 → 0.59 | 1.17 → 1.20 | 3.52 → 3.77 | 10.71 → 10.83 | 14.67 → 15.05 |
| Tier 3, the Belt | 0.74 → 0.94 | 1.69 → 1.80 | 5.08 → 5.47 | 15.93 → 16.64 | 22.97 → 23.94 |
| Tier 4, Full Expanse | 0.11 → 0.23 | 0.35 → 0.53 | 1.66 → 1.93 | 8.13 → 8.53 | 13.84 → 14.28 |
| A3, lives off Earth | 0.43 → 0.56 | 1.12 → 1.14 | 3.36 → 3.56 | 10.42 → 10.50 | 14.37 → 14.77 |
| Energy link on the home page chain | 67.5 → 72.8 | 75.8 → 82.2 | 87.0 → 89.7 | 92.8 → 94.5 | 93.8 → 96.1 |
| Drive link | 5.5 → 6.9 | 10.4 → 12.1 | 22.4 → 24.9 | 46.7 → 49.5 | 56.8 → 59.1 |
| Motive link | 4.5 → 5.9 | 8.4 → 10.1 | 17.2 → 21.2 | 32.5 → 38.8 | 40.4 → 47.5 |
| Launch link | 12.0 → 13.1 | 19.8 → 20.8 | 33.9 → 35.5 | 50.7 → 51.5 | 57.2 → 58.5 |

**The headline rose, by about the width of the noise.** The attribution puts the whole move at +0.12 points by 2071, +0.03 by 2080, +0.25 by 2095, +0.13 by 2136 and +0.38 with no deadline, against a noise band of 0.11, 0.15, 0.27, 0.44 and 0.51. Only the 2071 figure is outside the band, and only just. None of the seven entries can be separated from the others, since each changed the tree's shape rather than a number, so the whole move is reported as the remainder.

## What moved and why

The steps the pass rewired rose a good deal on their own; the headline did not, because the Belt tier still needs every one of its eight requirements at once, and A2 needs a rotating role on top.

- **Off-Earth product sold at a profit** rose the most: 6.4 → 8.6 percent by 2071 and 48.6 → 58.3 with no deadline. Candidate 7's asteroid route (11.0 percent by 2071 on its own) gives it a second supply. It does not reach the headline, because Tier 3 still names lunar material at scale directly, so every play-through that reaches the Belt already has the lunar route. Moving that tier requirement onto the either-route step was not part of the ruling; it is listed below.
- **Lunar material at scale** rose from 16.7 to 18.2 percent by 2071 (candidate 1): the new power step is 72.8 percent by 2071 against the reactor's 67.5, because polar solar with storage now counts. On a scratch copy with the reactor link put back and everything else as landed, the headline by 2071 is 0.48 rather than 0.59, so candidate 1 is worth about a tenth of a point there, and less in the longer windows.
- **Fast transit (candidate 6)** is 32.7 percent by 2071 against routine nuclear propulsion's 28.8, which Tier 3 required before. With Tier 3 put back on nuclear propulsion, the headline is 0.54 by 2071 and 14.70 with no deadline, so the change is worth +0.05 and +0.35. Its own number carries a cost: the step asks for three ships a year actually going to the asteroid belt, a conditional of 0.50 by 2071, and with that set to 1 the headline would be 0.63 and 15.65. The second route adds about twice what the belt requirement takes back.
- **Crewed site beyond the Earth-Moon system** rose from 9.6 to 10.6 percent by 2071 (candidate 5): the widened round trip is 39.2 percent against the Mars trip's 35.4. On the headline it is inside the noise.
- **The lunar programme (candidate 3)** is 74.4 percent by 2071 against 71.8. Inside the noise on the headline.
- **The fast drive (candidate 4)** rose from 3.4 to 5.1 percent by 2071, and is level with no deadline (47.7 → 47.8). The re-estimate was set so the fusion-plant route alone gives about the old chance; the rise by 2071 is the fission route, plus the world draw treating two moderate numbers differently from one small one. It feeds only Tier 4, which rose with it.
- **Closed-loop life support (candidate 9)** did not move beyond the dice, as intended.

The decision comparison at the six-year fork is unchanged in reading: 0.59 against 0.56 percent by 2071, 3.77 against 3.99 by 2095, inside the noise, and the row stays reported but not read until the access-branch review.

## The second number

A rotation at a station or lunar base, Belt or no Belt, is 8.9 percent by 2071, 14.6 by 2080, 23.7 by 2095, 31.9 by 2136 and 33.9 with no deadline, against 8.9, 14.8, 23.6, 32.4 and 34.7 before. Nothing the pass changed sits under it (Tier 1 and the rotating-role step), so the differences are the dice.

## First estimates set in this pass, not yet ruled by John

| Step | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| Power through the lunar night at a site, 100 kW, any source (given a route) | 0.90 | 0.93 | 0.95 | 0.97 | 0.98 |
| Polar solar with storage runs a lunar site for a year | 0.55 | 0.68 | 0.82 | 0.90 | 0.93 |
| Power sent down from orbit runs a lunar site for a year | 0.08 | 0.12 | 0.22 | 0.38 | 0.48 |
| Lunar programme across two changes of backer (re-estimate; was 0.75 / 0.80 / 0.85 / 0.90 / 0.92) | 0.78 | 0.82 | 0.87 | 0.91 | 0.93 |
| A 100 MW power source of at most 100 tonnes (given a route) | 0.08 | 0.12 | 0.20 | 0.40 | 0.55 |
| A flight-built fission-electric system reaches 100 MW | 0.04 | 0.07 | 0.14 | 0.28 | 0.38 |
| Fast drive, given the light power source (re-estimate; was 0.03 / 0.06 / 0.15 / 0.35 / 0.50 given the fusion plant) | 0.38 | 0.50 | 0.75 | 0.88 | 0.91 |
| Crewed round trip beyond the Earth-Moon system (re-estimate; the Mars trip was 0.45 / 0.60 / 0.78 / 0.90 / 0.93) | 0.52 | 0.66 | 0.82 | 0.92 | 0.94 |
| Three missions a year reach the asteroid belt within a year (given a route) | 0.50 | 0.62 | 0.76 | 0.87 | 0.91 |
| Megawatt solar-electric propulsion on three missions a year | 0.40 | 0.52 | 0.68 | 0.82 | 0.87 |
| A hundred tonnes a year of asteroid material delivered to orbit | 0.08 | 0.13 | 0.25 | 0.45 | 0.55 |

The either-route step for off-Earth material carries 1.0, as the biology hedge does, so its number is its routes'.

## Left for the next sessions

- John rules on the first estimates in the table above. Any he moves lands as a probability revision with its own ledger entry and a fresh run.
- **Tier 3 still names lunar material at scale.** Under the rule, the Belt tier would list the either-route off-Earth material step instead, which is what would let the asteroid route reach the headline. That is a tier change and was not in the ruling; it is the most consequential open question the sweep leaves.
- **The fast drive's criterion still says fusion-powered** (step 27, item 70, written to match the old fusion-plant link). With a fission-electric route under its power step, John may want the criterion to admit any power source; as written, a fission route helps it only as evidence that a light source can be built.
- **Fast transit names the Belt.** A world whose outer site is Mars, with fast ships going only there, does not meet Tier 3's transit step. That follows the ruling's criterion and is recorded here so it is a choice rather than an accident.
- **The beyond-the-Moon boundary.** The crewed site beyond the Earth-Moon system counts anything "farther from Earth than the Moon's orbit". The far side of the Moon itself is slightly farther than that, which is why the new round-trip step uses five million kilometres. The site step's own boundary could be tightened the same way at the next review.
- **Retired steps on the site.** Two steps are marked replaced for the first time. Their pages show the "Replaced" callout and link to the new step, but they still show their old probability table and a run figure of zero; a small site change could hide the table for a retired step.
- Two new `verify` flags, the tall-mast lunar solar awards and the solar-electric transit time to the Belt, go to the next scan with the rest of the verify list.
- Candidate 2, the reusable crewed lander under lunar material, stays as it is, checked and left.
