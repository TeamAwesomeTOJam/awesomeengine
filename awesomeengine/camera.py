import sdl2hl
import engine
import math
from component import verify_attrs


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

    def render(self):

        texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target, self.entity.width, self.entity.height)

        self.renderer.render_target = texture
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        draw_width, draw_height = get_bounding_box(self.entity.width, self.entity.height, self.entity.angle)
        draw_x = self.entity.x - draw_width / 2
        draw_y = self.entity.y - draw_height / 2

        to_draw = engine.get_engine().entity_manager.get_in_area('draw',
                            (draw_x, draw_y, draw_width, draw_height))
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
        points = [(r[0], r[1]),(r[0]+r[2],r[1]),(r[0]+r[2],r[1] + r[3]),(r[0],r[1]+r[3]), (r[0],r[1])]
        transformed_points = map(self.world_to_camera, points)
        sdlpoints = map(lambda x : sdl2hl.Point(x[0], x[1]), transformed_points)
        self.renderer.draw_color = c
        self.renderer.draw_lines(*sdlpoints)

    def draw_image(self, p, texture, rotation=0):
        if len(p) == 2:
            x , y = self.world_to_camera(p)
            w, h = texture.width, texture.height
        elif len(p) == 4:
            x, y = self.world_to_camera((p[0], p[1]))
            w, h = p[2], p[3]
        self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - w/2), int(y - h/2), w, h), rotation=self.entity.angle - rotation)


def get_bounding_box(w, h, a):
    cosw = w*math.cos(math.radians(a))
    sinw = w*math.sin(math.radians(a))
    cosh = h*math.cos(math.radians(a))
    sinh = h*math.sin(math.radians(a))

    nwidth = int(max(cosw + sinh, cosw - sinh, -1*cosw + sinh, -1* cosw - sinh))
    nheight = int(max(sinw + cosh, sinw - cosh, -1*sinw + cosh, -1* sinw - cosh))

    return nwidth, nheight