# How the numbers are computed

Written 2026-09-19 (roadmap step 12), the day the tree was first run end to end. This is the document the website renders on its methodology page and the one a reader should be able to argue with. What the question is and what the tiers mean is in definitions.md; this document is only about how a tree of sixty nodes becomes a handful of percentages, how those percentages will be scored against reality, and how the decision comparison is run.

Updated 2026-09-20, when the outside review (roadmap step 27) landed: the tree stands at sixty-nine nodes after nine were added on the reviewers' arguments, every number has been through the review described below, and the run reports one more figure beside the headline, A2 at Tier 1, explained under "What is reported and what is not". The counts elsewhere in this document are the ones of 2026-09-19 and are left as written.

## The tree

A node is one thing that could happen: a launcher flies a hundred times in a year, a fusion plant sells electricity, a child is born off Earth, John graduates from his training pipeline. Every node has a name a stranger can read, a criterion that says exactly what would count as it having happened and where to look, and a list of other nodes it cannot happen without. There are sixty of them as of 2026-09-19, sorted under the eight factors of the equation (window, launch, energy, drive, biology, motive, regime, access) and the Contact Clause beside it. The dependency lists turn the sixty nodes into a directed graph with no cycles, which the script checks before it does anything else.

Each node carries five probabilities, one per longevity scenario, because the deadline is the thing that changes between scenarios. The scenarios are the years the window closes: 2071 (the baseline, refined from John's own record on 2026-09-08), 2080, 2095, 2136 (a 150-year life), and no deadline at all (the escape-velocity case). A node's number under a scenario is the chance it happens before that year, given that everything it depends on has happened. That conditional form is the one a person can actually estimate: not "how likely is orbital manufacturing at scale by 2071" but "if launch is cheap and a hundred people already work up there, how likely is it then". The script refuses a set of numbers that falls as the window lengthens, since a longer wait cannot make a thing less likely to have happened by the end of it.

The numbers themselves are estimates, first proposed by Claude with a one-line reason and then accepted or moved by John, each recorded with its date and reason on the node. They are the least reliable part of the method and the part the rest of the method exists to correct over time. Before anything is published they go through an outside review: each factor's nodes, criteria, reasons and numbers are given to at least two other frontier models with a fixed brief (name a missing node, challenge a criterion, argue a number up or down with a reason and a confidence), the answers are filed under docs/reviews/, and John rules on every disagreement. An external forecaster's answers to the same questions, asked cold, are kept as a comparison column (the first row is in docs/forecasts/) and are never adopted as the tree's numbers.

## Function over route

Added 2026-09-25 (docs/proposal-function-over-route-2026-09-25.md, approved by John the same day), after the question "why does it have to be a nuclear reactor?"

**The rule.** A dependency names the function a downstream event needs, not one route to it, whenever more than one route could supply that function. If lunar mining at scale needs power through the two-week lunar night, the step it depends on is "power through the lunar night at a surface site", not "a fission reactor on the lunar surface". The reactor stays in the tree as one route, with its own criterion and probability, and the function step can happen once any route has.

**The test, applied to every link in the tree.** Name the thing the child actually takes from the parent. If a second event, not the parent, would supply the same thing and the child would go ahead just as well, the link names one route and should point at a function step instead. If no plausible second route exists, or the child's own criterion names the route (a crew *landing* needs a lander), the link stands.

**What a function step looks like.** Either a threshold criterion written without naming a route ("at least a hundred kilowatts of net electrical power available at a lunar surface site for ninety percent of a year, from any source"), with the routes listed under it as the ways it can come about; or an either-route step, which happens when any of its routes does and carries no probability of its own beyond what the routes supply. The threshold form is preferred where a single checkable number exists; the either-route form where the routes are already steps with criteria of their own.

**Why it matters for the numbers.** A link that names one route multiplies the child by that route's chance, when the true chance is that of any route coming good. It is the same mistake the world draw below corrects for shared causes, made at the level of a single link, and it always biases the tree low. The first founding rule (long shots stay on the board) keeps unlikely routes in; this rule keeps the tree from treating one route as the only one.

**What it does not do.** It does not remove specific events. The lunar reactor, the reusable lander and nuclear propulsion all stay, as routes and as tracked events. It changes which step the children point at. The first sweep of the whole tree under this rule was made on 2026-09-25 (docs/runs/2026-09-25-function-over-route.md), and every new link from then on is written to it.

## How the tree is played out

The script plays the whole tree out twenty thousand times per scenario. In each play-through it visits the nodes in dependency order. A node that has already happened in the real world is fixed at yes; one that has already failed is fixed at no. A node John decides (a choice point) is set to whatever the current plan says and is never rolled. Every other node is rolled: if everything it depends on came up yes in this play-through, it comes up yes with its probability for the scenario, and otherwise it is no. A tier is reached in a play-through when every node it requires came up yes. The number reported for a tier is simply the fraction of play-throughs that reached it, and the headline is the fraction that reached A2, working off Earth on rotation.

This is a Bayesian network evaluated by simulation, which is the standard way to get a probability out of a graph of conditional probabilities when the graph is too large to multiply out by hand. It is also, on its own, wrong in a known way, which the next section is about.

## The world draw

If every node is rolled independently, the tree says the Belt does not exist by 2095 (Tier 3 at 0.2 percent on the first run, 2026-09-19) even though every node on the way there is individually likely. That is what happens when fifteen moderately likely things are all required and are multiplied as if unrelated. But they are related: cheap launch, sustained money, and a working off-Earth economy are causes shared across most of the tree, and a world where one of them comes good is a world where the others tend to. Independence understates the chance that everything lines up, and it understates it more the longer the chain.

The fix in version one is the simplest one that is honest about what it does. Before each play-through, the script draws one number for how favourable the world turned out, from a normal distribution with mean zero and a spread of 1.0 on the log-odds scale. It then shifts every open node's probability by that number on the same scale before rolling it. One standard deviation up turns a 50 percent node into 73 percent and a 20 percent node into 40 percent; one standard deviation down does the reverse. Nodes already resolved, choice points, and nodes at exactly 0 or 1 are not moved. The effect is that in some play-throughs everything is easier and in some everything is harder, which is what shared causes do.

Why 1.0. A spread of 0 is independence, which the first run showed to be too pessimistic by inspection. A spread of 2.0 would let one draw carry a 20 percent node to 80 percent, which treats the world as nearly a single coin flip and makes the individual estimates almost irrelevant. At 1.0 a typical good world roughly doubles the odds of a middling node and a typical bad world roughly halves them, which is about the size of swing the last two decades of spaceflight have actually shown between the pessimistic and optimistic readings of the same facts. It is a judgment, it is the one free parameter in the method, and the script prints the independent-roll result beside the world-draw result on every run so the reader can see exactly how much the parameter is worth. On the 2026-09-19 run it is worth the difference between 0.5 percent and 5.6 percent at the headline by 2095. The annual review revisits it; a finer treatment (correlation by factor, or between named pairs of nodes) is on the list under docs/node-schema.md, Known simplifications, and is not worth its weight until the tree has stopped changing shape.

## What the numbers assume about timing

A node's number is the chance it happens before the window closes, given that everything it depends on has happened. That condition says nothing about when the parents happened. A parent done in 2035 leaves its child thirty-six years before the 2071 deadline; one done in December 2070 leaves it a few weeks. Every estimate in the tree therefore averages, by the estimator's feel, over when its parents are likely to finish, and nothing in the script checks the averaging.

The assumption version one makes, stated so it can be argued with: each number is read as if the node's parents finish at about the time they typically would, in the worlds where they finish at all. Where that is wrong, it is most likely wrong in one direction. In the play-throughs where a long chain of parents all come true only just before the deadline, the child still gets its full chance, when in the world it would have almost no time left. So the numbers for events at the top of long chains, under the shorter windows, probably lean high, which is the opposite of the lean the world draw corrects. How much is not known. The fix is a different kind of estimate, a spread of completion dates for each node rather than one probability per window, and it is a version-two question, described in docs/methodology-pass-2026-09-25.md under item 101 and not built.

## What is reported and what is not

The run reports, for each of the five scenarios, the chance of each system tier (Outpost, Settlement, Slow Expanse, Full Expanse) and each access tier (contributes from Earth, has flown, works off Earth on rotation, lives off Earth), then the four Contact Clause rungs in their own section, then every node's overall chance, which is its conditional number multiplied through by the chance its dependencies came true.

One more figure is reported beside the headline, from 2026-09-20: the chance of working a rotation at a station or a lunar base whether or not a Belt exists, which is A2's own requirement (a role whose holders rotate off Earth) met together with Tier 1 (an outpost) rather than with Tier 3. The outside review's largest structural point was that a visitor reading "become a Belter" may picture exactly that nearer thing, while the headline measures the narrower event of working rotations in a Belt that exists. The headline was kept as it was, because that is what a Belter is, and the nearer figure is shown beside it so the gap is visible instead of hidden. It is computed in the same play-throughs (a play-through counts when both the outpost tier and the rotation-role node held), so the two figures are always from the same run.

The five scenarios are reported side by side and are not combined into one number. The window factor's own nodes (the trials, the regulator, the first drug that slows aging) describe how likely the longer scenarios are to be the true one, and a future version could turn them into weights and report a single headline. Version one does not, on purpose: the spread across the five columns is itself the finding, because it shows how much of the question is about spaceflight and how much is about medicine, and a single weighted number would hide it. The data file leaves room for the weights and does not fill them.

The Contact Clause is reported and never multiplied into any tier. It is on the board because the founding rule keeps long shots on the board, and it is beside the equation rather than in it because whether a mind of another perspective is ever met is a different question from whether John gets to the Belt.

## The decision comparison

Some nodes in the access branch are John's decisions rather than the world's: at the six-year mark, re-enlist or separate into civilian space or defence work. These are never rolled. Instead the script runs the whole tree once per option, with that option forced and everything else as usual, and reports the headline for each. The difference between the rows is what the decision is worth, in probability of A2, under the tree's current beliefs about the world.

This is standard decision analysis: a decision node is not a random variable, and the value of an option is the outcome distribution given that you take it. It is also the reason the project exists as something more than a forecast. On the first pass (2026-09-19) the two options differ by under a point, which is inside the noise of an access branch that is still a sketch. The branch is rebuilt with real detail after John graduates from the pipeline in May 2027, and the comparison is re-run then; until that point the row is reported but not read.

## Running the tree for somebody else

Added 2026-09-20 with the "Run it for yourself" page (website step 39; the decisions behind it,
with their alternatives, are in docs/run-it-yourself-plan.md). Everything above is about John's
odds. This section is about what the same tree says for a visitor, and about the one piece of
arithmetic that needs, which is not in the sections above.

The deadline is the whole difficulty. Every probability in the tree is the chance of something
happening before one of five years: 2071, 2080, 2095, 2136, and no deadline at all. Those years
are not arbitrary and they are not general. They are John's ages 85, 94, 109 and 150, for a man
born in January 1986. A visitor born in 2000 who picks the baseline scenario is asking about
their own 85th year, which is 2085, and the tree has no numbers for 2085.

So the page does two things. First it shifts: a reader's five windows are John's five windows
moved by the difference in birth years, which keeps the scenarios meaning the same thing (the
same age, under the same assumption about medicine) rather than the same calendar year. Second
it reads a number for each open event at the shifted year, by drawing a straight line between
the two neighbouring windows' numbers.

The line is drawn on the log-odds scale, the same scale the world draw already works on. The
reason is that probabilities near the ends of the range do not move in even steps. An event
going from 2 percent to 4 percent has doubled in odds, and so has one going from 50 percent to
67 percent; on the plain scale those look like a move of two points and a move of seventeen. The
tree's five estimates sit far more evenly spaced on the log-odds scale than on the plain one,
which is what makes a straight line between two of them a reasonable reading rather than a
distortion. Because no event's number is allowed to fall as the window lengthens, the reading
never falls either.

Two ends need a rule of their own:

- **Before the first window.** A reader older than John has a baseline deadline earlier than
  2071, and the tree was never estimated for a shorter wait. Nothing is read downward: the
  number holds flat at the baseline value. This is a floor, not an answer. For a reader whose
  deadline has already passed or is nearly here, the honest statement is that the tree cannot
  see below its own first window, and the page says so in those words rather than printing a
  confident figure.
- **After the last window.** A reader much younger than John has a radical-extension deadline
  past 2136, and the only thing beyond it is the no-deadline number. The reading moves toward
  that number and closes half the remaining distance every 41 years, which is the gap between
  the last two named windows. It reaches the no-deadline number only in the limit and never
  passes it, which is right: no finite deadline can be worth more than no deadline at all.

**What this is and is not.** It is a reading of five estimates, not six. Nobody sat down and
estimated a probability for 2085; the five numbers were each estimated on their own, as five
separate answers to five separate questions, and were never meant as points on a smooth curve.
Drawing a line between them assumes they lie on one, and that assumption is the method's own,
not the estimator's. The further a reader's deadline sits from one of John's five windows, the
more of the answer is the line and the less is the estimate. Nothing here changes a stored
probability, a committed run, or the headline: the page reads the tree and never writes to it.

**A reader's own part.** The tree can say how likely the world is to offer an opportunity. It
cannot say whether a particular person takes it, because that depends on their money, their
health, their work and their luck, none of which is in the tree and none of which the project
knows. So a route on that page is split in two and the halves are never added up silently: the
world's part comes from the tree, and the reader's own part is a number the reader types, shown
beside it and labelled as their guess. The two multiplied together is shown last and smallest,
because it is the least reliable figure on the page.

## The calibration score

A forecast that is never scored is an opinion. Every node has a resolution criterion so that it can be scored, and the score is the Brier score, the standard measure of how well a set of probabilities matched what happened: for each node that has resolved, take the probability that was on the record for it under the baseline scenario at the time it resolved, subtract one if it happened and zero if it did not, square the difference, and average across the resolved nodes. Zero is perfect; 0.25 is what you get by saying fifty percent about everything; a score above 0.25 is worse than saying nothing.

The score is computed each January at the annual review over every node that resolved in the year, and again cumulatively over every node that has ever resolved, and both numbers go in the changelog post. Nodes that resolved before their first probability was recorded (three as of 2026-09-19) are not scored, since there was no forecast to score. The same holds for any node resolved retrospectively later, meaning one found to have happened before a probability for it was on the record: it is unscored. That includes the two cases the outside review raised on 2026-09-19, the recession node and C1 (items 89 and 90 of docs/reviews/2026-09-19-rulings.md), had either been resolved on a past event; John ruled both reworded and kept open instead, so neither is resolved today. The test is mechanical rather than a label someone must remember to add: a node is scored only if its record holds a probability dated before its resolution date, either as its current number or in its revision log. (Confirmed 2026-09-25 at the methodology pass, docs/methodology-pass-2026-09-25.md, item 102.) The leaves, the third of the tree that could resolve within five years, are what make this work at all: without them the first score would be decades away. The quarterly scan exists to catch them resolving. A score alone does not say which numbers were wrong, so the review also lists each resolved node with its recorded probability and outcome, and the year-over-year movement of the headline, which is the product the project actually delivers.

## What is fixed and what moves

Fixed for version one, and changed only at an annual review with a changelog line: the question, the tiers and what they require, the eight factors, the five scenarios, the world-draw spread, and the scoring rule. Moved whenever the world moves, with a dated revision on the node: a node's status when it resolves, and its probabilities when the quarterly scan or a review finds reason to. Added at any time, with a changelog line: new nodes, when a scan or a critic finds a gap. Never changed once a probability has been published against it: a node's id and its criterion, so that the score can always find the forecast it is scoring; a node that needs a different criterion after publication is retired and replaced. Before publication, a criterion may be corrected in place with a dated revision on the node and a re-estimate, as two regime nodes were on 2026-09-19.

The first use of that rule for the tiers was the methodology pass of 2026-09-25 (docs/methodology-pass-2026-09-25.md), the single structural review the outside-model review protocol set aside (docs/reviews/protocol.md, decision 5). John ruled that it counts as the review this rule requires, so its tier changes landed the same day rather than waiting for the January 2027 annual review: Tier 1 is now tested by the hundred-workers node alone, the anti-satellite test ban no longer gates Tier 4, and the Tier 2 and Tier 4 definitions changed their words to match their lists. Each changed list has a structure entry in data/ledger.toml, and the runs on either side are the snapshots 2026-09-25-c5 and 2026-09-25-methodology-pass. A later change to a tier needs a review of its own, and an ordinary quarterly scan is not one. The second such review was the function-over-route pass of the same day (docs/proposal-function-over-route-2026-09-25.md), which John also counted as the review this rule requires: Tier 3's propulsion requirement changed from routine nuclear propulsion to routine fast transit by any propulsion, with a structure entry in data/ledger.toml, and the runs on either side are the snapshots 2026-09-25-methodology-pass and 2026-09-25-sweep-function-over-route.
