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

        self.transform_point = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle
        self.transform_length = self.world_to_camera_length

    def render(self):

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.screen_width, self.entity.screen_height)

        self.renderer.render_target = texture

        self.transform_point = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle
        self.transform_length = self.world_to_camera_length

        for layer in self.layers:
            layer.draw(self)

        self.transform_point = self.hud_to_camera
        self.transform_angle = self.hud_to_camera_angle
        self.transform_length = self.hud_to_camera_length

        for e in self.hud_entities:
            e.handle('draw', self)

        self.renderer.render_target = None

        self.renderer.copy(texture,
                           source_rect=None,
                           dest_rect=sdl2hl.Rect(self.entity.screen_x, self.entity.screen_y, self.entity.screen_width, self.entity.screen_height))

    def hud_to_camera(self, p):
        x = p[0]
        y = self.entity.screen_height - p[1]

        return int(x), int(y)

    def hud_to_camera_angle(self, a):
        return -a

    def hud_to_camera_length(self, l):
        return l


    def world_to_camera(self, p):
        tx = p[0] - self.entity.x
        ty = p[1] - self.entity.y

        rx = tx * math.cos(math.radians(self.entity.angle)) + ty * math.sin(math.radians(self.entity.angle))
        ry = ty * math.cos(math.radians(self.entity.angle)) - tx * math.sin(math.radians(self.entity.angle))

        cx = rx + self.entity.width / 2
        cy = ry + self.entity.height / 2

        sx = float(self.entity.screen_width) / self.entity.width * cx
        sy = float(self.entity.screen_height) / self.entity.height * cy

        return int(sx), int(self.entity.screen_height - sy)

    def world_to_camera_angle(self, a):
        return self.entity.angle - a

    def world_to_camera_length(self, l):
        return int(float(self.entity.screen_width)/self.entity.width*l)

    def draw_rect(self, c, r):
        points = [r.top_left, r.bottom_left, r.bottom_right, r.top_right, r.top_left]
        transformed_points = map(self.transform_point, points)
        sdlpoints = map(lambda x : sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_image(self, r, texture):
        x,y = self.transform_point(r.center)
        w,h = self.transform_length(r.w), self.transform_length(r.h)
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - w/2), int(y - h/2), w,h), rotation=self.transform_angle(r.a))

    def clear(self, colour):
        self.renderer.draw_color = colour
        self.renderer.clear()