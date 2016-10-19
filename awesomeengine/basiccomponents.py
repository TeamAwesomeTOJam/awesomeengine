import sdl2hl

from component import *
import engine
import rectangle


class DrawHitBoxComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height', ('colour', (255,0,255,255)))
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        camera.draw_rect(entity.colour, rectangle.from_entity(entity))
        camera.draw_rect(entity.colour, rectangle.from_entity(entity).bounding_rect())


class DrawScaledImageComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height', 'image', ('angle', 0))
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        camera.draw_image(rectangle.from_entity(entity), engine.get().resource_manager.get('image', entity.image))


class VelocityMoveComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', ('vx', 0), ('vy', 0))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        entity.x += dt * entity.vx
        entity.y += dt * entity.vy
        engine.get().entity_manager.update_position(entity)


class ForceVelocityComponent(Component):
    
    def __init__(self):
        self.required_attrs = ('mass', ('fx', 0), ('fy', 0), ('vx', 0), ('vy', 0))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        entity.vx += dt * entity.fx / entity.mass
        entity.vy += dt * entity.fy / entity.mass


class StaticTextComponent(Component):

    def __init__(self):
        self.required_attrs = ('colour', 'size', 'text', 'font')
        self.event_handlers = (('draw', self.handle_draw),)

    def add(self, entity):
        Component.add(self, entity)

        font = engine.get().resource_manager.get('font', (entity.font, entity.size))
        surface = font.render_solid(entity.text, entity.colour)
        entity.texture = sdl2hl.Texture.from_surface(engine.get().renderer, surface)

        entity.width = entity.texture.w
        entity.height = entity.texture.h

    def handle_draw(self, entity, camera):

        try:
            x_percent = entity.x_percent
            y_percent = entity.y_percent

            x, y = camera.screen_percent_point((x_percent,y_percent))

        except AttributeError:
            x, y = entity.x , entity.y

        try:
            a = entity.angle
        except AttributeError:
            a = 0

        camera.draw_image(rectangle.Rect(x, y, entity.width, entity.height, a), entity.texture)


class DynamicTextComponent(Component):

    def __init__(self):
        self.required_attrs = ('colour', 'size', 'text', 'topleft', 'font')
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        if len(entity.text) > 0:
            font = engine.get().resource_manager.get('font', (entity.font, entity.size))
            surface = font.render_solid(entity.text, entity.colour)
            texture = sdl2hl.Texture.from_surface(engine.get().renderer, surface)
            x,y = camera.screen_percent_point(entity.topleft)
            r = rectangle.Rect(x + texture.w/2, y - texture.h/2, texture.w, texture.h)
            camera.draw_image(r, texture)
