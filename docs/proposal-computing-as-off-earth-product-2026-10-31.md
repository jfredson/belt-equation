# Proposal: does a service sold from equipment built off Earth count as an off-Earth economy?

*Written 2026-10-31 by Claude, after John asked what a post by Elon Musk meant for the economic side of the tree; revised the same day after John questioned the rule against rewording published criteria (see "Why not just reword the old node"). Status: proposed. Nothing in the tree changes until John rules. This touches a Tier 3 requirement, so under docs/methodology.md ("Fixed for version one, and changed only at an annual review") it lands at a review: the annual review on 2027-01-03, or earlier if John counts this proposal as the review, as he did for the function-over-route pass on 2026-09-25.*

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

- **Add a second route beside the old node** (this proposal: three nodes, the old one unchanged).
- **Retire the old node and replace it with one wider node** that counts a product or a service, with its own single number (two nodes, the old one marked superseded).

This proposal recommends the first, for three reasons:

1. The two routes differ greatly in difficulty. Making propellant is chemistry, while making working solar cells from lunar soil is something nobody can do yet. One blended number would hide that difference, and two numbers show it.
2. The weekly scan can watch the computing route on its own, so news about lunar manufacturing has a node to land on.
3. The old node keeps going as it is, with its forecast and its meaning, and nothing about it is retired.

The cost is one more node than the alternative, and a tier list that points at a node with no number of its own. The tree already accepts that cost for the biology hedge and the access branch.

## The proposed change

Three parts, in the either-route form the tree already uses for the biology hedge and the access branch.

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
affiliated with the company; a government customer counts and is disclosed. A company using
the equipment for its own work earns nothing under this test, because there is no sale to
measure."""
source = "The company's audited accounts or equivalent public filing"
horizon = "root"
depends_on = ["L-off-earth-material-delivered-at-scale", "R-off-earth-resource-rights-recognised-by-major-powers", "R-us-and-china-recognise-keep-out-zones-around-off-earth-installations", "M-commercial-insurance-written-on-a-private-lunar-asset"]
status = "open"
probability = { baseline = 0.25, moderate = 0.35, strong = 0.5, radical = 0.65, open = 0.72 }
estimated_on = 2027-01-03
rationale = "Given the same supply, rules and insurance the product route needs, this route still needs working solar cells and radiators made from lunar or asteroid material, which nobody can do today, where the product route's likeliest case is propellant, chemically much simpler. Placed well under the product route for that reason."
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
| Revenue counts only from customers not affiliated with the company | **Moderate.** Without it a company could sell to itself at any price and show a profit. The cost: the likeliest first user is the builder running its own AI, which this test does not count. | Standard accounting caution; the paying-customer node already uses it. | Count affiliated sales, disclosed, as the product node does for government buyers. Catches the in-house case sooner, but the profit figure would then rest on a price the company set for itself. |
| Same four gates as the product route | **Moderate.** Both routes need material at scale, the right to keep what you mine, safe zones and an insurable asset. The service route arguably also needs a way to make working hardware off Earth, and the tree has no node for that. | Judgment. | Add a gate node, "working solar cells made off Earth from off-Earth material". More honest about the extra step, but a fourth new node and a new number. I would leave it out for now and let the route node's low numbers carry it; flag if you disagree. |
| First numbers 0.25 / 0.35 / 0.50 / 0.65 / 0.72, given the gates | **Low.** There is no record to reason from: nobody has built a working machine from lunar material. They sit well under the product route (0.65 to 0.95) because making solar cells is much harder than making propellant. | Judgment, a first proposal for you to accept or move. | Start lower, around 0.10 to 0.40, to match how far today's technology is from this. The headline would then barely move, which may be the more honest result. |
| Land at the annual review on 2027-01-03, not now | **Moderate.** Nothing in the world has moved, so there is no rush; a tier change waits for a review unless you rule otherwise. | Standard under docs/methodology.md. | Count this proposal as the review and land it now, as with the 2026-09-25 passes. Quicker, but it uses up the exception for a change that no event is waiting on. |

On reflection I would change one thing myself if you wanted a smaller change: the gate question. Leaving out a node for "making working hardware off Earth" is the weakest part, because the whole difficulty of the service route lives there. I have kept it out to keep the change small, not because it is right.

## What happens to the numbers

Adding a second route can only raise Tier 3 and the headline, because "either happens" is never less likely than one of them. The rise should be small, because both routes share the same four gates and the new route is placed well under the old one. Most of its chance falls in play-throughs where the product route has already succeeded. The run that lands this gets its own snapshot and a structure entry in the ledger, and the changelog names this proposal.

## Not covered here

The post also shows a second, larger gap, which this proposal does not try to fix. Musk's future is mostly robots: a robot factory throwing robot satellites into orbit. It could make the economic and energy parts of the tree look strong while the people parts stay weak. Tier 3 still needs tens of thousands of people off Earth in its words, but the tree tests that only indirectly (docs/definitions.md, the paragraph on headcounts), and an outside model made the same point on 2026-09-20: computing, manufacturing and mining need few workers in space. Counting people directly is already a candidate for version two (methodology pass item 98). This post is a reason to move that candidate up, not a change to make now.

## What John decides

1. Whether a service from equipment built off Earth counts toward Tier 3, or Tier 3 means physical goods only (in which case definitions.md should say so).
2. If it counts: the either-route form above, or retiring the product node and replacing it with one wider node. Either works under the current rule or the rewritten one (docs/proposal-rewording-rule-2026-10-31.md).
3. The three tests in the new node: mass, outside customers only, and the same four gates. Also whether to add a gate for making working hardware off Earth.
4. The first numbers for the new route.
5. Whether this lands at the annual review on 2027-01-03, or now under the 2026-09-25 precedent.
