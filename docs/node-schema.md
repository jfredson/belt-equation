# Node schema and data format

Drafted 2026-09-08 (roadmap step 2) and DECIDED the same day: Claude proposed six choices with confidence levels and alternatives, changed two of them on reflection (the choice-point default and where the habitat hedge lives), and John accepted the amended set. The decisions and the known simplifications are recorded at the end. This document is the source of truth for the record layout, and the compute script refuses any file that does not follow it.

## What a node is

A node is one breakthrough, event, or decision that the tree tracks. It has a name anyone can read, a criterion that says exactly what would count as it having happened, and a place in the tree (its factor, and what it depends on). Later it gets a probability. A node without a resolution criterion is not a node.

Two kinds of node exist. A **world event** is something that happens to the world (a launcher flies a hundred times in a year; a child is born off Earth). A **choice point** is something John decides (re-enlist or separate at the six-year mark). The tree is sampled for world events and forced for choice points, which is how the decision comparison works: run the whole tree once per option and compare.

## File format and layout

TOML, one file per factor, read by Python's standard library (`tomllib`, present since Python 3.11; the Mac has 3.14). TOML is plain text, allows comments, keeps each field on its own line so a change to one number shows as a one-line diff, and supports multi-line text for descriptions and rationales. The alternative was JSON, which the standard library also reads but which has no comments and diffs badly for prose.

    data/
      scenarios.toml      the four longevity scenarios and their window years
      tiers.toml          the system tiers and access tiers, each as the set of nodes it requires
      W-window.toml       nodes under the window factor
      L-launch.toml       nodes under launch
      E-energy.toml       nodes under energy
      D-drive.toml        nodes under drive
      B-biology.toml      nodes under biology
      M-motive.toml       nodes under motive
      R-regime.toml       nodes under regime
      A-access.toml       nodes under access (a sketch until pipeline graduation; nothing personal)
      C-contact.toml      the Contact Clause rungs, beside the equation and never multiplied into it

Each factor file is a list of `[[node]]` tables. Ids must be unique across all files.

## The node record

Required fields are marked. Everything else may be left out until it is known.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable identifier: the factor letter, a dash, then a short lowercase slug with dashes, like `L-heavy-launcher-100-per-year`. The Contact Clause rungs use `C1` to `C4`, which are already their names. Never renamed once a probability has been recorded against it; retire it with `status = "superseded"` and point to the replacement instead. |
| `name` | yes | Plain-language name, one line, readable by someone outside the project. |
| `factor` | yes | One of `W`, `L`, `E`, `D`, `B`, `M`, `R`, `A`, `C`. Must match the file it lives in. |
| `kind` | yes | `"world"` (happens to the world) or `"choice"` (John decides). |
| `description` | yes | Two or three sentences on what the breakthrough is and why it matters to the tree. |
| `resolution` | yes | The observable event that counts as "resolved yes", stated so that two people reading it would agree whether it has happened. |
| `source` | yes | Who or what settles it: a named public record, database, or announcement type. "Common knowledge" is not a source. |
| `horizon` | yes | `"leaf"` (could resolve within 1 to 5 years), `"mid"` (5 to 20 years), or `"root"` (window-scale). At least a third of all nodes should be leaves. |
| `depends_on` | no | List of ids that must all resolve before this node can. Empty or absent means no dependencies. |
| `depends_on_any` | no | List of groups, each a list of ids; at least one id in every group must resolve before this node can. This is how a node says "by either route", for example the biology node that resolves if partial-gravity health works out or if a rotating habitat with Earth-normal gravity exists. |
| `choice_group` | choice only | Name shared by the mutually exclusive options at one choice point, such as `"six-year-fork"`. The decision comparison forces exactly one node in a group to yes per run. |
| `current_plan` | choice only | `true` on exactly one node in each choice group: the option John currently intends to take. The headline number is computed with every choice group set to its current plan, and the decision comparison reports how much each alternative moves it. |
| `probability` | from Phase 3 | Table with one entry per scenario key from scenarios.toml: `{ baseline = 0.6, moderate = 0.65, strong = 0.7, open = 0.8 }`. Each number is the probability that the node resolves yes before that scenario's window, **given that its dependencies resolve**. Absent until the tree is stable. Choice nodes have no probability. |
| `estimated_on` | with probability | Date (YYYY-MM-DD) of the current probability. |
| `rationale` | with probability | One line on why the number is what it is. |
| `status` | yes | `"open"`, `"resolved-yes"`, `"resolved-no"`, or `"superseded"`. |
| `resolved_on` | if resolved | Date it resolved. |
| `resolved_by` | if resolved | The specific record that settled it (a link or citation). |
| `superseded_by` | if superseded | Id of the replacement node. |
| `revisions` | no | List of `{ date, field, old, new, why }` tables, newest last, one per change to any field after the node's first commit. Probability changes always get one. |
| `notes` | no | Anything else worth keeping with the node. |

### What is not in the record

- **Which tiers the node feeds.** This is not stored on the node. It lives in `tiers.toml`, where each tier lists the nodes it requires, and the compute script can print it per node. Storing it in both places is how the two drift apart. (The roadmap listed "which tiers it feeds" as a node field; this proposal moves it.)
- **A single probability.** Every probability is per scenario, because the window is what changes between scenarios. A node whose number is the same in every scenario just repeats it four times, and that repetition is information.
- **John's health.** The window factor's nodes are about longevity research in general. The refined window date lives in `scenarios.toml` as a year with a plus-or-minus and nothing more.

## How the pieces fit

**Dependencies.** A node cannot resolve unless every id in `depends_on` resolved. Its probability is conditional on that, which is the number a person can actually estimate ("if we have cheap launch, how likely is orbital manufacturing at scale by 2070?"). The compute script samples nodes in dependency order and refuses to run if there is a cycle. A leaf that depends on a root is a sign the horizon classes are wrong.

**Tiers.** `tiers.toml` defines each system tier (1 to 4) and access tier (A0 to A3) as a set of required nodes and lower tiers, all of which must resolve. A run reaches a tier when its requirements are met. The headline number is how often A2 is reached; Tier 3 is the bar for "the Belt exists". "Either of these" logic does not live in the tier file; it lives on nodes, through `depends_on_any`. The rotating-habitat hedge on biology is therefore one biology node, "humans can live off Earth long term by some route", which resolves if either the partial-gravity route or the habitat route does, and the tiers require that node. It gets a name, a probability of its own, and a place in the visual, and the tier file stays a plain list.

**Scenarios.** `scenarios.toml` lists the four longevity scenarios with a key, a plain name, and the window year (or none, for escape velocity). The compute script runs the whole tree once per scenario and reports each separately. How the window factor's own nodes weigh the scenarios against each other is a methodology question for step 12, not a schema question; the file leaves room for a weight per scenario and does not fill it.

**Choice points.** Nodes with `kind = "choice"` are never sampled. In an ordinary run, every choice group is set to its `current_plan` option, so the headline is the forecast for the path John currently intends, not for a person who never decides anything. In the decision comparison, the script takes one choice group at a time, forces each of its options to yes in turn with the others no, runs the tree, and reports how far each alternative moves the headline from the current plan. The difference between the runs is the value of the decision.

**The Contact Clause.** `C-contact.toml` follows the same schema so the rungs get criteria, probabilities, and revisions like everything else, but no tier requires a C node and the script reports them in their own section, never multiplied into the headline.

## Worked example: the first real node

This node lives in `data/L-launch.toml` and is the one the compute script is first written against.

    [[node]]
    id = "L-heavy-launcher-100-per-year"
    name = "A fully reusable heavy launcher flies 100 orbital missions in one calendar year"
    factor = "L"
    kind = "world"
    description = """
    Launch cost is set less by the rocket than by how often the same rocket flies.
    A fully reusable heavy launcher (both stages recovered and reflown) reaching
    a hundred orbital flights in a single year is the point at which mass to orbit
    stops being the constraint on everything downstream: stations, habitats, and
    lunar supply all assume it."""
    resolution = """
    In one calendar year, a launch vehicle whose first and second stages are both
    designed for recovery and reuse completes at least 100 orbital launches, counting
    only flights that reached orbit. Test flights that reached orbit count; suborbital
    flights and failures do not."""
    source = "Public orbital launch logs, checked against the operator's own flight manifest"
    horizon = "leaf"
    depends_on = []
    status = "open"
    notes = "Written 2026-09-08 as the schema's worked example. Probability comes in Phase 3."

A choice-point node, for illustration only (the access branch stays a sketch until pipeline graduation, and this one is not yet in the data):

    [[node]]
    id = "A-reenlist-at-six-years"
    name = "Re-enlist at the six-year mark"
    factor = "A"
    kind = "choice"
    choice_group = "six-year-fork"
    current_plan = true
    description = "One option at the first fork in the personal pathway. The other option in the group is separating into civilian work."
    resolution = "A signed re-enlistment contract at the end of the first six-year term."
    source = "John's service record"
    horizon = "mid"
    depends_on = ["A-pipeline-graduation"]
    status = "open"

An "either route" node, also for illustration only (the ids it names do not exist yet; the biology brainstorm writes them):

    [[node]]
    id = "B-long-term-off-earth-living-by-some-route"
    name = "Humans can live off Earth long term, by partial gravity or by a spinning habitat"
    factor = "B"
    kind = "world"
    description = "The hedge on biology. Resolves if either route does: humans stay healthy for years in partial gravity, or a rotating habitat with Earth-normal gravity is occupied long term."
    resolution = "Either of the two route nodes below has resolved yes."
    source = "The resolving route node's own source"
    horizon = "root"
    depends_on_any = [["B-multi-year-partial-gravity-health", "B-rotating-habitat-occupied-long-term"]]
    status = "open"

## Rules the compute script enforces

1. Every required field is present and every enumerated field has an allowed value.
2. Ids are unique across all files, and every id named in `depends_on`, `depends_on_any`, `requires`, or `superseded_by` exists.
3. No dependency cycles, counting both `depends_on` and `depends_on_any`.
4. Every node has a resolution criterion (the roadmap's rule); an empty string does not count.
5. Before a run that reports numbers: every open world node has a probability for every scenario key. Before Phase 3 the script can still validate the tree and print its shape; it just cannot report numbers.
6. A node's probability never falls as the window lengthens: baseline, then moderate, then strong, then open must be non-decreasing. A node that breaks this has been estimated inconsistently.
7. Choice nodes have a `choice_group` and no probability, and every choice group has exactly one node with `current_plan = true`.

## Decisions (2026-09-08)

Proposed by Claude with a confidence level and the strongest alternative for each, two changed on reflection, the amended set accepted by John. Recorded here so the reasoning is checkable later.

1. **TOML, one file per factor.** High confidence in TOML (standard-library reader, comments, one field per line for clean diffs); moderate on per-factor layout, which is taste. Alternative: one Markdown file per node with a small header block, which reads as a page on GitHub and opens in Obsidian, at the cost of a hand-written parser. Revisit if the tree outgrows one file per factor.
2. **Tier membership lives only in tiers.toml.** High confidence; single source of truth. The compute script prints per-node tier membership as a derived view.
3. **Probabilities per scenario, conditional on dependencies, absent until Phase 3.** High confidence in conditional probabilities over a dependency graph (a Bayesian network evaluated by simulation, which is the standard method). Moderate confidence in four explicit numbers per node. Alternative: estimate one median year and spread per node and derive the four numbers, which is fewer estimates and consistent by construction, at the cost of a curve-shape assumption inside the script that makes the numbers less arguable. Kept the explicit numbers because transparency is the product; added the non-decreasing check (rule 6) as the cheap guard. Revisit at the first annual review.
4. **Choice points are forced, never sampled, and default to the current plan.** High confidence in forcing (how decision analysis treats decisions). Changed from the first draft, which treated untaken choices as unresolved and so forecast for a person who never decides.
5. **"Either route" logic lives on nodes, not in the tier file.** Changed from the first draft, which put it in the tier definitions and would have repeated the habitat hedge in Tiers 2, 3 and 4. The hedge is now one named biology node with its own probability.
6. **Ids are factor letter, dash, slug; Contact Clause rungs keep C1 to C4.** High confidence; cosmetic. Follows the project rule against bare identifiers.

## Known simplifications

Recorded so the methodology document (roadmap step 12) and the annual review can revisit them.

- **Dependencies are hard.** A node cannot resolve unless its parents did. In reality a parent usually makes a child more likely rather than possible; full conditional tables would fix this and are far too heavy for a tree people argue about by hand.
- **Nodes are independent given their parents.** A common cause that drags many nodes down at once, such as a general funding collapse, is only captured if the tree names it as a shared parent. That is the regime factor's job, and the brainstorm should wire its nodes as parents widely enough to carry that weight.
- **Time enters only through the four scenarios.** There is no ordering of events within a window. If the annual review finds that "which comes first" matters, the median-year alternative under decision 3 is the path.
