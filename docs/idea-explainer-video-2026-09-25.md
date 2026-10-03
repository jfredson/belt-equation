# Idea: explainer video for new visitors (tentative)

Status: tentative idea, parked 2026-09-25 by John for a later date. Nothing is scheduled and nothing on the site changes until he picks it up.

## What exists

A 51-second silent motion explainer (1920x1080, 30 fps), made in Cowork on 2026-09-25 and revised with John in the same conversation. The source is in `docs/explainer-video/`:

- `scene.html`: the whole animation as one canvas page. `render(t)` draws the scene at any moment, so the same file can play live in a browser or be recorded to video.
- `render.py`: records it to MP4 with Playwright and ffmpeg. `python3 render.py video out.mp4` renders the full video (about a minute); `python3 render.py stills` writes check frames. The `KNOTS` table sets the pacing: flat runs are reading holds, shallow runs are slowed builds.
- `fonts/`: Source Serif 4 and IBM Plex Mono (SIL Open Font License, from @fontsource), self-hosted.
- `belt-equation-explainer-2026-09-25.mp4`: the approved render.

The numbers are hard-coded from snapshot `2026-09-25-methodology-pass` (the `LINKS` and `DIAL` constants near the top of `scene.html`). Before any use, they must come from the current snapshot.

## The story, in order

1. The frozen question, one line at a time: "What is the probability that, before I die, / I get to live and work in a solar system where / human industry reaches beyond Earth and Mars?"
2. "Seven things all have to go right." The seven links appear on a chain, each with its chance by 2071, then the caption: "These are the numbers played out 20,000 times. The links build on each other, so when one comes true, the ones that depend on it get more likely."
3. "The chance it happens for me": the headline number, then a "How long I live" dial that stops at each date (2071, 2080, 2095, 2136, No limit) with a one-line explanation for each date.
4. "The odds move as the world does.", then beltequation.com after a pause, then "Calculate your own odds."

The copy follows the public-copy rules: no "Belter" and no mention of John's career.

## Implementation plan, agreed in principle 2026-09-25

- One source for both the site and the file: `scene.html` reads its numbers from the site's exported data instead of constants.
- On the site, it plays live in a canvas inside a click-to-play section near the top of the home page (for example "New here? 50-second explainer"). It does not autoplay, since current practice keeps autoplaying hero motion short and looping, and this is 51 seconds. It has a still-frame preview, a transcript underneath for search and screen readers, a stacked layout for phone widths (the 16:9 frame's caption text is about 7 px tall on a phone), and it respects a visitor's reduced-motion setting.
- `scripts/publish.py` re-renders the MP4 whenever the headline or chain numbers change, for social posts and link previews (og:video).
- The number stays first on the home page; the explainer must not push it down.
