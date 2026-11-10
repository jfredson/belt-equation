# Proposal: does a service sold from equipment built off Earth count as an off-Earth economy?

*Written 2026-10-31 by Claude, after John asked what a post by Elon Musk meant for the economic side of the tree; revised the same day after John questioned the rule against rewording published criteria (see "Why not just reword the old node"). Status: agreed in principle by John on 2026-11-09, and revised the same day at his request to carry his three rulings: in-house use counts when the company sells what that computing produces to outside customers; a gate node is added for making working solar cells from off-Earth material; and the first numbers are lowered, so that the route and its gate together sit near 0.10 to 0.40. The revision is listed under "Revised 2026-11-09" below. It lands at the annual review on 2027-01-03; until then nothing in the tree changes. This touches a Tier 3 requirement, so under docs/methodology.md ("Fixed for version one, and changed only at an annual review") it lands at a review: the annual review on 2027-01-03, or earlier if John counts this proposal as the review, as he did for the function-over-route pass on 2026-09-25.*

## What prompted it

On 2026-10-31 Elon Musk [posted on X](https://x.com/elonmusk/status/2116526323938328597) that launching "super intelligence satellites" into deep space with a mass driver on the Moon could add more than a petawatt of capacity a year (a petawatt is a thousand terawatts, about fifty times all the power humanity uses today), and that this would be worth more than Earth's whole economy. A mass driver is an electric track that throws payloads off the Moon without rocket fuel, which works there because the Moon has no air and weak gravity.

The plan, as I read it: build solar-powered computers on the Moon, mostly from lunar material (solar cells, structures and heat radiators make up most of the mass; the chips would come from Earth), throw them into orbit around the Sun, and sell what they compute. Nothing here is happening yet, and the post resolves nothing. What it does is show a gap in how the tree asks its economic question.

## The gap

Tier 3, the bar for the headline, requires an off-Earth economy, tested by the profitable-product node (`M-off-earth-product-sold-at-a-profit`, "Something mined or made off Earth is sold at a profit"). Its criterion asks for revenue from **selling a physical product**, extracted or manufactured off Earth from material mostly, by mass, extracted off Earth, exceeding the product's full cost over a financial year.

Suppose a company builds computing satellites out of lunar material, keeps and operates them, and sells computing time to customers on Earth. That would be a large business resting on off-Earth mining and manufacturing, which is what Tier 3 is reaching for. But no physical product changes hands: the company sells a service, and the hardware stays its own. Read strictly, the node would not resolve. So the first profitable off-Earth industry could arrive without the node meant to catch it noticing.

The tree already has a node for computing in orbit, the paying-customer node (`M-paying-customer-for-work-done-in-orbit`, ten million dollars a year from an outside customer for work done in orbit). It does not close the gap. It counts work done on any equipment, including satellites built on Earth and launched from there, so it says nothing about industry off Earth. It is also a smaller bar (revenue, not profit) and sits below the tiers, not in them.

This is the same kind of fault the function-over-route rule (docs/proposal-function-over-route-2026-09-25.md) was written to fix. That rule says a requirement should name what the tier needs, not one way of getting it. What Tier 3 needs here is an off-Earth industry that pays for itself. Selling a physical product is one way to get there, and selling a service from equipment built off Earth is a second.

## Why not just reword the old node

The first draft of this proposal said the old node could not be reworded because docs/methodology.md forbids changing a published criterion. John asked whether that rule was still right, and it turned out to be only half right. Its stated reason, that the yearly score could not find the forecast, does not hold as long as every change comes with a dated re-estimate. The tree has also reworded three published criteria in place since the site went public. A rewrite is proposed separately (docs/proposal-rewording-rule-2026-10-31.md).

Under either rule, though, this change should not be an edit in place. Counting services as well as products makes the event more likely than the number on record assumed, and it moves toward the outcome the project hopes for. A change like that should be loud, with a new node and a new number, not a quiet edit. So the real choice is between two forms:

- **Add a second route beside the old node** (this proposal: the old node unchanged, plus three new nodes since the revision of 2026-11-09: the route, the either-route node and a gate under the route).
- **Retire the old node and replace it with one wider node** that counts a product or a service, with its own single number (two nodes, the old one marked superseded).

This proposal recommends the first, for three reasons:

1. The two routes differ greatly in difficulty. Making propellant is chemistry, while making working solar cells from lunar soil is something nobody can do yet. One blended number would hide that difference, and two numbers show it.
2. The weekly scan can watch the computing route on its own, so news about lunar manufacturing has a node to land on.
3. The old node keeps going as it is, with its forecast and its meaning, and nothing about it is retired.

The cost is two more nodes than the alternative (the either-route node and, since 2026-11-09, the gate), and a tier list that points at a node with no number of its own. The tree already accepts that cost for the biology hedge and the access branch.

## Revised 2026-11-09

John agreed the proposal in principle on 2026-11-09 and ruled on the three open points. This revision writes them in:

1. **In-house use counts, through outside sales.** A company that runs the equipment for its own work counts when it sells what that work produces to customers not affiliated with it, such as an AI service run on lunar-built satellites. Its own internal prices never count: the revenue in the test is always money from outside customers, so the profit cannot rest on a price the company set for itself. The route node's resolution below says so.
2. **A gate node for working hardware made off Earth.** The whole difficulty of the service route is making working machines from lunar or asteroid material, and the first draft left that to the route node's low numbers. A fourth node, `L-solar-cells-made-off-earth-in-service-for-a-year`, now prices it on its own, and gives the weekly scan a node for news about lunar manufacturing to land on.
3. **Lower first numbers.** The gate and the route are set so that together they sit near 0.10 by 2071 and 0.40 in the open window, the range of the first draft's alternative. With the gate carrying most of the difficulty, the route node given its gates is higher than in the first draft, and the pair together is lower.

## The proposed change

Four parts, in the either-route form the tree already uses for the biology hedge and the access branch.

**1. Keep the profitable-product node exactly as it is.** It becomes one of two routes. Its criterion, number and history are untouched, so its score still works.

**2. Add a second route node:**

```toml
[[node]]
id = "M-service-sold-from-off-earth-built-equipment-at-a-profit"
name = "A service sold from equipment built off Earth turns a profit"
factor = "M"
kind = "world"
description = """
The second way an off-Earth industry can pay for itself: not selling a thing made out there,
but selling what a machine made out there does. Computing time from satellites built on the
Moon is the case that prompted the node; power beamed from arrays built off Earth, or
processing done in a lunar-built factory for an outside customer, would count the same way.
Equipment built on Earth and launched does not count here; that is the paying-customer node."""
resolution = """
A company reports, in audited accounts or an equivalent public filing, that revenue from
selling a service performed by equipment built off Earth, from material mostly, by mass,
extracted off Earth, exceeded the full cost of providing that service over a financial year.
Full cost means all costs the company attributes to the service in its accounts, including
building, launching and wearing out the equipment. Revenue counts only from customers not
affiliated with the company, whether they buy the service itself or something the company
makes with it, such as an AI service run on the equipment, provided the company's accounts
attribute that revenue to the equipment's work; a government customer counts and is disclosed.
Prices the company charges itself or its affiliates never count as revenue."""
source = "The company's audited accounts or equivalent public filing"
horizon = "root"
depends_on = ["L-off-earth-material-delivered-at-scale", "R-off-earth-resource-rights-recognised-by-major-powers", "R-us-and-china-recognise-keep-out-zones-around-off-earth-installations", "M-commercial-insurance-written-on-a-private-lunar-asset", "L-solar-cells-made-off-earth-in-service-for-a-year"]
status = "open"
probability = { baseline = 0.4, moderate = 0.48, strong = 0.55, radical = 0.62, open = 0.68 }
estimated_on = 2027-01-03
rationale = "Given the same supply, rules and insurance the product route needs, and given working solar cells already made off Earth (the gate node, which carries the hardest step), what is left is a business: radiators and structure, which are simpler than cells, chips shipped from Earth, a buyer for the computing, and a cost below building the same machine on Earth and launching it. Placed under the product route because that business case is untested and Earth-built satellites will compete on price the whole way. Revised 2026-11-09 from 0.25 / 0.35 / 0.50 / 0.65 / 0.72, which had carried the manufacturing difficulty before the gate node priced it."
notes = "Proposed 2026-10-31 (docs/proposal-computing-as-off-earth-product-2026-10-31.md) after Elon Musk's post of the same day on lunar-built computing satellites."
```

**3. Add a function node that Tier 3 points at instead of the product node:**

```toml
[[node]]
id = "M-off-earth-industry-turns-a-profit-by-some-route"
name = "An industry built on off-Earth material turns a profit, by either route"
factor = "M"
kind = "world"
description = """
What Tier 3 requires of the economy: a business resting on off-Earth material that pays for
itself, whether it sells a product made out there or a service from equipment built out there.
One node with a name so the tier file stays a plain list."""
resolution = "Either route node it depends on has resolved yes."
source = "The resolving route node's own source"
horizon = "root"
depends_on_any = [["M-off-earth-product-sold-at-a-profit", "M-service-sold-from-off-earth-built-equipment-at-a-profit"]]
status = "open"
probability = { baseline = 1, moderate = 1, strong = 1, radical = 1, open = 1 }
estimated_on = 2027-01-03
rationale = "Resolves whenever either route does; certainty here means the number is carried entirely by the two route nodes, as with the biology hedge."
```

**4. Add a gate node under the service route** (added 2026-11-09):

```toml
[[node]]
id = "L-solar-cells-made-off-earth-in-service-for-a-year"
name = "Solar cells made off Earth from off-Earth material power something for a year"
factor = "L"
kind = "world"
description = """
Making a machine that works out of lunar or asteroid rock is harder than making propellant
from it. Propellant is chemistry; a solar cell needs purified silicon or another semiconductor,
thin layers laid down precisely, and wiring, all made where there is no factory. Solar cells
are the test case because they are most of what a computing or power satellite is made of,
after its structure and radiators, and because work on making them from lunar soil has begun
on Earth. This is the step between mining off Earth and selling what machines built there do."""
resolution = """
Solar cells made at a site off Earth, from material mostly, by mass, extracted off Earth,
deliver at least 100 kilowatts of electrical output, in operation, through a continuous
twelve-month period, confirmed by the operating agency or company with independent
confirmation. Cells made on Earth and assembled off Earth do not count; cover glass, wiring
and other parts shipped from Earth are allowed if the cells' own material is mostly off-Earth
by mass."""
source = "The operating agency's or company's record, with independent confirmation"
horizon = "mid"
depends_on = []
status = "open"
probability = { baseline = 0.2, moderate = 0.3, strong = 0.42, radical = 0.55, open = 0.62 }
estimated_on = 2027-01-03
rationale = "Solar cells have been made from simulated lunar soil in laboratories on Earth, but none has been made off Earth, and a hundred kilowatts in service for a year needs a production line on the Moon or an asteroid, not a demonstration. Set well under the first tonne of propellant made off Earth (0.50 by 2071), because a semiconductor line is a harder thing to run remotely than a chemical plant."
notes = "Proposed 2026-11-09 as a gate under M-service-sold-from-off-earth-built-equipment-at-a-profit (docs/proposal-computing-as-off-earth-product-2026-10-31.md), at John's ruling that the service route's manufacturing step needs a node of its own."
verify = ["Solar cells have been made from simulated lunar soil in laboratories on Earth (the rationale's claim, written from memory on 2026-11-09). Lead found 2026-11-09: secondary reports (Space.com, Universe Today) say Blue Origin announced on 2023-02-10 that its Blue Alchemist process made working solar cells from lunar soil simulant; Blue Origin's own page (https://www.blueorigin.com/news/blue-alchemist-powers-our-lunar-future) refused the request that day, so the claim is not yet confirmed against the primary record."]
```

Taken together, the gate and the route give the service route about 0.08 / 0.14 / 0.23 / 0.34 / 0.42 given the four gates it shares with the product route, against the product route's 0.65 to 0.95. The first draft's alternative asked for 0.10 to 0.40.

The Tier 3 list in data/tiers.toml swaps `M-off-earth-product-sold-at-a-profit` for `M-off-earth-industry-turns-a-profit-by-some-route`, with a structure entry in data/ledger.toml naming this proposal.

**Words that follow the change.** Each of these says "sold at a profit" about Tier 3 and would read:

- data/tiers.toml, the Tier 3 definition, and docs/definitions.md, the Tier 3 line: "Something mined or made off Earth, or a service from equipment built off Earth, sold at a profit."
- docs/definitions.md, the paragraph on headcounts: "a profitable product" becomes "a profitable off-Earth industry".
- The public About page (site/src/components/AboutMethod.astro): "something made out there sold at a profit" becomes "a business built from material out there that pays for itself".

## Each choice, with confidence and the strongest alternative

| Choice | Confidence | Standard or judgment | Strongest alternative, and its cost |
|---|---|---|---|
| A service from equipment built off Earth should count toward Tier 3 at all | **High.** Tier 3's own words describe "a resource economy", and a lunar factory selling computing time is one by any plain reading. | Judgment, but it follows the tree's own function-over-route rule. | Rule that Tier 3 means trade in physical goods only, and say so in definitions.md. Cheap, but the tree could then show no off-Earth economy in a world where the largest business off Earth was running. |
| Add a route node and an either-route node, rather than reword the old node | **Moderate to high.** Rewording in place is ruled out on its merits, because the change loosens toward the hoped-for outcome (see "Why not just reword the old node"). Two routes beat one blended number because their difficulty differs so much. | Standard for this tree: it already uses this form for the biology hedge and the access branch. | Retire the product node and replace it with one wider node that counts a product or a service. Two nodes instead of three and a plainer tier list, at the cost of one number that hides how far apart the two routes are. |
| The equipment must be mostly off-Earth material by mass | **Moderate.** It matches the product node's test and stops Earth-built satellites with a lunar bolt from counting. It lets chips come from Earth, which is right, since they are light. | Judgment, copied from the existing node. | Count value instead of mass (most of the equipment's cost from off-Earth manufacturing). Closer to "industry" in spirit, but hard to check from accounts, since costs are not broken out that way. |
| Revenue counts only from customers not affiliated with the company, but includes what the company sells them that it made with the equipment (ruled by John 2026-11-09) | **Moderate.** It catches the likeliest first case, a builder running its own AI and selling the result, and still never counts a price the company sets for itself. The cost: the revenue has to be attributed to the equipment in the company's accounts, which is a judgment the company makes. | Judgment; the outside-customer half is standard accounting caution and the paying-customer node already uses it. | Count outside sales of the service only, as the first draft did. Simpler to audit, but it would probably miss the first real case. |
| The four gates of the product route, plus a fifth: solar cells made off Earth in service for a year (the gate added 2026-11-09, at John's ruling) | **Moderate.** The gate puts the hardest step where it can be watched and priced on its own. Solar cells stand for all the hardware because they are the hardest part of it that is made in bulk. | Judgment; the propellant node is the same kind of gate for the product route. | Leave the gate out and let the route node's low numbers carry it, as the first draft did. One node fewer, but the hardest step would have no number and no place for news to land. |
| The gate's bar: 100 kilowatts of off-Earth-made cells in service for a year | **Low to moderate.** It is far past a laboratory demonstration and short of a factory's output, the same place the propellant node's first tonne sits. | Judgment. | A smaller bar, such as one kilowatt, which resolves sooner and records the first success, but says little about whether a business can be built on it. |
| First numbers: the gate 0.20 / 0.30 / 0.42 / 0.55 / 0.62, the route given its gates 0.40 / 0.48 / 0.55 / 0.62 / 0.68, about 0.08 to 0.42 together (revised 2026-11-09) | **Low.** There is no record to reason from: nobody has made a working machine from lunar material. Together they sit inside the 0.10 to 0.40 range John chose. | Judgment, for John to accept or move at the review. | Put more of the difficulty on the route and less on the gate. The pair would come out the same, but the gate would then promise more than the business case behind it. |
| Land at the annual review on 2027-01-03, not now | **Moderate.** Nothing in the world has moved, so there is no rush; a tier change waits for a review unless you rule otherwise. | Standard under docs/methodology.md. | Count this proposal as the review and land it now, as with the 2026-09-25 passes. Quicker, but it uses up the exception for a change that no event is waiting on. |

On reflection I would change one thing myself if you wanted a smaller change: the gate question. Leaving out a node for "making working hardware off Earth" is the weakest part, because the whole difficulty of the service route lives there. I have kept it out to keep the change small, not because it is right.

## What happens to the numbers

Adding a second route can only raise Tier 3 and the headline, because "either happens" is never less likely than one of them. The rise should be small, because both routes share the same four gates and the new route is placed well under the old one. Most of its chance falls in play-throughs where the product route has already succeeded. The run that lands this gets its own snapshot and a structure entry in the ledger, and the changelog names this proposal.

## Not covered here

The post also shows a second, larger gap, which this proposal does not try to fix. Musk's future is mostly robots: a robot factory throwing robot satellites into orbit. It could make the economic and energy parts of the tree look strong while the people parts stay weak. Tier 3 still needs tens of thousands of people off Earth in its words, but the tree tests that only indirectly (docs/definitions.md, the paragraph on headcounts), and an outside model made the same point on 2026-09-20: computing, manufacturing and mining need few workers in space. Counting people directly is already a candidate for version two (methodology pass item 98). This post is a reason to move that candidate up, not a change to make now.

## What John decides

Decided on 2026-11-09: that a service from equipment built off Earth counts toward Tier 3; the either-route form; that in-house use counts through outside sales; that the service route gets its own gate for making hardware off Earth; and that the first numbers sit near 0.10 to 0.40; and that the change lands at the annual review on 2027-01-03. Left for the review:

1. The gate's bar (100 kilowatts for a year) and its numbers, and the route's numbers given its gates.
2. The mass test and the attribution of revenue to the equipment in the company's accounts, as worded in the route node.
3. The gate's one claim to check (solar cells made from simulated lunar soil on Earth). A lead is recorded in the node's `verify` line; Blue Origin's own page could not be opened on 2026-11-09, so it is confirmed before the review if that page answers, and the node goes in with its record linked.
