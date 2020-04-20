from awesomeengine import engine
from awesomeengine.behavior import Behavior


class ChangeMode(Behavior):

    def __init__(self):
        self.required_attrs = []

    def handle_input(self, entity, action, value):
        if action == 'welcome' and value == 1:
            engine.get().change_mode('welcome')
        elif action == 'main' and value == 1:
            engine.get().change_mode('main')
        elif action == 'button' and value == 1:
            engine.get().change_mode('button')
