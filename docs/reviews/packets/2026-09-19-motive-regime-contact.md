# Review packet: motive-regime-contact (2026-09-19)

You are reviewing part of a forecasting tree called the Belt Equation. It estimates the probability that one person, born in January 1986, works off Earth on months-long rotations before he dies, computed from a dependency tree of about sixty breakthroughs ("nodes") under eight factors. Each node has a resolution criterion (what would count as it having happened), the nodes it depends on, and five probabilities: the chance it resolves yes before the window closes in 2071, 2080, 2095, 2136, and with no deadline at all, in each case given that the nodes it depends on have already resolved. Numbers were proposed by one AI model and accepted by the author, who wants them challenged by models from other labs before publishing. Your job is critique, not agreement. Plain language throughout; a reader outside the field should follow every sentence.

Below are the nodes for this packet, then the scenario table and what each tier of the tree requires. Give your answer as three parts, in this order, with a table at the top of each part.

Part 1, missing nodes. Name up to three breakthroughs, events, or dependencies that these factors need and the tree does not have. For each: a name, a one-line resolution criterion (what record would settle it), and which existing node or tier it should gate. If you think nothing is missing, say so and say why.

Part 2, criteria. For any node whose resolution criterion is ambiguous, cannot be measured from public records, has already been met, or measures the wrong thing for what the node is about, name the node and propose the fix in one sentence. If a node has already resolved in your knowledge, say so and cite what settled it.

Part 3, numbers. For any node where you would put the probability at least 0.15 higher or lower than the tree does in any of the five scenarios, give your own five numbers, a one-paragraph reason, and your confidence in the disagreement (low, medium, high). Remember the numbers are conditional on the dependencies having resolved. Differences smaller than 0.15 are not worth arguing; leave those nodes out. Your numbers must not fall as the window lengthens.

You may look things up. If you do, say where in your answer, so facts from lookup can be told from your judgment. Do not soften findings to be polite; a factor with nothing to challenge is a possible finding, but an unlikely one.

## The nodes

## Factor M: Motive (4 nodes)

### A commercial customer pays for a service performed in orbit, other than communications, imaging, or navigation
Id: `M-paying-customer-for-work-done-in-orbit`. Factor M. Horizon: leaf. Status: open.
What it is: Satellites already earn money by relaying signals and taking pictures. The new thing is paying for work done in orbit: computing in an orbital data centre, manufacturing crystals or fibre in free fall, testing materials. The first sizeable paying customer is the sign that orbit has a second economy, which is what makes megawatt spacecraft and orbital assembly worth building.
Resolves when: A company publicly reports, by contract announcement or financial filing, at least ten million dollars in a single year of paid revenue from a customer for computing, manufacturing, or processing performed in orbit.
Source of truth: The company's public contract announcement or financial filing
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.85 / 0.90 / 0.93 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: Orbital-compute contracts are already announced and the bar is one company, one year.

### A spacecraft beams at least a kilowatt of power to a receiver on the ground
Id: `M-power-beamed-from-orbit-to-ground-at-kilowatt-scale`. Factor M. Horizon: leaf. Status: open.
What it is: Space-based solar power, if it ever pays, is a reason to build very large things in orbit and to have people maintaining them. Small demonstrations have transmitted watts. A kilowatt received on the ground is the step that makes the engineering argument real, and several agencies plan demonstrations within a few years.
Resolves when: A spacecraft in orbit transmits power to a receiver on Earth's surface that delivers at least one kilowatt of usable electrical power, reported in a peer-reviewed publication or an agency mission record.
Source of truth: The peer-reviewed publication or the agency's mission record
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.75 / 0.85 / 0.92 / 0.95 / 0.96  (estimated 2026-09-19)
Rationale: Demonstrations at watts have flown and agency kilowatt demonstrations are planned, but every one so far has slipped, and the economic case may never justify the step.

### A hundred people are living and working off Earth at the same time, for pay
Id: `M-hundred-people-working-off-earth-for-pay`. Factor M. Horizon: mid. Status: open.
What it is: The space station holds seven. A hundred people employed off Earth at once, whatever the mix of stations and surface bases, means there are jobs out there rather than missions, which is the economic shape of Tier 1 and the precondition for anyone rotating through.
Resolves when: On a single day, at least one hundred people are off Earth in paid roles, counting all stations and surface sites, according to the operators' public crew records.
Source of truth: Operators' public crew records, tallied
Depends on: `L-heavy-launcher-100-per-year`, `R-space-funding-holds-through-a-recession`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.60 / 0.72 / 0.85 / 0.93 / 0.95  (estimated 2026-09-19)
Rationale: Private stations and a lunar base get to dozens; a hundred needs a reason beyond government seats. An outside model's 30 percent (Astra, 2026-09-19) was for ten thousand self-sustaining residents, a far higher bar.
Notes: Edges drawn at step 7 (2026-09-08): a hundred people off Earth at once needs launch cadence, and getting there takes long enough that funding will have to survive a downturn on the way.

### Something mined or made off Earth is sold at a profit
Id: `M-off-earth-product-sold-at-a-profit`. Factor M. Horizon: root. Status: open.
What it is: The Tier 3 criterion in economic terms. Propellant made from lunar ice, metal from an asteroid, structures built from lunar material: the first product whose sale covers its cost is the moment a solar-system economy exists rather than a set of subsidised outposts.
Resolves when: A company reports, in audited accounts or an equivalent public filing, that revenue from selling a physical product extracted or manufactured off Earth exceeded the full cost of producing it over a financial year.
Source of truth: The company's audited accounts or equivalent public filing
Depends on: `L-lunar-material-delivered-to-orbit-at-scale`, `R-off-earth-resource-rights-recognised-by-major-powers`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.55 / 0.65 / 0.80 / 0.90 / 0.93  (estimated 2026-09-19)
Rationale: With supply and ownership settled, profit still needs a buyer at a price above a first-of-kind cost; propellant in orbit is the likeliest product.
Notes: Edges drawn at step 7 (2026-09-08): the only supply route in the tree is lunar material at scale (an asteroid route would be a second option if a node is added), and selling it needs the ownership rules to exist.

## Factor R: Regime (5 nodes)

### A crewed lunar program keeps flying across two changes of its government
Id: `R-crewed-lunar-program-outlives-two-changes-of-president`. Factor R. Horizon: mid. Status: open.
What it is: Every large space program since Apollo has been redrawn or cancelled by a new administration. A program that keeps its funding and keeps flying hardware across two changes of the government that pays for it has become an institution rather than a policy, which is what a multi-decade build needs. Any nation's or company's crewed lunar program counts, because Tier 1 is an outpost by anyone; the US program is the one to watch first.
Resolves when: A crewed lunar program (a national program or a company's program with a national anchor customer) receives its yearly funding and flies crewed hardware in each of two successive governments after the one in office when it first flew crew. For the US program, counting from 2026, that means two successive presidential administrations after the current one. A program that is cancelled and later restarted, or a different nation's program that reaches the mark, resolves the node when it gets there.
Source of truth: The funding nation's appropriations records and the program's flight record
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.75 / 0.80 / 0.85 / 0.90 / 0.92  (estimated 2026-09-19)
Rationale: With any nation's program counting and a restart still able to resolve it, the question is whether some crewed lunar program anywhere becomes an institution over forty-five years; two rival national programs and a flying commercial lander make that likely, and the longer windows add more attempts. Proposed with the rewording, 2026-09-19.

### Space spending recovers within three years of a recession
Id: `R-space-funding-holds-through-a-recession`. Factor R. Horizon: mid. Status: open.
What it is: Downturns are when long builds get cut. The test is whether, after a recession, the government human-spaceflight budget and the largest private launch company's flight rate come back to where they were rather than being cut and left there. A dip is allowed; what the tree needs is that the field keeps its funding across the business cycle. The node is tested at every recession and resolves yes the first time the field comes through one.
Resolves when: Within three calendar years after the end of a US recession as dated by the National Bureau of Economic Research, the US human-spaceflight appropriation is back within ten percent of its pre-recession level in real terms and the largest US launch provider's orbital launch count is back within ten percent of its pre-recession count. Resolves yes at the first recession that passes the test; a recession that fails it leaves the node open for the next.
Source of truth: NBER recession dates, federal appropriations records, public launch logs
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.80 / 0.82 / 0.85 / 0.90 / 0.90  (estimated 2026-09-19)
Rationale: The 2008 and 2020 downturns both saw space budgets and launch counts recover within three years, and the private flight rate is carried by constellation customers; the residual is a downturn deep enough to restructure the field. Rises slowly because every added recession is another chance to pass. Proposed with the rewording, 2026-09-19.

### The major space powers are bound by a ban on debris-creating anti-satellite tests
Id: `R-binding-ban-on-debris-creating-anti-satellite-tests`. Factor R. Horizon: mid. Status: open.
What it is: A single war in orbit, or even one more test that shatters a satellite, could make low orbit unusable for decades and stop everything above it. A binding agreement among the powers that can do it is the clearest sign that orbit is being treated as shared infrastructure rather than a battlefield.
Resolves when: The United States, China, and Russia are all party to a legally binding agreement prohibiting anti-satellite tests that create orbital debris, and the agreement is in force.
Source of truth: The treaty text and the depositary's record of parties
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.30 / 0.40 / 0.55 / 0.75 / 0.80  (estimated 2026-09-19)
Rationale: Unilateral pledges exist, a binding three-party treaty does not; it needs either a scare in orbit or a detente, and Russia is the holdout.

### The United States and China both recognise the same rules for owning what is mined off Earth
Id: `R-off-earth-resource-rights-recognised-by-major-powers`. Factor R. Horizon: root. Status: open.
What it is: Nobody will spend a decade building a mine on the Moon if another power can call the ore stolen. A common framework for who may extract and own off-Earth resources, whether a treaty or matching national laws, is what lets the motive nodes attract long money.
Resolves when: A treaty in force, or national laws whose provisions mutually recognise each other, gives the United States and China (and at least one of the European Union, India, or Russia) the same rules for extracting and owning resources at off-Earth sites, as documented in the treaty record or the enacted statutes.
Source of truth: The treaty record or the enacted statutes
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.45 / 0.55 / 0.70 / 0.85 / 0.90  (estimated 2026-09-19)
Rationale: Two rival frameworks today; convergence usually follows the first real mine. An outside model's 70 percent by 2070 (Astra, 2026-09-19) was for transferable rights among major jurisdictions without requiring the United States and China to match.

### An off-Earth site accepts people as permanent residents, with no return scheduled
Id: `R-off-earth-site-accepts-permanent-residents`. Factor R. Horizon: root. Status: open.
What it is: What separates living off Earth (the A3 tier) from working there on rotation (A2). Early settlements may be work camps by policy for decades, with every person on a return schedule, even after the biology allows staying. The node resolves when some site's own rules allow residence with no return planned and someone has actually lived that way for years. Choosing to stay is John's decision, not the world's, and belongs with the choice points once the access branch firms up.
Resolves when: Under an off-Earth site's published residence terms, at least one person has lived there continuously for three years with no scheduled return to Earth, confirmed by the operator or governing body.
Source of truth: The site's published residence terms and the operator's or governing body's record
Depends on: `B-long-term-off-earth-living-by-some-route`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.50 / 0.60 / 0.75 / 0.90 / 0.93  (estimated 2026-09-19)
Rationale: Once the biology allows it, the rule is a liability and policy question; work-camp terms could persist for decades after staying becomes safe.
Notes: Added 2026-09-08 (agreed by John) so that A3 has a node distinguishing it from A2. Placed under regime because permanent residence is a rule somebody sets, not a technology.

## Factor C: Contact Clause (4 nodes)

### A non-human mind produces knowledge beyond us
Id: `C1`. Factor C. Horizon: leaf. Status: open.
What it is: An artificial system delivers a scientific or mathematical result that humans could not have produced and cannot fully check by hand, verified by machine and confirmed against nature. Plausibly already resolving; the first probabilities session decides how close.
Resolves when: A result in mathematics or the natural sciences is produced by an artificial system, is verified by machine checking or by experiment, is acknowledged in the peer-reviewed record as beyond what human researchers had been able to produce, and its full derivation is not checkable by a human reader without machine assistance.
Source of truth: The peer-reviewed record and the verification artefact
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.92 / 0.95 / 0.97 / 0.98 / 0.98  (estimated 2026-09-19)
Rationale: Plausibly resolving now; the remaining doubt is whether the record will say beyond human researchers in so many words.

### Humans learn from it
Id: `C2`. Factor C. Horizon: mid. Status: open.
What it is: Beyond receiving a result: humans come to understand something conceptual they could not have reached, in a way that changes how human science is done.
Resolves when: A concept or method that originated with an artificial system, and that the record shows human researchers had not reached, is adopted as a standard part of how a scientific field works, as evidenced by its use in textbooks or in the majority of new papers in that field.
Source of truth: The field's textbooks and publication record
Depends on: `C1`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.80 / 0.88 / 0.93 / 0.96 / 0.97  (estimated 2026-09-19)
Rationale: Adoption lags production by a decade or two, but forty-five years is long enough for one field to reorganise around one machine-born method.

### An intelligence not descended from us is detected
Id: `C3`. Factor C. Horizon: root. Status: open.
What it is: A signal or structure that only technology could have made (a technosignature), evidence of life more complex than microbes on another world (a biosignature), or an artefact. Low probability, fully resolvable. The instruments that would find it, a radio array on the far side of the Moon and a telescope at the Sun's gravitational focus, are the kind of large off-Earth projects the rest of the tree makes possible.
Resolves when: A detection of a signal or structure that only technology could have made, of evidence of life more complex than microbes beyond Earth, or of an artefact of non-human origin is confirmed by at least two independent teams and accepted as such in the peer-reviewed record.
Source of truth: The peer-reviewed record, two independent confirmations
Depends on: nothing (a root of its own).
Long shot. Mechanism: Instruments improve in steps that are already planned: a far-side lunar radio array shielded from Earth's noise, a telescope placed where the Sun's gravity focuses light from other stars, and spectrographs that read the air of nearby planets. Each step widens what could be seen. If anything is there within reach, one of these finds it; the remaining step is the confirmation by a second team.
Breaking point: Detection needs something to exist within reach and to be visible with the instruments we can build. Sixty years of listening have found nothing, and every model of how common such signals should be rests on guesses. The node cannot be made likelier by engineering alone.
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.05 / 0.07 / 0.10 / 0.18 / 0.30  (estimated 2026-09-19)
Rationale: Sixty years of nothing; the planned instruments widen the search by orders of magnitude but cannot make anything be there.

### Communion
Id: `C4`. Factor C. Horizon: root. Status: open.
What it is: Knowledge enters human understanding whose provenance is demonstrably not human and not human-built. The dream in its most beautiful form, kept on the board by the founding rule.
Resolves when: A body of knowledge is received and understood by humans whose origin is established, in the peer-reviewed record and by more than one independent line of evidence, as neither human nor produced by any human-built system.
Source of truth: The peer-reviewed record
Depends on: `C3`
Long shot. Mechanism: A confirmed detection (C3) turns out to carry structure, the structure is decoded, and the decoded content is shown to be knowledge rather than noise, the way a message with a proof in it could be checked. Each of those is a recognisable step from the one before.
Breaking point: There is no known test that establishes a piece of knowledge's provenance as non-human rather than the output of a human-built system, and nothing to decode has ever been received. Both the detection and the provenance test would have to be invented.
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.10 / 0.12 / 0.18 / 0.30 / 0.40  (estimated 2026-09-19)
Rationale: Given a detection, most detections would be a signature rather than a message, and the provenance test does not exist yet.

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
