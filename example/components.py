from awesomeengine.component import verify_attrs
from awesomeengine.component import Component

class InputRotateComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['angle', ('va', 0)])

        entity.register_handler('update', self.handle_update)
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        entity.unregister_handler('input', self.handle_input)

    def handle_update(self, entity, dt):
        entity.angle = (entity.angle + entity.va*dt) % 360

    def handle_input(self, entity, action, value):
        if action == 'ccw' and value == 1:
            entity.va = 10
        elif action == 'cw' and value == 1:
            entity.va = -10
        elif (action == 'ccw' or action == 'cw') and value == 0:
            entity.va = 0

class InputVelocityComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['vx', 'vy'])

        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, action, value):
        if action == 'up' and value == 1:
            entity.vy = 10
        elif action == 'down' and value == 1:
            entity.vy = -10
        elif (action == 'up' or action == 'down') and value == 0:
            entity.vy = 0
        if action == 'left' and value == 1:
            entity.vx = -10
        elif action == 'right' and value == 1:
            entity.vx = 10
        elif (action == 'left' or action == 'right') and value == 0:
            entity.vx = 0