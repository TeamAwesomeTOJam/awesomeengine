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

        # print self.entity.angle

        self.draw_width, self.draw_height = get_bounding_box(self.entity.width, self.entity.height, self.entity.angle)

        self.texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target,
                                      self.draw_width, self.draw_height)

        self.renderer.render_target = self.texture

        self.draw_x = self.entity.x - self.draw_width / 2
        self.draw_y = self.entity.y - self.draw_height / 2

        to_draw = engine.get_engine().entity_manager.get_in_area('draw',
                            (self.draw_x, self.draw_y, self.draw_width, self.draw_height))
        for e in to_draw:
            e.handle('draw', self)

        rotated_width, rotated_height = get_bounding_box(self.draw_width, self.draw_height, self.entity.angle)

        rotated_texture = sdl2hl.Texture(self.renderer, self.pixel_format, sdl2hl.TextureAccess.target,
                                         rotated_width, rotated_height)

        self.renderer.render_target = rotated_texture
        self.renderer.copy(self.texture,
                           source_rect=None,
                           dest_rect=None,
                           rotation=self.entity.angle)

        self.renderer.render_target = None
        self.renderer.copy(rotated_texture,
                                  source_rect=sdl2hl.Rect(
                           int(self.entity.height * math.cos(math.radians(self.entity.angle)) * math.sin(math.radians(self.entity.angle))),
                           int(self.entity.width * math.cos(math.radians(self.entity.angle)) * math.sin(math.radians(self.entity.angle))),
                           self.entity.width, self.entity.height),
                                  dest_rect=sdl2hl.Rect(self.screen_x, self.screen_y, self.screen_width, self.screen_height),
                                  rotation=0)
        self.renderer.present()


    def world_to_draw_area(self, p):
        return (int(p[0] - self.draw_x), int(p[1] - self.draw_y))

    def draw_rect(self, c, r):
        x, y = self.world_to_draw_area((r[0], r[1]))
        self.renderer.draw_color = c
        sdlr = sdl2hl.Rect(x, y, int(r[2]), int(r[3]))
        self.renderer.draw_rect(sdlr)

    def draw_image(self, p, texture):
        x, y = self.world_to_draw_area(p)
        self.renderer.copy(texture,dest_rect=sdl2hl.Rect(x, y, 100, 100))

def get_bounding_box(w, h, a):
    cosw = w*math.cos(math.radians(a))
    sinw = w*math.sin(math.radians(a))
    cosh = h*math.cos(math.radians(a))
    sinh = h*math.sin(math.radians(a))

    nwidth = int(max(cosw + sinh, cosw - sinh, -1*cosw + sinh, -1* cosw - sinh))
    nheight = int(max(sinw + cosh, sinw - cosh, -1*sinw + cosh, -1* sinw - cosh))

    return nwidth, nheight