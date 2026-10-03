# Seventh run of the tree: 2026-10-02, the function-over-route estimates ruled

The function-over-route pass of 2026-09-25 (docs/runs/2026-09-25-function-over-route.md) left eleven numbers as Claude's first estimates, waiting on John. On 2026-10-02 Claude reviewed all eleven with John, giving for each its confidence and the strongest alternative, and John ruled on them in one sitting.

What was ruled:

- **Nine stand as set on 2026-09-25**, now accepted by John: power through the lunar night given a route (0.90 by 2071), power sent down from orbit (0.08), the lunar programme across two changes of backer (0.78), the hundred-megawatt power source under a hundred tonnes given a route (0.08), the fission-electric system reaching a hundred megawatts (0.04), the fast drive given the light power source (0.38), the crewed round trip beyond the Earth-Moon system (0.52), three missions a year reaching the asteroid belt within a year given a route (0.50), and a hundred tonnes a year of asteroid material (0.08). Each step's reasoning now says so.
- **Polar solar with storage runs a lunar site for a year: raised** from 0.55 / 0.68 / 0.82 / 0.90 / 0.93 to 0.65 / 0.76 / 0.86 / 0.92 / 0.94. Every south-pole base plan starts on solar, so fifteen points under the reactor (0.70) was too cautious. It stays below the reactor in every window.
- **Megawatt solar-electric propulsion in routine use: raised** from 0.40 / 0.52 / 0.68 / 0.82 / 0.87 to 0.50 / 0.60 / 0.73 / 0.84 / 0.88. It had been set level with routine nuclear propulsion, but it is further along and needs no reactor approvals. In the two longest windows it stays just under nuclear propulsion, because solar power weakens with distance from the Sun.

Who decided what: both raises were proposed by Claude and accepted by John, and only the 2071 figure of each was put to him. The figures for the four longer windows are Claude's, scaled to keep each step's shape; John can move them at the annual review. The fast-transit step (three missions a year to the Belt) was discussed as the one that matters most, because the Belt tier requires it directly; it was left at 0.50 with low-to-moderate confidence and is marked for another look at the annual review of 2027-01-03.

One wording addition: the polar-solar step's reasoning now says that forty kilowatts is the route's own bar, the same as the reactor's, and that the step up to a hundred kilowatts is priced in the step above it.

Each raise has a dated revision on its step and its own entry in data/ledger.toml. Before the run, main was merged into the branch (the 2026-09-27 weekly scan, the question's rewording, the Contact Clause rung rename); nothing in that merge changed a number.

Command: `python3 scripts/compute.py run --snapshot estimates-ruled --snapshot-date 2026-10-02` (20,000 runs per scenario, seed 2026, world spread 1.0). Snapshot: data/snapshots/2026-10-02-estimates-ruled.json. Attribution: data/attribution/2026-10-02-estimates-ruled.json, from `python3 scripts/compute.py attribute 2026-10-02-estimates-ruled --write`.

## Headline and tiers

```
Tier reached, by scenario:
  tier    baseline  moderate    strong   radical      open
  T1         0.361     0.444     0.569     0.703     0.729
  T2         0.069     0.122     0.224     0.438     0.533
  T3         0.008     0.018     0.058     0.164     0.236
  T4         0.002     0.005     0.021     0.085     0.140
  A0         0.146     0.219     0.309     0.393     0.400
  A1         0.363     0.490     0.639     0.768     0.818
  A2         0.005     0.012     0.038     0.108     0.148  <- headline
  A3         0.004     0.011     0.036     0.104     0.146
```

The full per-node table is in the snapshot.

## Read against the run before

Against `2026-09-25-sweep-function-over-route`, same seed. Percentages:

| | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| A2, the headline | 0.59 → 0.47 | 1.20 → 1.21 | 3.77 → 3.78 | 10.83 → 10.75 | 15.05 → 14.84 |
| Tier 3, the Belt | 0.94 → 0.79 | 1.80 → 1.78 | 5.47 → 5.78 | 16.64 → 16.40 | 23.94 → 23.56 |
| Tier 4, Full Expanse | 0.23 → 0.19 | 0.53 → 0.53 | 1.93 → 2.06 | 8.53 → 8.54 | 14.28 → 14.01 |
| Second number, a rotation at a station or lunar base | 8.9 → 9.3 | 14.6 → 14.9 | 23.7 → 23.7 | 31.9 → 32.1 | 33.9 → 33.8 |
| Energy link on the home page chain | 72.8 → 75.3 | 82.2 → 83.8 | 89.7 → 89.7 | 94.4 → 94.6 | 96.1 → 96.2 |
| Drive link | 6.9 → 6.8 | 12.1 → 12.5 | 24.9 → 25.9 | 49.5 → 49.8 | 59.1 → 58.8 |

**The headline did not move beyond the dice.** Two numbers went up and the headline by 2071 reads lower, 0.47 against 0.59, which is the figure it had before the function-over-route pass. That is not the rulings pulling it down. The attribution puts the two entries together at −0.06 points by 2071, +0.10 by 2080, −0.13 by 2095, −0.13 by 2136 and −0.18 with no deadline, every one inside its noise band (0.10, 0.15, 0.27, 0.44 and 0.50), and with mixed signs. Changing a step's number changes which play-throughs it comes up yes in, and that reshuffle is larger than the effect of the raises themselves. The plain reading of the two runs together is that the headline by 2071 is about half a percent and the function-over-route pass, estimates included, has not moved it by an amount this method can see.

## What moved and why

- **Power through the lunar night** rose from 72.8 to 75.3 percent by 2071, which is the polar-solar raise arriving where it should (polar solar itself went from 53 to 63 percent). Lunar material at scale followed, 18.2 to 18.9 percent.
- **Megawatt solar-electric propulsion** went from 40 to 50 percent by 2071, and **fast transit** from 32.7 to 35.2. The Belt tier needs seven other things at once, so that gain is too small to show in Tier 3 against the dice.
- The second number sits under nothing that changed; its differences are the dice.

## Left for the next sessions

The four questions the sweep left open stand, and none was ruled on 2026-10-02:

- Tier 3 still names lunar material at scale, so the asteroid route cannot reach the headline.
- The fast drive's criterion still says fusion-powered, so the fission route under its power step can never satisfy it.
- Fast transit names the Belt; a world whose fast ships go only to Mars does not meet it. Marked for the annual review together with its 0.50.
- The boundary of "beyond the Earth-Moon system" on the crewed-site step.

Also carried over: retired steps still show their old probability table on the site, and two `verify` flags (the tall-mast lunar solar awards, the solar-electric transit time to the Belt) go to the next scan.
