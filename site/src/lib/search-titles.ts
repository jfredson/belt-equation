// What search engines show for a page: its title (the link in the results) and, where given, its
// description (the line under it). Only these change; the heading and text on each page stay as
// written, so every leaf keeps its exact test as its heading. Each title leads with the words a
// person would type, within the 60 or so characters Google shows, and Base.astro adds
// " · The Belt Equation" after it. A proper name appears only where the page itself names it.
// Agreed by John 2026-11-27, from timeassembler/docs/drafts/search-titles-2026-11-27.md.
// Keys are page addresses with their trailing slash. A page not listed keeps its own title.

export const SEARCH_TITLES: Record<string, { title: string; description?: string }> = {
  '/': {
    title: 'When will humans colonise space? The odds in my lifetime',
  },
  '/tree/': {
    title: 'Space settlement milestones: what has to happen',
    description:
      'Every breakthrough between today and human industry beyond Mars, from launch costs to life support, each with the test that would settle it.',
  },
  '/missions/': { title: 'Upcoming space missions to watch, and their dates' },
  '/news/': { title: "Space news: what moved The Belt Equation's odds" },
  '/run/': { title: 'Space settlement odds calculator: run it yourself' },

  // The branches
  '/tree/launch/': { title: 'Reusable rockets, launch costs and propellant depots' },
  '/tree/energy/': { title: 'Power in space: lunar reactors, fusion and solar' },
  '/tree/drive/': { title: 'Spacecraft propulsion: nuclear and faster transit' },
  '/tree/biology/': { title: 'Living in space: gravity, radiation and life support' },
  '/tree/motive/': { title: 'The space economy: who pays for work off Earth' },
  '/tree/regime/': { title: 'Space law and politics: treaties, rights and funding' },
  '/tree/window/': { title: 'Living long enough: aging research and lifespan' },
  '/tree/access/': { title: 'Getting to space: seats, training and careers' },
  '/tree/contact/': { title: 'First contact: alien and machine minds' },

  // Launch
  '/tree/launch/L-fully-reusable-heavy-launcher-recovers-both-stages/': { title: 'Fully reusable rocket: recovering both Starship stages' },
  '/tree/launch/L-heavy-launcher-100-per-year/': { title: 'Starship launch rate: 100 orbital flights in a year' },
  '/tree/launch/L-orbital-propellant-transfer-at-scale/': { title: 'Orbital refuelling: 100 tonnes of propellant transferred' },
  '/tree/launch/L-crew-lands-on-moon-in-reusable-lander/': { title: 'Reusable lunar lander: a crew lands on the Moon' },
  '/tree/launch/L-launch-price-below-200-dollars-per-kg/': { title: 'Launch cost per kg: below $200 to low Earth orbit' },
  '/tree/launch/L-large-structure-assembled-in-orbit/': { title: 'In-space assembly: a 100-metre structure built in orbit' },
  '/tree/launch/L-lunar-material-delivered-to-orbit-at-scale/': { title: 'Lunar mining: 100 tonnes of Moon material to orbit' },
  '/tree/launch/L-off-earth-material-delivered-at-scale/': { title: 'Space mining: 100 tonnes a year from the Moon or asteroids' },
  '/tree/launch/L-asteroid-material-delivered-to-orbit-at-scale/': { title: 'Asteroid mining: 100 tonnes delivered to orbit in a year' },
  '/tree/launch/L-cryogenic-propellant-stored-in-orbit-six-months-and-used/': { title: 'Propellant depot: cryogenic fuel stored six months in orbit' },
  '/tree/launch/L-propellant-produced-off-earth-and-fired-in-a-thruster/': { title: 'Space-made rocket fuel: propellant from off-Earth material' },

  // Energy
  '/tree/energy/E-megawatt-spacecraft-operates-in-orbit/': { title: 'Megawatt power in space: one spacecraft, one megawatt' },
  '/tree/energy/E-fission-reactor-runs-on-lunar-surface/': { title: 'Nuclear reactor on the Moon: a year of fission surface power' },
  '/tree/energy/E-power-through-the-lunar-night-at-a-surface-site/': { title: 'Power through the lunar night: 100 kW for a year' },
  '/tree/energy/E-solar-with-storage-powers-a-lunar-polar-site-for-a-year/': { title: 'Solar power on the Moon: a polar site powered all year' },
  '/tree/energy/E-power-delivered-from-orbit-to-the-lunar-surface-for-a-year/': { title: 'Power beaming to the Moon: a surface site run for a year' },
  '/tree/energy/E-superconducting-wire-price-falls-tenfold/': { title: 'Superconducting wire cost: a tenfold price drop' },
  '/tree/energy/E-fusion-plant-delivers-net-electricity/': { title: 'Fusion power to the grid: the first net electricity' },
  '/tree/energy/E-compact-power-source-at-fast-drive-scale/': { title: 'Compact power for spacecraft: 100 MW under 100 tonnes' },
  '/tree/energy/E-fission-electric-space-power-system-reaches-a-hundred-megawatts/': { title: 'Nuclear electric power in space: 100 megawatts' },
  '/tree/energy/E-construction-begins-on-a-fusion-plant-meant-to-sell-electricity/': { title: 'Commercial fusion plant: construction begins' },
  '/tree/energy/E-megawatt-heat-rejected-for-thirty-days-in-vacuum/': { title: 'Spacecraft radiators: a megawatt of heat shed in vacuum' },

  // Drive
  '/tree/drive/D-nuclear-propulsion-changes-orbit-in-space/': { title: 'Nuclear thermal propulsion: DRACO and the first test in space' },
  '/tree/drive/D-nuclear-propulsion-in-routine-use/': { title: 'Nuclear propulsion in routine use: several missions a year' },
  '/tree/drive/D-fast-transit-in-routine-use/': { title: 'Fast travel to the asteroid belt: under a year from Earth' },
  '/tree/drive/D-high-power-solar-electric-propulsion-in-routine-use/': { title: 'Solar electric propulsion at megawatt scale' },
  '/tree/drive/D-crew-round-trip-to-mars/': { title: 'Crewed Mars mission: landing and return to Earth' },
  '/tree/drive/D-crew-round-trip-beyond-the-earth-moon-system/': { title: 'Crewed deep space mission beyond the Moon and back' },
  '/tree/drive/D-constant-acceleration-drive-demonstrated/': { title: 'Fast interplanetary engine: high thrust and exhaust speed' },
  '/tree/drive/D-permanent-crewed-site-beyond-the-earth-moon-system/': { title: 'Permanent crewed outpost beyond the Moon' },

  // Biology
  '/tree/biology/B-mammal-born-and-weaned-in-partial-gravity/': { title: 'Reproduction in low gravity: a mammal born and weaned' },
  '/tree/biology/B-human-year-in-partial-gravity-without-disqualifying-harm/': { title: 'Partial gravity health: a year on the Moon or Mars' },
  '/tree/biology/B-human-child-born-off-earth/': { title: 'The first child born in space and raised off Earth' },
  '/tree/biology/B-crewed-spin-gravity-demonstration/': { title: 'Artificial gravity in space: a crew lives a month spinning' },
  '/tree/biology/B-earth-gravity-habitat-occupied-for-a-year/': { title: 'Rotating space station: a year at Earth-normal gravity' },
  '/tree/biology/B-long-term-off-earth-living-by-some-route/': { title: 'Long-term living in space: low gravity or a spinning habitat' },
  '/tree/biology/B-shielding-halves-deep-space-radiation-dose/': { title: "Space radiation shielding: halving a crew's dose" },
  '/tree/biology/B-closed-loop-life-support-year-off-earth/': { title: 'Closed-loop life support: a year of food, water and air' },
  '/tree/biology/B-radiation-resistance-treatment-for-humans/': { title: 'A drug for space radiation resistance' },
  '/tree/biology/B-staple-crop-grown-from-seed-to-harvest-off-earth/': { title: 'Growing food in space: a staple crop from seed to harvest' },
  '/tree/biology/B-major-operation-under-anaesthesia-performed-off-earth/': { title: 'Surgery in space: a major operation under anaesthesia' },

  // Motive
  '/tree/motive/M-paying-customer-for-work-done-in-orbit/': { title: 'In-space services: a paying customer for work in orbit' },
  '/tree/motive/M-power-beamed-from-orbit-to-ground-at-kilowatt-scale/': { title: 'Space-based solar power: a kilowatt beamed to the ground' },
  '/tree/motive/M-hundred-people-working-off-earth-for-pay/': { title: 'Jobs in space: 100 people working off Earth at once' },
  '/tree/motive/M-off-earth-product-sold-at-a-profit/': { title: 'Space mining profit: the first off-Earth product sold' },
  '/tree/motive/M-commercial-insurance-written-on-a-private-lunar-asset/': { title: 'Space insurance: a private lunar asset insured' },

  // Regime
  '/tree/regime/R-crewed-lunar-program-outlives-two-changes-of-president/': { title: 'Moon programme politics: surviving two changes of government' },
  '/tree/regime/R-crewed-lunar-program-outlives-two-changes-of-backer/': { title: 'Moon programme funding: surviving two changes of backer' },
  '/tree/regime/R-space-funding-holds-through-a-recession/': { title: 'Space budgets in a recession: recovery within three years' },
  '/tree/regime/R-binding-ban-on-debris-creating-anti-satellite-tests/': { title: 'Anti-satellite test ban: a binding treaty among space powers' },
  '/tree/regime/R-off-earth-resource-rights-recognised-by-major-powers/': { title: 'Space mining rights: the Artemis Accords, the US and China' },
  '/tree/regime/R-off-earth-site-accepts-permanent-residents/': { title: 'Living in space permanently: the first permanent residents' },
  '/tree/regime/R-us-and-china-recognise-keep-out-zones-around-off-earth-installations/': { title: 'Safety zones on the Moon: US and China recognition' },
  '/tree/regime/R-space-traffic-management-authority-among-major-powers/': { title: 'Space traffic management: an authority with real power' },

  // Window (whether I live long enough)
  '/tree/window/W-dog-rapamycin-trial-reports-longer-life/': { title: 'Rapamycin in dogs: the TRIAD lifespan trial result' },
  '/tree/window/W-regulator-accepts-aging-as-an-indication/': { title: 'Aging as a disease: a drug regulator accepts it' },
  '/tree/window/W-composite-aging-trial-positive-in-humans/': { title: 'TAME trial: does metformin delay age-related disease?' },
  '/tree/window/W-partial-reprogramming-reaches-human-trials/': { title: 'Partial reprogramming: the first human trial' },
  '/tree/window/W-first-drug-approved-to-slow-aging/': { title: 'First drug approved to slow aging' },
  '/tree/window/W-human-therapy-cuts-death-rate-in-older-adults/': { title: 'A treatment that cuts deaths in older adults by a quarter' },
  '/tree/window/W-verified-human-lifespan-passes-122/': { title: 'Maximum human lifespan: a verified life past 122' },
  '/tree/window/W-regulator-accepts-a-biological-measure-of-aging-as-a-trial-endpoint/': { title: 'Biological age tests as an approved trial endpoint' },

  // News
  '/news/2026-11-14-hera-arrives-at-the-asteroid-nasa-struck/': { title: "Hera reaches Dimorphos, the asteroid NASA's DART struck" },
  '/news/2026-11-13-starship-flight-15-reaches-orbit-booster-catch-called-off/': { title: 'Starship Flight 15 reaches orbit: why the ship catch matters' },
  '/news/2026-10-27-rubin-first-dwarf-planet-candidate/': { title: 'Likely new dwarf planet beyond Pluto: the Rubin Observatory find' },
};
