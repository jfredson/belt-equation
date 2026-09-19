# Review packet: launch-energy-drive (2026-09-19)

You are reviewing part of a forecasting tree called the Belt Equation. It estimates the probability that one person, born in January 1986, works off Earth on months-long rotations before he dies, computed from a dependency tree of about sixty breakthroughs ("nodes") under eight factors. Each node has a resolution criterion (what would count as it having happened), the nodes it depends on, and five probabilities: the chance it resolves yes before the window closes in 2071, 2080, 2095, 2136, and with no deadline at all, in each case given that the nodes it depends on have already resolved. Numbers were proposed by one AI model and accepted by the author, who wants them challenged by models from other labs before publishing. Your job is critique, not agreement. Plain language throughout; a reader outside the field should follow every sentence.

Below are the nodes for this packet, then the scenario table and what each tier of the tree requires. Give your answer as three parts, in this order, with a table at the top of each part.

Part 1, missing nodes. Name up to three breakthroughs, events, or dependencies that these factors need and the tree does not have. For each: a name, a one-line resolution criterion (what record would settle it), and which existing node or tier it should gate. If you think nothing is missing, say so and say why.

Part 2, criteria. For any node whose resolution criterion is ambiguous, cannot be measured from public records, has already been met, or measures the wrong thing for what the node is about, name the node and propose the fix in one sentence. If a node has already resolved in your knowledge, say so and cite what settled it.

Part 3, numbers. For any node where you would put the probability at least 0.15 higher or lower than the tree does in any of the five scenarios, give your own five numbers, a one-paragraph reason, and your confidence in the disagreement (low, medium, high). Remember the numbers are conditional on the dependencies having resolved. Differences smaller than 0.15 are not worth arguing; leave those nodes out. Your numbers must not fall as the window lengthens.

You may look things up. If you do, say where in your answer, so facts from lookup can be told from your judgment. Do not soften findings to be polite; a factor with nothing to challenge is a possible finding, but an unlikely one.

## The nodes

## Factor L: Launch (7 nodes)

### A fully reusable heavy launcher flies 100 orbital missions in one calendar year
Id: `L-heavy-launcher-100-per-year`. Factor L. Horizon: leaf. Status: open.
What it is: Launch cost is set less by the rocket than by how often the same rocket flies. A fully reusable heavy launcher (both stages recovered and reflown) reaching a hundred orbital flights in a single year is the point at which mass to orbit stops being the constraint on everything downstream: stations, habitats, and lunar supply all assume it.
Resolves when: In one calendar year, a launch vehicle whose first and second stages are both designed for recovery and reuse completes at least 100 orbital launches, counting only flights that reached orbit. Test flights that reached orbit count; suborbital flights and failures do not.
Source of truth: Public orbital launch logs, checked against the operator's own flight manifest
Depends on: `L-fully-reusable-heavy-launcher-recovers-both-stages`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.85 / 0.90 / 0.93 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: The partially reusable predecessor passed a hundred flights a year in 2023; full reuse plus a constellation and lunar manifest gets there within the decade, and forty-five years is a long time to miss.
Notes: Written 2026-09-08 as the schema's worked example. Probability comes in Phase 3. Edge drawn at step 7: a hundred flights a year of a fully reusable launcher needs both stages to have been recovered at least once.

### A heavy launcher recovers both of its stages intact from one orbital flight
Id: `L-fully-reusable-heavy-launcher-recovers-both-stages`. Factor L. Horizon: leaf. Status: open.
What it is: Full reusability means the booster and the ship both come back to be flown again. The booster has been caught at its launch tower since 2024; the ship, which comes back from orbital speed, had only been landed in the ocean as of July 2026. A first tower catch was planned for late August 2026, then deferred: on 2026-08-20 the company's chief executive said the catch would come "in a few months", and the flight itself slipped to no earlier than mid-September. The first flight to bring both stages back intact is the day the cost curve everything else assumes actually starts.
Resolves when: On a single orbital flight, a launch vehicle's first stage and its second stage are both recovered intact for reuse (caught, landed, or otherwise returned undamaged), confirmed by the operator and independent observation.
Source of truth: The operator's flight record and independent observation
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.95 / 0.96 / 0.97 / 0.98 / 0.98  (estimated 2026-09-19)
Rationale: Booster catch routine since 2024 and the ship catch deferred by months, not years; the residual risk is a program cancellation, not physics.
Notes: Checked 2026-09-08: no upper-stage catch was attempted in August 2026; the attempt was deferred by a few months and the flight slipped to mid-September at the earliest. Still open. Re-check at the first quarterly scan.

### A hundred tonnes of propellant are pumped from one spacecraft to another in orbit
Id: `L-orbital-propellant-transfer-at-scale`. Factor L. Horizon: leaf. Status: open.
What it is: Everything beyond low Earth orbit on a reusable architecture depends on refilling ships in space, which has been done only at small scale. A hundred-tonne transfer is the size that a lunar landing or a Mars departure needs, and the demonstrations are scheduled within a few years.
Resolves when: At least one hundred tonnes of propellant are transferred between two vehicles in orbit in a single operation, confirmed by the operator and by the customer agency's public record.
Source of truth: The operator's mission record and the customer agency's milestone acceptance
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.90 / 0.93 / 0.95 / 0.97 / 0.97  (estimated 2026-09-19)
Rationale: Contracted, funded, and scheduled within a few years, with the lunar program depending on it; the risk is delay, not failure.

### A crew lands on the Moon in a lander designed to fly again
Id: `L-crew-lands-on-moon-in-reusable-lander`. Factor L. Horizon: leaf. Status: open.
What it is: The first crewed lunar landing since 1972 is scheduled for the next few years, on a lander built for reuse rather than thrown away. It is the near-term marker that the cheap-launch architecture reaches the Moon with people, which every lunar node downstream assumes.
Resolves when: People land on the lunar surface and return safely aboard a lander whose design is intended for more than one landing, confirmed by the responsible agency's mission record.
Source of truth: The responsible agency's mission record
Depends on: `L-orbital-propellant-transfer-at-scale`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.85 / 0.90 / 0.93 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: Two funded landers and a committed agency; a decade of slips still lands inside 2071, and the downside is cancellation after a mishap.

### Mass to low Earth orbit is sold for less than two hundred dollars a kilogram
Id: `L-launch-price-below-200-dollars-per-kg`. Factor L. Horizon: mid. Status: open.
What it is: Today's price for a full flight runs a few thousand dollars per kilogram. Two hundred, in 2026 dollars, is roughly the point at which a tonne to orbit costs less than a mid-range car and building large things in space becomes a question of will rather than money. Reusable heavy launchers flying often are the only known route there.
Resolves when: A launch provider sells, by public price list or a signed contract made public, a full manifest to low Earth orbit at two hundred 2026 dollars or less per kilogram of payload.
Source of truth: The provider's published price list or a public contract record
Depends on: `L-heavy-launcher-100-per-year`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.70 / 0.80 / 0.88 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: Flight rate is the mechanism, but a public sold price is a demand-and-competition question and a single provider can hold price above cost for decades; an outside model (Astra, 2026-09-19) put a hundred dollars at 75 percent by 2070 unconditionally.

### A structure more than a hundred metres across is assembled in orbit from separately launched parts
Id: `L-large-structure-assembled-in-orbit`. Factor L. Horizon: mid. Status: open.
What it is: The orbital-construction node of the habitat branch. The space station is about a hundred metres long and took a decade of crewed assembly flights. A spinning habitat, a large power station, or a shipyard needs structures at least that size assembled mostly by machines from parts launched cheaply. This is the step from launching things to building things.
Resolves when: A single connected structure with a longest dimension over one hundred metres is assembled in orbit from parts delivered on at least five separate launches, with most of the joining done by robots or automated systems, confirmed by the operator and independent tracking.
Source of truth: The operator's records and independent orbital tracking
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.60 / 0.70 / 0.85 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: Possible at today's prices, as the station proved, but nobody has a customer for it yet; the likelihood rides on cheap launch without depending on it.
Notes: Drafted as depending on the two-hundred-dollar launch price; loosened at step 7 (2026-09-08) because a structure this size could be assembled at today's prices with enough money, as the space station was. Cheap launch makes it likely, not possible.

### A hundred tonnes of material dug or made on the Moon are delivered to orbit in one year
Id: `L-lunar-material-delivered-to-orbit-at-scale`. Factor L. Horizon: root. Status: open.
What it is: The lunar-supply and materials node of the habitat branch. Lifting mass from the Moon takes a twentieth of the energy of lifting it from Earth, so once mining, refining, and a way up (rockets burning lunar oxygen, or an electromagnetic launcher) exist, the Moon becomes the quarry for everything built in space. A hundred tonnes a year is the scale at which a habitat or a propellant depot can be fed from the Moon rather than from Earth.
Resolves when: In one calendar year, at least one hundred tonnes of material originating on the Moon (loose surface rock and dust, oxygen, water, metal, or products made from them) are delivered to lunar or Earth orbit and used there, reported by the operator with independent confirmation.
Source of truth: The operator's public accounting, confirmed by the customer or an agency
Depends on: `L-crew-lands-on-moon-in-reusable-lander`, `E-fission-reactor-runs-on-lunar-surface`, `R-crewed-lunar-program-outlives-two-changes-of-president`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.35 / 0.50 / 0.70 / 0.85 / 0.90  (estimated 2026-09-19)
Rationale: Even with power, people, and political continuity, mining and launching from the Moon at scale needs a buyer in orbit; the first forty-five years are the hard ones.
Notes: Edges drawn at step 7 (2026-09-08): mining at scale needs surface power through the lunar night, and a decade of lunar work needs the program to outlive elections.

## Factor E: Energy (5 nodes)

### A single spacecraft generates and uses a megawatt of electricity in orbit
Id: `E-megawatt-spacecraft-operates-in-orbit`. Factor E. Horizon: leaf. Status: open.
What it is: The space station, the largest thing ever flown, makes about a tenth of a megawatt. Orbital data centres, large electric tugs, and any industrial process in space start at a megawatt. Several companies plan megawatt-class solar spacecraft within a few years, so this is the near-term marker that power in space is scaling.
Resolves when: One spacecraft in orbit generates and consumes at least one megawatt of electrical power continuously for thirty days, confirmed by the operator and consistent with independent observation of the vehicle.
Source of truth: The operator's records and independent observation
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.85 / 0.90 / 0.93 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: Several companies have megawatt-class vehicles funded for the late 2020s, and orbital computing gives the power a customer.

### A nuclear reactor runs on the lunar surface for a year
Id: `E-fission-reactor-runs-on-lunar-surface`. Factor E. Horizon: mid. Status: open.
What it is: A lunar night lasts two weeks, so any permanent base needs power that does not come from the Sun. A small fission reactor of a few tens of kilowatts is the planned answer; the US program aimed at the end of this decade and, as of 2026, plans delivery of a reactor to the launch pad in the early 2030s. It is the power source that mining, refining, and a permanent outpost assume.
Resolves when: A fission reactor delivering at least forty kilowatts of electricity operates on the lunar surface for twelve continuous months, confirmed by the responsible agency's mission record.
Source of truth: The responsible agency's mission record
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.70 / 0.80 / 0.90 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: The schedule has already slipped to the early 2030s and reactor programs slip more than most, but two space agencies and a rival national program are all aimed at it.
Notes: Drafted as a leaf; moved to mid on 2026-09-08 after checking the program's schedule, which has slipped to the early 2030s.

### High-temperature superconducting wire costs a tenth of what it does today
Id: `E-superconducting-wire-price-falls-tenfold`. Factor E. Horizon: mid. Status: open.
What it is: The strong, light magnets that compact fusion, magnetic radiation shielding, and some drive concepts all need are made of high-temperature superconducting tape, and its price is what keeps those magnets rare. A tenfold fall from the 2026 price puts a fusion plant's magnets, or a shield around a crew cabin, within an ordinary project budget. This node feeds nodes in biology and drive as well as fusion.
Resolves when: Published price lists or public procurement records show high-temperature superconducting tape sold in production quantities at one tenth or less of its 2026 price, measured the way the industry prices it (per unit of current the tape carries over a metre, the kiloamp-metre) and adjusted for inflation.
Source of truth: Vendor price lists and public procurement or agency cost reports
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.55 / 0.65 / 0.80 / 0.90 / 0.92  (estimated 2026-09-19)
Rationale: Tape prices have been falling and fusion demand is scaling production, but a full tenfold in real terms needs a manufacturing shift, not just volume; the most uncertain number in this group.

### A fusion power plant delivers net electricity to a grid
Id: `E-fusion-plant-delivers-net-electricity`. Factor E. Horizon: mid. Status: open.
What it is: The point where fusion stops being an experiment: a plant that puts more electricity onto a grid than it draws, for long enough to count. Several private plants are scheduled to try in the early 2030s. Fusion on the ground is the technology base that any fusion drive, and any large off-Earth power plant that cannot rely on the Sun, would be built from.
Resolves when: A fusion power plant exports net electrical energy to a public grid over a continuous period of at least thirty days, with net export confirmed by the grid operator's metering.
Source of truth: The grid operator's metering record and the plant operator's report
Depends on: `E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.60 / 0.70 / 0.85 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: Several private plants target the early 2030s; first attempts usually miss, but forty-five years and several routes make a first success more likely than not.
Notes: Drafted with a hard dependency on cheap superconducting wire; removed at step 7 (2026-09-08) because only the magnet route needs it and laser and other routes do not. The link stays in the mechanism of the fusion drive node. Now depends on a plant having started construction, which has happened.

### Construction begins on a fusion plant built to sell electricity to a customer
Id: `E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity`. Factor E. Horizon: leaf. Status: resolved-yes.
What it is: The step before net electricity: someone breaks ground on a plant whose purpose is to sell power, with a customer signed. It has happened. A company backed by a purchase agreement with a large technology firm began building its first plant in Washington state in July 2025, aiming to deliver electricity in 2028. The node stays in, resolved, as the first rung on the fusion ladder and a resolved leaf the calibration score can count.
Resolves when: A company begins site construction of a fusion power plant that has a signed agreement to sell electricity to a named customer, confirmed by the company's announcement and local permitting records.
Source of truth: The company's announcement and the county's permitting record
Depends on: nothing (a root of its own).
Resolved 2025-07-30: Helion's announcement of 2025-07-30 that it had secured land and begun building at Malaga, Washington, under its power purchase agreement with Microsoft; reported by World Nuclear News and BusinessWire
Notes: Added at step 7 (2026-09-08); the date and facts checked the same day against the company's newsroom and trade press.

## Factor D: Drive (5 nodes)

### A nuclear-powered engine changes a spacecraft's orbit in space for the first time
Id: `D-nuclear-propulsion-changes-orbit-in-space`. Factor D. Horizon: mid. Status: open.
What it is: Nuclear propulsion, whether a reactor heating propellant directly or a reactor driving electric thrusters, has been designed and ground-tested for sixty years and never flown. The first in-space burn that actually moves a vehicle is the step from paper to hardware, and it is what routine nuclear propulsion, the Tier 3 criterion, has to start from.
Resolves when: A spacecraft in space changes its velocity by at least one kilometre per second using propulsion powered by a nuclear reactor, confirmed by the operator and by independent orbital tracking.
Source of truth: The operator's mission record and independent orbital tracking
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.60 / 0.72 / 0.85 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: Sixty years of ground tests and no flight, and the most recent flight demonstration program was cancelled in 2025; it needs a mission only nuclear can do.
Notes: Shares a technology base with the lunar surface reactor (an energy node); whether that is a hard dependency is for step 7.

### Nuclear propulsion is used on several missions a year
Id: `D-nuclear-propulsion-in-routine-use`. Factor D. Horizon: root. Status: open.
What it is: The Tier 3 criterion in propulsion terms. One demonstration proves it can be done; several missions a year means it is the ordinary way to move heavy things around the inner solar system, which is what transit times of months to the Belt assume.
Resolves when: In one calendar year, at least three separate missions beyond low Earth orbit use nuclear-powered propulsion for their main transfer, confirmed by the operators and independent tracking.
Source of truth: Operators' mission records and independent tracking
Depends on: `D-nuclear-propulsion-changes-orbit-in-space`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.50 / 0.60 / 0.75 / 0.88 / 0.92  (estimated 2026-09-19)
Rationale: One demonstration to routine use is the gap the space station took two decades to cross; a Mars cadence would pull it forward.

### A crew lands on Mars and returns to Earth
Id: `D-crew-round-trip-to-mars`. Factor D. Horizon: root. Status: open.
What it is: The transit-in-months milestone with people aboard: the first round trip proves that a crew can be carried across the inner solar system and back, which is what working rotations to an outer site require. It needs the launch, propellant, and life-support nodes as much as the drive, and it is placed under drive because the transit is the hard part it resolves.
Resolves when: People land on the surface of Mars and return alive to Earth, confirmed by the responsible agency or company and independent tracking of the vehicles.
Source of truth: The responsible agency's or company's mission record and independent tracking
Depends on: `L-orbital-propellant-transfer-at-scale`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.55 / 0.70 / 0.85 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: One company is building for it; the return leg and two to three years of crew health are the unproven parts, and it is likely by 2095 if the launch architecture works at all.
Notes: Edge drawn at step 7 (2026-09-08): a Mars departure on any current architecture needs refilling in orbit. Life support and shielding make it safer, not possible, so they are not hard dependencies.

### A drive that could cross the solar system in weeks is fired in space
Id: `D-constant-acceleration-drive-demonstrated`. Factor D. Horizon: root. Status: open.
What it is: The Epstein drive in plain terms: an engine whose exhaust is fast enough and whose thrust is high enough that a ship can accelerate the whole way and reach the Belt in weeks rather than months. Nothing like it exists. Chemical rockets have the thrust but not the exhaust speed; electric thrusters have the speed but push like a breath. This is the node that separates the Slow Expanse from the Full Expanse, and it is the project's clearest long shot.
Resolves when: A propulsion system operating in space sustains, for at least one hour, an exhaust speed above one hundred kilometres per second (chemical rockets manage under five) together with a push of more than one kilonewton (roughly the weight of a hundred kilograms on Earth, which today's high-speed electric thrusters miss by a thousandfold), confirmed by the operator and by independent measurement of the vehicle's acceleration.
Source of truth: The operator's test record and independent tracking of the vehicle's acceleration
Depends on: `E-fusion-plant-delivers-net-electricity`
Long shot. Mechanism: A fusion reaction whose products are steered out the back directly, rather than used to boil water and spin a turbine, gives exhaust speeds of thousands of kilometres per second in principle. The path runs through fusion plants on the ground (proving the reaction can be sustained), then compact magnet-based reactors made cheap by superconducting wire, then a reactor light enough to fly, then a nozzle that turns its output into thrust. Pulsed designs that detonate small fuel pellets are the leading route on paper because they avoid holding a steady plasma.
Breaking point: The reactor has to be light as well as working. Ground fusion designs come to tens or hundreds of tonnes for each megawatt of electricity; paper drive concepts need about a kilowatt for each kilogram, a gap of a hundred- to a thousandfold that no built device has closed, and fission-electric systems top out near a fifth of a kilowatt per kilogram. No fusion device has ever produced thrust. Everything past a heavy fusion plant on the ground is engineering nobody has done.
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.03 / 0.06 / 0.15 / 0.35 / 0.50  (estimated 2026-09-19)
Rationale: A hundredfold weight gap and no thrust ever produced from fusion; a coin flip with no deadline is the founding rule at work. An outside model's 50 percent for a 90-day belt transit by 2070 is a much lower bar and does not transfer.
Notes: Weight-gap figures checked 2026-09-08 against a European Space Agency assessment of open magnetic fusion for propulsion and NASA fusion-rocket studies: conceptual fusion drives are projected at one to ten kilowatts per kilogram, fission-electric near 0.2, and the practical requirement is quoted as above one kilowatt per kilogram.

### A site beyond the Earth-Moon system is crewed without a break for a year
Id: `D-permanent-crewed-site-beyond-the-earth-moon-system`. Factor D. Horizon: root. Status: open.
What it is: The Tier 3 definition needs at least one site beyond the Earth-Moon system: Mars, the asteroid belt, an outer moon, or a habitat out there. A crew round trip proves people can get there and back; a site crewed continuously for a year, with rotations, proves people can stay. It sits under drive because keeping a site beyond the Moon supplied is a transit problem before it is anything else.
Resolves when: A site beyond the Earth-Moon system is occupied by people continuously for twelve months, with at least one crew rotation during that time, confirmed by the operator and independent tracking of the vehicles involved.
Source of truth: The operator's records and independent tracking
Depends on: `D-crew-round-trip-to-mars`, `B-closed-loop-life-support-year-off-earth`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.40 / 0.55 / 0.75 / 0.90 / 0.93  (estimated 2026-09-19)
Rationale: Getting there and back is proven by the dependency; staying needs a reason to keep a rotation running, which is a motive question the tree asks elsewhere.
Notes: Added at step 7 (2026-09-08) because no node covered Tier 3's beyond-the-Moon criterion. The criterion is deliberately inclusive: Mars, the asteroid belt, an outer moon, a free-flying habitat, or anywhere else beyond the Earth-Moon system all count, and any one of them resolves the node. Confirmed by John 2026-09-08 that every kind of habitation at Tier 3's level should count.

## The five scenarios (when the window closes)
- baseline: Baseline, no extension beyond current trends, 2071
- moderate: Moderate extension, 2080
- strong: Strong extension, 2095
- radical: Radical extension, a 150-year life, 2136
- open: Escape velocity, window open, no deadline

## What each tier requires (every listed node, and any listed lower tier)
- T1 Outpost: Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth. Requires: `L-crew-lands-on-moon-in-reusable-lander`, `E-fission-reactor-runs-on-lunar-surface`, `M-hundred-people-working-off-earth-for-pay`, `R-crewed-lunar-program-outlives-two-changes-of-president`
- T2 Settlement: Thousands living off Earth at one or more sites, at least one child born and raised off Earth, partial local self-sufficiency in air, water, and food. Requires: `T1`, `L-launch-price-below-200-dollars-per-kg`, `B-long-term-off-earth-living-by-some-route`, `B-closed-loop-life-support-year-off-earth`
- T3 Slow Expanse: Tens of thousands off Earth, including at least one site beyond the Earth-Moon system. Transit times in months. Something mined or made off Earth sold at a profit. Nuclear propulsion in routine use. This is the bar for the headline. Requires: `T2`, `D-permanent-crewed-site-beyond-the-earth-moon-system`, `D-nuclear-propulsion-in-routine-use`, `M-off-earth-product-sold-at-a-profit`, `R-off-earth-resource-rights-recognised-by-major-powers`, `B-shielding-halves-deep-space-radiation-dose`, `L-lunar-material-delivered-to-orbit-at-scale`
- T4 Full Expanse: Millions off Earth, transit times in weeks on constant-acceleration drives, a Belt population with its own political identity and economy. Requires: `T3`, `D-constant-acceleration-drive-demonstrated`, `R-binding-ban-on-debris-creating-anti-satellite-tests`, `B-human-child-born-off-earth`
- A0 Contributes from Earth: Works in or for the off-world industry without leaving. Requires: `A-working-in-or-for-the-off-earth-industry`
- A1 Has flown: At least one trip to space, suborbital or orbital, as passenger or crew. Requires: `A-first-spaceflight`
- A2 Works off Earth on rotation: Months at a time living and working at an off-world site. The headline number. Requires: `T3`, `A-in-a-role-whose-holders-rotate-off-earth`
- A3 Lives off Earth: Permanent residence at an off-world site. Reported beside the headline as the stretch. Requires A2 plus a site that accepts permanent residents; the choice to stay is a future choice point, not a world event. Requires: `A2`, `R-off-earth-site-accepts-permanent-residents`
