# Review packet: window-biology (2026-09-19)

You are reviewing part of a forecasting tree called the Belt Equation. It estimates the probability that one person, born in January 1986, works off Earth on months-long rotations before he dies, computed from a dependency tree of about sixty breakthroughs ("nodes") under eight factors. Each node has a resolution criterion (what would count as it having happened), the nodes it depends on, and five probabilities: the chance it resolves yes before the window closes in 2071, 2080, 2095, 2136, and with no deadline at all, in each case given that the nodes it depends on have already resolved. Numbers were proposed by one AI model and accepted by the author, who wants them challenged by models from other labs before publishing. Your job is critique, not agreement. Plain language throughout; a reader outside the field should follow every sentence.

Below are the nodes for this packet, then the scenario table and what each tier of the tree requires. Give your answer as three parts, in this order, with a table at the top of each part.

Part 1, missing nodes. Name up to three breakthroughs, events, or dependencies that these factors need and the tree does not have. For each: a name, a one-line resolution criterion (what record would settle it), and which existing node or tier it should gate. If you think nothing is missing, say so and say why.

Part 2, criteria. For any node whose resolution criterion is ambiguous, cannot be measured from public records, has already been met, or measures the wrong thing for what the node is about, name the node and propose the fix in one sentence. If a node has already resolved in your knowledge, say so and cite what settled it.

Part 3, numbers. For any node where you would put the probability at least 0.15 higher or lower than the tree does in any of the five scenarios, give your own five numbers, a one-paragraph reason, and your confidence in the disagreement (low, medium, high). Remember the numbers are conditional on the dependencies having resolved. Differences smaller than 0.15 are not worth arguing; leave those nodes out. Your numbers must not fall as the window lengthens.

You may look things up. If you do, say where in your answer, so facts from lookup can be told from your judgment. Do not soften findings to be polite; a factor with nothing to challenge is a possible finding, but an unlikely one.

## The nodes

## Factor W: Window (7 nodes)

### The large dog trial of rapamycin reports that treated dogs live measurably longer
Id: `W-dog-rapamycin-trial-reports-longer-life`. Factor W. Horizon: leaf. Status: open.
What it is: The Dog Aging Project's TRIAD trial gives rapamycin, the best-studied life-extending drug in mice, to hundreds of pet dogs in a placebo-controlled design and follows them for years. It is the first lifespan trial of an aging drug in a large mammal living in ordinary conditions, and its result is due within a few years. A positive result is the single strongest near-term signal that mouse longevity results carry over to animals like us.
Resolves when: The trial's primary lifespan analysis, published in a peer-reviewed journal, reports a statistically significant increase in lifespan for the rapamycin group over placebo.
Source of truth: The Dog Aging Project's published TRIAD results
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.45 / 0.45 / 0.45 / 0.45 / 0.45  (estimated 2026-09-08)
Rationale: One trial, one readout around 2031: the mouse evidence is strong and a dog pilot showed heart benefits, but lifespan trials fail more often than they succeed, so a little under even; the same in every scenario because the window does not change when the trial reports.

### A major drug regulator accepts slowing aging as something a drug can be approved for
Id: `W-regulator-accepts-aging-as-an-indication`. Factor W. Horizon: leaf. Status: open.
What it is: Today a drug must target a named disease. There is no approvable indication for slowing aging itself, which is why aging drugs are tested against single diseases and why companies avoid the field. In 2015 the US regulator agreed that one trial could use a composite of age-related diseases as its primary endpoint, which is the precedent; what does not yet exist is guidance saying a drug can be approved, and labelled, for slowing aging. That is what changes what gets funded and trialed.
Resolves when: The US Food and Drug Administration or the European Medicines Agency publishes guidance stating that slowing aging, extending healthy lifespan, or delaying a composite of age-related diseases is an indication for which a drug can be approved and labelled. Accepting such a composite as a trial endpoint, which the US regulator did in 2015, does not count.
Source of truth: The regulator's own published guidance
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.55 / 0.60 / 0.70 / 0.85 / 0.90  (estimated 2026-09-08)
Rationale: The 2015 composite-endpoint precedent and a growing field make guidance within forty-five years somewhat more likely than not; every added decade of trials and lobbying raises it.
Notes: Checked 2026-09-08 against the trial's own design papers and the National Institute on Aging's page on regulator review of aging-related applications: the regulator approved the trial's composite design and the trial 'holds the potential' to lead to aging being considered an indication, which confirms that no approvable indication exists yet.

### A randomized human trial shows one drug delays several age-related diseases at once
Id: `W-composite-aging-trial-positive-in-humans`. Factor W. Horizon: mid. Status: open.
What it is: The Targeting Aging with Metformin trial and others like it test whether one cheap drug can delay the arrival of heart disease, cancer, dementia, and death taken together in older adults. A positive result is the first proof in humans that aging can be slowed as a whole rather than one disease at a time.
Resolves when: A randomized, placebo-controlled trial of at least a thousand older adults reports a statistically significant delay in a combined measure, fixed before the trial began, of several age-related diseases or death (a pre-registered composite endpoint), published in a peer-reviewed journal.
Source of truth: The trial's peer-reviewed primary publication and its pre-registration record
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.70 / 0.75 / 0.80 / 0.90 / 0.90  (estimated 2026-09-08)
Rationale: The metformin trial alone is perhaps two in five to report positive around 2031, but a dozen other composite trials over the following decades make at least one success likely.
Notes: Checked twice on 2026-09-08: no primary results publication for the Targeting Aging with Metformin trial (about 3,000 adults aged 65 to 79, four years, composite of heart disease, cancer, dementia, and death) was found in journal, registry, or sponsor sources; aggregator sites claiming a positive result are unconfirmed. Stays open. Re-check at the first quarterly scan.

### A cell-rejuvenation treatment based on partial reprogramming is given to people in a registered trial
Id: `W-partial-reprogramming-reaches-human-trials`. Factor W. Horizon: leaf. Status: resolved-yes.
What it is: Partial reprogramming turns back the age markers of cells by briefly switching on the genes used to make stem cells, without erasing what the cell is. It has restored sight and extended life in mice and is the most-funded route to actually reversing rather than slowing aging. The first human trial is the point where it becomes a medicine rather than a lab result, and it has happened: the first participant was dosed in June 2026, in a safety trial for two causes of age-related vision loss.
Resolves when: A registered clinical trial (on clinicaltrials.gov or an equivalent registry) doses at least one human participant with a partial-reprogramming therapy, for any indication.
Source of truth: The trial registry entry and the sponsor's announcement of first dosing
Depends on: nothing (a root of its own).
Resolved 2026-06-09: Life Biosciences press release of 2026-06-09 announcing the first participant dosed in its Phase 1 trial of ER-100 (registry entry NCT07290244), with independent press coverage
Notes: Drafted open on 2026-09-08 and found resolved the same evening when checked under the verification rule, before any probability was estimated.

### The first drug is approved whose purpose is to slow aging, not to treat one disease
Id: `W-first-drug-approved-to-slow-aging`. Factor W. Horizon: mid. Status: open.
What it is: The point where slowing aging becomes ordinary medicine that a doctor can prescribe. This is what moves the baseline scenario toward the moderate one for everyone, not only trial participants.
Resolves when: The US Food and Drug Administration or the European Medicines Agency approves a treatment whose labeled indication is slowing aging, extending healthy lifespan, or delaying a composite of age-related diseases.
Source of truth: The regulator's approval record and the product label
Depends on: `W-regulator-accepts-aging-as-an-indication`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.60 / 0.65 / 0.75 / 0.90 / 0.92  (estimated 2026-09-08)
Rationale: Given a regulator has opened the door, a first approval follows within a decade or two more often than not; the gap to certainty is trials that fail on safety in the old.
Notes: Almost certainly also depends on a positive composite trial; whether that is a hard dependency is for step 7.

### A treatment is shown in a large trial to cut the death rate of older adults by at least a quarter
Id: `W-human-therapy-cuts-death-rate-in-older-adults`. Factor W. Horizon: root. Status: open.
What it is: The result that would make the moderate scenario (a window around 2080) the expected case rather than a hope: a therapy that reduces all-cause mortality in people over sixty-five by a quarter or more over the trial period. Nothing yet approved comes close; statins and blood pressure drugs move single causes of death by smaller amounts.
Resolves when: A randomized, placebo-controlled trial in adults aged sixty-five or over, followed for at least five years, reports that deaths from any cause fell by twenty-five percent or more in the treated group, published in a peer-reviewed journal and not later retracted.
Source of truth: The trial's peer-reviewed primary publication
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.20 / 0.25 / 0.35 / 0.60 / 0.70  (estimated 2026-09-08)
Rationale: A quarter off all deaths in the over-65s is beyond anything approved; one in five by 2071 reflects that reprogramming and combination therapies are real but unproven in humans.

### Someone verifiably lives past 122, the longest human life on record
Id: `W-verified-human-lifespan-passes-122`. Factor W. Horizon: root. Status: open.
What it is: Jeanne Calment's 122 years has stood since 1997 and no verified case has come within three years of it since, which is the strongest evidence that current medicine moves average lifespan but not maximum lifespan. A verified case beyond it is the first sign that the ceiling has moved, which is what the strong and open scenarios need.
Resolves when: A person's age at death, or current age while living, exceeds 122 years and 164 days, verified by the Gerontology Research Group or an equivalent body with documentary evidence of birth.
Source of truth: Gerontology Research Group validated supercentenarian records
Depends on: nothing (a root of its own).
Long shot. Mechanism: Someone born around 1905 to 1930 who has already reached 110 benefits from late-life medicine that did not exist for Calment (better cardiac, infection, and fall care), and survives the last few years at a mortality rate that today runs near fifty percent a year. Later, a person who received an approved aging therapy in their sixties or seventies carries a slower rate of decline into their hundreds.
Breaking point: Annual mortality past 110 appears to plateau near fifty percent, so each further year is a coin flip and 122 needs a run of a dozen heads; the record has not moved in almost thirty years despite far more people reaching 100. Passing it by more than a year or two requires that some intervention lower the late-life mortality rate itself, which nothing tested in humans has done.
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.05 / 0.08 / 0.15 / 0.45 / 0.60  (estimated 2026-09-08)
Rationale: The record has stood since 1997 and late-life mortality has not moved; passing it needs a therapy that lowers that rate, so near-impossible by 2071 and better than a coin flip only in the 150-year scenario.
Notes: Checked 2026-09-08: the record is 122 years and 164 days (1997); the second-longest verified life is 119 years and 107 days (2022), just over three years short, and the third is 119 years and 97 days (1999).

## Factor B: Biology (9 nodes)

### A mammal is conceived, born, and weaned in partial gravity
Id: `B-mammal-born-and-weaned-in-partial-gravity`. Factor B. Horizon: leaf. Status: open.
What it is: Whether pregnancy and early development work in less than Earth's gravity is the biggest open question in off-Earth biology and has never been tested end to end. Mice have flown in a spinning enclosure on the space station that produces lunar or Martian gravity, so the experiment is within reach. A live, weaned litter is the first evidence that a settlement, rather than a work camp, is biologically possible.
Resolves when: A peer-reviewed publication reports that a mammal was conceived, carried to term, born, and weaned entirely at a sustained gravity level between one-sixth and one-half of Earth's, whether in a centrifuge in orbit or on the Moon or Mars, with offspring surviving to weaning.
Source of truth: The peer-reviewed publication and the space agency's mission record
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.80 / 0.82 / 0.85 / 0.92 / 0.95  (estimated 2026-09-08)
Rationale: The centrifuge hardware exists and the experiment is cheap next to everything else in the tree; the risk is that partial-gravity gestation fails biologically, which would resolve the node no, not that nobody tries.

### A person lives a full year in partial gravity and comes home without disqualifying harm
Id: `B-human-year-in-partial-gravity-without-disqualifying-harm`. Factor B. Horizon: mid. Status: open.
What it is: The longest stays off Earth are a year or more in free fall on the space station, where bone, muscle, eye, and heart changes are well documented. Nobody has lived even a month in partial gravity. A year on the Moon (or in a spinning facility set to lunar or Martian gravity) with published health outcomes that would not bar a return trip is what a rotation of months, the A2 tier, assumes.
Resolves when: A person completes twelve continuous months at a sustained gravity level between one-sixth and one-half of Earth's, and a peer-reviewed report of their health outcomes finds no condition that the responsible agency's own standards would count as disqualifying for a further mission.
Source of truth: The peer-reviewed health report and the agency's crew-health standards
Depends on any one of: `L-crew-lands-on-moon-in-reusable-lander`, `B-crewed-spin-gravity-demonstration`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.35 / 0.42 / 0.50 / 0.65 / 0.70  (estimated 2026-09-08)
Rationale: Given people on the Moon or a spin facility, a year-long stay is a matter of decades, and then roughly two in three that the health outcomes clear the bar; bone and eye effects in free fall are the warning.
Notes: Edge drawn at step 7 (2026-09-08): a year in partial gravity needs either people on the Moon or a spinning facility; either route will do.

### A child is born off Earth and raised there through early childhood
Id: `B-human-child-born-off-earth`. Factor B. Horizon: root. Status: open.
What it is: The marker that separates a settlement from a work camp, and the criterion Tier 2 uses. Early settlements may forbid it for years, so it resolves late even if the biology allows it.
Resolves when: A child is born at a site off Earth and lives there continuously to at least age five, with the birth and residence publicly documented by the operating agency or company.
Source of truth: Public records of the operating agency or company, confirmed by independent reporting
Depends on: `B-mammal-born-and-weaned-in-partial-gravity`, `B-human-year-in-partial-gravity-without-disqualifying-harm`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.15 / 0.22 / 0.35 / 0.65 / 0.75  (estimated 2026-09-08)
Rationale: Given both the animal result and the human year, the remaining barriers are policy and ethics, which early settlements are likely to hold for decades; raising a child needs a settlement, not a base.

### A crew lives for a month in a spinning spacecraft that produces artificial gravity
Id: `B-crewed-spin-gravity-demonstration`. Factor B. Horizon: leaf. Status: open.
What it is: Artificial gravity by spinning has been proposed since the 1950s and never flown with people. A month-long crewed demonstration at any useful gravity level settles the practical questions (motion sickness, docking, structural behaviour) that keep it a paper idea, and is the first step on the habitat route that sidesteps the partial-gravity question entirely.
Resolves when: A crewed spacecraft or station module rotates to produce at least one-sixth of Earth's gravity at the crew's living level for thirty continuous days with people aboard, confirmed by the operator and independent tracking.
Source of truth: The operator's mission record and independent orbital tracking
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.70 / 0.75 / 0.80 / 0.90 / 0.92  (estimated 2026-09-08)
Rationale: Proposed since the 1950s, never flown, but private station builders now plan it and the engineering is modest; the risk is that nobody funds a month-long test when partial gravity on the Moon is available instead.

### People live for a year in a spinning habitat with Earth-normal gravity
Id: `B-earth-gravity-habitat-occupied-for-a-year`. Factor B. Horizon: root. Status: open.
What it is: The full version of the habitat route: a structure large enough (roughly a hundred metres or more in radius, spinning about three times a minute) that its occupants feel Earth's gravity and need no adaptation at all. If partial gravity turns out to be unlivable, this is the only route to a Belt, and it is the route some space futurists prefer anyway.
Resolves when: A rotating habitat produces at least ninety percent of Earth's gravity at its living level and is continuously occupied by at least ten people for twelve months, confirmed by the operator and independent tracking.
Source of truth: The operator's records and independent orbital tracking
Depends on: `B-crewed-spin-gravity-demonstration`, `L-large-structure-assembled-in-orbit`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.25 / 0.32 / 0.45 / 0.70 / 0.80  (estimated 2026-09-08)
Rationale: Given a spin demo and hundred-metre assembly, an Earth-gravity habitat is a matter of money and motive; one in four by 2071 because both are large and the partial-gravity route may make it unnecessary.
Notes: Edge drawn at step 7 (2026-09-08): a habitat with Earth-normal gravity is a hundred-metre-class structure, so it needs orbital assembly to have been done at that scale.

### Humans can live off Earth long term, by partial gravity or by a spinning habitat
Id: `B-long-term-off-earth-living-by-some-route`. Factor B. Horizon: root. Status: open.
What it is: The hedge on biology, as one node so it has a name and a number. Resolves if either route does: people stay healthy for a year in partial gravity, or a rotating habitat with Earth-normal gravity is occupied for a year. The system tiers that need long-term living require this node rather than either route alone.
Resolves when: Either of the two route nodes it depends on has resolved yes.
Source of truth: The resolving route node's own source
Depends on any one of: `B-human-year-in-partial-gravity-without-disqualifying-harm`, `B-earth-gravity-habitat-occupied-for-a-year`
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 1.00 / 1.00 / 1.00 / 1.00 / 1.00  (estimated 2026-09-08)
Rationale: Resolves whenever either route does; certainty here means the number is carried entirely by the two route nodes.

### A shielding system flown in space cuts the deep-space radiation dose to a crew by half
Id: `B-shielding-halves-deep-space-radiation-dose`. Factor B. Horizon: mid. Status: open.
What it is: Beyond Earth's magnetic field, galactic cosmic rays deliver a dose that puts a multi-year mission near or past current career limits, and the heavy nuclei in that radiation are hard to stop with thin walls. Passive routes (thick water or hydrogen-rich walls, regolith) and active routes (superconducting magnetic shields) both exist on paper. A flown demonstration that halves the dose makes rotations of months at an outer site a matter of engineering rather than of accepting the risk.
Resolves when: A shielding system flown beyond low Earth orbit is measured to reduce the dose from deep-space radiation (the galactic cosmic rays that Earth's magnetic field otherwise keeps out) at the crew position by fifty percent or more compared with an unshielded reference, reported in a peer-reviewed publication.
Source of truth: The peer-reviewed flight measurement
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.50 / 0.55 / 0.65 / 0.80 / 0.85  (estimated 2026-09-08)
Rationale: Thick water walls could do it today at a mass cost; halving the dose in a flown test within forty-five years is even odds because the passive route is expensive and the magnetic route waits on cheap superconductors.
Notes: The magnetic route depends on high-temperature superconductors at practical cost, an energy node; drawn at step 7.

### A crew off Earth lives for a year with most of its food, water, and air recycled on site
Id: `B-closed-loop-life-support-year-off-earth`. Factor B. Horizon: mid. Status: open.
What it is: The space station recycles most of its water and makes its oxygen from that water, but every calorie is shipped up. Ground experiments (a year-long sealed habitat in China) have closed the food loop on Earth. Doing it off Earth for a year is what partial self-sufficiency, the Tier 2 criterion, means in practice.
Resolves when: A crew at a site off Earth completes twelve continuous months during which more than half of their calories are grown on site and more than ninety-five percent of water and oxygen are recycled, as reported by the operating agency or company.
Source of truth: The operator's published life-support accounting
Depends on: nothing (a root of its own).
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.50 / 0.58 / 0.70 / 0.85 / 0.90  (estimated 2026-09-08)
Rationale: Done on the ground for a year at 98 percent closure; doing it off Earth needs a site with the volume for farming, which is a settlement-scale project, so even odds by 2071.

### A treatment is approved that makes people substantially more resistant to chronic space radiation
Id: `B-radiation-resistance-treatment-for-humans`. Factor B. Horizon: root. Status: open.
What it is: The long shot on the biology side: rather than stopping the radiation, change the person. Some organisms shrug off doses that would kill us, and a few of the responsible genes and proteins are known. A drug or gene therapy that halves the long-term cancer and tissue damage from chronic cosmic-ray exposure would loosen the mission limits that shielding otherwise has to meet.
Resolves when: A drug or gene therapy is approved by a major regulator, or adopted by a space agency's crew-health standard, with evidence that it reduces the long-term harm from chronic galactic-cosmic-ray-type exposure by half or more.
Source of truth: The regulator's approval record or the agency's published crew-health standard
Depends on: nothing (a root of its own).
Long shot. Mechanism: Radioprotective drugs already exist for acute exposure (amifostine protects tissue during radiotherapy). Proteins from radiation-tolerant organisms, such as the tardigrade's Dsup, have reduced DNA damage in human cells in the lab, and gene therapies that deliver a single protein are now routine medicine. The step is from lab cells to a therapy shown to cut lifetime cancer risk from chronic heavy-ion exposure, tested first in animals on the station or the Moon.
Breaking point: Nobody knows whether the harm from years of heavy-ion exposure comes mostly from DNA damage, which such proteins address, or from other tissue and vascular effects that they do not. There is no human data on chronic heavy-ion exposure at all, and a preventive therapy given to healthy people for a rare exposure faces an approval bar that no current evidence could meet.
Probabilities (2071 / 2080 / 2095 / 2136 / no deadline): 0.08 / 0.10 / 0.15 / 0.35 / 0.45  (estimated 2026-09-08)
Rationale: A preventive therapy for a rare exposure faces an approval bar no current evidence meets, and the biology of chronic heavy-ion harm is not understood; a long shot that only becomes plausible over a century.

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
