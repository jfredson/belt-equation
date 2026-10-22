# The spending record: what The Belt Equation spends, and the go it was spent under

*Started 2026-10-21, for the Missions page's daily launch-day check, under the workspace rule on the
monthly API credits (`~/Code/CLAUDE.md`, "Anthropic API credits: the monthly $200";
`timeassembler/docs/session-routing.md`, rule 3): a credit-paid job expected to cost more than about
$50 comes to John first; smaller credit-paid runs do not need his go, and each is recorded here with
the vendor written "Anthropic credits". Spend out of pocket always needs his go first. Before this
file the project spent nothing outside the plan: the weekly scan runs in a session on the plan.*

## Standing jobs

| Job | Vendor | Since | Estimate | Ceiling | Go |
|---|---|---|---|---|---|
| The daily launch-day check (`scripts/missions_watch.py`, `scripts/launchd/README.md`) | Anthropic credits (the `weekly-readings` workspace key) | 2026-10-21 | about $5 a month on average; about $20 to $30 in the busiest month | stop and ask John if any month passes $50 | John, 2026-10-21: switch it on if under about $50 a month. Switched on 2026-10-21, then off the same evening before a restart of the Mac; off until John says to switch it on again |

**How the estimate was made (2026-10-21).** One test run on 2026-10-21 checked one milestone (Hera's
second braking burn) with three web searches and cost $0.36: 76,469 input tokens and 1,328 output
tokens at $4 and $20 per million, plus $0.03 for the searches (prices read that day from
https://platform.claude.com/docs/en/about-claude/pricing.md). Counted day by day over the two years
from 2026-10-22 against the milestones as they stood, the check would call the API on about 220 days
and look at about 320 milestones in all, about $0.35 to $0.45 each: about $130 over two years, or
about $5 a month. The busy months are those where a milestone is dated only to a month, since the
check then looks every day of it: November 2026 (Hera's arrival, Starship's fifteenth flight; about
46 milestone checks, about $18) and September 2027 (MMX and ESCAPADE at Mars, Lucy's flybys; about 74,
about $30). Most months cost nothing. The actual cost of each run is in
`~/Library/Logs/belt-missions-watch.csv` on the Mac, which the month-end credits sweep adds up here.

## Runs

| Date | What | Vendor | Cost | Source |
|---|---|---|---|---|
| 2026-10-21 | Test run of the daily check, one milestone, three searches | Anthropic credits | $0.36 | `~/Library/Logs/belt-missions-watch.csv` |
