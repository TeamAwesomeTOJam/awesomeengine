from awesomeengine.behavior import verify_attrs
from awesomeengine.behavior import Behavior
from awesomeengine import engine


class RotateOnInput(Behavior):

    def __init__(self):
        self.required_attrs = ('angle', ('va', 0))
        self.event_handlers = {
            'update': self.handle_update, 
            'input': self.handle_input
        }

    def handle_update(self, entity, dt):
        entity.angle = (entity.angle + entity.va*dt) % 360

        engine.get().entity_manager.update_position(entity)

    def handle_input(self, entity, action, value):
        if action == 'ccw' and value == 1:
            entity.va = 10
        elif action == 'cw' and value == 1:
            entity.va = -10
        elif (action == 'ccw' or action == 'cw') and value == 0:
            entity.va = 0


class ChangeVelocityOnInput(Behavior):

    def __init__(self):
        self.required_attrs = (('vx', 0), ('vy', 0))
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'up' and value == 1:
            entity.vy = 100
        elif action == 'down' and value == 1:
            entity.vy = -100
        elif (action == 'up' or action == 'down') and value == 0:
            entity.vy = 0
        if action == 'left' and value == 1:
            entity.vx = -100
        elif action == 'right' and value == 1:
            entity.vx = 100
        elif (action == 'left' or action == 'right') and value == 0:
            entity.vx = 0


class ZoomOnInput(Behavior):

    def __init__(self):
        self.required_attrs = ('width', 'height')
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'zoom in' and value == 1:
            entity.width /= 1.5
            entity.height /= 1.5
        elif action == 'zoom out' and value == 1:
            entity.width *= 1.5
            entity.height *= 1.5


class ChangeMode(Behavior):

    def __init__(self):
        self.required_attrs = []
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'welcome' and value == 1:
            engine.get().change_mode('welcome')
        elif action == 'main' and value == 1:
            engine.get().change_mode('main')
        elif action == 'button' and value == 1:
            engine.get().change_mode('button')
