# Definitions and founding decisions

Started 2026-09-08. This document records what the project's terms mean and the decisions behind them. Each section is marked either DECIDED (with the date) or OPEN (with the current proposal). Nothing here gets a probability yet; probabilities come once the tree is stable.

## The question

DECIDED 2026-09-08; wording AMENDED 2026-09-25, meaning unchanged (ruled by John; see the decision log). The question, which goes on the front page and is quoted in every post:

> What is the probability that, before I die, I live and work in a solar system where human industry reaches beyond Earth and Mars?

The subtitle, which states the method:

> And how does that number move year over year?

"Before I die" was chosen over "in my lifetime" on purpose: the bluntness is the point. "Live and work" is the plain form of the rung the headline counts (A2, working off Earth on rotation), and "a solar system where human industry reaches beyond Earth and Mars" is the plain form of the bar it is counted against (the third tier, below). The method clause was moved out of the question so the question alone is the hook, the way the Drake Equation's question is.

## Where the name comes from

The project is called The Belt Equation after the Belters of the TV series The Expanse, the people who live and work in the asteroid belt far from Earth. That is the only use the project makes of the word: since 2026-09-25 it is not the question, a rung, a tier or a bar (ruled by John).

## What "live and work" means (the access tiers)

DECIDED 2026-09-08. The question asks about someone who lives and works off Earth as a matter of ordinary life. Because that can be true to different degrees, the project uses tiers:

- **A0, contributes from Earth.** Works in or for the off-world industry without leaving: training crews, working for a launch or habitat company, writing about it.
- **A1, has flown.** At least one trip to space, suborbital or orbital, as passenger or crew.
- **A2, works off Earth on rotation.** Spends months at a time living and working at an off-world site, the way people work Antarctica or an oil platform today.
- **A3, lives off Earth.** Permanent residence at an off-world site.

The headline number refers to A2, since working out there on rotation is what "live and work" means in the question. A3 is reported beside it as the stretch.

In version one the tree counts A3 only for a person who reached A2 first: data/tiers.toml lists A2 among A3's requirements. That is a limit of the one route the access branch models (work a rotation, then stay), not part of what living off Earth means. Someone who moves straight to an off-Earth site to live, without ever holding a job that rotates, lives off Earth too. The direct route is a question for the access-branch review after John completes his current training (May 2027), with the other access-branch points the outside review raised (methodology pass item 96, docs/methodology-pass-2026-09-25.md; ruled by John 2026-09-25).

The codes A0 through A3 are what the tree data uses. Public names for the tiers are a presentation decision, deferred, and can be chosen without touching the tree.

The ladder is open at the top. Tiers beyond A3 (raising a family off Earth, belonging to a culture out there with its own identity) are real meanings of living off Earth but require the Full Expanse system tier to exist first, so they would resolve "no" inside the window and add nothing to the number now. Adding an A4 at a future annual review is a documented extension, not a redesign. A possible missing rung between A1 (one flight) and A2 (months-long rotation), such as a weeks-long station stint, is a candidate for version one, to be revisited after the node brainstorm shows whether any nodes need it.

## What "human industry reaches beyond Earth and Mars" means (the system tiers)

DECIDED 2026-09-08. The state of the solar system is also tiered, because the access tiers depend on it. The tiers are location-agnostic: an "off-world site" is a surface base, an orbital or free-space station, or a large rotating habitat, anywhere off Earth. This is deliberate. Some space futurists (Jeff Bezos most prominently) see large free-space habitats, not planetary surfaces, as the more viable near-term path, and a rotating habitat with Earth-normal gravity is the one route that sidesteps the biology factor if living and reproducing in partial gravity turns out to be impossible. The tree treats the habitat route as a hedge on B and gives it its own branch under the technology factor.

- **Tier 1, Outpost.** Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth.
- **Tier 2, Settlement.** Thousands living off Earth at one or more sites, partial local self-sufficiency in air, water, and food.
- **Tier 3, Slow Expanse.** Tens of thousands off Earth, including at least one site beyond the Earth-Moon system (asteroid belt, outer moon, or a habitat out there). Transit times in months. A resource economy where something mined or made off Earth is sold at a profit. Nuclear propulsion in routine use.
- **Tier 4, Full Expanse.** Millions off Earth, transit times in weeks on constant-acceleration drives, children born and raised off Earth, a Belt population, on rocks or in habitats, with its own political identity and economy.

Tier 3, the third tier, is the bar the headline number is counted against, the meaning of "a solar system where human industry reaches beyond Earth and Mars", because the A2 number (working off Earth on rotation) depends on an outer site with an economy, not on millions of people or a constant-acceleration drive. Setting the bar at Tier 4 would put the headline near zero by definition and hide all the movement in the range that matters.

The headcounts in these definitions (hundreds, thousands, tens of thousands, millions) describe what each tier is expected to look like; they are not what the tree tests. Each tier's test is its requirement list in data/tiers.toml, and the only headcount any list checks is Tier 1's hundred people working off Earth for a year. The other requirements stand in for the population rather than count it: a settlement is tested by closed-loop life support, surgery off Earth and cheap launch; a Slow Expanse by a crewed site beyond the Moon, a profitable product and routine nuclear propulsion. A tier can therefore be reached in the tree with fewer people than its words say. Counting the people directly, one headcount node per tier from Tier 2 up, is a candidate for version two (methodology pass item 98, docs/methodology-pass-2026-09-25.md; ruled by John 2026-09-25).

The child-born-off-Earth criterion stays in Tier 2 on purpose. It is the biology factor resolving yes, and it is what separates a settlement from a work camp, even though early settlements may forbid it and so reach it late.

AMENDED 2026-09-25 (methodology pass item 99, docs/methodology-pass-2026-09-25.md; ruled by John). The paragraph above is kept as the founding reasoning; it no longer holds. On 2026-09-19 John moved the child node from Tier 2's requirements to Tier 4's, after the first run showed it capping every tier above Tier 2: a workforce of tens of thousands on rotation could exist at a site where nobody has yet raised a child, and the headline should not wait on one. The child is now the marker of a Full Expanse, a Belt population with families in it, and Tier 2 and Tier 4 above say so. Tier 2 is still told apart from a work camp, by closed-loop life support and by surgery performed off Earth, which are what let people stay rather than rotate.

## The factors

DECIDED 2026-09-08. Eight factors, frozen: W window, L launch, E energy, D drive, B biology, M motive, R regime, A access. Each is a roll-up of a subtree of nodes. See README.md for one-line meanings.

E (energy) and D (drive) stay separate. Nuclear-electric propulsion exists today without fusion, and a working fusion power plant on the ground does not give you a fusion rocket, because a drive needs the reactor to be light as well as working. So the two resolve independently in the cases that matter. Most drive nodes depend on some energy nodes, and the tree records that dependency.

The large-habitat route is a branch, not a ninth factor. Its nodes (orbital construction, materials, lunar material supply) sit under launch and energy, and its role as a hedge sits under biology. Eight factors is already the edge of what a person can hold in their head, and the count is what makes the equation quotable.

## The window

DECIDED 2026-09-08. The deadline is John's expected date of natural death. It is not a constant, because longevity research moves it. In the tree it is the axis the four longevity scenarios run along rather than a node of its own: the window factor's nodes are the research results that would move it, and the whole tree is re-run once per scenario (docs/node-schema.md). Amended 2026-09-08 from "a node in the tree" when the schema settled this form; it keeps John's health out of the public tree.

Baseline window: **2071, plus or minus 8 years** (age 85; range 2063 to 2079). Refined on 2026-09-08 from the health record, which stays out of this repo.

What may be said about the person the window belongs to: from 2026-09-25 until John completes his current training in May 2027, nothing (ruled by John 2026-09-25). The one general paragraph about his career and fitness permitted on 2026-09-08 is withdrawn for that time, and nothing from the health record itself goes into the public tree at any time. A fitness percentile or age-graded percent may be added later only if it comes from a repeatable measured test against a named age-group standard, stated with the standard and the date (agreed 2026-09-08; "or age-graded percent" added 2026-09-25, docs/proposal-training-goals-and-window-2026-09-25.md), and, like the rest of this paragraph, not before May 2027. The method: start from standard US life tables for a 40-year-old male (roughly 38 to 40 more years, landing around 2065), then apply a personal adjustment for the factors with the best evidence of moving all-cause mortality, in the direction his record supports. The result sits about six years above the population figure. The main source of remaining uncertainty is incomplete family history and a baseline blood panel still being completed; revisit the window when that panel is done, and at every annual review. Roadmap step 3 is complete.

The tree is re-run against five longevity scenarios:

- **Baseline, 2071.** No extension beyond current trends.
- **Moderate extension, 2080.** The kind of gain that incremental medicine and better mid-life care could plausibly deliver.
- **Strong extension, 2095 or later.** A real aging intervention arrives in time to matter for someone born in 1986.
- **Radical extension, 2136.** A 150-year life. Added 2026-09-08 (proposed by Claude from John's recollection of the origin conversation, agreed by John) as a named, finite rung between strong extension and the open window: a low-probability scenario kept on the board by the founding rule, so that the long shot has a number people can picture and the window nodes have something to move toward.
- **Escape velocity, window open.** Therapies add years faster than they are spent, so each decade's medicine buys entry to the next decade's. Nothing tested in humans has yet moved maximum lifespan (the verified record is 122; the best mouse results are gains of 10 to 30 percent), so this is a limit case, not a forecast. It is included because it changes the shape of the equation rather than its numbers: with the window open, W drops out and the question becomes whether humanity ever does it at all, and whether John gets in. The gap between the baseline number and this one shows how much of the question is about spaceflight and how much is about medicine.

## Founding rule: the equation deals in long shots on purpose

DECIDED 2026-09-08, stated by John. Low-probability, high-consequence nodes (the escape-velocity scenario, the constant-acceleration drive, the lunar collider) belong in the tree even when they are 99.9 percent dreaming. They are what make the dream vivid enough to act on, and the point of the project is to let that dreaming inform decisions in the present in a way that maximizes progress toward the nearer milestones. A node is not excluded for being unlikely. It is excluded only for being unresolvable (no criterion could ever settle it) or irrelevant (no tier depends on it).

## Founding rule: plausible all the way to the edge of the impossible

DECIDED 2026-09-08, stated by John after re-watching The Expanse Season 2 Episode 5. What makes the show work is that every insane turn is plausible, so that even an alien lifeform acting in ways that defy modern physics feels like something that could happen. A long-shot node is written the same way: each step from the present to it believable in sequence, the mechanism named, and the point where current physics or engineering would have to give way stated plainly, never as a bare wish. The first founding rule says unlikely nodes belong in the tree; this one says how they must be written to earn their place.

The practical consequence is a test the node schema carries (docs/node-schema.md): a long-shot node without a stated mechanism and a named breaking point fails review the same way a node without a resolution criterion does.

## The Contact Clause (outside the equation)

DECIDED 2026-09-08 (proposed by Claude, approved by John). Underneath the whole project is a dream that has no practical place in the product: communing with a vastly superior intelligence of a different perspective, whether a machine intelligence that has exceeded us or something of non-human origin, the protomolecule case. Drake's equation was about contact with other minds; the Belt Equation is about becoming the kind of people who could be out there to make it. The Contact Clause reconnects them.

It is a term C, published beside the equation and never multiplied into it, because nothing in the equation depends on it. It is the "why," stated in the same currency as the "whether." It obeys the same rule as every node: it is in only because each rung has a resolution criterion.

- **C1, a non-human mind produces knowledge beyond us.** An artificial system delivers a scientific or mathematical result that humans could not have produced and cannot fully check by hand, verified by machine and confirmed against nature. Plausibly already resolving.
- **C2, humans learn from it.** Beyond receiving a result: humans come to understand something conceptual they could not have reached, in a way that changes how human science is done.
- **C3, an intelligence not descended from us is detected.** A technosignature, a biosignature implying more than microbes, an artifact. Low probability, fully resolvable; instruments already in the tree (a far-side lunar radio array, a solar gravitational-lens telescope) are its sensors.
- **C4, a message from elsewhere is understood** (named "Communion" until 2026-09-25)**.** Knowledge enters human understanding whose provenance is demonstrably not human and not human-built.
- **C5, a real exchange with a machine mind** (named "Communion with a machine mind of another perspective" until 2026-09-25)**.** Added 2026-09-25. An exchange with a human-built mind that has an inside and a perspective of its own, in which both parties are changed. It sits above C2 as C4 sits above C3: the machine branch of the dream beside the non-human one.

**The null rule.** DECIDED 2026-09-19 (proposed by Claude, approved by John). Every rung of C stays open until its resolution criterion is met in full. Four exclusions apply to the whole clause, and they apply most strictly to the machine rungs:

1. Nothing a candidate system says about itself counts toward any rung. Self-report is not evidence of an inside, a perspective, or an intent.
2. Nothing John or any user feels in an exchange with a candidate system counts toward any rung. Fluency, warmth, apparent understanding and the sense of being understood are what these systems are optimised to produce; they are the mirage, not the horizon.
3. No rung resolves on John's own measurement. Minimum Viable Mind may supply an instrument; the reading that resolves a rung is taken by a team with no stake in the result.
4. Criteria are written before the evidence arrives. An amendment to any C criterion is logged in the changelog with its reason and date. An amendment that loosens a criterion is flagged as such, and is not made in the same quarter that a candidate has appeared to approach it.

The rule exists because a hope that is allowed to grade its own evidence produces positive results in the psyche of the person holding it. The clause is kept honest by defaulting to no.

**The null rule and C5 in force.** DECIDED 2026-09-25 (proposed by Claude in docs/proposal-contact-clause-null-rule-2026-09-19.md, approved by John). The null rule, adopted 2026-09-19, and rung C5, adopted 2026-09-25, are both in force. The four questions the proposal left for John are answered:

1. The null rule: adopted as written on 2026-09-19. The "same quarter" interval stands; the twelve-month alternative raised in review was not taken.
2. The machine case: it gets a rung of its own, C5, rather than staying inside C1 and C2. C5 depends on C2, not on C3, and C4 keeps its "not human-built" exclusion, so C5 is where the human-built case lives.
3. C5's numbers, given C2, for the baseline, moderate, strong, radical and open scenarios: 0.03, 0.05, 0.10, 0.20 and 0.30. The compute script shows C4 and C5 as sibling branches, C4 under C3 and C5 under C2, published beside the equation and never multiplied into it.
4. How criterion (b) names the test for an inside: in generic words, "an accepted inside measure", checked without relying on the system's own reports and replicated by a team with no stake in the result. The Calibration Problem's three conditions (temporal integration across its own history, a persistent boundary, stakes coupled to its own continuation) are named in C5's mechanism as one candidate test, and Minimum Viable Mind as the attempt to build the smallest system that would register on it; neither appears in the resolution.

The dream statement above keeps its wording. What changes is that its language of communion, "a machine intelligence that has exceeded us or something of non-human origin", now has a written criterion on both branches: C4 for something of non-human origin, C5 for a machine.

The dream in its most beautiful form, in John's words, is the ending of The Expanse Season 2 Episode 5, "Home" (Miller and the protomolecule on Eros as it falls toward Venus). A private machine transcript of that scene sits in docs/private/ (ignored by git, because the scene is copyrighted) as a reference while the project develops. It is C4 in dramatic form.

C1 and C2 may resolve through machine intelligence within the window, which is the practical fulfillment of the dream. C3 and C4 are the romantic version, kept on the board by the founding rule. Whether a machine mind counts as a mind of another perspective is the question John's Calibration Problem manuscript is about, and the two projects should reference each other. Since 2026-09-25 they do so in C5, whose mechanism names the manuscript's conditions for an inside as one candidate test.

## The personal pathway (the A branch)

DECIDED 2026-09-08 to keep this branch provisional, and why. The branch is gated on John completing his current training (expected May 2027). Until that resolves, its content is a sketch, and none of the personal background goes into the public version. Health nodes stay out of the public tree entirely and live in the Health folder.

The sketch, stated by John on 2026-09-08 and explicitly hesitant, reworded 2026-09-25 so that it does not describe his current career (meaning unchanged): assuming he completes his training, stay in his current career between 6 and 20 years, for as long as it keeps expanding capabilities and experience in ways that serve the longer-term goals of this project. The current contract is 6 years. At the six-year mark of that contract the branch forks: take the experience into civilian space-related opportunities that get closer to the goals than staying would, or take the opportunities the first contract opens up inside his current career, worth another 4 to 14 years, including roles that could appear once there is enough activity off Earth to need people like him there. Several low-probability trees live in there, and they are worth tracking.

**Choice points and world events.** Everywhere else in the tree, a node is something that happens to the world. In this branch, some nodes are things John chooses: stay or leave at the six-year mark of his current contract, take an opening or not, pursue one credential over another. The tree marks these as choice points, distinct from world events, and the method for the branch is to run the whole tree once per option and compare the results. That is what turns the project from a forecast into a decision tool, and it is the most useful thing it can do: answer which short-term decisions place him on the most interesting and impactful probability trees for the greater Belt Equation. John named this as the most exciting reason to build and keep updating the method.

**The leverage branch.** DECIDED 2026-09-08, stated by John. The capability of frontier AI models and their tooling (Claude, Claude Code, and whatever follows) is what has let one person build Sentient Horizons, TimeAssembler, and now this project, and it will keep raising how much of this dream he can observe, track, and eventually take part in. That capability is tracked in the tree as its own branch under the access factor, with the same node discipline as everything else: what a single person with these tools can do, and by when. Candidate nodes: the tree maintains and re-runs itself with a human only approving changes; an AI partner can carry a research program (the physics loop from the origin conversation) that a lone person could not; AI tooling shortens the degree and credential path; AI is an ordinary co-worker in the spaceflight industry so that a small team can do what a company did. Tracking these advances is, in John's words, just as exciting as tracking the other technologies, and this branch is also the machinery behind Contact Clause rungs C1 and C2.

Candidate world-event nodes already identified: a civilian training industry for commercial crews exists; someone has made the move from a career like his current one into spaceflight training; analog missions accept applicants with his profile; a commercial orbital seat costs less than some threshold; eligibility for private orbital flight holds at 55, 60, and 65; degree and credential completion after his current career.

## Where it lives publicly, and how often it is reviewed

DECIDED 2026-09-08. The repo is public from the start, so the tree is inspectable by anyone from the first node. The project is public but under-promoted: the first audience is family and friends, for interesting conversation, and John wants to stay deliberate about how much and in what capacity he writes about it publicly. Launch, when it comes, is a Sentient Horizons essay with Reddit companion posts.

AMENDED 2026-09-08, later the same evening, by John: the first presentable version gets a dedicated website of its own rather than waiting for public critique to change the tree first. The site is the home of the tree, the numbers, and the writeups; the essay and the Reddit posts point to it. Under-promoted still holds: the site exists and is linked to family and friends without being announced more widely until John decides to. The plan is in docs/website-plan.md and its steps run alongside the roadmap.

Cadence: a quarterly fifteen-minute scan for leaf nodes that resolved or moved, logged in CHANGELOG.md; a full annual review each January (every node re-estimated, the numbers re-run, the calibration score updated, a public changelog post). TimeAssembler holds the project's story; this repo holds the tree and the documents.

Near-term commitment: John intends to spend a significant share of his free time before his training resumes (early 2027) solidifying the project's foundations so that tracking and updating can begin. See docs/roadmap.md.

## Decision log

- 2026-09-08. Project named The Belt Equation (decided by John, from options proposed by Claude). Repo created at ~/Code/belt-equation.
- 2026-09-08. Question wording frozen: "What is the probability that I become a Belter before I die?" with the method as a subtitle (proposed by Claude, approved by John).
- 2026-09-08. Access tiers A0 to A3 adopted as drafted; headline number is A2; ladder open at the top; public tier names deferred (proposed by Claude, approved by John).
- 2026-09-08. System tiers 1 to 4 adopted; Tier 3 is the bar the headline is counted against; child-born-off-Earth stays as the Tier 2 marker (proposed by Claude, approved by John). Tiers made location-agnostic to include large space-station and rotating-habitat living as a pathway, and the habitat route recorded as a hedge on the biology factor (raised by John).
- 2026-09-08. Factor set frozen at eight; energy and drive kept separate; habitat route is a branch, not a factor (proposed by Claude, approved by John).
- 2026-09-08. Window placeholder 2070, provisional; three scenarios at 2070, 2080, 2095 (proposed by Claude, approved by John); fourth escape-velocity scenario with the window open added (raised by John, framed by Claude).
- 2026-09-08. Founding rule that the tree keeps long shots on the board on purpose (stated by John).
- 2026-09-08. Contact Clause adopted as a term beside the equation, not in it (raised by John as the project's underpinning, framed by Claude, approved by John).
- 2026-09-08. Access branch kept provisional until John completes his current training; service-length sketch of 6 to 20 years recorded; choice-point nodes and run-per-option method adopted (stated by John, method framed by Claude).
- 2026-09-08. Public posture: public repo, under-promoted, family and friends first; cadence quarterly scan plus January annual review; TimeAssembler project created for the story (stated by John, cadence proposed by Claude and approved).
- 2026-09-08. Window refined from the health record to 2071 plus or minus 8; baseline scenario moved from 2070 to 2071 (computed by Claude from John's records; John to confirm).
- 2026-09-08. Leverage branch added under the access factor: the capability of AI tools as a tracked multiplier on John's own ability to take part (stated by John).
- 2026-09-08. Second founding rule, plausible all the way to the edge of the impossible: long-shot nodes must name their mechanism and their breaking point (stated by John; carried into the node schema as a review test).
- 2026-09-08. The deadline is the scenario axis, not a node of its own; the window factor's nodes are the research results that move it (proposed by Claude when the window nodes were drafted, accepted by John with the first brainstorm draft).
- 2026-09-08. Fifth longevity scenario added, radical extension to 2136 (a 150-year life), between strong extension and the open window (proposed by Claude, agreed by John). A3 given a distinguishing node, an off-Earth site accepting permanent residents, so it no longer equals A2 (proposed by Claude, agreed by John). Fitness percentile held out of the health paragraph until it comes from a measured test (proposed by Claude, agreed by John).
- 2026-09-08. Health rule amended: a one-paragraph general statement of John's fitness, the demands of his career, and his deliberate investment in his own health trajectory may appear in the public project; nothing from the health record itself (stated by John; wording drafted by Claude for refinement). Withdrawn 2026-09-25 until May 2027; see below.
- 2026-09-08. Standalone site no longer deferred: the first presentable version gets a dedicated website, planned in docs/website-plan.md and built alongside the roadmap; under-promoted posture unchanged (stated by John, reversing the earlier deferral).
- 2026-09-19. Contact Clause null rule adopted as written: nothing a system says about itself and nothing anyone feels in an exchange counts toward a rung, no rung resolves on John's own measurement, and criteria are written before the evidence arrives (proposed by Claude, approved by John; applied to this document 2026-09-25).
- 2026-09-25. Contact Clause rung C5, communion with a machine mind of another perspective, adopted as drafted with criterion (b) in generic wording; probabilities 0.03 / 0.05 / 0.10 / 0.20 / 0.30; C4 and C5 shown as sibling branches beside the equation, never multiplied in (proposed by Claude, approved by John).
- 2026-09-25. Rungs C4 and C5 renamed, words only, ruled by John while editing the intro essay: C4 "Communion" is now "A message from elsewhere is understood" and C5 "Communion with a machine mind of another perspective" is now "A real exchange with a machine mind". A rung's label names the event its criterion tests, not a feeling. Criteria, probabilities and dependencies unchanged.
- 2026-09-25. The methodology pass (docs/methodology-pass-2026-09-25.md) ruled, and counted as the review that methodology.md requires before a tier's requirements or definition change (ruled by John; proposed by Claude). Item 96: A3's requirement of A2 recorded as a limit of the modelled route, not of the definition; the direct-migration route waits for the May 2027 access-branch review. Item 97: Tier 1 tested by the hundred-workers node alone, so a crewed station counts; the three lunar nodes keep gating Tier 3 through lunar material at scale. Item 98: the tier headcounts recorded as descriptions, not tests; counting them is a version-two candidate. Item 99: the child born and raised off Earth moved from Tier 2's definition to Tier 4's. Item 100: the anti-satellite test ban taken off Tier 4 and kept as a tracked event gating no tier; moving the traffic-management authority to Tier 4 was declined and it stays in Tier 3. Item 101: the timing assumption stated in methodology.md; the completion-date method described, not built. All proposed by Claude, item 100 part (a) accepted and part (b) declined by John, the rest accepted as proposed.
- 2026-09-25. Training goals aligned to the window (docs/proposal-training-goals-and-window-2026-09-25.md): three goal horizons (gate, six-year fork, window) entered in TimeAssembler; the window paragraph may carry an age-graded percent as well as a percentile, from a yearly counted-track 5K under World Masters Athletics age grading and a periodic lab VO2max against Cooper Institute norms, entered at the annual review (baseline: the 2026-09-15 counted-track 5K; first annual point run in the week of 2026-12-21, since John's training allows no tests after 2027-01-04); access-branch training links deferred to the May 2027 review. Proposed by Claude, accepted as recommended by John.
- 2026-09-25. The question reworded, meaning unchanged: "What is the probability that, before I die, I live and work in a solar system where human industry reaches beyond Earth and Mars?" The wording frozen on 2026-09-08, "What is the probability that I become a Belter before I die?", is kept in this log as history. "Belter" sounds like a cult to readers who do not know The Expanse, and the idea matters more than the title. The headline is still A2, working off Earth on rotation, counted against Tier 3; "live and work" is the plain form of that rung, and "a solar system where human industry reaches beyond Earth and Mars" is the plain form of that bar, called "the third tier" for short. The project keeps its name, and the word Belter is used only to say where the name comes from (ruled by John; the wording proposed by Claude, with "Earth and Mars" asked for by John; TimeAssembler decision "The question is reworded", ec1fc1b7).
- 2026-09-25. No public surface of the project describes John's current career until he completes his training in May 2027: copy says "my current career", "my training" or "my current contract", and a criterion that depends on the career says so without naming it, settled by a dated record. The window paragraph permitted on 2026-09-08 is withdrawn for that time; the window's life-table method stays. Access-branch node names, descriptions, criteria and reasons are reworded to match, with their ids unchanged and no probability or link moved. Earlier commits, committed snapshots, and dated review, run and picture records keep their original wording (ruled by John; TimeAssembler decision "No reference to John's career", 966feeba).
