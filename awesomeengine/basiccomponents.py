from component import *
import engine

class DrawHitBoxComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        camera.draw_rect((255, 0, 255, 0), (entity.x, entity.y, entity.width, entity.height))

class DrawImageComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'image'])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        camera.draw_image((entity.x, entity.y), engine.get_engine().resource_manager.get('image', entity.image))

class VelocityMoveComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'vx', 'vy'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.x += dt * entity.vx
        entity.y += dt * entity.vy