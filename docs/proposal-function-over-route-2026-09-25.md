# Proposal: function over route (a rule for how nodes and dependencies are written)

*Written 2026-09-25. Rule ratified in principle by John the same day, in conversation, after the essay question "why does it have to be a nuclear reactor?" The rule text below is for methodology.md and node-schema.md; the candidate list is for John to rule node by node. Nothing in the tree changes until he does. This is a structure change, outside the Radar's limits, so it lands in a session, not in a scan.*

## The rule

**A dependency names the function a downstream event needs, not one route to it, whenever more than one route could supply that function.** If lunar mining at scale needs power through the two-week night, the node it depends on is "power through the lunar night at a mining site," not "a fission reactor on the lunar surface." The reactor stays in the tree as one route, with its own criterion and probability, and the function node resolves when any route does.

The mechanism already exists. The schema's `depends_on_any` and the "by some route" pattern (the biology hedge `B-long-term-off-earth-living-by-some-route`, the access node `A-working-in-or-for-the-off-earth-industry`) are exactly this. The rule makes the pattern the default rather than a special case used twice.

**The test, applied to every edge in the tree:** name the thing the child actually consumes from the parent. If a second event that is not the parent would supply the same thing, and the child would proceed just as well, the edge is route-specific and should point at a function node instead. If no plausible second route exists, or the child's criterion itself names the route (a crew *landing* needs a lander), the edge stands.

**What the function node looks like.** Either a threshold criterion written route-free ("at least a hundred kilowatts of net electrical power available at a lunar surface site for ninety percent of a year, from any source"), or an either-route node with `depends_on_any` listing the routes as children and no probability of its own beyond what the routes supply. Prefer the threshold form where a single checkable number exists; prefer the either-route form where the routes are already nodes with their own criteria.

**Why it matters for the numbers.** A route-specific edge multiplies the child by one route's probability when the true probability is that of the union of routes. That is the same lie the world draw corrects at the level of shared causes, at the level of a single edge, and it always biases the tree low. The first founding rule (long shots stay on the board) keeps unlikely routes in; this rule keeps the tree from treating one route as the only one.

**What it does not do.** It does not remove specific events. The reactor, the reusable lander, nuclear propulsion, the Mars round trip all stay, as routes and as tracked events. It changes which node the children point at.

## Candidate edges (for ruling, one line each)

Read from the tree at commit 807eae3, 2026-09-25. "Function" is what the child consumes; "handling" is the proposed change.

1. **`L-lunar-material-delivered-to-orbit-at-scale` ← `E-fission-reactor-runs-on-lunar-surface`.** Function: power at a lunar surface site through the night. Other routes: solar with storage at a polar site with near-continuous sunlight; power beamed from orbit (the tree already has `M-power-beamed-from-orbit-to-ground-at-kilowatt-scale` as a cousin). Handling: new function node `E-power-through-the-lunar-night-at-a-surface-site` (threshold form, any source), reactor becomes one route under it. This is the edge the essay question found, and the one the home page's energy link currently rests on (`chain_gates` fallback of 2026-09-25 would then pick up the function node).
2. **`L-lunar-material-delivered-to-orbit-at-scale` ← `L-crew-lands-on-moon-in-reusable-lander`.** Function: routine access to the lunar surface for people and cargo. Other routes: uncrewed reusable cargo landers at scale with a crew arriving by other means. Handling: judgment call; a hundred tonnes a year almost certainly needs reusable landers, but not necessarily crewed ones. Propose either-route node `L-routine-lunar-surface-access` with crewed-reusable and cargo-reusable as routes, or leave and log. Weak candidate.
3. **`L-lunar-material-delivered-to-orbit-at-scale` ← `R-crewed-lunar-program-outlives-two-changes-of-president`.** Function: a sustained lunar program. Other route: a commercial lunar program that outlives its first two funding rounds without a government customer. Handling: widen the regime node's criterion to "a crewed lunar program, government or commercial, keeps flying across two changes of its principal backer," or add the commercial route and an either-route node. Moderate candidate.
4. **`D-constant-acceleration-drive-demonstrated` ← `E-fusion-plant-delivers-net-electricity`.** Function: a compact power source of the right class. Other routes: a fusion drive need not follow a grid plant; direct fusion drives, or fission-electric at very high power, are separate development paths. Handling: replace the edge with a function node `E-compact-power-source-at-the-scale-a-fast-drive-needs` (threshold form) with the grid fusion plant as one route. Strong candidate, though it only moves the long-shot node.
5. **`D-permanent-crewed-site-beyond-the-earth-moon-system` ← `D-crew-round-trip-to-mars`.** Function: a crewed round trip beyond the Earth-Moon system. Other routes: a near-Earth asteroid or Mars-moon round trip. Handling: widen the parent's criterion to "a crew travels beyond the Earth-Moon system and returns" (Mars becomes the likeliest instance rather than the requirement). Strong candidate, and it touches the Tier 3 chain.
6. **Tier 3 requirement `D-nuclear-propulsion-in-routine-use`.** Function: transit fast enough that the outer solar system is a place people go to work. Other routes: high-power solar-electric propulsion, or chemical with orbital refuelling accepted at longer transit times. Handling: function node `D-fast-transit-in-routine-use` with a transit-time criterion (Earth to the main belt in under N months, several missions a year), nuclear as one route. Strong candidate, touches Tier 3 and the essay's tier definition ("nuclear propulsion in routine use" would become "transit fast enough to work the outer system").
7. **`M-off-earth-product-sold-at-a-profit` ← `L-lunar-material-delivered-to-orbit-at-scale`.** Function: material at scale from any off-Earth body. Other route: asteroid material returned to orbit. Handling: either-route node `L-off-earth-material-delivered-at-scale` with lunar and asteroid routes; the asteroid route is a new node. Strong candidate; this is the tightest link in the tree and the one the essay says gates the Belt.
8. **`E-fusion-plant-delivers-net-electricity` ← `E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity`.** Not a candidate: construction is the only route to a plant. Listed so the sweep shows it was checked.
9. **`B-closed-loop-life-support-year-off-earth` ← `B-staple-crop-grown-from-seed-to-harvest-off-earth`.** Function: most food produced on site. Other route: cultured or fermented food at scale off Earth. Handling: widen the parent's criterion to "a staple food is produced from raw inputs to the table off Earth" rather than adding a node. Weak candidate.
10. **The access branch.** Already written function-first (`A-working-in-or-for-the-off-earth-industry`, `A-first-spaceflight` "by purchase or by the job"). No change; the May 2027 access-branch review applies the rule to any route it adds.

Edges not listed were checked and are threshold-based or single-route (the launch-price chain, the regime nodes, the window nodes, the Contact Clause).

## What happens to the numbers

Unknown until run, and it will move them. Every change above can only raise the child's overall probability (a union is never less likely than one of its members), so Tier 3 and the headline will rise by some amount, most of it through items 5, 6 and 7. Per methodology.md this is a structural review, so the run that lands it gets its own snapshot and attribution record, and the changelog entry names this proposal as the reason. The 2026-09-25 precedent (the methodology pass counted as the required review) can apply here if John rules it so; otherwise the changes wait for the 2027-01-03 annual review.

## Text to land if ratified

In methodology.md, a new short section "Function over route" carrying the rule and the test above. In node-schema.md, one line under `depends_on_any` noting it is the default form whenever more than one route could satisfy a child, and a note under "Known simplifications" that the 2026-09-25 sweep is the first application and future brainstorms apply the test to every new edge.

## Rulings needed from John

- Ratify the rule text for methodology.md and node-schema.md (the principle is already accepted; this is the wording).
- Rule on candidates 1 through 7 and 9 individually: change as proposed, change differently, or leave and log.
- Rule whether this pass counts as the review the tier change in item 6 requires (as the methodology pass did on 2026-09-25), so it lands now, or waits for 2027-01-03.
- Once ruled, the work runs in a Claude Code cloud session with jfredson/belt-equation attached, since it ends in a push; the prompt follows the rulings.
