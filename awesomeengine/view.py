from awesomeengine import engine
from awesomeengine.camera import Camera
from awesomeengine.geometry import Rect
from awesomeengine._ffi.SDL import *


class View:

    def __init__(self, screen_rect: Rect, camera: Camera):
        self.screen_rect = screen_rect
        self.camera = camera

    def draw(self):
        r = engine.get()._renderer
        SDL_RenderSetClipRect(r, SDL_Rect(self.screen_rect.x, self.screen_rect.y, self.screen_rect.w, self.screen_rect.h))

        self.camera.before_draw()
        for entity in self.camera.entities():
            entity.handle('draw', self)

    def draw_rect(self, color, rect):
        r = engine.get()._renderer
        points = (rect.top_left, rect.bottom_left, rect.bottom_right, rect.top_right, rect.top_left)
        transformed_points = [self.camera.world_to_screen(self.screen_rect, p) for p in points]
        sdl_points = [SDL_Point(p.x, p.y) for p in transformed_points]
        SDL_SetRenderDrawColor(r, *color)
        SDL_RenderDrawLines(r, sdl_points, len(sdl_points))

    # def draw_image(self, r, texture):
    #     x,y = self.transform_point(r.center)
    #     w,h = self.transform_width(r.w), self.transform_height(r.h)
    #     self.renderer.copy(texture, dest_rect=sdl2hl.Rect(int(x - w/2), int(y - h/2), w,h), rotation=self.transform_angle(r.a))
    #
    # def draw_image_part(self, r, texture, source_rect, flip=0):
    #     x,y = self.transform_point(r.center)
    #     w,h = self.transform_width(r.w), self.transform_height(r.h)
    #     self.renderer.copy(texture, source_rect=source_rect, dest_rect=sdl2hl.Rect(int(x - w/2), int(y - h/2), w,h), rotation=self.transform_angle(r.a), flip=flip)
    #
    # def draw_line(self, c, p1, p2):
    #     points = [self.transform_point(p1), self.transform_point(p2)]
    #     sdlpoints = map(lambda x: sdl2hl.Point(x[0], x[1]), points)
    #     self.renderer.draw_color = c
    #     self.renderer.draw_lines(*sdlpoints)
    #
    # def draw_lines(self, c, points):
    #     transformed_points = map(self.transform_point, points)
    #     sdlpoints = map(lambda x: sdl2hl.Point(x[0], x[1]), transformed_points)
    #     self.renderer.draw_color = c
    #     self.renderer.draw_lines(*sdlpoints)
    #
    # def draw_filled_circle(self, c, p, r):
    #     p = self.transform_point(p)
    #     r = self.transform_width(r)
    #
    #     primitives = sdl2hl.gfx.GfxPrimitives(self.renderer)
    #     primitives.draw_filled_circle(p[0],p[1],r,c)
    #
    # def draw_filled_trigon(self, c, p1, p2, p3):
    #     p1 = self.transform_point(p1)
    #     p2 = self.transform_point(p2)
    #     p3 = self.transform_point(p3)
    #
    #     primitives = sdl2hl.gfx.GfxPrimitives(self.renderer)
    #     primitives.draw_filled_trigon(p1[0], p1[1],
    #                                   p2[0], p2[1],
    #                                   p3[0], p3[1],
    #                                   c)

