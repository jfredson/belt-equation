# Outside-model review protocol

Roadmap step 27. PROPOSED 2026-09-19, awaiting John's ruling; nothing below is in force until the decisions at the end are accepted. Promoted from "Later, not now" on 2026-09-08 when John accepted the first probabilities on Claude's recommendation and asked that they be reviewed against other frontier models before anything is published.

## Purpose

Every number in the tree was proposed by one model (Claude) and accepted by John, who has said on the record that he defers to the proposals for now for want of field experience. That is one source of error with no check on it. The review puts each factor's nodes in front of at least two models from other labs with a fixed brief, files what they say verbatim, and has John rule on every disagreement. It is a critique pass, not a vote: the reviewers can move the numbers only through John's ruling, and a ruling to keep a number over a reviewer's objection is a valid outcome that goes on the record with its reason.

The external forecaster baseline (docs/forecasts/) is a different thing and stays separate: it asked a model cold, with nothing shown, for its own numbers as a comparison column. The review shows the reviewer everything and asks for criticism.

## What is reviewed

The seven world factors and the Contact Clause: window, launch, energy, drive, biology, motive, regime, and C1 to C4. Everything on each node goes to the reviewer: name, description, resolution criterion and source, dependencies, horizon class, the five probabilities with their date and rationale, and for long shots the mechanism and breaking point. The reviewer also gets the scenario table and the tier requirement lists, so a criterion can be judged against what it gates.

The access branch is not reviewed before pipeline graduation (May 2027), by John's standing rule. Its five personal nodes are sketch-grade and its world nodes (the training industry, the instructor hire, the seat price) go in with the first post-graduation review.

The methodology (the world-draw spread, the tier definitions, the scoring rule) is not part of this review. It gets its own single pass after the node review is done, with a different brief, so structural critique does not arrive mixed into node critique.

## The reviewers

At least two models from labs other than the proposer's, per factor. Proposed: GPT-6 Astra through the ChatGPT desktop app, which is already in hand and produced the baseline, and Google's current Gemini model through its app. A third is optional and is added when the first two disagree with each other on a factor. Model, version as the app reports it, date, and mode (documents shown, lookup allowed) are recorded at the top of every filed response. If a lab ships a new model mid-review, the review finishes on the model it started with; the new one is used at the next annual review.

## The brief

One fixed text, sent unchanged to every reviewer for every packet, so the answers are comparable. It asks for three things, in order, and for a table first:

1. Missing nodes. Name up to three breakthroughs, events, or dependencies that the factor needs and the tree does not have, each with a one-line resolution criterion. Say which existing node or tier they would gate.
2. Criteria. For any node whose criterion is ambiguous, unmeasurable, already met, or measuring the wrong thing, say which and propose the fix in one sentence.
3. Numbers. For any node where you would put the probability at least 0.15 higher or lower in any scenario, give your five numbers, a one-paragraph reason, and your confidence in the disagreement (low, medium, high). Numbers within 0.15 are not worth arguing and should be left alone.

The brief tells the reviewer what the numbers mean (chance of resolving before the scenario's window, given dependencies resolved), that lookup is allowed and should be flagged when used, that plain language is required, and that it should not be polite: a factor with nothing to challenge is a finding, but an unlikely one.

The full text is in docs/reviews/brief.md and the packets that carry it are generated, not hand-written, by scripts/review_packets.py from the data files, so a packet is always the tree as of its date.

## Packets and order

Three packets, matching the brainstorm groups so the reviewer sees a factor's neighbours: window and biology (16 nodes); launch, energy and drive (17); motive, regime and the Contact Clause (13). Two reviewers times three packets is six sessions. John runs the sessions, since the reviewer apps are on his machine; Claude prepares the packets and files the responses. Each response is pasted into a file as it comes back, before the next session, so nothing is lost or paraphrased.

## Filing

- `docs/reviews/YYYY-MM-DD-<packet>-<model>.md`: the packet's date, the model line, the brief as sent, and the response verbatim. Never edited after filing.
- `docs/reviews/YYYY-MM-DD-rulings.md`: one line per item raised, across all responses, in the form: item, reviewer(s), John's ruling (accept, accept with change, decline), reason. Every accepted item lands the same day as a revision entry on the node (or a new node) and a dated line in CHANGELOG.md, and the tree is re-run. A declined item keeps its reason on the record so the next review can see it was considered.
- Two reviewers disagreeing with each other about a number is ruled the same way as one disagreeing with the tree; John picks, or splits, with a reason.

## Done

Every factor and the Contact Clause reviewed by two models, every item ruled, the changes landed, the tree re-run and the new headline in the changelog. Target 2026-11-09, before website step 24. Then the methodology pass, then Phase 4.

## Decisions to rule on (each with confidence, whether it is standard practice, and the alternative)

1. **Reviewers see everything, and lookup is allowed.** Confidence high. Standard practice for a critique pass (a referee reads the paper). Alternative: a second cold elicitation per model, no documents, to get independent numbers. Cheaper per session, but the baseline already does that, and cold numbers cannot challenge a criterion they have not seen.
2. **The 0.15 threshold for a number to count as disputed.** Confidence moderate; it is a judgment about signal versus noise. Not standard, there is no standard. Alternative: no threshold, file every difference. Costs John a ruling on dozens of two-point quibbles and buries the real disagreements.
3. **Three packets by brainstorm group rather than eight by factor.** Confidence moderate. Judgment call: fewer sessions and the reviewer sees cross-factor dependencies, at the cost of longer prompts (the largest packet is about 4,600 words). Alternative: one packet per factor, sixteen sessions, sharper answers. Take this if the apps truncate or the answers get shallow.
4. **Two named reviewers, Astra and Gemini, third optional on disagreement.** Confidence moderate on the pair, high on "at least two from other labs". Standard practice is two referees. Alternative: three always. More rulings, more cost in John's time, more robust; worth it at the annual review, not for the first pass.
5. **Access branch excluded until May 2027; methodology reviewed separately afterwards.** Confidence high; the first is John's existing rule, the second keeps structural critique from arriving mixed into node critique. Alternative: include the methodology in packet three. Saves one session, muddies the record.
6. **John runs the sessions, Claude prepares and files.** Confidence high; there is no other way to reach the other models from here, and the transcript stays in John's hands. Alternative: none that keeps the review independent of the proposer.
