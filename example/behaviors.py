from awesomeengine.behavior import verify_attrs
from awesomeengine.behavior import Behavior
from awesomeengine import engine


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
