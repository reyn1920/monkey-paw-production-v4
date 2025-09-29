
# Run inside Blender's Text Editor → Run Script
import bpy, math, os

# ---------- CONFIG ----------
PRESET = 'gradient'   # 'gradient' | 'particles' | 'neonorbs'
RES_X, RES_Y = 1920, 1080
FPS = 30
DURATION_SEC = 8
OUTPUT_DIR = bpy.path.abspath('//renders')
MAKE_ALPHA = True  # Film Transparent + RGBA

# ---------- SETUP SCENE ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.engine = 'BLENDER_EEVEE'
scn.eevee.use_bloom = True
scn.eevee.bloom_intensity = 0.05
scn.eevee.use_ssr = True
scn.render.resolution_x = RES_X
scn.render.resolution_y = RES_Y
scn.render.fps = FPS
scn.frame_start = 1
scn.frame_end = int(DURATION_SEC*FPS)
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_mode = 'RGBA'  # include alpha
scn.render.filepath = os.path.join(OUTPUT_DIR, PRESET, '')

# Transparent background
scn.render.film_transparent = MAKE_ALPHA

# Camera
cam_data = bpy.data.cameras.new('Cam')
cam = bpy.data.objects.new('Cam', cam_data)
bpy.context.collection.objects.link(cam)
scn.camera = cam
cam.location = (0, -6, 2.4)
cam.rotation_euler = (math.radians(75), 0, 0)

# Light
light_data = bpy.data.lights.new('Key', type='AREA')
light = bpy.data.objects.new('Key', light_data)
bpy.context.collection.objects.link(light)
light.location = (2.5, -2.5, 4)
light.data.energy = 300

# World
world = bpy.data.worlds.new('World')
scn.world = world
world.use_nodes = True
wn = world.node_tree
for n in wn.nodes: wn.nodes.remove(n)
out = wn.nodes.new('ShaderNodeOutputWorld')
bg = wn.nodes.new('ShaderNodeBackground')
bg.inputs[1].default_value = 1.0
wn.links.new(bg.outputs['Background'], out.inputs['Surface'])

# ---------- PRESETS ----------
def make_gradient():
    p = bpy.data.objects.new('Plane', bpy.data.meshes.new('PlaneMesh'))
    bpy.context.collection.objects.link(p)
    bpy.context.view_layer.objects.active = p
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_plane_add(size=2)
    bpy.ops.object.editmode_toggle()

    # Big plane acts as backdrop; material: animated gradient
    mat = bpy.data.materials.new('GradMat')
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    grad = nt.nodes.new('ShaderNodeTexGradient')
    tex = nt.nodes.new('ShaderNodeTexCoord')
    colramp = nt.nodes.new('ShaderNodeValToRGB')
    colramp.color_ramp.elements[0].position = 0.2
    colramp.color_ramp.elements[0].color = (0.05,0.1,0.3,1)
    colramp.color_ramp.elements[1].position = 0.9
    colramp.color_ramp.elements[1].color = (0.05,0.6,0.9,1)
    map1 = nt.nodes.new('ShaderNodeMapping'); map1.vector_type='POINT'
    nt.links.new(tex.outputs['Generated'], map1.inputs['Vector'])
    nt.links.new(map1.outputs['Vector'], grad.inputs['Vector'])
    nt.links.new(grad.outputs['Fac'], colramp.inputs['Fac'])
    nt.links.new(colramp.outputs['Color'], em.inputs['Color'])
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])

    # animate mapping rotation for subtle movement
    map1.inputs['Rotation'].default_value[2] = 0.0
    map1.inputs['Rotation'].keyframe_insert('default_value', index=2, frame=1)
    map1.inputs['Rotation'].default_value[2] = 6.283  # 360deg
    map1.inputs['Rotation'].keyframe_insert('default_value', index=2, frame=scn.frame_end)

    p.data = bpy.data.meshes.new('Backdrop')
    bpy.context.collection.objects.link(p)
    p = bpy.data.objects['Plane']
    p.location = (0,0,0)
    p.scale = (12, 12, 1)
    p.data.materials.append(mat)

def make_particles():
    # simple particle plane with emission spheres
    bpy.ops.mesh.primitive_plane_add(size=16, location=(0,0,0))
    plane = bpy.context.active_object
    mat_bg = bpy.data.materials.new('BG')
    mat_bg.use_nodes=True
    nt = mat_bg.node_tree
    for n in nt.nodes: nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value=0.2
    em.inputs['Color'].default_value = (0.02,0.06,0.12,1)
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    plane.data.materials.append(mat_bg)

    bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
    ps = plane.particle_systems[0]; pset = ps.settings
    pset.count = 600
    pset.frame_start = 1; pset.frame_end = scn.frame_end
    pset.lifetime = scn.frame_end
    pset.emit_from = 'FACE'
    pset.physics_type = 'NEWTON'
    pset.normal_factor = 0.0
    pset.object_align_factor = (0,0,0.02)
    pset.render_type = 'HALO'
    pset.particle_size = 0.02
    pset.use_dynamic_rotation = True

def make_neonorbs():
    import random
    for i in range(30):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(random.uniform(-4,4),random.uniform(-2,2), random.uniform(0.5,3)))
        s = bpy.context.active_object
        mat = bpy.data.materials.new(f'Orb_{i}'); mat.use_nodes=True
        nt = mat.node_tree
        for n in nt.nodes: nt.nodes.remove(n)
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        em = nt.nodes.new('ShaderNodeEmission')
        hue = i/30.0
        em.inputs['Color'].default_value=(0.2+0.8*hue,0.4,1.0-hue,1)
        em.inputs['Strength'].default_value=5.0
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
        s.data.materials.append(mat)
        # animate subtle Z float
        s.keyframe_insert('location', frame=1)
        s.location.z += 0.3
        s.keyframe_insert('location', frame=scn.frame_end)

if PRESET=='gradient': make_gradient()
elif PRESET=='particles': make_particles()
else: make_neonorbs()

print('Ready. Render Animation to output PNG RGBA sequence.')
