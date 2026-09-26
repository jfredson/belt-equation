# Fifth run of the tree: 2026-09-25, the methodology pass landed

The methodology pass is the one structural review that the outside-model review protocol set aside (docs/reviews/protocol.md, decision 5). Claude proposed a change for each of the seven tier and method items that the 2026-09-19 rulings deferred to it (docs/methodology-pass-2026-09-25.md; item 102, a text fix, landed with the proposal). John ruled on all of them on 2026-09-25 and counted the pass as the review that methodology.md requires before a tier's requirements change, so everything landed the same day. The ruling is in TimeAssembler as the decision entry "Methodology pass ruled 2026-09-25". This run follows the Contact Clause C5 landing earlier the same day (snapshot `2026-09-25-c5`), and is read against it.

What landed:

- **Item 96:** a note in definitions.md that A3 requiring A2 is a limit of the one route the tree models. The direct-migration route waits for the access-branch review after pipeline graduation (May 2027). Words only.
- **Item 97:** Tier 1 is tested by the hundred-workers node alone, so a crewed station counts. The reusable lunar lander, the lunar reactor and the lunar programme left Tier 1's list; they still gate Tier 3 through lunar material at scale.
- **Item 98:** a note in definitions.md that the tier headcounts describe each tier and the requirement lists test it. Counting people directly is left to version two. Words only.
- **Item 99:** the child born and raised off Earth moved from Tier 2's definition to Tier 4's, matching the 2026-09-19 move of the requirement itself. Words only.
- **Item 100:** part (a) only. The anti-satellite test ban left Tier 4 and stays in the tree as a tracked event that gates no tier. Moving the traffic-management authority into its place (part b) was declined, so the authority stays a Tier 3 requirement as ruled on 2026-09-19.
- **Item 101:** the timing assumption stated in methodology.md. The completion-date method is described in the proposal and not built. Words only.
- **One change John approved during the landing:** the home page chain names each factor's link from the steps the headline's tiers list. When Tier 1 stopped listing the lunar reactor, energy had no listed step left and would have dropped off the chain, although the Belt still waits on that reactor through lunar material at scale. John approved a fallback on 2026-09-25: a factor with no listed step takes the nearest steps of its own that the listed ones depend on (`chain_gates` in scripts/compute.py). On the tree before this pass the fallback changes nothing, since every factor had a listed step; on this tree it gives energy the lunar reactor back.

Command: `cd ~/Code/belt-equation && python3 scripts/compute.py run --snapshot methodology-pass --snapshot-date 2026-09-25` (20,000 runs per scenario, seed 2026, world spread 1.0). Snapshot: data/snapshots/2026-09-25-methodology-pass.json. Attribution: data/attribution/2026-09-25-methodology-pass.json.

## Headline and tiers

```
Runs per scenario: 20000 (seed 2026), world spread 1 on the log-odds scale

Tier reached, by scenario:
  tier    baseline  moderate    strong   radical      open
  T1         0.350     0.442     0.566     0.704     0.735
  T2         0.068     0.117     0.220     0.437     0.530
  T3         0.007     0.017     0.051     0.159     0.230
  T4         0.001     0.004     0.017     0.081     0.138
  A0         0.139     0.216     0.309     0.398     0.409
  A1         0.354     0.491     0.644     0.773     0.818
  A2         0.005     0.012     0.035     0.107     0.147  <- headline
  A3         0.004     0.011     0.034     0.104     0.144
```

The full per-node table is in the snapshot.

## Read against the run before

Against `2026-09-25-c5`, with the same seed, so a figure whose tier did not change is identical rather than merely close. Percentages:

| | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| Tier 1, outpost | 18.2 → 35.0 | 26.0 → 44.2 | 38.3 → 56.6 | 53.6 → 70.4 | 58.0 → 73.5 |
| Tier 2, settlement | 5.0 → 6.8 | 8.9 → 11.7 | 17.5 → 22.0 | 36.2 → 43.7 | 44.4 → 53.0 |
| Tier 4, Full Expanse | 0.1 → 0.1 | 0.3 → 0.4 | 1.4 → 1.7 | 7.4 → 8.1 | 12.6 → 13.8 |
| A2 at Tier 1, the second number | 6.0 → 8.9 | 10.8 → 14.8 | 18.3 → 23.6 | 27.2 → 32.4 | 29.6 → 34.7 |
| Regime link on the home page chain | 18.4 → 21.5 | 25.0 → 28.8 | 37.9 → 43.0 | 57.0 → 63.3 | 66.1 → 72.2 |

**Did not move, to the last play-through:** the headline (A2 0.47 / 1.2 / 3.5 / 10.7 / 14.7 percent), Tier 3, A0, A1, A3, every node's own figure, the Contact Clause, the decision comparison at the six-year fork, and the launch, energy, drive, biology, motive and access links of the chain. The attribution puts the headline's move at exactly zero in every scenario, against a noise band of 0.10 points by 2071.

Tier 1, Tier 2 and the second number moved as the proposal predicted for item 97 (it had Tier 1 at 34.9 and the second number at 8.8 by 2071, from the 2026-09-20 tree; the C5 landing gave the Contact Clause dice of their own, which shifts every figure by a few tenths). Tier 4 moved as predicted for item 100 part (a). The regime link rose because it no longer includes the lunar programme directly; that step now sits under lunar material at scale, which the launch link carries. The launch link lost the reusable lander for the same reason, and its rate did not change, because lunar material at scale already requires the lander.

## The second number

A rotation at a station or lunar base, Belt or no Belt, is now 8.9 percent by 2071 and 23.6 percent by 2095, up from 6.0 and 18.3. This is the figure the pass changed most, and the one a visitor sees beside the headline. It rose because the outpost tier now counts a station.

## Left for the next sessions

- The access-branch review after pipeline graduation (May 2027) takes item 96's direct-migration route, beside item 29's three personal nodes.
- Item 98's headcount nodes and item 101's completion-date method are version-two candidates for a later annual review.
- The anti-satellite ban and the megawatt radiator are now the two tracked steps that gate no tier. The first founding rule excludes a node for being irrelevant; both are kept by John's ruling, and the annual review may retire either.
