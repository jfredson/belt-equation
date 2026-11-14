# Scripted animation pilot: a fly-in over the inner solar system

*Built 2026-10-27 in one working session, on John's Mac (Apple M4, 16 GB of memory). This
note is for John, not for the public sites, so it names the tools. Nothing in it is
published, and no money was spent.*

## What this answers

John read a thread on 2026-10-27 in which someone had an AI write scripts that drove the 3D
program Blender with no window open: the scripts built every model, light and camera move
from code, rendered small check frames to look at its own work, and then rendered the final
minute of animation (eight hours on a top gaming graphics card). He asked whether the same
method could make visually striking animations of the solar system and the galaxy for The
Belt Equation and The Quiet Galaxy. This pilot answers with a real clip rather than a plan.

## What was built

- **`belt-flyin-2026-10-27.mp4`**: a silent 15-second clip, 1280 by 720, 24 frames a second.
  The camera starts wide and high above the Sun and glides down and in until the asteroid
  belt fills the foreground with the Sun and the inner planets beyond it.
- **Three stills** from the clip: `still-wide.png` (the opening view), `still-mid.png`
  (halfway in) and `still-belt.png` (the closing view across the belt).
- **`scripts/blender/inner_solar_system.py`**, the one file that makes all of it. It builds the
  Sun, Mercury, Venus, Earth, Mars and Jupiter with their orbit rings, the main asteroid belt
  as 6,000 small rocks, a field of 1,600 stars, a point light at the Sun, a soft glow in the
  compositor, and a camera move keyed on every frame, then renders. No saved scene file, no
  downloaded models or textures. Run it as the comment at the top of the file says.

**Where the numbers come from.** The orbit sizes and the planets' diameters are from NASA's
[Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) and
[Sun Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html). The belt runs
from 2.06 to 3.27 astronomical units, the inner and outer edges set by Jupiter's 4:1 and 2:1
resonances, with thinner rings at the 3:1 and 5:2 gaps, from Wikipedia's
[Asteroid belt](https://en.wikipedia.org/wiki/Asteroid_belt) and
[Kirkwood gap](https://en.wikipedia.org/wiki/Kirkwood_gap) articles. All of this is written in
the script's header comment beside the numbers.

**Not to scale, and any public use must say so.** The distances between the orbits are true
to each other (one astronomical unit, the Earth-Sun distance, is ten scene units). The bodies
are not: at true scale every planet would be smaller than a pixel against its orbit, so each
body's drawn size grows with the logarithm of its real diameter. That keeps the order right
(Jupiter bigger than Earth, Earth bigger than Mars) while making every body visible, and the
Sun is drawn larger still so it reads as the Sun. The planets' positions along their orbits
are arbitrary, chosen to spread them out, not where they were on any date. The belt's
thickness, the rocks' size and the stars are visual choices, not measurements.

## How long each step took on this Mac

| Step | Time |
|---|---|
| Install Blender 5.2.3 LTS with Homebrew (about 400 MB) | about 3 minutes |
| Build the scene from the script (runs before every render) | about 22 seconds |
| Preview pass: 15 frames (every 24th) at 640 by 360, 16 samples | 29 seconds in all, under a second a frame |
| Four-frame check renders while fixing the look (three rounds) | about 26 seconds each |
| Full clip: 360 frames at 1280 by 720, 32 samples, two halves run side by side | 103 and 107 seconds for the two halves, about 1 minute 50 seconds of wall time; about half a second a frame once the scene is built, on the M4's own graphics unit |
| Join the frames into the mp4 with ffmpeg | 2 seconds |

The look took three rounds of check frames to get right. The first pass used the renderer's
default glare, which drew cross-shaped streaks on every star; the second had the belt so
bright it swallowed the Sun; the third had it so dim it vanished. Each round was a change to
a few numbers in the script and a 26-second run, which is the method's real strength: the
loop from "that looks wrong" to a new picture is under a minute.

## What a full-quality render would need

The clip here is a preview-quality render: the fast rasterising renderer (EEVEE), 32 samples,
720p, simple materials, no planet textures, no atmosphere, no depth of field. A full-quality
version, the kind the Reddit poster made, would mean the path-tracing renderer (Cycles),
1080p or 4K, several hundred samples a frame, textured planets, and a longer clip. That is
where the hours go.

| Render | On this Mac (estimate) | On a rented GPU (estimate) |
|---|---|---|
| This clip again at 1080p, same renderer | about 5 to 7 minutes | a minute or two |
| 15 seconds, path-traced, 1080p, 256 samples | roughly 2 to 4 hours (the M4's GPU has 16 GB shared with everything else, so the 6,000-rock belt and 4K frames would be at its edge) | about 15 to 30 minutes on an RTX 4090, less on a 5090 |
| 60 seconds, path-traced, 4K, 512 samples | a day or more, and probably out of memory | roughly 4 to 8 hours on an RTX 4090 |

**RunPod cost, proposed to John, not started.** RunPod's prices read 2026-10-27
([pricing page](https://www.runpod.io/gpu-cloud/pricing), updated July 2026, with a
[third-party guide](https://www.hostinger.com/tutorials/?p=158956) giving the same range): an
RTX 4090 at $0.34 an hour on the shared "community" tier or about $0.74 on the dedicated tier,
an RTX 5090 at $0.69, an A100 80 GB at $1.19 to $1.39. A one-minute, 4K, path-traced clip at
6 hours on a 4090 would be about $2 to $5; the same on a 5090 about $4; a 15-second 1080p clip
under $1. Setting up (a Blender image, uploading the script, downloading the frames) is a
one-time hour of work and pennies of storage. In other words the rendering itself is cheap;
the cost of this method is the sessions that write and check the scripts, which the plan
covers, not the GPU time. Under the standing rule (2026-10-24) heavy compute goes to RunPod
and any spend needs John's go first, so nothing has been rented.

## What the method does well

- **Everything is a number in a file.** Orbit sizes, belt edges, planet order and camera
  path are code with the source cited beside each. That is exactly the sourcing discipline
  the trackers already run, carried into pictures: the belt's edges in the picture are the
  belt's edges in the Wikipedia article.
- **Fast iteration.** A scene this size builds and renders a check frame in under half a
  minute, so the look is tuned by looking, not by guessing.
- **Scale and particles.** Thousands of rocks, orbit rings and a star field are a loop each;
  a galaxy of a hundred thousand stars is the same loop with a different distribution.
- **Camera moves.** A fly-in keyed on every frame from a formula is one function; a slow
  orbit, a pull-back from a planet to the whole system, or a cut between scales is a change
  to that function.
- **Repeatable.** Change a number in the data and re-run; the clip updates. The explainer
  video idea (`docs/idea-explainer-video-2026-09-25.md`) wanted exactly that for the headline
  numbers, and this could feed it a 3D opening shot.

## Where it fell short

- **No textures, no atmospheres, no detail.** The planets are coloured balls. Real planet
  textures (NASA publishes free maps) and a thin atmosphere shell are each an hour's work, but
  were out of this pilot's scope.
- **Judging the picture needs eyes.** The script cannot tell that the belt is too bright or
  the Sun clipped at the frame edge; a person (or the model looking at the frame) has to.
  This pilot did that by reading the check frames, which worked but is where the time goes.
- **Visual choices are not facts.** The rocks' size, the belt's thickness, the planets'
  self-glow so they show at the wide view, and the logarithmic sizes are all choices made for
  legibility. Any public use needs a "not to scale" line, and the trackers' habit of saying
  who chose what should carry over.
- **Blender's scripting interface moves.** Three things changed between the Blender the
  Reddit poster used and 5.2 here (the renderer's name, the compositor's setup, the glare
  node's settings). The script handles both forms, but any such script will need tending
  across versions.
- **The Mac's limits.** Preview-quality renders are quick here; full quality is not, and the
  16 GB of shared memory is the ceiling before the processor's speed is.

## Next for The Quiet Galaxy

A galaxy-scale scene is the same method with a different distribution of points: a thin disc
with spiral arms (a logarithmic spiral with scatter), a central bulge, a halo of globular
clusters, and a marker for the Sun's position about 26,000 light-years from the centre (from
Wikipedia's [Milky Way](https://en.wikipedia.org/wiki/Milky_Way) article, to be cited in the
script). Steps, in order:

1. Build the disc as 150,000 to 300,000 emissive points on two or four arms, coloured by
   population (blue-white in the arms, yellow in the bulge), and check a wide still.
2. Add a "we are here" marker and a pull-back from the Sun's neighbourhood to the whole disc,
   which is the shot the Fermi question wants: how small our one listening post is.
3. Overlay the explainer's own numbers (a sphere for how far our radio signals have reached,
   about 100 light-years, which is invisible at galaxy scale and is the point).
4. Render at preview quality here, propose a full-quality render on RunPod with a cost in
   the spending record, and only then write any public copy, with no tool named.

## Files

- `belt-flyin-2026-10-27.mp4`: the clip.
- `still-wide.png`, `still-mid.png`, `still-belt.png`: three frames from it.
- `../../scripts/blender/inner_solar_system.py`: the script.
