from component import *
import engine
import rectangle
import sdl2hl

class DrawHitBoxComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        try:
            c = entity.colour
        except AttributeError:
            c = (255,0,255,255)

        camera.draw_rect(c, rectangle.from_entity(entity))
        camera.draw_rect(c, rectangle.from_entity(entity).bounding_rect())

class DrawScaledImageComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height', 'image', ('angle', 0)])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        camera.draw_image(rectangle.from_entity(entity), engine.get_engine().resource_manager.get('image', entity.image))

class VelocityMoveComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('vx', 0), ('vy', 0)])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.x += dt * entity.vx
        entity.y += dt * entity.vy
        engine.get_engine().entity_manager.update_position(entity)

class ForceVelocityComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['mass', ('fx', 0), ('fy', 0), ('vx', 0), ('vy', 0)])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.vx += dt * entity.fx / entity.mass
        entity.vy += dt * entity.fy / entity.mass

class StaticTextComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['colour', 'size', 'text', 'font'])

        font = engine.get_engine().resource_manager.get('font', (entity.font, entity.size))
        surface = font.render_solid(entity.text, entity.colour)
        entity.texture = sdl2hl.Texture.from_surface(engine.get_engine().renderer, surface)

        entity.width = entity.texture.w
        entity.height = entity.texture.h

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

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

    def add(self, entity):
        verify_attrs(entity, ['colour', 'size', 'text', 'topleft', 'font'])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        if entity.text:
            font = engine.get_engine().resource_manager.get('font', (entity.font, entity.size))
            surface = font.render_solid(entity.text, entity.colour)
            texture = sdl2hl.Texture.from_surface(engine.get_engine().renderer, surface)
            x,y = camera.screen_percent_point(entity.topleft)
            r = rectangle.Rect(x + texture.w/2, y - texture.h/2, texture.w, texture.h)
            camera.draw_image(r, texture)
