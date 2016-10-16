import sdl2hl
import engine
import math
from component import verify_attrs
import rectangle


class Camera(object):

    def __init__(self, renderer, entity, layers=[], hud=[]):
        verify_attrs(entity, ('x', 'y', 'width', 'height', 'angle', 'screen_x', 'screen_y', 'screen_width', 'screen_height'))
        self.entity = entity
        self.hud_entities = hud
        self.layers = layers
        self.renderer = renderer
        self.pixel_format = sdl2hl.PixelFormat.argb8888

        self.transform_point = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle
        self.transform_width = self.world_to_camera_width
        self.transform_height = self.world_to_camera_height

    def render(self):

        screen_x = int_or_percent(self.entity.screen_x, engine.get().window.size[0])
        screen_y = int_or_percent(self.entity.screen_y, engine.get().window.size[1])

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self._screen_width(), self._screen_height())

        self.renderer.render_target = texture

        self.transform_point = self.world_to_camera
        self.transform_angle = self.world_to_camera_angle
        self.transform_width = self.world_to_camera_width
        self.transform_height = self.world_to_camera_height

        for layer in self.layers:
            layer.draw(self)

        self.transform_point = self.hud_to_camera
        self.transform_angle = self.hud_to_camera_angle
        self.transform_width = self.hud_to_camera_length
        self.transform_height = self.hud_to_camera_height

        for e in self.hud_entities:
            e.handle('draw', self)

        self.renderer.render_target = None

        self.renderer.copy(texture,
                           source_rect=None,
                           dest_rect=sdl2hl.Rect(screen_x, screen_y, self._screen_width(), self._screen_height()))

    def _screen_height(self):
        return int_or_percent(self.entity.screen_height, engine.get().window.size[1])

    def _screen_width(self):
        return int_or_percent(self.entity.screen_width, engine.get().window.size[0])

    def screen_percent_point(self, p):
        return (int_or_percent(p[0],  engine.get().window.size[0]), int_or_percent(p[1], engine.get().window.size[1]))

    def hud_to_camera(self, p):
        p = self.screen_percent_point(p)
        x = p[0]
        y = self._screen_height() - p[1]

        return int(x), int(y)

    def hud_to_camera_angle(self, a):
        return -a

    def hud_to_camera_length(self, w):
        return int_or_percent(w, engine.get().window.size[0])

    def hud_to_camera_height(self, h):
        return int_or_percent(h, engine.get().window.size[1])


    def world_to_camera(self, p):
        tx = p[0] - self.entity.x
        ty = p[1] - self.entity.y

        if self.entity.angle == 0:
            rx = tx
            ry = ty
        else:
            rx = tx * math.cos(math.radians(self.entity.angle)) + ty * math.sin(math.radians(self.entity.angle))
            ry = ty * math.cos(math.radians(self.entity.angle)) - tx * math.sin(math.radians(self.entity.angle))

        cx = rx + self.entity.width / 2
        cy = ry + self.entity.height / 2

        sx = self.transform_width(cx)
        sy = self.transform_height(cy)

        return int(sx), int(self._screen_height() - sy)

    def world_to_camera_angle(self, a):
        return self.entity.angle - a

    def world_to_camera_width(self, w):
        return int(float(self._screen_width())/self.entity.width*w)

    def world_to_camera_height(self, h):
        return int(float(self._screen_height()) / self.entity.height * h)

    def draw_rect(self, c, r):
        points = [r.top_left, r.bottom_left, r.bottom_right, r.top_right, r.top_left]
        transformed_points = map(self.transform_point, points)
        sdlpoints = map(lambda x : sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_image(self, r, texture):
        x,y = self.transform_point(r.center)
        w,h = self.transform_width(r.w), self.transform_height(r.h)
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - w/2), int(y - h/2), w,h), rotation=self.transform_angle(r.a))

    def clear(self, colour):
        self.renderer.draw_color = colour
        self.renderer.clear()

    def draw_line(self, c, p1, p2):
        points = [self.transform_point(p1), self.transform_point(p2)]
        sdlpoints = map(lambda x: sdl2hl.Point(x[0], x[1]), points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_lines(self, c, points):
        transformed_points = map(self.transform_point, points)
        sdlpoints = map(lambda x: sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_filled_circle(self, c, p, r):
        p = self.transform_point(p)
        r = self.transform_width(r)

        primitives = sdl2hl.gfx.GfxPrimitives(self.renderer)
        primitives.draw_filled_circle(p[0],p[1],r,c)


def int_or_percent(value, base):
    if isinstance(value, str):
        if value.endswith("%"):
            percent = int(value[:-1])/100.0
            return int(percent * base)
    else:
        return int(value)
