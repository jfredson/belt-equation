# Handoff: land the function-over-route pass (approved September 25, 2026)

John approved `docs/proposal-function-over-route-2026-09-25.md` in full on 2026-09-25. Interpretation recorded here so the session and the ledger agree: the rule text is ratified for methodology.md and node-schema.md; candidates 1, 3, 4, 5, 6 and 7 change as proposed; candidate 2 (reusable crewed lander under lunar material) is left and logged as checked; candidate 9 (staple crop under closed-loop life support) takes the lighter handling, widening the parent's criterion; candidate 8 and the access branch are unchanged. The pass counts as the review methodology.md requires for the Tier 3 change (item 6), on the 2026-09-25 methodology-pass precedent, so everything lands now rather than at the 2027-01-03 annual review.

## Session prompt (Claude Agents, Opus, fresh session, repo jfredson/belt-equation attached)

```
Name this session "Belt Equation function-over-route pass".

You are working in the jfredson/belt-equation repository on a new branch, function-over-route, from main at or after commit 807eae3. Read docs/proposal-function-over-route-2026-09-25.md and docs/handoff-function-over-route-2026-09-25.md first, then docs/methodology.md, docs/node-schema.md, docs/definitions.md, and docs/runs/2026-09-25-methodology-pass.md so the run record you write matches the house form. John approved the proposal in full on 2026-09-25; the handoff file records exactly which candidates change and how. Do not re-decide any of it.

Land, in this order:

1. Rule text. Add a section "Function over route" to docs/methodology.md carrying the rule and the test from the proposal. In docs/node-schema.md, add one line under depends_on_any saying it is the default form whenever more than one route could satisfy a child, and a line under Known simplifications recording that the 2026-09-25 sweep is the first application and future brainstorms apply the test to every new edge.

2. Tree changes, each as its own commit with a ledger entry in data/ledger.toml naming the proposal and the candidate number as the reason, dated 2026-09-25, and a revisions entry on every node whose fields change:
   - Candidate 1: new node E-power-through-the-lunar-night-at-a-surface-site, threshold form: at least a hundred kilowatts of net electrical power available to loads at a lunar surface site for ninety percent of a twelve-month period, from any source, confirmed by the operator's record. Routes under it via depends_on_any: E-fission-reactor-runs-on-lunar-surface, plus two new route nodes you draft with criteria and first probabilities: solar-with-storage at a near-continuous-sunlight polar site, and power delivered to the surface from orbit. L-lunar-material-delivered-to-orbit-at-scale now depends on the function node instead of the reactor. The home page chain's energy link should pick up the function node through chain_gates in scripts/compute.py; confirm it does and say so in the run record.
   - Candidate 3: widen R-crewed-lunar-program-outlives-two-changes-of-president's criterion to a crewed lunar program, government or commercial, that keeps flying across two changes of its principal backer (a government changing hands, or a commercial program's principal funder changing). Rename the id and name to match; update every depends_on that references it.
   - Candidate 4: new function node E-compact-power-source-at-fast-drive-scale, threshold form (a power source of at least a hundred megawatts electrical at a specific mass a fast drive could carry; state the number you choose and why), with E-fusion-plant-delivers-net-electricity as one route under depends_on_any and one new route node for a fission-electric source at that class. D-constant-acceleration-drive-demonstrated depends on the function node.
   - Candidate 5: widen D-crew-round-trip-to-mars to D-crew-round-trip-beyond-the-earth-moon-system: a crew travels beyond the Earth-Moon system and returns to Earth. Mars becomes the likeliest instance in the description, not the requirement. Re-estimate its probabilities with a rationale.
   - Candidate 6: new function node D-fast-transit-in-routine-use with a transit-time criterion (Earth to the main asteroid belt in under twelve months, on at least three missions in one year, crewed or cargo), D-nuclear-propulsion-in-routine-use as one route under depends_on_any, and one new route node for high-power solar-electric transit at that class. Tier 3 in data/tiers.toml requires the function node instead of nuclear propulsion. Update the Tier 3 definition text in docs/definitions.md to "transit fast enough that people go out there to work" and record the tier change in the definitions decision log, citing this pass as the review.
   - Candidate 7: new either-route node L-off-earth-material-delivered-at-scale with L-lunar-material-delivered-to-orbit-at-scale and a new route node for asteroid material (a hundred tonnes of material from an asteroid delivered to a cislunar or Earth orbit in one year) under depends_on_any. M-off-earth-product-sold-at-a-profit depends on the either-route node.
   - Candidate 9: widen B-closed-loop-life-support-year-off-earth's criterion so the food half reads "most of its food produced on site from raw inputs" and keep B-staple-crop-grown-from-seed-to-harvest-off-earth as its parent unchanged; note in the node's revisions that the crop is the likeliest route and a cultured-food route would be added if one appears.
   - Candidate 2: no change; add a line to the run record that the edge was checked and left.
   Every new node follows docs/node-schema.md exactly: name a stranger can read, a resolution criterion two readers would agree on, a source, a horizon, a rationale, five probabilities, estimated_on 2026-09-25. New route probabilities are first estimates; mark them as such in the rationale.

3. Run the tree: cd into the repo and run python3 scripts/compute.py run --snapshot function-over-route --snapshot-date 2026-09-25, then the attribution against 2026-09-25-methodology-pass. Write docs/runs/2026-09-25-function-over-route.md in the form of the previous run records: what landed, the headline and tier table, the read against the run before, what moved and why, the second number, and what is left. Run scripts/export.py so site/src/data reflects the new tree. Check that the site builds.

4. Update CHANGELOG.md with one entry for the pass. Do not touch docs/private/. Do not reference John's current career in any public file; the access branch's existing wording stands.

5. Open a pull request from function-over-route to main titled "Function over route: rule and first sweep (approved 2026-09-25)", with the run record's headline table in the body and a list of every node added or changed. Do not merge. Report the new headline under all five scenarios, the Tier 3 figures, the second number, and every first-estimate probability you set, so John can rule on them before merging.
```

## What John does after the session reports

- Rule on the first-estimate probabilities for the new route nodes (the session will list them).
- Merge the PR; the site deploys on push to main.
- Tell the essay session the new Tier 3 wording and headline so the intro essay's tier list and numbers are updated before it publishes.
