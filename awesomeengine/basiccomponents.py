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
        camera.draw_rect((255, 0, 255, 255), rectangle.from_entity(entity))
        camera.draw_rect((255, 0, 255, 255), rectangle.from_entity(entity).bounding_rect())

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
        verify_attrs(entity, ['x', 'y', 'vx', 'vy'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.x += dt * entity.vx
        entity.y += dt * entity.vy
        engine.get_engine().entity_manager.update_position(entity)

class StaticTextComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['colour', 'size', 'text', 'x', 'y', 'font'])

        font = engine.get_engine().resource_manager.get('font', (entity.font, entity.size))
        surface = font.render_solid(entity.text, entity.colour)
        entity.texture = sdl2hl.Texture.from_surface(engine.get_engine().renderer, surface)

        entity.width = entity.texture.w
        entity.height = entity.texture.h

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        camera.draw_image(rectangle.from_entity(entity), entity.texture)