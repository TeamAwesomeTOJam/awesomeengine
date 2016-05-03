import sdl2hl
import engine
import math
from component import verify_attrs
import rectangle


class Camera(object):

    def __init__(self, renderer, entity, layers=[], hud=[]):
        verify_attrs(entity, ['x', 'y', 'width', 'height', 'angle', 'screen_x', 'screen_y', 'screen_width', 'screen_height'])
        self.entity = entity
        self.hud_entities = hud
        self.layers = layers
        self.renderer = renderer
        self.pixel_format = sdl2hl.PixelFormat.argb8888

        self.transform = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle

    def render(self):

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.width, self.entity.height)

        self.renderer.render_target = texture

        self.transform = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle

        for layer in self.layers:
            layer.draw(self)

        zoomed_texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.screen_width, self.entity.screen_height)

        self.renderer.render_target = zoomed_texture

        self.renderer.copy(texture)

        self.transform = self.hud_to_camera
        self.transform_angle = self.hud_to_camera_angle

        for e in self.hud_entities:
            e.handle('draw', self)

        self.renderer.render_target = None

        self.renderer.copy(zoomed_texture,
                           source_rect=None,
                           dest_rect=sdl2hl.Rect(self.entity.screen_x, self.entity.screen_y, self.entity.screen_width, self.entity.screen_height))

    def hud_to_camera(self, p):
        x = p[0]
        y = self.entity.screen_height - p[1]

        return int(x), int(y)

    def hud_to_camera_angle(self, a):
        return -a


    def world_to_camera(self, p):
        tx = p[0] - self.entity.x
        ty = p[1] - self.entity.y

        rx = tx * math.cos(math.radians(self.entity.angle)) + ty * math.sin(math.radians(self.entity.angle))
        ry = ty * math.cos(math.radians(self.entity.angle)) - tx * math.sin(math.radians(self.entity.angle))

        cx = rx + self.entity.width / 2
        cy = self.entity.height / 2 - ry

        return int(cx), int(cy)

    def world_to_camera_angle(self, a):
        return self.entity.angle - a

    def draw_rect(self, c, r):
        points = [r.top_left, r.bottom_left, r.bottom_right, r.top_right, r.top_left]
        transformed_points = map(self.transform, points)
        sdlpoints = map(lambda x : sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_image(self, r, texture):
        x,y = self.transform(r.center)
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - r.w/2), int(y - r.h/2), r.w, r.h), rotation=self.transform_angle(r.a))

    def clear(self, colour):
        self.renderer.draw_color = colour
        self.renderer.clear()