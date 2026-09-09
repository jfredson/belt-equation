# Node schema and data format

Drafted 2026-09-08 (roadmap step 2). PROPOSED: Claude's draft for John to accept or move. The choices that most need his eye are listed at the end under "Choices for John". Once accepted, this document is the source of truth for the record layout, and the compute script refuses any file that does not follow it.

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
| `depends_on` | no | List of ids that must resolve before this node can. Empty or absent means no dependencies. |
| `choice_group` | choice only | Name shared by the mutually exclusive options at one choice point, such as `"six-year-fork"`. The decision comparison forces exactly one node in a group to yes per run. |
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

**Tiers.** `tiers.toml` defines each system tier (1 to 4) and access tier (A0 to A3) as a set of required nodes. `requires` lists ids that must all resolve. `requires_any` lists groups of ids where at least one per group must resolve; this is how the rotating-habitat hedge on biology is expressed (a tier needs either partial-gravity health to work out or a habitat with Earth-normal gravity). A run reaches a tier when its requirements are met. The headline number is how often A2 is reached; Tier 3 is the bar for "the Belt exists".

**Scenarios.** `scenarios.toml` lists the four longevity scenarios with a key, a plain name, and the window year (or none, for escape velocity). The compute script runs the whole tree once per scenario and reports each separately. How the window factor's own nodes weigh the scenarios against each other is a methodology question for step 12, not a schema question; the file leaves room for a weight per scenario and does not fill it.

**Choice points.** Nodes with `kind = "choice"` are never sampled. In an ordinary run they are all treated as unresolved (the forecast with no decision taken). In the decision comparison, the script picks one option per `choice_group`, forces it to yes and the others to no, runs the tree, and repeats for each option. The difference between the runs is the value of the decision.

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
    description = "One option at the first fork in the personal pathway. The other option in the group is separating into civilian work."
    resolution = "A signed re-enlistment contract at the end of the first six-year term."
    source = "John's service record"
    horizon = "mid"
    depends_on = ["A-pipeline-graduation"]
    status = "open"

## Rules the compute script enforces

1. Every required field is present and every enumerated field has an allowed value.
2. Ids are unique across all files, and every id named in `depends_on`, `requires`, `requires_any`, or `superseded_by` exists.
3. No dependency cycles.
4. Every node has a resolution criterion (the roadmap's rule); an empty string does not count.
5. Before a run that reports numbers: every open world node has a probability for every scenario key. Before Phase 3 the script can still validate the tree and print its shape; it just cannot report numbers.
6. Choice nodes have a `choice_group` and no probability.

## Choices for John

1. TOML, one file per factor. The alternative is one file per node: more files, but each diff touches one record.
2. "Which tiers it feeds" lives in tiers.toml only, not on the node.
3. Probabilities are conditional on dependencies, stated per scenario, and absent until Phase 3.
4. Choice points are forced, never sampled, and grouped by `choice_group`.
5. The habitat hedge is expressed as `requires_any` in the tier definitions rather than as a node that stands for "either of these".
6. Id style: factor letter, dash, slug. Contact Clause rungs keep `C1` to `C4`.
