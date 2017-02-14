import numpy as np
import pyglet
from pyglet.window import key
import ratcave as rc
import config as cfg
from collections import defaultdict
import sys


reader = rc.WavefrontReader('resources/maze.obj')

arena = reader.get_mesh('Cube')
arena.texture = rc.Texture.from_image(rc.resources.img_uvgrid)
sphere = reader.get_mesh('Sphere')#, position=(0, 0, -1))
cylinder = reader.get_mesh('Cylinder')#, position=(0, 0, -1))


scene = rc.Scene(meshes=[arena, sphere, cylinder], bgColor=(1., 0., 0.))
scene.gl_states = scene.gl_states[:-1]
camera = scene.camera
camera.rotation.axes = 'sxyz'
camera.position.y = .3
camera.projection.z_near = .001
camera.projection.z_far = 4.5


class FPSGame(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(FPSGame, self).__init__(*args, **kwargs)
        self.set_exclusive_mouse(True)
        self.keys = defaultdict(bool)

        pyglet.clock.schedule(self.move_player)

    def on_draw(self):
        with rc.resources.genShader:
            scene.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        viewport = camera.projection.viewport
        rel_x, rel_y = float(x) / viewport.width - .5, float(y) / viewport.height - .5
        rel_dx, rel_dy = float(dx) / viewport.width, float(dy) / viewport.height
        camera.rotation.y -= rel_dx * 180
        camera.rotation.x += rel_dy * 45
        camera.rotation.z = 0

    def on_resize(self, width, height):
        camera.projection.aspect = float(width) / height
        camera.projection.update()
        print(camera.projection.viewport)

    def on_key_press(self, sym, mod):
        self.keys[sym] = True

    def on_key_release(self, sym, mod):
        self.keys[sym] = False
        if sym == key.F:
            self.set_fullscreen(not self.fullscreen)
        if sym == key.ESCAPE:
            self.close()
            sys.exit()

    def move_player(self, dt):
        step_fw = np.array(camera.orientation) * cfg.PLAYER_SPEED * dt
        if window.keys[key.W]:
            camera.position.x += step_fw[0]
            camera.position.z += step_fw[2]
        if window.keys[key.S]:
            camera.position.x += -step_fw[0]
            camera.position.z += -step_fw[2]




window = FPSGame(fullscreen=cfg.FULLSCREEN)
pyglet.app.run()