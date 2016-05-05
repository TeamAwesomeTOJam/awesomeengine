import sdl2hl

import basiccomponents
import camera
import clock
import componentmanager
import entity
import entitymanager
import input
import resourcemanager
import sdl2hl.ttf

_engine = None

class Engine(object):

    def __init__(self, res_prefix, *flags):
        global _engine
        _engine = self

        sdl2hl.init(*flags)
        sdl2hl.ttf.init()

        self.resource_manager = resourcemanager.ResourceManager(res_prefix)
        self.resource_manager.register_loader('entity', resourcemanager.LoadEntityData)
        self.resource_manager.register_loader('inputmap', resourcemanager.LoadInputMapping)
        self.resource_manager.register_loader('image', resourcemanager.LoadImage)
        self.resource_manager.register_loader('font', resourcemanager.LoadFont)

        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_module(basiccomponents)

        self.entity_manager = entitymanager.EntityManager()


        self.window = None
        self.cameras = []

        self.input_manager = input.InputManager()

        self.running = True
        self.current_mode = None
        self.modes = {}

    def add_entity(self, static_data_name, **kwargs):
        ent = entity.Entity(static_data_name, **kwargs)
        self.entity_manager.add_entity(ent)
        return ent

    def remove_entity(self, entity):
        self.entity_manager.remove_entity(entity)

    def create_window(self, size=(640,480), pos=None, title='awesome', *flags):
        if self.window is None:
            if pos:
                self.window = sdl2hl.Window(title=title, w=size[0], h=size[1], x=pos[0], y=pos[1], *flags)
            else:
                self.window = sdl2hl.Window(title=title, w=size[0], h=size[1], *flags)
            self.renderer = sdl2hl.Renderer(self.window)

    def create_camera(self, entity, layers=[], hud=[]):
        cam = camera.Camera(self.renderer, entity, layers, hud)
        self.cameras.append(cam)
        return cam

    def remove_camera(self, cam):
        if cam in self.cameras:
            self.cameras.remove(cam)

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def run(self):

        timer = clock.Clock()
        while self.running:
            dt = timer.tick(60)
            self.handle_events()
            self.update(dt)
            self.entity_manager.commit_changes()
            self.render()

        sdl2hl.quit()

    def handle_events(self):
        events = self.input_manager.process_events()
        for event in events:
            if event.target == 'ENGINE':
                if event.action == 'QUIT' and event.value > 0:
                    self.quit()
            else:
                if self.entity_manager.has_by_name(event.target):
                    self.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        to_update = self.entity_manager.get_by_tag('update')
        for e in to_update:
            e.handle('update', dt)

    def render(self):
        for c in self.cameras:
            c.render()
        self.renderer.present()

    def quit(self):
        self.running = False

    def change_mode(self, new_mode):

        if self.current_mode is not None:
            self.modes[self.current_mode].leave()

        self.current_mode = new_mode
        self.modes[self.current_mode].enter()
        self.entity_manager.commit_changes()



def get_engine():
    return _engine