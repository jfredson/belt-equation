# The Euclid comet post: sources and checks

The post: `site/src/content/news/2026-11-09-euclid-first-new-comet.md`, a discovery post, drafted
2026-11-09 by Claude at John's request. Not yet published: merging it to `main` deploys it.

## Why it is late

ESA announced the comet on 2026-10-19, eight days before the discovery watch began on 2026-10-27, so no
weekly scan recorded it. On 2026-11-09 ESA's Top News feed carried it dated 2026-11-06, a re-stamp from
ESA's site move; the release itself is dated 2026-10-19, and the post uses that date. John asked for the
post on 2026-11-09.

## Title and framing

- Title by John, 2026-11-09: "ESA's Euclid telescope has found its first new comet". Checked against
  `sentient-horizons/editorial/title-rules.md`: it names the subject (rule 2), makes a plain claim (rule
  4) and uses no coined phrase (rule 3). No Reddit title exists yet (rule 7).
- The post sticks to the news and says nothing about the odds, under John's ruling of 2026-11-09
  (docs/definitions.md, decision log; `scripts/check_news.py` no longer requires an odds ending).

## Facts, each against its source (opened 2026-11-09)

- ESA's release (https://www.esa.int/articles/about-us/directorates/science/euclid/euclid-discovers-new-comet,
  dated 2026-10-19): found in images of 16 to 24 September 2026; Mikko Pöntinen of the University of
  Helsinki, with the Euclid Consortium's solar system working group, using software he wrote; found in five
  fields of view, sixteen exposures in all; a fuzzy coma; no match in catalogues; the Minor Planet Center
  confirmed it on 8 October; about 1.3 billion kilometres from Earth, between the orbits of Jupiter and
  Saturn; "straight up" from the Sun's view; "thousands of years" per orbit, to be refined; Euclid avoids
  the planets' plane and "typically only visits each section of the sky once"; "a happy coincidence"; not
  a suitable target for Comet Interceptor, but "a real test case" for how the teams will coordinate;
  Euclid's first new comet, though it had imaged known ones.
- The Minor Planet Center's circular, MPEC 2026-T146 (https://www.minorplanetcenter.net/mpec/K26/K26TE6.html),
  issued 2026 October 8, 15:40 UT: the comet's designation and first orbit, observer Euclid, measurers
  Pöntinen and others.
- The Minor Planet Center's current orbit
  (https://www.minorplanetcenter.net/db_search/show_object?object_id=C%2F2026+S1), read 2026-11-09:
  inclination 85.2 degrees; perihelion 2027-09-13 at 8.74 astronomical units; period 149,478 years, given in
  the post as "something like 150,000 years" and marked as a first guess, since ESA says it will be refined.
  Saturn's own closest distance to the Sun is about 9.0 units, so 8.74 is "just inside Saturn's orbit".
- Left out: a secondary report's "345,000-year" period (IFLScience), which matches neither ESA nor the
  Minor Planet Center.

## Link what you name (`sentient-horizons/editorial/link-what-you-name.md`)

Every first mention linked and opened on 2026-11-09: the European Space Agency (https://www.esa.int/);
Euclid (ESA's mission page, https://www.esa.int/missions/about-us/directorates/science/euclid); the
University of Helsinki (https://www.helsinki.fi/en); the Minor Planet Center (https://www.minorplanetcenter.net/);
Comet Interceptor (ESA's mission page,
https://www.esa.int/missions/about-us/directorates/science/comet-interceptor/comet-interceptor). ESA's
release, the circular, the orbit page, the picture page and the licence all answered.

Not linked, with the reason: Mikko Pöntinen has no page of his own that could be found (no university
profile, no Wikipedia article); he is named in plain words with his role, as the rule allows. The Euclid
Consortium appears only in the picture credit, which is ESA's credit line as given.

## Voice Calibration (master version 2026-10-18)

- Substance gate: every figure re-checked against the pages above. "Only once" became "usually only
  once" (ESA: "typically"); "ESA's team calls it a happy coincidence" became a quotation of the release;
  the picture's alt text no longer claims galaxies that were not checked.
- Pattern 4: two contrasts in the first draft; kept "built to map billions of distant galaxies, not to
  chase things in our own neighbourhood", which carries the story, and cut "rather than travelling with it".
- Pattern 12: "It is not in the flat plane the planets move in. Its orbit is tilted 85 degrees" joined
  with a colon.
- Pattern 22: "The orbit worked out so far puts one trip around the Sun at…" rebuilt as "On the orbit
  worked out so far, one trip around the Sun takes…".
- Pattern 24: "a streak…: something moving fast" became "a streak…, which meant something was moving fast".
- Finite-verb scan: the closing line ("A better orbit, as…, and whether…") had no main verb; rewritten as
  two sentences.
- Flagged vocabulary, em dashes, triplets, announcing pivots, trailing meaning clauses: none found.
- Corpus coherence: a news post about a comet stakes no position the corpus holds; no wire tripped.

## Cold Reader

- Ninety seconds: the title and first paragraph say what happened and who did it; no project vocabulary
  appears anywhere in the post.
- Uninformed reader: "keeps the register" became "keeps the official register of asteroids and comets";
  "named it C/2026 S1" became "gave it its official name"; the planets' plane, Comet Interceptor and
  "astronomical distance" are all given in plain words.
- Coinage budget: zero project terms. Closed loop: every inline link is external.
