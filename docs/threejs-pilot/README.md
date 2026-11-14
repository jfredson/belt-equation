# Pilot: an interactive 3D map of the inner solar system, in the browser

Written 2026-10-27 for John. This is the sibling of the Blender video pilot run the same day:
that one makes a film, this one makes a scene a reader can turn with a finger. Nothing here is
linked from the site or published; the page lives at `site/public/lab/belt-scene.html` and would
be served at `/lab/belt-scene.html` after a deploy, unlinked and marked "do not index".

## What was built

One HTML file, about 22 KB, with no build step. It draws, entirely in code:

- the Sun, with a soft glow;
- Mercury, Venus, Earth, Mars and Jupiter, each going round the Sun at its real speed relative
  to the others, with its distance, size and year taken from the
  [NASA planetary fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/);
- the main asteroid belt as 4,000 points between 2.06 and 3.27 times Earth's distance from the
  Sun, the limits of the dense part of the belt given by
  [Wikipedia's Asteroid belt article](https://en.wikipedia.org/wiki/Asteroid_belt). Each point
  has its own distance and tilt and moves at the speed a real rock there would, so the belt
  slowly shears as the inner rocks overtake the outer ones;
- a sphere of 2,500 background stars;
- orbit lines and names.

The reader can drag to turn the view, scroll or pinch to zoom, and drag with two fingers or the
right mouse button to slide it. A small panel sets the speed of time (stopped, one day a second,
a week, 30 days, four months, a year a second), turns the orbit lines and names on and off, pauses,
and resets the view. A clock says how much time has passed. A folded note on the page says in
plain words that the sizes are exaggerated, where every number comes from, and what is simplified
(circular orbits in one flat plane, arbitrary starting positions, placeholder points rather than
real asteroids). If a reader has asked their device for less motion, the scene starts paused.

The one outside piece is the 3D library, loaded from a content-delivery network at a pinned
version so the page cannot change under a reader. It names no tool on the page. The page's colours
are the site's own "Ore" skin, copied in rather than imported, since the pilot is served as a
plain file.

## How it performs

| What | Measured |
|---|---|
| Frame rate on this Mac (M4, 1024 by 768 window, 2x pixel density) | 60 frames a second, the screen's limit |
| The page itself | 22 KB |
| The 3D library, downloaded once and then cached | 167 KB compressed |
| Time from opening the page to the first picture, library already cached | under a second |

The belt's 4,000 points are moved on the graphics chip, not by the page's script, so they cost
almost nothing; the planets are five small spheres. The pixel density is capped at 2x so a sharp
phone screen does not draw four times the pixels it needs. The scene stops drawing when the tab
is hidden. I have not had the page on a real phone: the phone layout was checked in the desktop
browser at a phone's width, where it reads well (screenshots below). A real test on John's phone
is the next step, and I expect it to run smoothly, since the scene is far lighter than a typical
3D product page.

Screenshots, taken 2026-10-27:

- `2026-10-27-desktop-start.jpg`: the opening view on a desktop, Jupiter at the edge.
- `2026-10-27-desktop-turned-and-zoomed.jpg`: after a drag and a scroll.
- `2026-10-27-phone.jpg`: the opening view at a phone's width.
- `2026-10-27-phone-note-open.jpg`: the scale-and-sources note unfolded on a phone.

## Interactive scene or rendered video: which does what well

**A rendered video** (the Blender route) is cinematic: it can have real lighting, textures,
camera moves timed to a script, and a look no browser scene matches. It plays the same everywhere,
needs nothing from the reader's device beyond playing a film, and it is the thing to put in a
social post, a link preview or an essay's opening. Its costs: a 15-second clip at 1080p is
typically several megabytes, far more than this whole page; every change means a re-render;
the reader can only watch; and it says one thing, the thing the camera was pointed at.

**An interactive scene** (this route) is a map rather than a film. The reader chooses where to
look and how fast time runs, which is what makes the shear of the belt, or the gap between Mars
and the belt, something they find rather than something they are told. It is tiny, it costs
nothing to change (edit a number, reload), and it can read live numbers from the site's data,
so a scene could show, for instance, where each node of the tree is set. Its costs: it depends
on the reader's device drawing it (old phones and some corporate browsers will not), it cannot
match the video's polish, and it cannot be posted to X or Reddit as a picture: those need a
still or a short screen recording taken from it.

My reading: the two are not rivals. The video is for reaching people (posts, previews, the top
of an essay); the scene is for keeping them (a page they explore). The same figures feed both.

## What it would take to put a scene on a real page

**On The Belt Equation.** The site is built from Astro into plain files, and a scene is a plain
file, so the fit is natural. The steps:

1. Move the scene from a whole-page file into a component that fills a box on a page, with the
   controls as part of the box, and a still image as the thing shown until the reader taps
   "explore", so a page never pays for 3D the reader did not ask for.
2. Serve the 3D library from the site itself rather than a content-delivery network, so the page
   has no third-party dependency and the site's privacy stance holds. This is a copied file of
   about 170 KB compressed.
3. Decide what the scene is *for*. A map of the inner solar system on its own is pretty but
   says nothing the site is about. The version worth building marks the places the tree's nodes
   are about (the Moon, Mars, the belt, the moons of Jupiter) and lets a reader tap one to see
   its probability. That needs a small data file joining nodes to places, and a label style.
4. Give it the site's accessibility floor: a text description of what the scene shows, keyboard
   control of the camera (arrow keys, plus and minus), and the paused start for readers who ask
   for less motion, which the pilot already has.
5. A real phone test, and a check in Safari, Firefox and Chrome.

Roughly a day's work for the component and the library, and a second day for the node-to-place
version with John's rulings on what is marked.

**On The Quiet Galaxy.** A galaxy-scale scene is the same technique at a different size. The
Milky Way as a disc of a few hundred thousand points in spiral arms is cheap to draw the same
way the belt is drawn here (on the graphics chip), with the Sun's position marked about 26,000
light-years from the centre, a sphere showing how far our radio signals have reached, and the
known exoplanet systems as points, from a public catalogue. The hard parts are not the drawing
but the sourcing: every placed thing needs a figure a reader can open (the galaxy's size and
the Sun's position from a review article or NASA page, exoplanet positions from the NASA
Exoplanet Archive), and the honesty note has to say which parts are art (the arms) and which are
data (the points). I would expect two to three days to a first version, of which the drawing is
the smallest part.

## What I would do next

1. John opens the page on his phone and in Safari, since those are the two things I could not
   test here. A sentence back on whether it runs smoothly settles the performance question.
2. If it does, decide whether the scene has a job on the site (the node-to-place idea above) or
   stays a lab piece. I would not put the plain map on a page: a visual that says nothing the
   site is about is decoration, and the site's rule is that the number comes first.
3. If it has a job, build it as a component with the library served from the site, and a still
   image shown until the reader chooses to explore.
4. Keep the video route for posts and previews. A screen recording of this scene could stand in
   for a rendered clip in a pinch, but it will not look as good as the Blender route can.

Nothing here is published or linked, no money was spent, and the site's pages are untouched.
