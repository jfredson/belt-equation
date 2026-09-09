# Definitions and founding decisions

Started 2026-09-08. This document records what the project's terms mean and the decisions behind them. Each section is marked either DECIDED (with the date) or OPEN (with the current proposal). Nothing here gets a probability yet; probabilities come once the tree is stable.

## The question

DECIDED 2026-09-08. The question, which goes on the front page and is quoted in every post:

> What is the probability that I become a Belter before I die?

The subtitle, which states the method:

> And how does that number move year over year?

"Before I die" was chosen over "in my lifetime" on purpose: the bluntness is the point, and it is the Belter register. The method clause was moved out of the question so the question alone is the hook, the way the Drake Equation's question is.

## What "Belter" means (the access tiers)

DECIDED 2026-09-08. A Belter is someone who lives and works off Earth as a matter of ordinary life, the way the Belters of The Expanse do. Because that can be true to different degrees, the project uses tiers:

- **A0, contributes from Earth.** Works in or for the off-world industry without leaving: training crews, working for a launch or habitat company, writing about it.
- **A1, has flown.** At least one trip to space, suborbital or orbital, as passenger or crew.
- **A2, works off Earth on rotation.** Spends months at a time living and working at an off-world site, the way people work Antarctica or an oil platform today.
- **A3, lives off Earth.** Permanent residence at an off-world site.

The headline number refers to A2, since working out there on rotation is what a Belter actually is. A3 is reported beside it as the stretch.

The codes A0 through A3 are what the tree data uses. Belter-flavored public names for the tiers are a presentation decision, deferred, and can be chosen without touching the tree.

The ladder is open at the top. Tiers beyond A3 (raising a family off Earth, belonging to a Belt culture with its own identity) are real meanings of "Belter" but require the Full Expanse system tier to exist first, so they would resolve "no" inside the window and add nothing to the number now. Adding an A4 at a future annual review is a documented extension, not a redesign. A possible missing rung between A1 (one flight) and A2 (months-long rotation), such as a weeks-long station stint, is a candidate for version one, to be revisited after the node brainstorm shows whether any nodes need it.

## What "the Belt exists" means (the system tiers)

DECIDED 2026-09-08. The state of the solar system is also tiered, because the access tiers depend on it. The tiers are location-agnostic: an "off-world site" is a surface base, an orbital or free-space station, or a large rotating habitat, anywhere off Earth. This is deliberate. Some space futurists (Jeff Bezos most prominently) see large free-space habitats, not planetary surfaces, as the more viable near-term path, and a rotating habitat with Earth-normal gravity is the one route that sidesteps the biology factor if living and reproducing in partial gravity turns out to be impossible. The tree treats the habitat route as a hedge on B and gives it its own branch under the technology factor.

- **Tier 1, Outpost.** Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth.
- **Tier 2, Settlement.** Thousands living off Earth at one or more sites, at least one child born and raised off Earth, partial local self-sufficiency in air, water, and food.
- **Tier 3, Slow Expanse.** Tens of thousands off Earth, including at least one site beyond the Earth-Moon system (asteroid belt, outer moon, or a habitat out there). Transit times in months. A resource economy where something mined or made off Earth is sold at a profit. Nuclear propulsion in routine use.
- **Tier 4, Full Expanse.** Millions off Earth, transit times in weeks on constant-acceleration drives, a Belt population, on rocks or in habitats, with its own political identity and economy.

Tier 3 counts as "the Belt exists" for the headline number, because the A2 number (working off Earth on rotation) depends on an outer site with an economy, not on millions of people or a constant-acceleration drive. Setting the bar at Tier 4 would put the headline near zero by definition and hide all the movement in the range that matters.

The child-born-off-Earth criterion stays in Tier 2 on purpose. It is the biology factor resolving yes, and it is what separates a settlement from a work camp, even though early settlements may forbid it and so reach it late.

## The factors

DECIDED 2026-09-08. Eight factors, frozen: W window, L launch, E energy, D drive, B biology, M motive, R regime, A access. Each is a roll-up of a subtree of nodes. See README.md for one-line meanings.

E (energy) and D (drive) stay separate. Nuclear-electric propulsion exists today without fusion, and a working fusion power plant on the ground does not give you a fusion rocket, because a drive needs the reactor to be light as well as working. So the two resolve independently in the cases that matter. Most drive nodes depend on some energy nodes, and the tree records that dependency.

The large-habitat route is a branch, not a ninth factor. Its nodes (orbital construction, materials, lunar material supply) sit under launch and energy, and its role as a hedge sits under biology. Eight factors is already the edge of what a person can hold in their head, and the count is what makes the equation quotable.

## The window

DECIDED 2026-09-08. The deadline is John's expected date of natural death. It is not a constant, because longevity research moves it. In the tree it is the axis the four longevity scenarios run along rather than a node of its own: the window factor's nodes are the research results that would move it, and the whole tree is re-run once per scenario (docs/node-schema.md). Amended 2026-09-08 from "a node in the tree" when the schema settled this form; it keeps John's health out of the public tree.

Baseline window: **2071, plus or minus 8 years** (age 85; range 2063 to 2079). Refined on 2026-09-08 from the health record, which stays out of this repo.

What may be said about the person the window belongs to, ruled by John 2026-09-08 (amending the earlier rule that nothing about his health appears here): John is a healthy man of forty in an elite, physically demanding military career that requires top physical and mental condition as a condition of the job, and an endurance athlete who trains and performs well above the average for his age. He puts a deliberate share of his time and income into finding the lifestyle and medical choices most likely to move his own health trajectory in the right direction, which is one reason the window is a thing he tracks rather than a number he accepts. Nothing more specific than this paragraph, and nothing from the health record itself, goes into the public tree. A fitness percentile may be added later only if it comes from a repeatable measured test against a named age-group standard, stated with the standard and the date (agreed 2026-09-08); the wording is a draft to be rewritten once the window is confirmed after the baseline blood panel. The method: start from standard US life tables for a 40-year-old male (roughly 38 to 40 more years, landing around 2065), then adjust for the factors with the best evidence of moving all-cause mortality, in the direction the record supports. The result sits about six years above the population figure. The main source of remaining uncertainty is incomplete family history and a baseline blood panel still being completed; revisit the window when that panel is done, and at every annual review. Roadmap step 3 is complete.

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

It is a term C, published beside the equation and never multiplied into it, because nothing about the Belt depends on it. It is the "why," stated in the same currency as the "whether." It obeys the same rule as every node: it is in only because each rung has a resolution criterion.

- **C1, a non-human mind produces knowledge beyond us.** An artificial system delivers a scientific or mathematical result that humans could not have produced and cannot fully check by hand, verified by machine and confirmed against nature. Plausibly already resolving.
- **C2, humans learn from it.** Beyond receiving a result: humans come to understand something conceptual they could not have reached, in a way that changes how human science is done.
- **C3, an intelligence not descended from us is detected.** A technosignature, a biosignature implying more than microbes, an artifact. Low probability, fully resolvable; instruments already in the tree (a far-side lunar radio array, a solar gravitational-lens telescope) are its sensors.
- **C4, communion.** Knowledge enters human understanding whose provenance is demonstrably not human and not human-built.

The dream in its most beautiful form, in John's words, is the ending of The Expanse Season 2 Episode 5, "Home" (Miller and the protomolecule on Eros as it falls toward Venus). A private machine transcript of that scene sits in docs/private/ (ignored by git, because the scene is copyrighted) as a reference while the project develops. It is C4 in dramatic form.

C1 and C2 may resolve through machine intelligence within the window, which is the practical fulfillment of the dream. C3 and C4 are the romantic version, kept on the board by the founding rule. Whether a machine mind counts as a mind of another perspective is the question John's Calibration Problem manuscript is about, and the two projects should reference each other.

## The personal pathway (the A branch)

DECIDED 2026-09-08 to keep this branch provisional, and why. The branch is gated on SERE pipeline graduation (expected May 2027). Until that resolves, its content is a sketch, and none of the personal background goes into the public version. Health nodes stay out of the public tree entirely and live in the Health folder.

The sketch, stated by John on 2026-09-08 and explicitly hesitant: assuming graduation, serve between 6 and 20 years, for as long as service keeps expanding capabilities and experience in ways that serve the longer-term goals of this project. The first contract is 6 years. At that point the branch forks: leverage the survival-instructor experience into space-related or defense-related civilian opportunities that get closer to the goals than staying would, or take military opportunities that the first contract opens up, worth another 4 to 14 years: intelligence-community roles, an increased military presence in space with a survival or operator requirement, or operator-type roles that could appear under long-shot developments in the Space Force. Several low-probability trees live in there, and they are worth tracking.

**Choice points and world events.** Everywhere else in the tree, a node is something that happens to the world. In this branch, some nodes are things John chooses: re-enlist or separate at the six-year mark, take an opening or not, pursue one credential over another. The tree marks these as choice points, distinct from world events, and the method for the branch is to run the whole tree once per option and compare the results. That is what turns the project from a forecast into a decision tool, and it is the most useful thing it can do: answer which short-term decisions place him on the most interesting and impactful probability trees for the greater Belt Equation. John named this as the most exciting reason to build and keep updating the method.

**The leverage branch.** DECIDED 2026-09-08, stated by John. The capability of frontier AI models and their tooling (Claude, Claude Code, and whatever follows) is what has let one person build Sentient Horizons, TimeAssembler, and now this project, and it will keep raising how much of this dream he can observe, track, and eventually take part in. That capability is tracked in the tree as its own branch under the access factor, with the same node discipline as everything else: what a single person with these tools can do, and by when. Candidate nodes: the tree maintains and re-runs itself with a human only approving changes; an AI partner can carry a research program (the physics loop from the origin conversation) that a lone person could not; AI tooling shortens the degree and credential path; AI is an ordinary co-worker in the spaceflight industry so that a small team can do what a company did. Tracking these advances is, in John's words, just as exciting as tracking the other technologies, and this branch is also the machinery behind Contact Clause rungs C1 and C2.

Candidate world-event nodes already identified: a civilian survival and contingency training industry for commercial crews exists; someone has made the move from military survival instruction into spaceflight training; analog missions accept applicants with his profile; a commercial orbital seat costs less than some threshold; eligibility for private orbital flight holds at 55, 60, and 65; post-service degree and credential completion.

## Where it lives publicly, and how often it is reviewed

DECIDED 2026-09-08. The repo is public from the start, so the tree is inspectable by anyone from the first node. The project is public but under-promoted: the first audience is family and friends, for interesting conversation, and John wants to stay deliberate about how much and in what capacity he writes about it publicly. Launch, when it comes, is a Sentient Horizons essay with Reddit companion posts.

AMENDED 2026-09-08, later the same evening, by John: the first presentable version gets a dedicated website of its own rather than waiting for public critique to change the tree first. The site is the home of the tree, the numbers, and the writeups; the essay and the Reddit posts point to it. Under-promoted still holds: the site exists and is linked to family and friends without being announced more widely until John decides to. The plan is in docs/website-plan.md and its steps run alongside the roadmap.

Cadence: a quarterly fifteen-minute scan for leaf nodes that resolved or moved, logged in CHANGELOG.md; a full annual review each January (every node re-estimated, the numbers re-run, the calibration score updated, a public changelog post). TimeAssembler holds the project's story; this repo holds the tree and the documents.

Near-term commitment: John intends to spend a significant share of his free time before the SERE pipeline resumes (early 2027) solidifying the project's foundations so that tracking and updating can begin. See docs/roadmap.md.

## Decision log

- 2026-09-08. Project named The Belt Equation (decided by John, from options proposed by Claude). Repo created at ~/Code/belt-equation.
- 2026-09-08. Question wording frozen: "What is the probability that I become a Belter before I die?" with the method as a subtitle (proposed by Claude, approved by John).
- 2026-09-08. Access tiers A0 to A3 adopted as drafted; headline number is A2; ladder open at the top; public tier names deferred (proposed by Claude, approved by John).
- 2026-09-08. System tiers 1 to 4 adopted; Tier 3 is the "Belt exists" bar; child-born-off-Earth stays as the Tier 2 marker (proposed by Claude, approved by John). Tiers made location-agnostic to include large space-station and rotating-habitat living as a pathway, and the habitat route recorded as a hedge on the biology factor (raised by John).
- 2026-09-08. Factor set frozen at eight; energy and drive kept separate; habitat route is a branch, not a factor (proposed by Claude, approved by John).
- 2026-09-08. Window placeholder 2070, provisional; three scenarios at 2070, 2080, 2095 (proposed by Claude, approved by John); fourth escape-velocity scenario with the window open added (raised by John, framed by Claude).
- 2026-09-08. Founding rule that the tree keeps long shots on the board on purpose (stated by John).
- 2026-09-08. Contact Clause adopted as a term beside the equation, not in it (raised by John as the project's underpinning, framed by Claude, approved by John).
- 2026-09-08. Access branch kept provisional until pipeline graduation; service-length sketch of 6 to 20 years recorded; choice-point nodes and run-per-option method adopted (stated by John, method framed by Claude).
- 2026-09-08. Public posture: public repo, under-promoted, family and friends first; cadence quarterly scan plus January annual review; TimeAssembler project created for the story (stated by John, cadence proposed by Claude and approved).
- 2026-09-08. Window refined from the health record to 2071 plus or minus 8; baseline scenario moved from 2070 to 2071 (computed by Claude from John's records; John to confirm).
- 2026-09-08. Leverage branch added under the access factor: the capability of AI tools as a tracked multiplier on John's own ability to take part (stated by John).
- 2026-09-08. Second founding rule, plausible all the way to the edge of the impossible: long-shot nodes must name their mechanism and their breaking point (stated by John; carried into the node schema as a review test).
- 2026-09-08. The deadline is the scenario axis, not a node of its own; the window factor's nodes are the research results that move it (proposed by Claude when the window nodes were drafted, accepted by John with the first brainstorm draft).
- 2026-09-08. Fifth longevity scenario added, radical extension to 2136 (a 150-year life), between strong extension and the open window (proposed by Claude, agreed by John). A3 given a distinguishing node, an off-Earth site accepting permanent residents, so it no longer equals A2 (proposed by Claude, agreed by John). Fitness percentile held out of the health paragraph until it comes from a measured test (proposed by Claude, agreed by John).
- 2026-09-08. Health rule amended: a one-paragraph general statement of John's fitness, the demands of his career, and his deliberate investment in his own health trajectory may appear in the public project; nothing from the health record itself (stated by John; wording drafted by Claude for refinement).
- 2026-09-08. Standalone site no longer deferred: the first presentable version gets a dedicated website, planned in docs/website-plan.md and built alongside the roadmap; under-promoted posture unchanged (stated by John, reversing the earlier deferral).
