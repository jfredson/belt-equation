# Third run of the tree: 2026-09-20, the outside-model review landed

Roadmap step 27, the landing. John ruled on all 105 items of the outside-model review on 2026-09-19 (docs/reviews/2026-09-19-rulings.md); this session (Cowork, branch step-27-landing) put every ruling on the node records, added the nine nodes the reviews were missing, and ran the tree again. The nine new nodes' first probabilities and the three re-estimates the rulings left open (items 69, 90, 92) were proposed by Claude and accepted by John as proposed on 2026-09-20.

Command: `cd ~/Code/belt-equation && python3 scripts/compute.py run --snapshot step-27` (20,000 runs per scenario, seed 2026, world spread 1.0). Snapshot: data/snapshots/2026-09-20-step-27.json, the first marked reviewed. Attribution: data/attribution/2026-09-20-step-27.json.

## Headline and tiers

```
Runs per scenario: 20000 (seed 2026), world spread 1 on the log-odds scale

Tier reached, by scenario:
  tier    baseline  moderate    strong   radical      open
  T1         0.178     0.261     0.382     0.538     0.577
  T2         0.050     0.088     0.173     0.367     0.445
  T3         0.006     0.017     0.050     0.163     0.229
  T4         0.001     0.003     0.014     0.075     0.126
  A0         0.140     0.211     0.306     0.399     0.403
  A1         0.358     0.487     0.643     0.772     0.817
  A2         0.004     0.011     0.035     0.107     0.145  <- headline
  A3         0.004     0.011     0.034     0.104     0.142

The same tiers with nodes rolled independently (world spread 0), for comparison:
  T1         0.104     0.201     0.365     0.576     0.629
  T2         0.003     0.021     0.088     0.345     0.468
  T3         0.000     0.000     0.002     0.071     0.157
  T4         0.000     0.000     0.000     0.011     0.043
  A0         0.083     0.152     0.273     0.374     0.398
  A1         0.314     0.482     0.689     0.826     0.878
  A2         0.000     0.000     0.001     0.027     0.062
  A3         0.000     0.000     0.000     0.024     0.059

Contact Clause, beside the equation and never multiplied into it:
  C1          0.931     0.940     0.955     0.969     0.969  A non-human mind produces knowledge beyond us
  C2          0.723     0.800     0.864     0.914     0.927  Humans learn from it
  C3          0.031     0.046     0.073     0.140     0.239  An intelligence not descended from us is detected
  C4          0.004     0.007     0.015     0.042     0.098  Communion
```

The full per-node table is in the snapshot.

## Read against the run before

The second run of 2026-09-19 had the headline (A2, working rotations in a Belt that exists) at 0.9 percent by 2071, 2.2 by 2080, 5.6 by 2095, 14 by 2136 and 18 with no deadline. This run has it at 0.4 / 1.1 / 3.5 / 11 / 14. Tier 3, the Belt existing at all, went from 1.6 / 3.6 / 8.9 / 23 / 30 to 0.6 / 1.7 / 5.0 / 16 / 23. A1, flying once, went from 39 to 36 percent by 2071.

The fall is mostly structural, and the two runs are not like for like. Seven new requirements sit on the chain that were not there before: a staple crop harvested off Earth, cryogenic propellant stored six months and burned, a tonne of off-Earth propellant fired, a major operation performed off Earth, commercial insurance on a lunar asset, mutually recognised keep-out zones, and a space traffic authority with enforcement. Each is a real thing that has to happen and each can only lower the tiers that need it. The traffic authority costs the most (0.35 by 2071 as a Tier 3 requirement with nothing under it), then the surgery node under Tier 2. Of the fifteen number changes, the ones that reach the headline are the cuts to the launch price, routine nuclear propulsion, the Mars round trip and a hundred people working off Earth, partly offset by the rises to lunar material at scale, the partial-gravity year, the Earth-gravity habitat and the profitable product.

## The second number

Item 95: the headline stays A2 at Tier 3, and the site now reports beside it A2 at Tier 1, a rotation at a station or lunar base whether or not a Belt exists: 5.8 percent by 2071, 10 by 2080, 18 by 2095, 27 by 2136, 29 with no deadline. Computed as a joint over the outpost tier and the rotation-role node in the same play-throughs, so it is the plain-wording event a visitor may picture, and it is fifteen times the headline by 2071. That gap is Astra's structural point made visible, which was the purpose of the ruling.

## Left for the next sessions

- Verify items on the record: the 2026 superconducting-tape reference price and specification (E-superconducting-wire-price-falls-tenfold), the Tiangong rice life cycle (B-staple-crop-grown-from-seed-to-harvest-off-earth), the Chelan County permit page (E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity), and the FunSearch and AlphaEvolve candidates against C1's new wording, which the weekly scan reads under the Contact Clause null rule.
- The methodology pass (protocol decision 5) inherits items 96 to 102, including item 102's description fix on the fusion-construction node and the Tier 4 alternative for the traffic authority (with item 100).
- The access-branch review after May 2027 inherits item 29 and the A3 shape (item 96).
