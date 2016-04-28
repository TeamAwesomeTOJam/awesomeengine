import sdl2hl
import engine
import math
from component import verify_attrs
import rectangle


class Camera(object):

    def __init__(self, entity, screen_x, screen_y, screen_width, screen_height, renderer):
        verify_attrs(entity, ['x', 'y', 'width', 'height', 'angle'])
        self.entity = entity
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.renderer = renderer
        self.pixel_format = sdl2hl.PixelFormat.argb8888

        self.background_colour = (0, 0, 0, 255)

    def render(self):

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.width, self.entity.height)

        self.renderer.render_target = texture
        self.renderer.draw_color = self.background_colour
        self.renderer.clear()

        draw_width, draw_height = get_bounding_box(self.entity.width, self.entity.height, self.entity.angle)
        draw_x = self.entity.x - draw_width / 2
        draw_y = self.entity.y - draw_height / 2

        to_draw = engine.get_engine().entity_manager.get_in_area('draw', rectangle.from_entity(self.entity))
        for e in to_draw:
            e.handle('draw', self)

        self.renderer.render_target = None

        self.renderer.copy(texture,
                           source_rect=None,
                           dest_rect=sdl2hl.Rect(self.screen_x, self.screen_y, self.screen_width, self.screen_height))

    def world_to_camera(self, p):
        tx = p[0] - self.entity.x
        ty = p[1] - self.entity.y

        rx = tx * math.cos(math.radians(self.entity.angle)) + ty * math.sin(math.radians(self.entity.angle))
        ry = ty * math.cos(math.radians(self.entity.angle)) - tx * math.sin(math.radians(self.entity.angle))

        cx = rx + self.entity.width / 2
        cy = self.entity.height / 2 - ry

        return int(cx), int(cy)

    def draw_rect(self, c, r):
        points = [r.top_left, r.bottom_left, r.bottom_right, r.top_right, r.top_left]
        transformed_points = map(self.world_to_camera, points)
        sdlpoints = map(lambda x : sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_image(self, r, texture):
        x,y = self.world_to_camera(r.center)
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - r.w/2), int(y - r.h/2), r.w, r.h), rotation=self.entity.angle - r.a)


def get_bounding_box(w, h, a):
    cosw = w*math.cos(math.radians(a))
    sinw = w*math.sin(math.radians(a))
    cosh = h*math.cos(math.radians(a))
    sinh = h*math.sin(math.radians(a))

    nwidth = int(max(cosw + sinh, cosw - sinh, -1*cosw + sinh, -1* cosw - sinh))
    nheight = int(max(sinw + cosh, sinw - cosh, -1*sinw + cosh, -1* sinw - cosh))

    return nwidth, nheight