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
        self.transform_width = self.world_to_camera_width
        self.transform_height = self.world_to_camera_height

    def render(self):

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.screen_width, self.entity.screen_height)

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
                           dest_rect=sdl2hl.Rect(self.entity.screen_x, self.entity.screen_y, self.entity.screen_width, self.entity.screen_height))

    def hud_to_camera(self, p):
        x = p[0]
        y = self.entity.screen_height - p[1]

        return int(x), int(y)

    def hud_to_camera_angle(self, a):
        return -a

    def hud_to_camera_length(self, w):
        return w

    def hud_to_camera_height(self, h):
        return h


    def world_to_camera(self, p):
        tx = p[0] - self.entity.x
        ty = p[1] - self.entity.y

        rx = tx * math.cos(math.radians(self.entity.angle)) + ty * math.sin(math.radians(self.entity.angle))
        ry = ty * math.cos(math.radians(self.entity.angle)) - tx * math.sin(math.radians(self.entity.angle))

        cx = rx + self.entity.width / 2
        cy = ry + self.entity.height / 2

        sx = self.transform_width(cx)
        sy = self.transform_height(cy)

        return int(sx), int(self.entity.screen_height - sy)

    def world_to_camera_angle(self, a):
        return self.entity.angle - a

    def world_to_camera_width(self, w):
        return int(float(self.entity.screen_width)/self.entity.width*w)

    def world_to_camera_height(self, h):
        return int(float(self.entity.screen_height) / self.entity.height * h)

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

    def draw_text(self, colour, font, top_left, text):
        surface = self.font.render_solid(text, colour)
        texture = sdl2hl.Texture.from_surface(self.renderer, surface)
        x , y = self.transfrom((top_left))
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(x,y,texture.w, texture.h))