# Methodology pass: items 96 to 102 of the outside review (2026-09-25)

Proposed 2026-09-25 by Claude, awaiting John's ruling. This is the single methodology pass that the outside-model review protocol set aside for structural questions (docs/reviews/protocol.md, decision 5: the node review came first, so critique of the tree's shape would not arrive mixed into critique of its numbers). It takes the seven items the 2026-09-19 rulings deferred to it (docs/reviews/2026-09-19-rulings.md, items 96 to 102). All seven were raised by GPT-6 Astra; item 101 was raised in all three of its packets.

What this pull request changes, and what it does not:

- **Item 102 is fixed now.** It was a text contradiction, not a question of structure: the fusion-construction node described itself as something the calibration score could count, and the scoring rule says it cannot. The node's description is reworded (with a dated revision on the node) and docs/methodology.md's scoring rule gains a sentence confirming the rule. No number, status or criterion changed.
- **Items 96 to 101 are proposals only.** What each tier requires, and what each tier's definition says, are structure and John's call; methodology.md lists them as fixed for version one and changed only at a review with a changelog line. Nothing from these six items is applied to data/ or to the definitions here. Each section below gives the change ready to apply, tested on a scratch copy of the tree.

Every recommendation is in the form the ground rule of 2026-09-08 requires (docs/roadmap.md, "Ground rules for every session"): how confident Claude is, whether it is standard practice or a judgment call, and the strongest alternative with what it would cost.

## How the numbers below were made

Each proposed change was applied to a scratch copy of data/ and the tree was played out exactly as a committed snapshot is: 20,000 play-throughs per longevity scenario, seed 2026, world spread 1.0, with the second number (A2 at Tier 1, a rotation at a station or lunar base whether or not a Belt exists) computed from the same play-throughs. The unchanged tree reproduces the reviewed snapshot of 2026-09-20 (`2026-09-20-step-27`) exactly, so every "before" figure below is that snapshot.

The five columns are the five longevity scenarios: the window closing in 2071 (the baseline), 2080, 2095, 2136, and no deadline. Figures are percentages. Because every run uses the same seed, a change that leaves a tier's requirements alone leaves its figure exactly where it was, and a difference of a tenth of a point is real rather than dice. Adding nodes (item 98's alternative) shifts the dice for everything after them, so there, movements under about half a point in tiers the change does not touch are noise.

The tree before any change (snapshot `2026-09-20-step-27`):

| tier | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| Tier 1, outpost | 17.8 | 26.1 | 38.2 | 53.8 | 57.7 |
| Tier 2, settlement | 5.0 | 8.8 | 17.3 | 36.7 | 44.5 |
| Tier 3, Slow Expanse (the Belt exists) | 0.6 | 1.7 | 5.0 | 16.3 | 22.9 |
| Tier 4, Full Expanse | 0.1 | 0.3 | 1.4 | 7.5 | 12.6 |
| A0, contributes from Earth | 14.0 | 21.1 | 30.6 | 39.9 | 40.3 |
| A1, has flown | 35.8 | 48.7 | 64.3 | 77.2 | 81.7 |
| **A2, works off Earth on rotation (headline)** | **0.4** | **1.1** | **3.5** | **10.7** | **14.5** |
| A3, lives off Earth | 0.4 | 1.1 | 3.4 | 10.4 | 14.2 |
| A2 at Tier 1 (the second number) | 5.8 | 10.4 | 18.1 | 27.0 | 29.3 |

## Item 96: living off Earth without first working a rotation

**What the tree does now.** data/tiers.toml:

```toml
[[access_tier]]
key = "A3"
name = "Lives off Earth"
definition = "Permanent residence at an off-world site. Reported beside the headline as the stretch. Requires A2 plus a site that accepts permanent residents; the choice to stay is a future choice point, not a world event."
requires = ["A2", "R-off-earth-site-accepts-permanent-residents"]
```

docs/definitions.md defines A3 as "Permanent residence at an off-world site", with no mention of working a rotation first.

**What the reviewer said.** A3 need not require a prior spell of rotational work; moving straight to an off-Earth site to live is another route.

**Recommendation: the tree change waits for the access-branch review after pipeline graduation (May 2027); a note goes into definitions.md now so the words and the list stop disagreeing silently.** Confidence high that the shape change waits: the access branch is not reviewed before graduation by John's standing rule (protocol, "What is reviewed"), and a direct-migration route needs a new personal node, which is exactly the kind of node that rule holds back, beside the three personal nodes item 29 already sent to that review. Confidence moderate that the note is worth adding now rather than in May 2027. Judgment call. The reviewer is right on the definition: A3 as written in definitions.md does not require A2, and only the requirement list does. The list is a limit of the one route the access branch models (take a rotating job, then stay), and the note says so.

Strongest alternative: add a direct-migration node now (for example, "John holds permanent resident status at an off-Earth site, by any route") and let A3 require it instead of A2. It costs a personal node written before the branch is rebuilt, which is what the standing rule exists to prevent, and it would be rewritten in May 2027 anyway. The other alternative, doing nothing until May 2027, costs nothing in numbers but leaves definitions.md and tiers.toml disagreeing for eight months with no word about it.

**The change, ready to apply** (docs/definitions.md only; the decision-log line at the foot of that document is added on landing, dated the day John rules):

```diff
--- a/docs/definitions.md
+++ b/docs/definitions.md
@@ -27,2 +27,4 @@
 
+In version one the tree counts A3 only for a person who reached A2 first: data/tiers.toml lists A2 among A3's requirements. That is a limit of the one route the access branch models (work a rotation, then stay), not part of what living off Earth means. Someone who moves straight to an off-Earth site to live, without ever holding a job that rotates, lives off Earth too. The direct route is a question for the access-branch review after pipeline graduation (May 2027), with the other access-branch points the outside review raised (methodology pass item 96, docs/methodology-pass-2026-09-25.md).
+
 The codes A0 through A3 are what the tree data uses. Belter-flavored public names for the tiers are a presentation decision, deferred, and can be chosen without touching the tree.
```

The May 2027 shape, for the record and not for now: A3 would require Tier 3, the permanent-residents node, and one new "either route" access node that resolves if John holds a rotating role and stays, or if he emigrates directly (a `depends_on_any` group, as the biology hedge does it).

**Does it move a headline number?** The note: no. To size what the A2 requirement costs A3, the scratch run replaced A2 with Tier 3 in A3's list, which is the most A3 could be if John's own part of a direct move were certain. That is a ceiling, not a proposal:

| tier | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|
| A3, now | 0.4 | 1.1 | 3.4 | 10.4 | 14.2 |
| A3, ceiling without A2 | 0.6 | 1.6 | 4.8 | 15.8 | 22.3 |

Every other tier, the headline and the second number are unchanged. So the most the direct route could ever add to A3 is about a point and a half by 2095, and the real figure would be well under that once John's own part of it has a number.

## Item 97: Tier 1 admits only the lunar route

**What the tree does now.** data/tiers.toml:

```toml
[[system_tier]]
key = "T1"
name = "Outpost"
definition = "Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth."
requires = [
  "L-crew-lands-on-moon-in-reusable-lander",
  "E-fission-reactor-runs-on-lunar-surface",
  "M-hundred-people-working-off-earth-for-pay",
  "R-crewed-lunar-program-outlives-two-changes-of-president",
]
```

**What the reviewer said** (in two packets). The definition permits a permanently crewed station, but the list insists on a reusable lunar lander, a reactor on the Moon and a lunar program that survives two changes of government. That is one development path, not every outpost the definition allows. A hundred people working on commercial stations with no lunar program at all fails Tier 1 while meeting its definition.

**Recommendation: Tier 1 requires the hundred-workers node alone.** Confidence moderate to high. The principle, that a tier's test should admit everything its definition admits, is standard practice; the choice of which node carries the test is a judgment call. The hundred-workers node (`M-hundred-people-working-off-earth-for-pay`) already counts "all stations and surface sites" and asks for a hundred people in paid roles in each of twelve consecutive months, which is the tree's existing reading of "permanent crewed presence". definitions.md made the tiers location-agnostic on purpose on 2026-09-08, so that a station or a rotating habitat counts. The three lunar nodes lose nothing: they still gate Tier 3 through `L-lunar-material-delivered-to-orbit-at-scale`, which depends on all three.

Strongest alternative: an either-route Tier 1. A roll-up node for the lunar route (the three lunar nodes together) and a new node for the station route (for example, "a commercial station is crewed without a break for three years"), with one "outpost by either route" node that the tier requires. It keeps a distinct lunar signal at the bottom of the ladder, at the cost of two new nodes, one new estimate, and a roll-up node that says nothing the hundred-workers node does not already say about a station. Taking neither leaves Tier 1 lunar-only against its own words.

Worth noting for the ruling: the lunar-program node was already widened on 2026-09-19 (the first run read Tier 1 as US-specific), and this change goes one step further by taking it off Tier 1 entirely. That is not reopening the 2026-09-19 ruling, which reworded the node and left the tier list as it was.

**The change, ready to apply:**

```diff
--- a/data/tiers.toml
+++ b/data/tiers.toml
@@ -8,11 +8,12 @@
 name = "Outpost"
 definition = "Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth."
 requires = [
-  "L-crew-lands-on-moon-in-reusable-lander",
-  "E-fission-reactor-runs-on-lunar-surface",
   "M-hundred-people-working-off-earth-for-pay",
-  "R-crewed-lunar-program-outlives-two-changes-of-president",
 ]
+# Methodology pass item 97 (docs/methodology-pass-2026-09-25.md): Tier 1 is location-agnostic, so
+# its test is the location-agnostic headcount node alone. The three lunar nodes (reusable lander,
+# surface reactor, lunar program) left this list; they still gate Tier 3 through
+# L-lunar-material-delivered-to-orbit-at-scale, which depends on all three.
 
 [[system_tier]]
 key = "T2"
```

**Does it move a headline number?** Not the headline. Tier 1 roughly doubles at the short windows, Tier 2 rises by about a third, and the second number rises, because the station route now counts. Tier 3, A2 and A3 do not move at all, since the lunar nodes still gate Tier 3.

| tier | | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|---|
| Tier 1 | before | 17.8 | 26.1 | 38.2 | 53.8 | 57.7 |
| | after | 34.9 | 43.9 | 56.6 | 71.1 | 73.5 |
| Tier 2 | before | 5.0 | 8.8 | 17.3 | 36.7 | 44.5 |
| | after | 6.8 | 11.6 | 21.8 | 44.4 | 53.7 |
| A2 at Tier 1 | before | 5.8 | 10.4 | 18.1 | 27.0 | 29.3 |
| | after | 8.8 | 14.4 | 23.6 | 32.5 | 34.2 |
| Tier 3, Tier 4, A0 to A3 | | unchanged | | | | |

The second number is the one a reader of the home page sees beside the headline, so this is the change a visitor would notice: a rotation at a station or lunar base goes from 5.8 to 8.8 percent by 2071.

## Item 98: no requirement counts the people the tiers promise

**What the tree does now.** The tier definitions in data/tiers.toml name a population at every level: "hundreds of people" (Tier 1), "Thousands living off Earth" (Tier 2), "Tens of thousands off Earth" (Tier 3), "Millions off Earth" (Tier 4). The only headcount any requirement list checks is Tier 1's `M-hundred-people-working-off-earth-for-pay`. Tier 3's list, for example, is:

```toml
requires = [
  "T2",
  "D-permanent-crewed-site-beyond-the-earth-moon-system",
  "D-nuclear-propulsion-in-routine-use",
  "M-off-earth-product-sold-at-a-profit",
  "R-off-earth-resource-rights-recognised-by-major-powers",
  "B-shielding-halves-deep-space-radiation-dose",
  "L-lunar-material-delivered-to-orbit-at-scale",
  "R-space-traffic-management-authority-among-major-powers",
]
```

**What the reviewer said** (in two packets). Every listed requirement can resolve with far fewer people than the words say. It proposed one measure with four thresholds (100 or 200; 1,000 or 2,000; 10,000 or 20,000; 1 or 2 million, each sustained for a year), and a definition of Tier 4's "own political identity".

**Recommendation: say plainly in definitions.md that the headcounts describe each tier and the requirement lists test it; leave counting the people to version two.** Confidence moderate. Judgment call. The reviewer is right that the lists do not count people. The case for leaving it there in version one comes from the founding decision itself: definitions.md sets the headline bar at Tier 3 "because the A2 number (working off Earth on rotation) depends on an outer site with an economy, not on millions of people". The requirements that stand in for the population (a crewed site beyond the Moon, a profitable product, routine nuclear propulsion, cheap launch) are the things the headline actually rests on. A headcount node would be one more late, low-probability node on the chain, estimated only conditionally on the headcount below it, and the tree already multiplies too many of those (item 101).

Strongest alternative: one headcount node per tier from Tier 2 up, at the lower of the reviewer's thresholds (a thousand, ten thousand, a million people off Earth every day for a year), each depending on the one below. The node records are written out in full below with first numbers Claude would propose if John takes this route. It costs three new estimates and it lowers the headline by between an eighth and nearly a third, most at the shorter windows (3.5 to 2.5 percent by 2095), because a Slow Expanse would then have to be populous as well as productive. That is the honest price of the stricter reading, and it may be the right one; it is John's call which of the two a Belt is.

The Tier 4 "own political identity" point is left for the same version-two review; no tier's figure within any window depends on Tier 4.

**The change, ready to apply** (docs/definitions.md only; the decision-log line is added on landing):

```diff
--- a/docs/definitions.md
+++ b/docs/definitions.md
@@ -42,2 +42,4 @@
 
+The headcounts in these definitions (hundreds, thousands, tens of thousands, millions) describe what each tier is expected to look like; they are not what the tree tests. Each tier's test is its requirement list in data/tiers.toml, and the only headcount any list checks is Tier 1's hundred people working off Earth for a year. The other requirements stand in for the population rather than count it: a settlement is tested by closed-loop life support, surgery off Earth and cheap launch; a Slow Expanse by a crewed site beyond the Moon, a profitable product and routine nuclear propulsion. A tier can therefore be reached in the tree with fewer people than its words say. Counting the people directly, one headcount node per tier from Tier 2 up, is a candidate for version two (methodology pass item 98, docs/methodology-pass-2026-09-25.md).
+
 The child-born-off-Earth criterion stays in Tier 2 on purpose. It is the biology factor resolving yes, and it is what separates a settlement from a work camp, even though early settlements may forbid it and so reach it late.
```

**The alternative, ready to apply if John prefers it** (data/tiers.toml and data/M-motive.toml):

```diff
--- a/data/tiers.toml
+++ b/data/tiers.toml
@@ -24,6 +24,7 @@
   "B-long-term-off-earth-living-by-some-route",
   "B-closed-loop-life-support-year-off-earth",
   "B-major-operation-under-anaesthesia-performed-off-earth",
+  "M-thousand-people-living-off-earth-for-a-year",
 ]
 # B-major-operation-under-anaesthesia-performed-off-earth added 2026-09-20 under step 27, item 2
 # (docs/reviews/2026-09-19-rulings.md, ruled 2026-09-19): a settlement cannot evacuate every appendix.
@@ -44,6 +45,7 @@
   "B-shielding-halves-deep-space-radiation-dose",
   "L-lunar-material-delivered-to-orbit-at-scale",
   "R-space-traffic-management-authority-among-major-powers",
+  "M-ten-thousand-people-living-off-earth-for-a-year",
 ]
 # R-space-traffic-management-authority-among-major-powers added 2026-09-20 under step 27, item 20
 # (ruled 2026-09-19): a real gate on tens of thousands in transit. Whether it belongs under Tier 4
@@ -58,6 +60,7 @@
   "D-constant-acceleration-drive-demonstrated",
   "R-binding-ban-on-debris-creating-anti-satellite-tests",
   "B-human-child-born-off-earth",
+  "M-million-people-living-off-earth",
 ]
 
 [[access_tier]]
--- a/data/M-motive.toml
+++ b/data/M-motive.toml
@@ -137,3 +137,65 @@
 estimated_on = 2026-09-20
 rationale = "The satellite insurance market already writes launch and in-orbit cover on commercial landers, and a lunar asset worth insuring at a million a year needs only a commercial lunar operation of any size, which the outpost tier assumes; the residual is that operators self-insure or governments carry the risk for decades. Proposed by Claude 2026-09-20 with the node's addition, accepted by John."
 notes = "Added 2026-09-20 under step 27, item 21 (docs/reviews/2026-09-19-rulings.md, ruled 2026-09-19): raised by Gemini as a missing node; a dependency of M-off-earth-product-sold-at-a-profit."
+
+[[node]]
+id = "M-thousand-people-living-off-earth-for-a-year"
+name = "A thousand people are living off Earth at the same time, every day for a year"
+factor = "M"
+kind = "world"
+description = """
+Tier 2's definition says thousands. The hundred-workers node is the only headcount in the tree,
+and every other Tier 2 requirement could resolve with a few hundred people off Earth. This node
+makes the tier's population a test rather than a picture."""
+resolution = """
+At least one thousand people, residents and workers together and not counting passengers on
+trips shorter than thirty days, are off Earth on every day of one calendar year, counting all
+stations, habitats and surface sites, according to the operators' public crew and resident
+records."""
+source = "Operators' public crew and resident records, tallied"
+horizon = "root"
+depends_on = ["M-hundred-people-working-off-earth-for-pay"]
+status = "open"
+probability = { baseline = 0.45, moderate = 0.55, strong = 0.7, radical = 0.85, open = 0.9 }
+estimated_on = 2026-09-25
+rationale = "Given a hundred paid workers off Earth for a year, a tenfold rise needs residents or a much larger workforce, which only comes with a reason to live there; a little under even odds by 2071. Proposed by Claude 2026-09-25 for methodology pass item 98, for John's ruling."
+
+[[node]]
+id = "M-ten-thousand-people-living-off-earth-for-a-year"
+name = "Ten thousand people are living off Earth at the same time, every day for a year"
+factor = "M"
+kind = "world"
+description = """
+Tier 3's definition, the bar for the headline, says tens of thousands. This node is the tier's
+population as a test: the lower of the two thresholds the outside reviewer proposed."""
+resolution = """
+At least ten thousand people, residents and workers together and not counting passengers on
+trips shorter than thirty days, are off Earth on every day of one calendar year, counting all
+stations, habitats and surface sites, according to the operators' public crew and resident
+records."""
+source = "Operators' public crew and resident records, tallied"
+horizon = "root"
+depends_on = ["M-thousand-people-living-off-earth-for-a-year"]
+status = "open"
+probability = { baseline = 0.3, moderate = 0.4, strong = 0.55, radical = 0.75, open = 0.85 }
+estimated_on = 2026-09-25
+rationale = "Another tenfold rise after the first thousand, at a time when most off-Earth work may be done by machines; below even odds before 2095. Proposed by Claude 2026-09-25 for methodology pass item 98, for John's ruling."
+
+[[node]]
+id = "M-million-people-living-off-earth"
+name = "A million people are living off Earth at the same time"
+factor = "M"
+kind = "world"
+description = """
+Tier 4's definition says millions. The population of a real Belt, as a test."""
+resolution = """
+At least one million people are off Earth on every day of one calendar year, counting all
+stations, habitats and surface sites, according to the operators' or governments' public
+resident records."""
+source = "Operators' and governments' public resident records, tallied"
+horizon = "root"
+depends_on = ["M-ten-thousand-people-living-off-earth-for-a-year"]
+status = "open"
+probability = { baseline = 0.02, moderate = 0.04, strong = 0.1, radical = 0.3, open = 0.5 }
+estimated_on = 2026-09-25
+rationale = "A hundredfold rise from ten thousand is a century's work at the growth rates any city has managed; near zero inside the baseline window. Proposed by Claude 2026-09-25 for methodology pass item 98, for John's ruling."
```

**Does it move a headline number?** The recommendation: no. The alternative:

| tier | | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|---|
| Tier 2 | before | 5.0 | 8.8 | 17.3 | 36.7 | 44.5 |
| | with headcounts | 3.9 | 7.2 | 14.8 | 32.7 | 41.5 |
| Tier 3 | before | 0.6 | 1.7 | 5.0 | 16.3 | 22.9 |
| | with headcounts | 0.4 | 1.3 | 3.7 | 13.0 | 19.7 |
| Tier 4 | before | 0.1 | 0.3 | 1.4 | 7.5 | 12.6 |
| | with headcounts | 0.0 | 0.1 | 0.5 | 4.0 | 8.4 |
| **A2 (headline)** | before | 0.4 | 1.1 | 3.5 | 10.7 | 14.5 |
| | with headcounts | 0.3 | 0.9 | 2.5 | 8.8 | 12.6 |
| A3 | before | 0.4 | 1.1 | 3.4 | 10.4 | 14.2 |
| | with headcounts | 0.2 | 0.8 | 2.4 | 8.6 | 12.4 |

Tier 1, A0, A1 and the second number move by under half a point, which is the shifted dice, not the change.

## Item 99: Tier 2's definition names a child its list no longer requires

**What the tree does now.** data/tiers.toml:

```toml
[[system_tier]]
key = "T2"
name = "Settlement"
definition = "Thousands living off Earth at one or more sites, at least one child born and raised off Earth, partial local self-sufficiency in air, water, and food."
requires = [
  "T1",
  "L-launch-price-below-200-dollars-per-kg",
  "B-long-term-off-earth-living-by-some-route",
  "B-closed-loop-life-support-year-off-earth",
  "B-major-operation-under-anaesthesia-performed-off-earth",
]
# B-human-child-born-off-earth was a Tier 2 requirement until 2026-09-19, when John ruled it moved to
# Tier 4 after the first run showed it capping every tier above Tier 2 (docs/runs/2026-09-19-first-run.md).
# Tier 2's definition still names a child born off Earth; the node remains in the tree and the visual.
```

and Tier 4 requires `B-human-child-born-off-earth`, while Tier 4's definition does not mention a child. docs/definitions.md still says "The child-born-off-Earth criterion stays in Tier 2 on purpose."

**What the reviewer said** (in two packets). Tier 2's definition requires a child born and raised off Earth, but the list does not include the child node; add it back if the definition is kept, and require "raised", not merely born. (The node already requires raising: residence off Earth to age five.)

**Recommendation: the definitions follow the lists.** Tier 2's definition drops the child, Tier 4's gains "children born and raised off Earth", and definitions.md keeps its founding paragraph with a dated amendment beneath it saying why it no longer holds. Confidence high. Judgment call, since the definitions are founding text and John's; but the requirement move itself was ruled by John on 2026-09-19, so this only brings the words into line with a decision already made. Tier 2 is still told apart from a work camp, now by closed-loop life support and by surgery performed off Earth.

Strongest alternative: put the child back into Tier 2's list, as the reviewer offers. It would undo John's 2026-09-19 ruling, which is a decided item, so it is shown only so the price is on the record: Tier 2 falls by more than half at 2071, and the headline falls from 3.5 to 2.5 percent by 2095.

**The change, ready to apply** (data/tiers.toml, definition text and comment only, and docs/definitions.md; the decision-log line is added on landing):

```diff
--- a/data/tiers.toml
+++ b/data/tiers.toml
@@ -17,7 +17,7 @@
 [[system_tier]]
 key = "T2"
 name = "Settlement"
-definition = "Thousands living off Earth at one or more sites, at least one child born and raised off Earth, partial local self-sufficiency in air, water, and food."
+definition = "Thousands living off Earth at one or more sites, partial local self-sufficiency in air, water, and food."
 requires = [
   "T1",
   "L-launch-price-below-200-dollars-per-kg",
@@ -29,7 +29,8 @@
 # (docs/reviews/2026-09-19-rulings.md, ruled 2026-09-19): a settlement cannot evacuate every appendix.
 # B-human-child-born-off-earth was a Tier 2 requirement until 2026-09-19, when John ruled it moved to
 # Tier 4 after the first run showed it capping every tier above Tier 2 (docs/runs/2026-09-19-first-run.md).
-# Tier 2's definition still names a child born off Earth; the node remains in the tree and the visual.
+# Tier 2's definition no longer names the child and Tier 4's does, so the words and the lists agree
+# (methodology pass item 99, docs/methodology-pass-2026-09-25.md).
 
 [[system_tier]]
 key = "T3"
@@ -52,7 +53,7 @@
 [[system_tier]]
 key = "T4"
 name = "Full Expanse"
-definition = "Millions off Earth, transit times in weeks on constant-acceleration drives, a Belt population with its own political identity and economy."
+definition = "Millions off Earth, transit times in weeks on constant-acceleration drives, children born and raised off Earth, a Belt population with its own political identity and economy."
 requires = [
   "T3",
   "D-constant-acceleration-drive-demonstrated",
```

```diff
--- a/docs/definitions.md
+++ b/docs/definitions.md
@@ -36,5 +36,5 @@
 - **Tier 1, Outpost.** Permanent crewed presence at the Moon, Mars, or a permanently crewed station, hundreds of people, fully supplied from Earth.
-- **Tier 2, Settlement.** Thousands living off Earth at one or more sites, at least one child born and raised off Earth, partial local self-sufficiency in air, water, and food.
+- **Tier 2, Settlement.** Thousands living off Earth at one or more sites, partial local self-sufficiency in air, water, and food.
 - **Tier 3, Slow Expanse.** Tens of thousands off Earth, including at least one site beyond the Earth-Moon system (asteroid belt, outer moon, or a habitat out there). Transit times in months. A resource economy where something mined or made off Earth is sold at a profit. Nuclear propulsion in routine use.
-- **Tier 4, Full Expanse.** Millions off Earth, transit times in weeks on constant-acceleration drives, a Belt population, on rocks or in habitats, with its own political identity and economy.
+- **Tier 4, Full Expanse.** Millions off Earth, transit times in weeks on constant-acceleration drives, children born and raised off Earth, a Belt population, on rocks or in habitats, with its own political identity and economy.
 
@@ -44,2 +44,4 @@
 
+AMENDED (methodology pass item 99, docs/methodology-pass-2026-09-25.md). The paragraph above is kept as the founding reasoning; it no longer holds. On 2026-09-19 John moved the child node from Tier 2's requirements to Tier 4's, after the first run showed it capping every tier above Tier 2: a workforce of tens of thousands on rotation could exist at a site where nobody has yet raised a child, and the headline should not wait on one. The child is now the marker of a Full Expanse, a Belt population with families in it, and Tier 2 and Tier 4 above say so. Tier 2 is still told apart from a work camp, by closed-loop life support and by surgery performed off Earth, which are what let people stay rather than rotate.
+
 ## The factors
```

**Does it move a headline number?** The recommendation: no, not by a single play-through; it changes words, not requirements. The alternative, for the record:

| tier | | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|---|
| Tier 2 | now | 5.0 | 8.8 | 17.3 | 36.7 | 44.5 |
| | child back in Tier 2 | 2.1 | 4.3 | 10.1 | 27.9 | 36.3 |
| Tier 3 | now | 0.6 | 1.7 | 5.0 | 16.3 | 22.9 |
| | child back in Tier 2 | 0.4 | 1.1 | 3.4 | 13.6 | 19.8 |
| **A2 (headline)** | now | 0.4 | 1.1 | 3.5 | 10.7 | 14.5 |
| | child back in Tier 2 | 0.2 | 0.7 | 2.5 | 9.1 | 12.8 |

## Item 100: the anti-satellite test ban as a Tier 4 requirement

**What the tree does now.** data/tiers.toml:

```toml
  "L-lunar-material-delivered-to-orbit-at-scale",
  "R-space-traffic-management-authority-among-major-powers",
]
# R-space-traffic-management-authority-among-major-powers added 2026-09-20 under step 27, item 20
# (ruled 2026-09-19): a real gate on tens of thousands in transit. Whether it belongs under Tier 4
# instead is revisited at the methodology pass with item 100 (the anti-satellite treaty under Tier 4).

[[system_tier]]
key = "T4"
name = "Full Expanse"
definition = "Millions off Earth, transit times in weeks on constant-acceleration drives, a Belt population with its own political identity and economy."
requires = [
  "T3",
  "D-constant-acceleration-drive-demonstrated",
  "R-binding-ban-on-debris-creating-anti-satellite-tests",
  "B-human-child-born-off-earth",
]
```

**What the reviewer said.** A treaty banning anti-satellite tests is a diplomatic milestone, not a guarantee of usable orbits: it covers neither wartime attacks nor accidental debris, and a Full Expanse could exist without it. Remove it as a mandatory Tier 4 requirement. The rulings noted that item 20's traffic authority (accepted on 2026-09-19 as a Tier 3 requirement, with its Tier 4 alternative left for this pass) is the stronger candidate for that slot.

**Recommendation, in two parts.**

(a) **The ban leaves Tier 4.** Confidence moderate. Judgment call. The node was placed there as a sign that orbit is treated as shared infrastructure, which is a Full Expanse condition in spirit rather than in logic, and the reviewer is right that the logic does not hold. The node stays in the tree as a tracked event that gates no tier. One tension to rule on: the first founding rule excludes a node for being irrelevant, meaning no tier depends on it. The megawatt radiator node, added 2026-09-20 and gating nothing, is the precedent for keeping one anyway; retiring the ban node is the stricter reading.

(b) **The traffic authority moves from Tier 3 to Tier 4, into the ban's place.** Confidence low to moderate. Judgment call, and the one change in this document that raises the headline, so it deserves the most suspicion. The argument: an authority among the major powers with enforcement over manoeuvres and launch windows is what traffic needs at weeks-long transit on constant-acceleration drives, with millions of people moving. A Slow Expanse (tens of thousands of people, transit in months) adds a few hundred crewed flights a year to an Earth orbit that already carries more than ten thousand working satellites under national licensing and voluntary coordination, with no enforcing authority. Air travel grew to billions of passengers a year on shared standards and national enforcement, never a body with power over every state's aircraft. So enforcement is plausibly a Tier 4 condition, and as a Tier 3 requirement it holds the headline down on something the Belt's existence does not need. The case against: the reviewer who raised it (Gemini, item 20) and Claude's own note on 2026-09-19 both put it in Tier 3, and John accepted that a week ago.

Strongest alternative: part (a) only. The ban leaves Tier 4, the traffic authority stays in Tier 3 as ruled on 2026-09-19, and no headline figure moves. It costs nothing in comparability and keeps a governance gate on the Belt; it keeps the headline down on a condition that, on the argument above, the Belt does not need.

**The change, ready to apply** (parts a and b together):

```diff
--- a/data/tiers.toml
+++ b/data/tiers.toml
@@ -43,11 +43,11 @@
   "R-off-earth-resource-rights-recognised-by-major-powers",
   "B-shielding-halves-deep-space-radiation-dose",
   "L-lunar-material-delivered-to-orbit-at-scale",
-  "R-space-traffic-management-authority-among-major-powers",
 ]
-# R-space-traffic-management-authority-among-major-powers added 2026-09-20 under step 27, item 20
-# (ruled 2026-09-19): a real gate on tens of thousands in transit. Whether it belongs under Tier 4
-# instead is revisited at the methodology pass with item 100 (the anti-satellite treaty under Tier 4).
+# R-space-traffic-management-authority-among-major-powers was added here 2026-09-20 under step 27,
+# item 20 (ruled 2026-09-19), and moved to Tier 4 under methodology pass item 100
+# (docs/methodology-pass-2026-09-25.md): enforcement over manoeuvres is what traffic at weeks-long
+# transit needs, not what a Slow Expanse needs.
 
 [[system_tier]]
 key = "T4"
@@ -56,9 +56,12 @@
 requires = [
   "T3",
   "D-constant-acceleration-drive-demonstrated",
-  "R-binding-ban-on-debris-creating-anti-satellite-tests",
+  "R-space-traffic-management-authority-among-major-powers",
   "B-human-child-born-off-earth",
 ]
+# R-binding-ban-on-debris-creating-anti-satellite-tests left this list under methodology pass
+# item 100: a treaty is a sign of shared orbit, not a condition of a Full Expanse. The node stays
+# in the tree as a tracked event that gates no tier, like the megawatt radiator node.
 
 [[access_tier]]
 key = "A0"
```

The alternative, part (a) alone:

```diff
--- a/data/tiers.toml
+++ b/data/tiers.toml
@@ -56,7 +56,6 @@
 requires = [
   "T3",
   "D-constant-acceleration-drive-demonstrated",
-  "R-binding-ban-on-debris-creating-anti-satellite-tests",
   "B-human-child-born-off-earth",
 ]
 
```

**Does it move a headline number?** Part (a) alone moves only Tier 4, slightly. Parts (a) and (b) together move the Belt and the headline up:

| tier | | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|---|
| Tier 3 | now | 0.6 | 1.7 | 5.0 | 16.3 | 22.9 |
| | (a) and (b) | 0.8 | 2.0 | 5.9 | 18.0 | 24.9 |
| Tier 4 | now | 0.1 | 0.3 | 1.4 | 7.5 | 12.6 |
| | (a) alone, or (a) and (b) | 0.1 | 0.4 | 1.6 | 8.3 | 13.8 |
| **A2 (headline)** | now | 0.4 | 1.1 | 3.5 | 10.7 | 14.5 |
| | (a) and (b) | 0.5 | 1.3 | 4.1 | 11.6 | 15.5 |
| A3 | now | 0.4 | 1.1 | 3.4 | 10.4 | 14.2 |
| | (a) and (b) | 0.4 | 1.3 | 3.9 | 11.3 | 15.2 |

Tier 4 is the same under (a) alone and under (a) and (b), because either way it requires the same set of nodes: the traffic authority reaches Tier 4 through Tier 3 in one case and directly in the other. Tiers 1 and 2, A0, A1 and the second number do not move.

## Item 101: when the parents finished, and causes that move many nodes at once

**What the tree does now.** A node's number is "the chance it happens before the window closes, given that everything it depends on has happened" (docs/node-schema.md, the `probability` field; docs/methodology.md, "The tree"). The world draw (methodology.md, "The world draw") shifts every open node's chance together in each play-through, by one number drawn with a spread of 1.0 on the log-odds scale. Nothing records when a parent happened.

**What the reviewer said** (in all three packets). Two things. First, timing: a parent done in 2035 and one done in December 2070 leave very different room for their child by 2071, and the numbers silently ignore that. Second, shared causes: cheap launch, demand, funding and political continuity move whole branches together, and conditioning on listed parents does not make the rest independent. The reviewer said these could move the headline more than any single number revision.

**Recommendation: state the timing assumption in methodology.md now, in plain words, with the direction it probably errs; build nothing in version one.** Confidence high that stating it is right; it is standard practice to write down an assumption a model makes and cannot yet test. The second point, shared causes, is already handled in the simplest honest way by the world draw, which was worth the difference between 0.5 and 5.6 percent at the headline by 2095 on 2026-09-19; the finer version (correlation by factor, or between named pairs of nodes) is already on the list of known simplifications in docs/node-schema.md and is not repeated here.

Strongest alternative: build the version-two method now (below). It is the right method eventually, but it costs a re-estimate of every node in a new form, while the tree is still changing shape (nine nodes added on 2026-09-20, a tenth, C5, on its way), and it would break comparison with every snapshot so far. The cheaper alternative, doing nothing, leaves an assumption that every estimator (Claude included) has been making by feel unwritten, which is the kind of thing a reader rightly holds against a forecast.

**The change, ready to apply** (docs/methodology.md):

```diff
--- a/docs/methodology.md
+++ b/docs/methodology.md
@@ -28,2 +28,8 @@
 
+## What the numbers assume about timing
+
+A node's number is the chance it happens before the window closes, given that everything it depends on has happened. That condition says nothing about when the parents happened. A parent done in 2035 leaves its child thirty-six years before the 2071 deadline; one done in December 2070 leaves it a few weeks. Every estimate in the tree therefore averages, by the estimator's feel, over when its parents are likely to finish, and nothing in the script checks the averaging.
+
+The assumption version one makes, stated so it can be argued with: each number is read as if the node's parents finish at about the time they typically would, in the worlds where they finish at all. Where that is wrong, it is most likely wrong in one direction. In the play-throughs where a long chain of parents all come true only just before the deadline, the child still gets its full chance, when in the world it would have almost no time left. So the numbers for events at the top of long chains, under the shorter windows, probably lean high, which is the opposite of the lean the world draw corrects. How much is not known. The fix is a different kind of estimate, a spread of completion dates for each node rather than one probability per window, and it is a version-two question, described in docs/methodology-pass-2026-09-25.md under item 101 and not built.
+
 ## What is reported and what is not
```

**Does it move a headline number?** No. It changes no data and no arithmetic.

**The version-two method, described and not built.** Each node would carry a spread of completion dates instead of one chance per window:

1. **What is estimated.** For each node, two things: the chance it ever happens once its parents have (the same kind of number as today's "no deadline" column), and how long it takes after its last parent finishes, given as a middle guess in years and a range (for example, "about 12 years after the lunar lander flies, somewhere between 5 and 30"). A long shot would carry a long, wide lag.
2. **How the tree is played out.** In each play-through, visit nodes in dependency order as now. A node whose parents all happened draws whether it ever happens; if it does, its completion year is the latest parent's year plus a lag drawn from its spread. A tier is reached by a given year when every requirement's completion year falls on or before it.
3. **What comes out.** One curve per tier instead of five separate figures, read at 2071, 2080, 2095 and 2136 and at "ever". The rule that no number may fall as the window lengthens is then true by construction and needs no check. The "run it for yourself" page could read any deadline directly, with no line drawn between two estimated windows. And the tree could state a middle year for the Belt, which it cannot now.
4. **The world draw in that method.** A good world would both raise each node's chance of ever happening and shorten its lag, so that shared causes speed things up as well as make them likelier.
5. **What it costs.** Every node re-estimated in the new form. Today's five numbers could be fitted to a lag spread as a starting point, but that fit would inherit the very assumption it is meant to remove, so each fit would need a person to check it. Snapshots before and after would not be comparable, and the ledger would say so with a structure entry. The site's node pages, which show five figures, would change. And the estimates become less direct to argue with: "12 years after the lander, give or take" is a harder claim for a reader to test than "35 percent by 2071". This is the alternative docs/node-schema.md recorded under decision 3 on 2026-09-08 (one middle year and a spread per node), which John passed over then because five explicit numbers are easier to argue with. That reason still stands until the tree stops changing shape.
6. **When.** Proposed as a design question for an annual review once the tree's shape has held for a year, not before January 2028 on the present pace, and not built until John rules on the design.

## Item 102: nodes that resolved before they were forecast are never scored (fixed in this pull request)

**What the tree did.** docs/methodology.md already said that nodes resolved before their first probability was recorded are not scored. But the description of `E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity` (construction begun on a fusion plant with a signed customer, which happened on 2025-07-30 and was added to the tree on 2026-09-08) ended "The node stays in, resolved, as the first rung on the fusion ladder and a resolved leaf the calibration score can count", which contradicted it.

**What the reviewer said.** A milestone added after it happened cannot count as a successful forecast; a score needs a probability recorded before the event.

**What changed, 2026-09-25.** The description now ends: "The node stays in, resolved, as the first rung on the fusion ladder. It was added in September 2026, after it had already happened, so no forecast was ever on the record for it and the calibration score leaves it out." The change is logged on the node as a revision dated 2026-09-25. methodology.md's scoring rule gains a sentence confirming that any node resolved retrospectively later is unscored, including the recession node and C1 had either been resolved on a past event under items 89 or 90 (John ruled both reworded and kept open instead, so neither is resolved today), and that the test is mechanical: a node is scored only if its record holds a probability dated before its resolution date. No number, status or criterion changed, the tree validates, and there is no ledger entry, since nothing moved.

## Every recommended change at once

Items 97, 99 and 100 (parts a and b) change data/tiers.toml; their diffs apply cleanly in either order (checked). Applied together on a scratch copy:

| tier | | 2071 | 2080 | 2095 | 2136 | open |
|---|---|---|---|---|---|---|
| Tier 1 | now | 17.8 | 26.1 | 38.2 | 53.8 | 57.7 |
| | all recommended | 34.9 | 43.9 | 56.6 | 71.1 | 73.5 |
| Tier 2 | now | 5.0 | 8.8 | 17.3 | 36.7 | 44.5 |
| | all recommended | 6.8 | 11.6 | 21.8 | 44.4 | 53.7 |
| Tier 3 | now | 0.6 | 1.7 | 5.0 | 16.3 | 22.9 |
| | all recommended | 0.8 | 2.0 | 5.9 | 18.0 | 24.9 |
| Tier 4 | now | 0.1 | 0.3 | 1.4 | 7.5 | 12.6 |
| | all recommended | 0.1 | 0.4 | 1.6 | 8.3 | 13.8 |
| **A2 (headline)** | now | 0.4 | 1.1 | 3.5 | 10.7 | 14.5 |
| | all recommended | 0.5 | 1.3 | 4.1 | 11.6 | 15.5 |
| A3 | now | 0.4 | 1.1 | 3.4 | 10.4 | 14.2 |
| | all recommended | 0.4 | 1.3 | 3.9 | 11.3 | 15.2 |
| A2 at Tier 1 | now | 5.8 | 10.4 | 18.1 | 27.0 | 29.3 |
| | all recommended | 8.8 | 14.4 | 23.6 | 32.5 | 34.2 |

The headline moves only through item 100 part (b). Items 96, 98 and 101 change words, not data.

## Landing, once John rules

Whatever John accepts lands in one session: the diffs above applied, a revision or comment dated the landing day, the decision-log lines in definitions.md, a `structure` entry in data/ledger.toml for each changed requirement list (docs/ledger-plan.md: a tier requirement moved breaks comparability and says so), a run with a snapshot, and a CHANGELOG.md line. methodology.md says the tiers and what they require change "only at an annual review with a changelog line", so either the landing waits for the first annual review (due 2027-01-03), or John rules that this pass counts as that review for these items. That timing is the last line below.

## John decides

1. Item 96: add the definitions.md note now and leave A3's route to the May 2027 access review, add a direct-migration node now, or leave both until May 2027.
2. Item 97: Tier 1 requires the hundred-workers node alone, take the either-route form with a new station node, or keep Tier 1 lunar-only.
3. Item 98: record the tier headcounts as descriptions and leave counting to version two, or add the three headcount nodes now with the first numbers given (headline 2.5 percent by 2095).
4. Item 99: move the child from Tier 2's definition to Tier 4's so the words match the 2026-09-19 move, or keep Tier 2's wording and accept that it disagrees with the list.
5. Item 100: take the ban out of Tier 4 and move the traffic authority into its place (headline 4.1 percent by 2095), take the ban out only, or keep both where they are; and whether a ban node that gates no tier stays or is retired.
6. Item 101: add the timing assumption to methodology.md now and hold the completion-date method for a later annual review, amend the wording, or reject it.
7. Timing: land the accepted changes at the annual review due 2027-01-03, or count this pass as a review and land them now.
