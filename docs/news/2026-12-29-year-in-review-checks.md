# The year-end post for 2026: sources and checks

The post: `site/src/content/news/2026-12-29-what-2026-did-to-my-odds-and-what-to-watch-in-2027.md`, kind
`year-review` (new; see below). Drafted 2026-11-15 by Claude, asked for by John the same day: an
end-of-year post on each of the five trackers with the year's most important findings and the events to
watch in 2027, published in the week of 2026-12-28. It is held: merging it deploys it, and its date is
2026-12-29, so merge only in that week.

## The new kind

No existing kind fits. `discovery` and `mission-news` would mislabel it, and a number kind would need a
record changed within fourteen days. Added: `year-review`, shown as "the year in review", which names no
record and no mission and is checked like a discovery (a source with an address, a link beside every
figure). Touched: `site/src/content.config.ts`, `site/src/lib/news.ts`, `scripts/check_news.py`,
`scripts/social-image.mjs` (card label), `scripts/test_news.py` (three tests).

| choice | confidence | standard or judgment | strongest alternative |
|---|---|---|---|
| A tenth kind, `year-review` | moderate: one post a year, and a label that says what it is | judgment | file it as `discovery` with no code change; cheaper, but the News list would call a year's review "a discovery" |

## The site's own numbers (read 2026-11-15)

- Headline A2, baseline: 0.465 percent by 2071 (`data/headline.json`, computed 2026-10-11; the home page
  shows "0.5%"). Weakest link on the home page: "a reason to go, at 5.9%".
- Headline history (`data/snapshots/`): 0.38 percent on 2026-09-20 (step-27, the first reviewed run;
  `compute.py score 2026` names it the year's first reviewed run), 0.47 on 2026-09-25, 0.59 after the
  function-over-route pass the same day, 0.465 on 2026-10-02, unchanged in the runs of 2026-10-04 and
  2026-10-11.
- Story page: "44 entries so far, across 9 runs of the tree". Ledger kinds: 22 structure, 17 revision,
  3 resolution (events of 2022, 2025 and June 2026, before the tree), 2 held-steady.
- Radar: 11 scan records, 289 step checks (export count), none moved or resolved. The post says "nearly
  three hundred".
- Step numbers quoted: both stages recovered, 95 percent by 2071 (step page).
- The yearly review of 2027-01-03 and what it settles: `docs/roadmap.md` step 18; `CHANGELOG.md`
  2026-10-03 (the Belt tier and off-Earth material by either route, held for the review);
  `docs/proposal-computing-as-off-earth-product-2026-10-31.md` (agreed in principle 2026-11-09, lands at
  the review, with the solar-cell gate); `data/B-biology.toml` (the year of food made on site, re-estimate
  due by the review); `docs/methodology.md` (the score is computed each January).

## Sources opened on 2026-11-15, each with what it confirmed

- https://www.nasa.gov/mission/artemis-ii/ : launched April 1, 2026; splashdown April 10, 2026.
- https://en.wikipedia.org/wiki/Artemis_II : the only crewed flight beyond low Earth orbit since Apollo 17 in 1972.
- https://en.wikipedia.org/wiki/List_of_Starship_launches : flights 12 (May 22), 13 (July 24), 14 (September 28, first orbit) in 2026; Flight 15 from the earlier post.
- https://www.cbsnews.com/news/spacex-catch-starship-rocket/ : "the first such recovery of a Starship from orbit"; 22 hours in space; booster's catch attempt.
- https://www.fool.com/earnings/call-transcripts/2026/10/20/spacex-spcx-q3-2026-earnings-call-transcript/ : "refly the second stage by early next year"; "We'll attempt an on-orbit refueling early next year"; Musk: "We expect Starship to fly weekly at some point in the first half next year".
- https://en.wikipedia.org/wiki/Starship_HLS : "An uncrewed lunar landing demonstration originally planned for 2025 has been delayed."
- https://www.nasa.gov/mission/artemis-iii/ : objectives in low Earth orbit, launch 2027, test one or both landers.
- https://en.wikipedia.org/wiki/Artemis_III : revised on February 27, 2026 to a crewed demonstration in low Earth orbit; launch NET June 2027.
- https://en.wikipedia.org/wiki/Haven-1 : until January 20, 2026 scheduled for late 2026, delayed to the first quarter of 2027.
- https://www.vastspace.com/haven-1 : "targeted to launch in 2027".
- https://www.news4jax.com/tech/2026/08/23/china-abruptly-postpones-ambitious-change-7-lunar-mission-launch/ : AP, August 23, 2026, Chang'e 7 postponed.
- https://en.wikipedia.org/wiki/Tianwen-2 : arrival at Kamoʻoalewa 4 July 2026; departure 24 April 2027; capsule landing 29 November 2027.
- https://www.esa.int/articles/about-us/directorates/operations/space-safety/hera/hera-spacecraft-in-rectangular-orbit-around-target-asteroids : Hera's arrival (and the earlier post's checks).
- https://global.jaxa.jp/press/2026/10/20261020-1_e.html : MMX launched 04:41:03 JST on October 20, 2026.
- https://www.dlr.de/en/latest/news/2026/off-to-the-moons-of-mars-mmx-mission-and-idefix-rover-ready-for-launch : MMX reaches Mars in the second half of 2027.
- https://science.nasa.gov/blogs/lucy/2026/10/28/nasas-lucy-reaches-trojan-asteroid-region-5-years-after-launch/ : Lucy the first spacecraft to enter the Jupiter Trojans.
- https://science.nasa.gov/mission/lucy/ : next flyby Aug. 11, 2027 (Eurybates per the missions record).
- https://en.wikipedia.org/wiki/ESCAPADE : Mars orbital insertion September 2027 (planned).
- https://www.astroforge.com/deepspace-2 : the page says both "LAUNCHING 2027" and "Launching in the fourth quarter of 2026"; rendezvous with a near-Earth asteroid and imaging.
- https://en.wikipedia.org/wiki/AstroForge : Odin launched 27 February 2025 and failed.
- Pages for names, opened and loading: spacex.com, spacex.com/vehicles/starship, nasa.gov, esa.int, ESA's Hera and Euclid mission pages, rubinobservatory.org, mmx.jaxa.jp/en, vastspace.com, astroforge.com, science.nasa.gov/mission/escapade, Wikipedia on Gwynne Shotwell, Elon Musk, Kamoʻoalewa, Phobos, Apollo 17 (not linked in the end), 3548 Eurybates, Jupiter trojans, Chang'e 7.
- This site's pages linked: home, About#story, Radar, the four step pages, the four earlier posts. All load.

## Left out, and why

- The 2026 calibration score's result. The brief says not to pre-empt the review. The post says only that
  the review gives the first score.
- The profit step's "about 6 percent once everything under it is counted" (the Flight 15 post): the
  post quotes the home page's 5.9 percent for the weakest link instead, which a reader can see.
- Hera's two small satellites in early 2027: ESA's Hera page as opened gives no 2027 date.
- ESA's MMX page cited on the Missions page now answers 404; DLR is used instead (follow-up below).
