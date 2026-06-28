from ursina import *
import math
import os
from PIL import Image

application.development_mode = False

app = Ursina()

def generate_transparent_clouds(input_path, output_path):
    base_dir = os.path.dirname(__file__)
    full_input_path = None

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().startswith('earth clouds'):
                full_input_path = os.path.join(root, f)
                break
        if full_input_path:
            break

    if not full_input_path or not os.path.exists(full_input_path):
        full_input_path = os.path.join(base_dir, 'image', input_path)

    out_dir = os.path.dirname(full_input_path) if os.path.exists(full_input_path) else os.path.join(base_dir, 'image')
    full_output_path = os.path.join(out_dir, output_path)

    if not os.path.exists(full_output_path) and os.path.exists(full_input_path):
        img = Image.open(full_input_path).convert("RGBA")
        data = img.getdata()
        new_data = []
        for item in data:
            brightness = item[0]
            new_data.append((255, 255, 255, brightness))
        img.putdata(new_data)
        img.save(full_output_path)

generate_transparent_clouds('earth clouds.jpg', 'earth_clouds_transparent.png')

focus_target = None

def create_ring_mesh(inner_radius=0.22, outer_radius=1.0, resolution=80):
    verts = []
    tris = []
    uvs = []

    for i in range(resolution + 1):
        angle = (i / resolution) * math.pi * 2
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        verts.append((cos_a * inner_radius, 0, sin_a * inner_radius))
        verts.append((cos_a * outer_radius, 0, sin_a * outer_radius))

        t = i / resolution
        uvs.append((0, t))
        uvs.append((1, t))

    for i in range(resolution):
        v0 = i * 2
        v1 = v0 + 1
        v2 = v0 + 2
        v3 = v0 + 3
        tris.append((v0, v1, v2))
        tris.append((v1, v3, v2))

    return Mesh(vertices=verts, triangles=tris, uvs=uvs)

def update():
    mercury_orbit.rotation_y += 416.7 * time.dt
    venus_orbit.rotation_y += 162.6 * time.dt
    earth_orbit.rotation_y += 100 * time.dt
    mars_orbit.rotation_y += 53.2 * time.dt
    jupiter_orbit.rotation_y += 8.4 * time.dt
    saturn_orbit.rotation_y += 3.4 * time.dt
    uranus_orbit.rotation_y += 1.2 * time.dt
    neptune_orbit.rotation_y += 0.6 * time.dt
    moon_orbit.rotation_y += 1338.7 * time.dt

    sun.rotation_y += 3.7 * time.dt
    mercury.spin += 1.7 * time.dt
    venus.spin -= 40.0 * time.dt
    earth.spin += 100 * time.dt
    mars.spin += 97.1 * time.dt
    jupiter.spin += 243.9 * time.dt
    saturn.spin += 222.2 * time.dt
    uranus.spin -= 138.9 * time.dt
    neptune.spin += 149.3 * time.dt

    mercury.rotation_y = mercury.spin - mercury_orbit.rotation_y
    venus.rotation_y = venus.spin - venus_orbit.rotation_y
    earth.rotation_y = earth.spin - earth_orbit.rotation_y
    mars.rotation_y = mars.spin - mars_orbit.rotation_y
    jupiter.rotation_y = jupiter.spin - jupiter_orbit.rotation_y
    saturn.rotation_y = saturn.spin - saturn_orbit.rotation_y
    uranus.rotation_y = uranus.spin - uranus_orbit.rotation_y
    neptune.rotation_y = neptune.spin - neptune_orbit.rotation_y

    cloud_layer.rotation_y += time.dt * 0.4
    cloud_layer.rotation_x += time.dt * 0.05

    if focus_target:
        cam.world_position = focus_target.world_position

cam = EditorCamera(distance=100)

window.fullscreen = True
window.borderless = True

sun = Entity(model='sphere',
             collider='sphere',
             texture='sun.jpg',
             scale=(25,25,25),
             position=(0,0,0),
             )

mercury_orbit = Entity(parent=sun,)
mercury = Entity(parent=mercury_orbit,
           model='sphere',
           collider='sphere',
           texture='mercury.jpg',
           world_scale=(0.085,0.085,0.085),
           world_position=(27.5,0,27.5),
           )
mercury.spin = 0

venus_orbit = Entity(parent=sun,)
venus = Entity(parent=venus_orbit,
               model='sphere',
               collider='sphere',
               texture='venus.jpg',
               world_scale=(0.215,0.215,0.215),
               world_position=(51,0,51),
               )
venus.spin = 0

earth_orbit = Entity(parent=sun,)
earth = Entity(parent=earth_orbit,
               model='sphere',
               collider='sphere',
               texture='earth day.jpg',
               world_scale=(0.23,0.23,0.23),
               world_position=(70.5,0,70.5),
               )
earth.spin = 0

cloud_layer = Entity(
    parent=earth,
    model='sphere',
    texture='earth_clouds_transparent.png',
    scale=1.008,
    double_sided=True
)

moon_orbit = Entity(parent=earth,)
moon = Entity(parent=moon_orbit,
              model='sphere',
              collider='sphere',
              texture='moon.jpg',
              world_scale=(0.06,0.06,0.06),
              world_position=(71.5,0,71.5),
              )

mars_orbit = Entity(parent=sun,)
mars = Entity(parent=mars_orbit,
              model='sphere',
              collider='sphere',
              texture='mars.jpg',
              world_scale=(0.12,0.12,0.12),
              world_position=(108,0,108),
              )
mars.spin = 0

#I could not make the asteroid belt :(

jupiter_orbit = Entity(parent=sun,)
jupiter = Entity(parent=jupiter_orbit,
                 model='sphere',
                 collider='sphere',
                 texture='jupiter.jpg',
                 world_scale=(2.51,2.51,2.51),
                 world_position=(368,0,368),
                 )
jupiter.spin = 0

saturn_orbit = Entity(parent=sun,)
saturn = Entity(parent=saturn_orbit,
                 model='sphere',
                 collider='sphere',
                 texture='saturn.jpg',
                 world_scale=(2.09,2.09,2.09),
                 world_position=(677.5,0,677.5),
                 )
saturn.spin = 0

saturn_ring = Entity(
    parent=saturn,
    model=create_ring_mesh(inner_radius=0.22, outer_radius=1.0, resolution=80),
    texture='saturn ring.png',
    double_sided=True,
    world_position=(677.5, 0, 677.5),
    world_scale=(4.745, 4.745, 4.745),
    rotation_x=0,
)

uranus_orbit = Entity(parent=sun,)
uranus = Entity(parent=uranus_orbit,
                 model='sphere',
                 collider='sphere',
                 texture='uranus.jpg',
                 world_scale=(0.91,0.91,0.91),
                 world_position=(1357.5,0,1357.5),
                 )
uranus.spin = 0

neptune_orbit = Entity(parent=sun,)
neptune = Entity(parent=neptune_orbit,
                 model='sphere',
                 collider='sphere',
                 texture='neptune.jpg',
                 world_scale=(0.885,0.885,0.885),
                 world_position=(2124.5,0,2124.5),
                 )
neptune.spin = 0

sky = load_texture('stars milky way.jpg')
background = Sky(texture=sky)

background_music1 = Audio(
    'c-style-963hz-energie-arcturienne.mp3',
    loop=True,
    autoplay=True,
    volume=1
)
background_music2 = Audio(
    'c-style-528-hz-resonance-solaire-arcturienne.mp3',
    loop=True,
    autoplay=True,
    volume=1
)

targets = {
    'Sun': sun, 'Moon': moon, 'Mercury': mercury, 'Venus': venus,
    'Earth': earth, 'Mars': mars, 'Jupiter': jupiter,
    'Saturn': saturn, 'Uranus': uranus, 'Neptune': neptune
}

menu_buttons = []

menu_btn = Button(
    text='Select Target',
    color=color.azure,
    scale=(0.18, 0.04),
    origin=(-0.5, 0.5),
    position=window.top_left + Vec2(0.02, -0.02)
)

free_btn = Button(
    text='Free View',
    color=color.orange,
    scale=(0.14, 0.04),
    origin=(-0.5, 0.5),
    position=window.top_left + Vec2(0.21, -0.02)
)

def set_camera_target(target_entity):
    global focus_target
    focus_target = target_entity
    if target_entity:
        cam.distance = max(2, target_entity.world_scale.x * 3.5)

free_btn.on_click = lambda: set_camera_target(None)

def toggle_menu():
    for b in menu_buttons:
        b.enabled = not b.enabled

menu_btn.on_click = toggle_menu

for i, (name, entity) in enumerate(targets.items()):
    b = Button(
        text=name,
        scale=(0.18, 0.035),
        origin=(-0.5, 0.5),
        position=menu_btn.position + Vec2(0, -0.045 - (i * 0.038)),
        enabled=False
    )
    b.on_click = lambda e=entity: [set_camera_target(e), toggle_menu()]
    menu_buttons.append(b)


def freeze_time():
    application.paused = not application.paused
    if application.paused:
        btn.text = "Resume Time"
    else:
        btn.text = "Freeze Time"

btn = Button(
    text='Freeze Time',
    color=color.black,
    scale=(0.20, 0.05),
    position=window.top_right + Vec2(-0.08, -0.02)
)

btn.on_click = freeze_time

app.run()