import numpy as np
import pyglet
from pyglet.window import key
import ratcave as rc
from collections import defaultdict
import sys


class FPSGame(pyglet.window.Window):

    player_speed = .7

    def __init__(self, player, scene, *args, **kwargs):
        super(FPSGame, self).__init__(*args, **kwargs)
        self.set_exclusive_mouse(True)
        self.keys = defaultdict(bool)

        self.player = player
        pyglet.clock.schedule(self.move_player)

        self.scene = scene

    def on_draw(self):
        with rc.resources.genShader:
            self.scene.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        viewport = self.scene.camera.projection.viewport
        rel_x, rel_y = float(x) / viewport.width - .5, float(y) / viewport.height - .5
        rel_dx, rel_dy = float(dx) / viewport.width, float(dy) / viewport.height
        self.player.rotation.y -= rel_dx * 180
        self.player.rotation.x += rel_dy * 45
        self.player.rotation.z = 0

    def on_resize(self, width, height):
        self.scene.camera.projection.aspect = float(width) / height
        self.scene.camera.projection.update()

    def on_key_press(self, sym, mod):
        self.keys[sym] = True

    def on_key_release(self, sym, mod):
        self.keys[sym] = False
        if sym == key.F:
            self.set_fullscreen(not self.fullscreen)
        if sym == key.M:
            self.set_exclusive_mouse(not self._mouse_exclusive  )
        if sym == key.ESCAPE:
            self.close()
            sys.exit()

    def move_player(self, dt):
        step_fw = np.array(self.player.orientation) * self.player_speed * dt
        player, keys = self.player, self.keys
        if keys[key.W]:
            player.position.x += step_fw[0]
            player.position.z += step_fw[2]
        if keys[key.S]:
            player.position.x += -step_fw[0]
            player.position.z += -step_fw[2]


def main():

    FULLSCREEN = True

    reader = rc.WavefrontReader('resources/maze.obj')

    arena = reader.get_mesh('Cube')
    arena.texture = rc.Texture.from_image(rc.resources.img_uvgrid)
    sphere = reader.get_mesh('Sphere')  # , position=(0, 0, -1))
    cylinder = reader.get_mesh('Cylinder')  # , position=(0, 0, -1))

    player = rc.Camera(projection=rc.PerspectiveProjection(z_near=.001, z_far=4.5), position=(0, .3, 0))
    player.rotation.axes = 'sxyz'

    scene = rc.Scene(meshes=[arena, sphere, cylinder], camera=player, bgColor=(1., 0., 0.))
    scene.gl_states = scene.gl_states[:-1]

    window = FPSGame(player=player, scene=scene, fullscreen=FULLSCREEN)
    pyglet.app.run()


if __name__ == '__main__':
    main()