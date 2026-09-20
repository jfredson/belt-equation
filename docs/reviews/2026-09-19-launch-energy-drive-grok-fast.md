# Review: launch-energy-drive packet, Grok (Fast mode), 2026-09-19

Model: Grok, Fast mode, through the Grok app, no subscription (the deeper reasoning mode was not available). Date: 2026-09-19. Mode: documents shown (the full packet), lookup used; the reviewer lists its sources at the end. Third reviewer on this packet under protocol decision 4, added because the first two reviewers (Gemini, Astra) disagreed with each other in direction on two nodes: `L-launch-price-below-200-dollars-per-kg` and `D-nuclear-propulsion-in-routine-use`. Because Fast mode is a lighter reviewer than the other two, its numbers are weighed as a tiebreak on those two nodes and recorded as single-reviewer items, held, elsewhere (docs/reviews/2026-09-19-rulings.md, items 103 to 105).

Packet sent: docs/reviews/packets/2026-09-19-launch-energy-drive.md, regenerated 2026-09-19 in the evening.

Filed verbatim by Claude (Cowork session, 2026-09-19). Never edited after filing.

---

**Part 1: Missing nodes**

| Name | Resolution criterion | Gates which node/tier |
|------|----------------------|-----------------------|
| Reliable catch-and-refly of Starship upper stage (tower catch, not ocean salvage) | Operator confirms a single orbital-flight Ship is caught by tower arms, inspected, and reflown on a subsequent orbital mission within 90 days | L-fully-reusable-heavy-launcher-recovers-both-stages and L-heavy-launcher-100-per-year |
| Sustained high-rate cryogenic tanker fleet operations (not single demo) | In one calendar year, ≥10 separate tanker-to-depot or tanker-to-ship cryogenic transfers totaling ≥500 t of propellant, with public accounting of boil-off losses <10 % | L-orbital-propellant-transfer-at-scale and L-crew-lands-on-moon-in-reusable-lander |
| Flight-qualified nuclear-electric or nuclear-thermal propulsion system with specific impulse >800 s and thrust >5 kN | Independent tracking confirms a spacecraft using a nuclear reactor achieves Δv ≥1 km/s on a single burn while producing the stated Isp and thrust | D-nuclear-propulsion-changes-orbit-in-space |

These are the largest gaps. The tree treats recovery of both stages as essentially solved once a single intact recovery occurs, yet the 2026 record shows only ocean recovery of a damaged Ship after Flight 13 and continued deferral of tower catch. Scale cryogenic transfer is still only internal-tank demos; the multi-tanker architecture required for lunar or Mars missions is unproven. Nuclear propulsion has new DoD/NASA funding (Antares $161 M, SR-1 Freedom targeting 2028) but no flight hardware has ever changed orbit; a pure “first burn” node under-weights the engineering distance from ground criticality to flight-qualified system.

**Part 2: Criteria**

| Node | Problem and one-sentence fix |
|------|------------------------------|
| L-fully-reusable-heavy-launcher-recovers-both-stages | Criterion is already partially met by ocean recovery of Ship after Flight 13 (July 2026, later towed to Christmas Island); change to “both stages recovered intact by tower catch or equivalent dry landing and subsequently reused on an orbital flight.” |
| L-orbital-propellant-transfer-at-scale | “100 tonnes in a single operation” is ambiguous about whether the vehicles are separate spacecraft or internal tanks and ignores boil-off; tighten to “≥100 t cryogenic propellant transferred between two independently launched vehicles in orbit, with measured transfer efficiency >90 %.” |
| L-launch-price-below-200-dollars-per-kg | “Sold by public price list or signed contract” can be satisfied by a one-off sweetheart deal that never scales; require a published, available-to-any-customer price list for a full Starship-class manifest at ≤$200/kg (2026 dollars). |
| L-large-structure-assembled-in-orbit | “Most of the joining done by robots” is soft; require ≥80 % of structural joints made by autonomous or tele-operated systems with no human EVA. |
| E-megawatt-spacecraft-operates-in-orbit | “Generates and consumes” for 30 days is hard to verify from public data; require continuous generation of ≥1 MW electrical power for 30 days, confirmed by both operator telemetry and independent RF/power signature observations. |
| E-fusion-plant-delivers-net-electricity | Already correctly depends on the resolved construction node; no change needed, but note Helion’s Malaga plant began site work July 2025 under a Microsoft PPA and remains on a 2028 target. |
| D-constant-acceleration-drive-demonstrated | Exhaust speed >100 km/s + thrust >1 kN for one hour is a reasonable long-shot criterion, but the dependency only on net-electricity fusion is too weak; the node should also require a demonstrated specific power >1 kW/kg in a flight-weight system. |

No other nodes have already resolved under their stated criteria as of September 2026. Starship Ship recovery was ocean-only and non-reusable; propellant transfer remains internal-tank only; Artemis III is still a 2027 LEO rehearsal, with crewed landing targeted no earlier than 2028 and still slipping.

**Part 3: Numbers**

| Node | Tree (2071/2080/2095/2136/open) | My numbers | Confidence |
|------|----------------------------------|------------|------------|
| L-fully-reusable-heavy-launcher-recovers-both-stages | 0.95/0.96/0.97/0.98/0.98 | 0.75/0.85/0.92/0.96/0.97 | High |
| L-heavy-launcher-100-per-year | 0.85/0.90/0.93/0.95/0.96 | 0.55/0.70/0.85/0.92/0.95 | High |
| L-orbital-propellant-transfer-at-scale | 0.90/0.93/0.95/0.97/0.97 | 0.70/0.82/0.90/0.95/0.96 | Medium |
| L-crew-lands-on-moon-in-reusable-lander | 0.85/0.90/0.93/0.95/0.96 | 0.65/0.80/0.90/0.95/0.96 | Medium |
| L-launch-price-below-200-dollars-per-kg | 0.70/0.80/0.88/0.93/0.95 | 0.45/0.60/0.78/0.90/0.93 | High |
| L-lunar-material-delivered-to-orbit-at-scale | 0.35/0.50/0.70/0.85/0.90 | 0.20/0.35/0.55/0.75/0.85 | Medium |
| E-fission-reactor-runs-on-lunar-surface | 0.70/0.80/0.90/0.95/0.96 | 0.50/0.65/0.80/0.92/0.95 | Medium |
| E-superconducting-wire-price-falls-tenfold | 0.55/0.65/0.80/0.90/0.92 | 0.35/0.50/0.70/0.85/0.90 | Medium |
| D-nuclear-propulsion-changes-orbit-in-space | 0.60/0.72/0.85/0.93/0.95 | 0.40/0.55/0.75/0.90/0.93 | Medium |
| D-nuclear-propulsion-in-routine-use | 0.50/0.60/0.75/0.88/0.92 | 0.25/0.40/0.60/0.80/0.88 | Medium |
| D-crew-round-trip-to-mars | 0.55/0.70/0.85/0.93/0.95 | 0.35/0.50/0.70/0.88/0.93 | Medium |
| D-constant-acceleration-drive-demonstrated | 0.03/0.06/0.15/0.35/0.50 | 0.01/0.02/0.08/0.20/0.35 | High |
| D-permanent-crewed-site-beyond-the-earth-moon-system | 0.40/0.55/0.75/0.90/0.93 | 0.25/0.40/0.60/0.82/0.90 | Medium |

**Reasons (each conditional on listed dependencies)**

L-fully-reusable…both-stages: As of mid-September 2026 the Ship has only been recovered from the ocean after Flight 13; tower catch remains deferred and salt-water exposure has already rendered vehicles non-reusable. Residual technical and regulatory risk is larger than the tree assumes.

L-heavy-launcher-100-per-year: Even after full recovery is solved, reaching 100 orbital flights requires a fleet, rapid turnaround, and regulatory cadence that Falcon 9 only achieved after a decade of partial reuse. The tree’s near-term numbers are optimistic.

L-orbital-propellant-transfer-at-scale: Internal-tank demos succeeded in 2024; inter-vehicle cryogenic transfer at 100 t scale has not flown and faces boil-off, docking, and thermal-control problems that routinely slip.

L-crew-lands-on-moon…: Artemis landing slipped from 2025–26 targets to 2028+ with further risk; the reusable-lander requirement adds another layer of development risk beyond a simple Apollo-style landing.

L-launch-price-below-200: Flight rate is necessary but not sufficient; providers can and historically do keep prices well above marginal cost for years. Public, available pricing at that level requires either competition or deliberate undercutting that may not occur.

L-lunar-material…: Even with power, crew, and political continuity, industrial-scale mining, refining, and delivery from the lunar surface has never been done; the first 100 t year is a major industrial project, not a technology demonstration.

E-fission-reactor…: Programs have already slipped into the early 2030s; surface-power reactors face unique thermal, radiation, and dust problems that ground and orbital demos do not fully address.

E-superconducting-wire…: Tenfold real-price reduction requires manufacturing breakthroughs beyond simple volume scaling; fusion demand helps but does not guarantee the full drop.

D-nuclear-propulsion-changes-orbit: New funding (Antares, SR-1 Freedom) is real, yet sixty years of ground work produced zero orbital burns; the step from criticality to flight system remains large.

D-nuclear-propulsion-in-routine-use: One successful demonstration does not automatically produce three missions per year; institutional, regulatory, and cost barriers persist.

D-crew-round-trip-to-mars: Propellant transfer is necessary but the multi-year crew health, return-leg propulsion, and abort options remain unproven; schedule pressure alone does not close those gaps by 2071.

D-constant-acceleration-drive: The specific-power gap (ground fusion designs vs required flight mass) is two to three orders of magnitude and no fusion system has ever produced thrust. A 50 % open-ended probability is far too high.

D-permanent-crewed-site…: A single Mars round-trip does not automatically create a continuously occupied, rotating site; sustained logistics and political will are additional barriers.

All numbers are strictly non-decreasing with longer windows, as required. Lookups used for status: SpaceX Flight 13 recovery reports (Ars Technica, AP, SpaceX posts, Aug–Sep 2026), Helion Malaga construction announcements (July–Oct 2025), Artemis schedule updates (USNI, NASA OIG, Sep 2026), Antares/NASA nuclear awards (Sep 2026), and Starship propellant-transfer project status (NASA TechPort, Wikipedia, Sep 2026). Judgment on probabilities is independent of those facts.
