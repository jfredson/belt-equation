# Proposal: when a published criterion may be reworded, and when the node must be retired and replaced

*Written 2026-10-31 by Claude, after John asked whether the rule against rewording published criteria was still the right one ("No requirement should be blindly followed without reviewing if it is still the correct way to do things"). Status: proposed. docs/methodology.md is unchanged until John rules. The scoring rule and what is fixed for version one are changed only at an annual review, so this lands at the review on 2027-01-03 unless John counts the proposal as the review. It came up beside the computing proposal (docs/proposal-computing-as-off-earth-product-2026-10-31.md), which follows the rule in either form.*

## The rule today

docs/methodology.md, "What is fixed and what moves":

> Never changed once a probability has been published against it: a node's id and its criterion, so that the score can always find the forecast it is scoring; a node that needs a different criterion after publication is retired and replaced. Before publication, a criterion may be corrected in place with a dated revision on the node and a re-estimate, as two regime nodes were on 2026-09-19.

## What is wrong with it

**1. Its stated reason is weaker than it reads.** The yearly score (`scored_resolutions` in scripts/compute.py) looks only at dates. It takes the number on record before the node resolved and never checks which wording that number was estimated for. So if a criterion is reworded and the number is re-estimated the same day, with a dated revision, the score still finds a forecast, and it is the right one. The score goes wrong only when wording changes without a new estimate, because then a number estimated for the old question is scored against the new one. Recording a re-estimate with every change prevents that, without forbidding the change.

**2. The tree has not kept to it.** The site has been public since 2026-09-20. Since then:

| Date | Node | What changed | How it was handled |
|---|---|---|---|
| 2026-09-25 | Crew round trip to Mars | Widened to any destination beyond the Earth-Moon system | Retired and replaced, citing this rule |
| 2026-09-25 | A crewed lunar programme outlives two changes of president | Widened to government or commercial programmes and any backer | Retired and replaced, citing this rule |
| 2026-09-25 | Staple crop grown off Earth (the year of recycled food, water and air) | "Grown on site" widened to "produced on site from raw inputs", so that cultured or fermented food counts | Reworded in place, numbers unchanged |
| 2026-10-03 | High-thrust, high-exhaust-speed engine fires in space | "Fusion-powered" dropped to "whatever powers it" | Reworded in place, numbers unchanged |
| 2026-10-03 | Permanent crewed site beyond the Earth-Moon system | "Farther than the Moon's orbit" changed to "at least five million kilometres from Earth" | Reworded in place, numbers unchanged |

(The five 2026-09-25 rewordings of the access-branch nodes that named John's career are left out: they changed how the criteria are worded in public, not what they mean.)

Each in-place change argued that no number moved, because the number had already been estimated for the new meaning. That is a sensible exception, and the tree has been using it without writing it down.

**3. It does not name the real danger.** The strongest reason to retire and replace is not the score. Widening a criterion toward the outcome you hope for is the easiest way to fool yourself, and it is the same danger the Contact Clause null rule guards against. Retire-and-replace makes such a change loud: a new node, a new number, the old one standing beside it. An edit in place makes it quiet. Today's rule protects against that only by accident, and only if it is followed strictly, which it has not been.

## The proposed rule

To replace the passage above:

> **Rewording a criterion after publication.** A node's id never changes once a probability has been published against it. Its criterion may change in one of two ways, and the revision on the node says which, and why.
>
> 1. **A correction, in place.** Allowed when the number on record was already estimated for the new reading, so that rewording does not move it: a drafting slip, a boundary that admitted cases nobody meant to count, a clause left over from a dependency that has since changed. The revision carries a dated re-estimate, stating the number even if it is unchanged, so the score scores the number against the wording it was estimated for.
> 2. **A change of meaning: retire and replace.** Required when the new reading would move the number if it were estimated honestly. The old node is marked superseded and keeps its number and history; a new node carries the new criterion and its own first estimate.
>
> A rewording that makes the event easier, so that it moves toward the outcome the project hopes for, is assumed to be a change of meaning unless its revision shows the number already covered the looser reading. It is named in the changelog either way. Before publication, a criterion may be corrected in place with a dated revision and a re-estimate, as two regime nodes were on 2026-09-19.

docs/node-schema.md's line on `id` ("Never renamed once a probability has been recorded against it; retire it with `status = "superseded"`") stays as it is, because it is about ids, which this rule keeps fixed.

## The three in-place changes, read against the proposed rule

- **The deep-space site boundary (2026-10-03):** a correction. The old wording could be read to admit a lunar site, and the numbers had been estimated for Mars or farther. It passes.
- **"Whatever powers it" on the drive (2026-10-03):** a correction, though a loosening. "Fusion-powered" was added on 2026-09-19 only so the wording matched a dependency that later widened, and the thresholds and numbers were estimated for the engine, not its power source. The revision says so, so it passes with the reason the new rule asks for.
- **The staple crop (2026-09-25):** this one fails. Counting cultured and fermented food makes the event itself more likely than when only crops counted, and the revision says the numbers were left unchanged only because no second route is drawn in the tree yet. Under the proposed rule it should have been retired and replaced, or re-estimated. Recommended handling: re-estimate it at the December sittings, and record that re-estimate as the number for the widened wording. Retiring it now, a month later, would add a node for little gain, because it has not resolved and its old number is still on the record.

## Each choice, with confidence and the strongest alternative

| Choice | Confidence | Standard or judgment | Strongest alternative, and its cost |
|---|---|---|---|
| Allow corrections in place, each with a dated re-estimate | **High.** It is what the tree already does, and the score handles it correctly given the dated re-estimate. | Standard: forecasting sites fix wording in place when the meaning does not change. | Keep the strict rule and retire every reworded node. Clean on paper, but the tree fills up with retired nodes for wording slips, and the rule stays one the project does not keep. |
| The test is whether an honest estimate of the new reading would move the number | **Moderate.** It is a judgment each time, and the person judging is the one who wants the change. The changelog line and the assumption against loosening are there to check that. | Judgment. | A mechanical test: any change to the resolution text is a retirement. Nothing to judge, but it treats a typo fix like a new question. |
| A loosening is assumed to be a change of meaning unless shown otherwise | **High.** It points the burden of proof at the direction where self-deception happens. | Judgment, in the spirit of the Contact Clause null rule. | Treat loosening and tightening alike. Simpler, but it drops the one guard this rule most needs. |
| Re-estimate the staple crop in December rather than retire it | **Moderate.** The node is far from resolving, so the record can be made right by a dated number without a new node. | Judgment. | Retire and replace it now, to apply the new rule strictly from the start. Cleaner, at the cost of one more retired node and a new id on the site. |

On reflection, the second row is the one I would watch. If the December sittings or the annual review find that "would it move the number" is being answered too easily, the mechanical alternative is the fallback.

## What John decides

1. Adopt the rewritten rule, amend it, or keep the strict rule (and say what happens to the three in-place changes).
2. Whether a loosening carries the burden of proof, as written.
3. The staple crop: re-estimate in December, or retire and replace.
4. Whether this lands at the annual review on 2027-01-03 or now.
