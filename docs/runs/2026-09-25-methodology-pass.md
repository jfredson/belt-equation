# Fourth run of the tree: 2026-09-25, the methodology pass landed

The methodology pass is the one structural review that the outside-model review protocol set aside (docs/reviews/protocol.md, decision 5). Claude proposed a change for each of the seven tier and method items that the 2026-09-19 rulings deferred to it (docs/methodology-pass-2026-09-25.md; item 102, a text fix, landed with the proposal). John ruled on all of them on 2026-09-25 and counted the pass as the review that methodology.md requires before a tier's requirements change, so everything landed the same day. The ruling is in TimeAssembler as the decision entry "Methodology pass ruled 2026-09-25".

What landed:

- **Item 96:** a note in definitions.md that A3 requiring A2 is a limit of the one route the tree models. The direct-migration route waits for the access-branch review after pipeline graduation (May 2027). Words only.
- **Item 97:** Tier 1 is tested by the hundred-workers node alone, so a crewed station counts. The reusable lunar lander, the lunar reactor and the lunar programme left Tier 1's list; they still gate Tier 3 through lunar material at scale.
- **Item 98:** a note in definitions.md that the tier headcounts describe each tier and the requirement lists test it. Counting people directly is left to version two. Words only.
- **Item 99:** the child born and raised off Earth moved from Tier 2's definition to Tier 4's, matching the 2026-09-19 move of the requirement itself. Words only.
- **Item 100:** part (a) only. The anti-satellite test ban left Tier 4 and stays in the tree as a tracked event that gates no tier. Moving the traffic-management authority into its place (part b) was declined, so the authority stays a Tier 3 requirement as ruled on 2026-09-19.
- **Item 101:** the timing assumption stated in methodology.md. The completion-date method is described in the proposal and not built. Words only.
- **One change John approved during the landing:** the home page chain names each factor's link from the steps the headline's tiers list. When Tier 1 stopped listing the lunar reactor, energy had no listed step left and would have dropped off the chain, although the Belt still waits on that reactor through lunar material at scale. John approved a fallback on 2026-09-25: a factor with no listed step takes the nearest steps of its own that the listed ones depend on. On the tree before this run the fallback changes nothing (checked against the 2026-09-20 snapshot's chain); on this tree it gives energy the lunar reactor back.

Command: `cd ~/Code/belt-equation && python3 scripts/compute.py run --snapshot methodology-pass --snapshot-date 2026-09-25` (20,000 runs per scenario, seed 2026, world spread 1.0). Snapshot: data/snapshots/2026-09-25-methodology-pass.json. Attribution: data/attribution/2026-09-25-methodology-pass.json.

## Headline and tiers

```
Runs per scenario: 20000 (seed 2026), world spread 1 on the log-odds scale

Tier reached, by scenario:
  tier    baseline  moderate    strong   radical      open
  T1         0.349     0.439     0.566     0.711     0.735
  T2         0.068     0.116     0.218     0.444     0.537
  T3         0.006     0.017     0.050     0.163     0.229
  T4         0.001     0.004     0.016     0.083     0.138
  A0         0.140     0.211     0.306     0.399     0.403
  A1         0.358     0.487     0.643     0.772     0.817
  A2         0.004     0.011     0.035     0.107     0.145  <- headline
  A3         0.004     0.011     0.034     0.104     0.142
```

The full per-node table is in the snapshot.

## Read against the run before

Against `2026-09-20-step-27`, with the same seed, so a figure whose tier did not change is identical rather than merely close:

| | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| Tier 1, outpost | 17.8 → 34.9 | 26.1 → 43.9 | 38.2 → 56.6 | 53.8 → 71.1 | 57.7 → 73.5 |
| Tier 2, settlement | 5.0 → 6.8 | 8.8 → 11.6 | 17.3 → 21.8 | 36.7 → 44.4 | 44.5 → 53.7 |
| Tier 4, Full Expanse | 0.1 → 0.1 | 0.3 → 0.4 | 1.4 → 1.6 | 7.5 → 8.2 | 12.6 → 13.8 |
| A2 at Tier 1, the second number | 5.8 → 8.8 | 10.4 → 14.4 | 18.1 → 23.6 | 27.0 → 32.5 | 29.3 → 34.2 |
| Regime link on the home page chain | 17.8 → 21.1 | 25.2 → 29.2 | 38.7 → 43.7 | 57.5 → 63.4 | 65.8 → 71.9 |

**Did not move, to the last play-through:** the headline (A2 0.4 / 1.1 / 3.5 / 10.7 / 14.5 percent), Tier 3, A0, A1, A3, every node's own figure, the Contact Clause, the decision comparison at the six-year fork, and the launch, energy, drive, biology, motive and access links of the chain. The attribution puts the headline's move at exactly zero in every scenario, against a noise band of 0.09 points by 2071.

Tier 1, Tier 2 and the second number moved exactly as the proposal predicted for item 97; Tier 4 moved as predicted for item 100 part (a). The regime link rose because it no longer includes the lunar programme directly, since that step now sits under lunar material at scale, which the launch link carries. The launch link lost the reusable lander for the same reason, and its rate did not change, because lunar material at scale already requires the lander.

The comparison was meant to be against a snapshot from the Contact Clause C5 landing (`2026-09-25-c5`). That landing had not been merged when this run was taken, so this run is read against the last committed snapshot instead. C5 sits beside the equation and never feeds a tier, so its snapshot is expected to show the same tier figures.

## The second number

A rotation at a station or lunar base, Belt or no Belt, is now 8.8 percent by 2071 and 23.6 percent by 2095, up from 5.8 and 18.1. This is the figure most changed by the pass, and the one a visitor sees beside the headline. It rose because the outpost tier now counts a station.

## Left for the next sessions

- The access-branch review after pipeline graduation (May 2027) takes item 96's direct-migration route, beside item 29's three personal nodes.
- Item 98's headcount nodes and item 101's completion-date method are version-two candidates for a later annual review.
- The anti-satellite ban and the megawatt radiator are now the two tracked steps that gate no tier. The first founding rule excludes a node for being irrelevant; both are kept by John's ruling, and the annual review may retire either.
