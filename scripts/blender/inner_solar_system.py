"""Build and render a short fly-in over the inner solar system and the main asteroid belt.

Everything in the scene is built from this script: no saved scene file, no models, no
textures. The script is run headless, with no window, like this (the part after the two
dashes is read by this script, the part before by the renderer):

    blender --background --python scripts/blender/inner_solar_system.py -- \
        --out /path/to/frames --width 1280 --height 720 --step 1

    --out      folder the frames are written to (PNG, one per frame)
    --width    frame width in pixels (default 1280)
    --height   frame height in pixels (default 720)
    --step     render every Nth frame; 24 gives a quick preview, 1 the full clip
    --samples  render samples per frame (default 32; lower is faster and grainier)
    --save     also write the built scene as a .blend file at this path, for opening by hand
    --start, --end   render only this range of frames (1 to 360), so a long render can be
               split into parts that run side by side

The clip is 15 seconds at 24 frames a second (360 frames). The camera starts wide and high,
looking at the Sun, and glides in toward the asteroid belt.

NOT TO SCALE. The distances between orbits ARE to scale with each other (one astronomical
unit, the Earth-Sun distance, is ten scene units). The bodies are NOT: a planet drawn at its
true size against a true-scale orbit would be smaller than one pixel, so each body's drawn
radius grows with the logarithm of its real diameter, which keeps the order of sizes right
(Jupiter bigger than Earth bigger than Mars) while making every body visible. The Sun is
drawn smaller than that rule would give it, or it would swallow Mercury's orbit. Any public
use of these pictures must say they are not to scale.

Sources for the numbers, read 2026-10-27:
  * Orbit sizes (semi-major axis, in astronomical units) and diameters (km) of the planets:
    NASA Planetary Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/
    (Mercury 0.387 AU, 4,879 km; Venus 0.723 AU, 12,104 km; Earth 1.000 AU, 12,756 km;
    Mars 1.524 AU, 6,792 km; Jupiter 5.203 AU, 142,984 km).
  * The Sun's diameter, 1,391,400 km (twice the volumetric mean radius of 695,700 km):
    NASA Sun Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
  * The main asteroid belt's extent: its inner edge sits at the 4:1 resonance with Jupiter at
    2.06 AU and its outer edge at the 2:1 resonance at 3.27 AU, with the belt's population
    thinning at the Kirkwood gaps between (drawn here as faint rings with fewer rocks at
    2.50 AU, the 3:1 resonance, and 2.82 AU, the 5:2 resonance):
    Wikipedia, "Asteroid belt" and "Kirkwood gap",
    https://en.wikipedia.org/wiki/Asteroid_belt  https://en.wikipedia.org/wiki/Kirkwood_gap
  * Most main-belt asteroids orbit within a few degrees of the plane of the planets; the
    scatter in height used here (a spread of about 1.5 scene units each side) is a visual
    choice, not a measured figure.
The positions of the planets along their orbits are arbitrary (chosen to spread them out
in the picture), not where they were on any date.

Written 2026-10-27 for the Belt Equation's scripted-animation pilot (docs/blender-pilot/).
"""

import argparse
import math
import os
import random
import sys

import bpy
import bmesh
from mathutils import Matrix
from mathutils import Vector

# ---------------------------------------------------------------- the facts (see sources above)
AU = 10.0                      # scene units per astronomical unit
FPS = 24
SECONDS = 15
FRAMES = FPS * SECONDS

# name, semi-major axis (AU), diameter (km), colour (red, green, blue, 0..1), angle on orbit (degrees)
PLANETS = [
    ("Mercury", 0.387,   4879, (0.55, 0.52, 0.50), 200),
    ("Venus",   0.723,  12104, (0.90, 0.78, 0.55),  40),
    ("Earth",   1.000,  12756, (0.25, 0.45, 0.90), 300),
    ("Mars",    1.524,   6792, (0.85, 0.40, 0.22), 120),
    ("Jupiter", 5.203, 142984, (0.80, 0.68, 0.52),  30),
]
SUN_DIAMETER_KM = 1_391_400
BELT_INNER_AU = 2.06
BELT_OUTER_AU = 3.27
KIRKWOOD_GAPS_AU = (2.50, 2.82)     # faint rings with fewer rocks
BELT_COUNT = 6000
BELT_HALF_THICKNESS = 1.5           # scene units each side of the plane (a visual choice)


def drawn_radius(diameter_km):
    """Visual radius: grows with the logarithm of the real diameter. Not to scale."""
    return 0.32 * math.log10(diameter_km / 1000.0) + 0.05


# ---------------------------------------------------------------- helpers
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(name, color, emission=None, emission_strength=0.0, roughness=0.7):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def add_sphere(name, radius, location, material, segments=48, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location,
                                         segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


def add_orbit_ring(name, radius_au, material, width=0.035):
    """A thin flat ring for a planet's orbit (a circle curve with a small bevel)."""
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius_au * AU, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.bevel_depth = width
    obj.data.bevel_resolution = 2
    obj.data.resolution_u = 64
    obj.data.materials.append(material)
    return obj


def add_belt(material, seed=7):
    """Thousands of small rocks between the belt's inner and outer edges, joined into one mesh."""
    rng = random.Random(seed)
    bm = bmesh.new()
    placed = 0
    while placed < BELT_COUNT:
        # draw a radius uniformly by area, so the belt is evenly dense across its width
        r_au = math.sqrt(rng.uniform(BELT_INNER_AU ** 2, BELT_OUTER_AU ** 2))
        # thin the belt near the Kirkwood gaps: most draws close to a gap are thrown away
        near_gap = min(abs(r_au - g) for g in KIRKWOOD_GAPS_AU)
        if near_gap < 0.04 and rng.random() < 0.8:
            continue
        angle = rng.uniform(0, 2 * math.pi)
        # height above the plane: bell-shaped, most rocks close to the plane
        z = rng.gauss(0, BELT_HALF_THICKNESS * 0.45)
        pos = Vector((r_au * AU * math.cos(angle), r_au * AU * math.sin(angle), z))
        size = rng.uniform(0.05, 0.12)
        m = Vector(pos)
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=size,
                                   matrix=Matrix.Translation(m))
        placed += 1
    mesh = bpy.data.meshes.new("belt")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Belt", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def add_stars(count=1600, radius=600.0, seed=11):
    """A star field: small bright spheres on a huge distant shell, so they never move with the camera much."""
    rng = random.Random(seed)
    bm = bmesh.new()
    for _ in range(count):
        # uniform direction on a sphere
        z = rng.uniform(-1, 1)
        t = rng.uniform(0, 2 * math.pi)
        s = math.sqrt(1 - z * z)
        pos = Vector((s * math.cos(t), s * math.sin(t), z)) * radius
        size = rng.choice((0.3, 0.45, 0.6, 0.85, 1.2))
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=size,
                                   matrix=Matrix.Translation(pos))
    mesh = bpy.data.meshes.new("stars")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Stars", mesh)
    bpy.context.collection.objects.link(obj)
    mat = make_material("StarMat", (0, 0, 0), emission=(1.0, 0.97, 0.9), emission_strength=4.0)
    obj.data.materials.append(mat)
    return obj


def set_world():
    world = bpy.data.worlds.new("Space")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.0025, 0.003, 0.006, 1.0)   # near-black with a hint of blue
    bg.inputs["Strength"].default_value = 1.0


def ease(t):
    """Smooth start and finish (the 'smoothstep' curve)."""
    return t * t * (3 - 2 * t)


def add_camera_move():
    """A 15-second glide: wide and high over the Sun, down and in toward the belt."""
    scene = bpy.context.scene
    target = bpy.data.objects.new("CameraTarget", None)
    scene.collection.objects.link(target)
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 35
    cam_data.clip_end = 5000
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"

    # waypoints (scene units): start wide and high; end low and close to the belt's near edge
    cam_start = Vector((-40.0, -150.0, 95.0))
    cam_end = Vector((10.0, -52.0, 20.0))      # outside the belt, low, looking in across it
    look_start = Vector((0.0, 0.0, 0.0))                 # the Sun
    look_end = Vector((5.0, -19.0, 0.0))                 # a point near the belt's inner edge

    scene.frame_start = 1
    scene.frame_end = FRAMES
    # key every frame along an eased path, so the motion is exactly the curve above
    for f in range(1, FRAMES + 1):
        t = ease((f - 1) / (FRAMES - 1))
        # a gentle sideways arc on the way in so the orbits sweep past rather than just shrinking
        arc = Vector((math.sin(t * math.pi) * 18.0, 0.0, 0.0))
        cam.location = cam_start.lerp(cam_end, t) + arc
        target.location = look_start.lerp(look_end, t)
        cam.keyframe_insert("location", frame=f)
        target.keyframe_insert("location", frame=f)
    return cam


def set_render(width, height, step, samples, out_dir):
    scene = bpy.context.scene
    # EEVEE's id changed between Blender versions; pick whichever this build has
    engines = {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
    scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_step = step
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = os.path.join(out_dir, "frame_")
    scene.eevee.taa_render_samples = samples
    # a filmic look so the bright Sun rolls off instead of clipping to flat white
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "AgX - Medium High Contrast" if scene.view_settings.view_transform == "AgX" else "None"

    # glow around the Sun and the stars, done in the compositor (the renderer's own bloom
    # was removed in the newer EEVEE)
    add_glare(scene)


def add_glare(scene):
    """Add a soft bloom in the compositor. Handles the API change in Blender 5."""
    if hasattr(scene, "compositing_node_group"):        # Blender 5.0 and later
        tree = bpy.data.node_groups.new("Compositing", "CompositorNodeTree")
        scene.compositing_node_group = tree
        nodes, links = tree.nodes, tree.links
        rl = nodes.new("CompositorNodeRLayers")
        out = nodes.new("NodeGroupOutput")
        tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        glare = nodes.new("CompositorNodeGlare")
        _set_glare(glare)
        links.new(rl.outputs["Image"], glare.inputs["Image"])
        links.new(glare.outputs["Image"], out.inputs[0])
    else:                                               # Blender 4.x
        scene.use_nodes = True
        tree = scene.node_tree
        nodes, links = tree.nodes, tree.links
        for n in list(nodes):
            nodes.remove(n)
        rl = nodes.new("CompositorNodeRLayers")
        comp = nodes.new("CompositorNodeComposite")
        glare = nodes.new("CompositorNodeGlare")
        _set_glare(glare)
        links.new(rl.outputs["Image"], glare.inputs["Image"])
        links.new(glare.outputs["Image"], comp.inputs["Image"])


def _set_glare(glare):
    """Set the glare node up as a soft bloom. The node's settings moved from properties to
    input sockets in Blender 5, so both forms are tried."""
    if "Type" in glare.inputs:                          # Blender 5: settings are sockets
        wanted = {"Type": "Bloom", "Quality": "Medium", "Threshold": 1.0, "Strength": 0.2, "Size": 0.7}
        for name, value in wanted.items():
            try:
                glare.inputs[name].default_value = value
            except Exception as exc:                    # a menu value this build lacks, say
                print(f"glare: could not set {name}={value!r}: {exc}")
    else:                                               # Blender 4: settings are properties
        types = {e.identifier for e in glare.bl_rna.properties["glare_type"].enum_items}
        glare.glare_type = "BLOOM" if "BLOOM" in types else "FOG_GLOW"
        for name, value in (("threshold", 1.0), ("mix", 0.0), ("size", 7), ("quality", "MEDIUM")):
            if hasattr(glare, name):
                setattr(glare, name, value)


# ---------------------------------------------------------------- build
def build():
    clear_scene()
    set_world()

    # the Sun: a glowing sphere plus a point light at its centre
    sun_r = drawn_radius(SUN_DIAMETER_KM) * 1.4      # about 1.5 units; Mercury orbits at 3.87
    sun_mat = make_material("SunMat", (1.0, 0.85, 0.55), emission=(1.0, 0.78, 0.45), emission_strength=30.0)
    add_sphere("Sun", sun_r, (0, 0, 0), sun_mat, segments=64, rings=32)
    light_data = bpy.data.lights.new("SunLight", "POINT")
    light_data.energy = 5.0e6
    light_data.shadow_soft_size = sun_r
    light_data.color = (1.0, 0.95, 0.85)
    light = bpy.data.objects.new("SunLight", light_data)
    bpy.context.collection.objects.link(light)

    # orbit rings and planets
    ring_mat = make_material("OrbitMat", (0.0, 0.0, 0.0), emission=(0.45, 0.55, 0.75), emission_strength=1.2)
    for name, a_au, d_km, color, angle in PLANETS:
        add_orbit_ring(f"{name}Orbit", a_au, ring_mat)
        th = math.radians(angle)
        pos = (a_au * AU * math.cos(th), a_au * AU * math.sin(th), 0.0)
        # a touch of self-glow so the far planets still read as dots at the wide view (a visual choice)
        mat = make_material(f"{name}Mat", color, emission=color, emission_strength=0.6, roughness=0.8)
        add_sphere(name, drawn_radius(d_km), pos, mat)

    # the belt: a dim grey, with a touch of glow so the far side still reads as a band
    belt_mat = make_material("BeltMat", (0.50, 0.47, 0.42), emission=(0.7, 0.66, 0.6), emission_strength=0.22, roughness=0.95)
    add_belt(belt_mat)

    add_stars()
    add_camera_move()


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--step", type=int, default=1)
    p.add_argument("--samples", type=int, default=32)
    p.add_argument("--save", default=None)
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=FRAMES)
    p.add_argument("--no-render", action="store_true")
    args = p.parse_args(argv)

    os.makedirs(args.out, exist_ok=True)
    build()
    set_render(args.width, args.height, args.step, args.samples, args.out)
    if args.save:
        bpy.ops.wm.save_as_mainfile(filepath=args.save)
    if not args.no_render:
        bpy.context.scene.frame_start = args.start
        bpy.context.scene.frame_end = args.end
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
