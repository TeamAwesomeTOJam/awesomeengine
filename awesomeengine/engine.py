import sdl2hl
import sdl2hl.mixer
import sdl2hl.ttf

import basiccomponents
import camera
import clock
import componentmanager
import entity
import entitymanager
import input
import resourcemanager
import collections
import rectangle

import Box2D

_instance = None

class Engine(object):

    def __init__(self, res_prefix):
        global _instance
        _instance = self

        sdl2hl.init(sdl2hl.InitFlag.everything)
        sdl2hl.mixer.init(sdl2hl.mixer.AudioInitFlag.ogg)
        sdl2hl.mixer.open_audio()
        sdl2hl.mixer.allocate_channels(64)
        sdl2hl.ttf.init()

        self.resource_manager = resourcemanager.ResourceManager(res_prefix)
        self.resource_manager.register_loader('entity', resourcemanager.LoadEntityData)
        self.resource_manager.register_loader('inputmap', resourcemanager.LoadInputMapping)
        self.resource_manager.register_loader('image', resourcemanager.LoadImage)
        self.resource_manager.register_loader('sound', resourcemanager.LoadSound)
        self.resource_manager.register_loader('font', resourcemanager.LoadFont)
        self.resource_manager.register_loader('map', resourcemanager.LoadMap)

        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_module(basiccomponents)

        self.entity_manager = entitymanager.EntityManager()

        self.window = None
        self.cameras = []

        self.input_manager = input.InputManager()

        self.running = True
        self.current_mode = None
        self.modes = {}
        self.box2d_world = None

        self.fps_queue = collections.deque(maxlen=30)

        self.update_layers = []

    def create_box2d_world(self, gravity):
        class ContactListener(Box2D.b2ContactListener):
            def __init__(self):
                Box2D.b2ContactListener.__init__(self)
            def BeginContact(self, contact):
                if 'entity' in contact.fixtureA.body.userData:
                    contact.fixtureA.body.userData['entity'].handle('contact', contact.fixtureB.body.userData.get('entity', None), True)
                if 'entity' in contact.fixtureB.body.userData:
                    contact.fixtureB.body.userData['entity'].handle('contact', contact.fixtureA.body.userData.get('entity', None), False)
            def EndContact(self, contact):
                pass
            def PreSolve(self, contact, oldManifold):
                pass
            def PostSolve(self, contact, impulse):
                pass

        if self.box2d_world is None:
            self.box2d_world = Box2D.b2World(gravity=gravity, doSleep=True, contactListener=ContactListener())

    def add_entity(self, static_data_name, **kwargs):
        ent = entity.Entity(static_data_name, **kwargs)
        self.entity_manager.add_entity(ent)
        return ent

    def add_entities_from_map(self, map_name):
        entity_info = self.resource_manager.get('map', map_name)
        for entity_name, overrides in entity_info:
            e = entity.Entity(entity_name, **overrides)
            self.entity_manager.add_entity(e)
        self.entity_manager.commit_changes()

    def remove_entity(self, entity):
        self.entity_manager.remove_entity(entity)

    def create_window(self, size=None, pos=None, title='awesome', *flags):
        if size is None:
            display = sdl2hl.video.Display(0)
            size = display.get_desktop_size()
        if self.window is None:
            if pos:
                self.window = sdl2hl.Window(title=title, w=size[0], h=size[1], x=pos[0], y=pos[1], *flags)
            else:
                self.window = sdl2hl.Window(title=title, w=size[0], h=size[1], *flags)
            self.renderer = sdl2hl.Renderer(self.window, flags={sdl2hl.RendererFlags.presentvsync})

    def create_camera(self, entity, layers=[], hud=[]):
        cam = camera.Camera(self.renderer, entity, layers, hud)
        self.cameras.append(cam)
        return cam

    def remove_camera(self, cam):
        if cam in self.cameras:
            self.cameras.remove(cam)

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def add_update_layer(self, tag, entity=None):
        self.update_layers.append((entity,tag))

    def remove_update_layer(self, tag, entity=None):
        if (entity, tag) in self.update_layers:
            self.update_layers.remove((entity, tag))

    def run(self):

        framecount = 0
        timer = clock.Clock()
        while self.running:
            framecount = (framecount + 1) % 200
            dt = timer.tick(60)
            self.handle_events()
            self.update(dt)
            self.handle_physics(dt)
            self.entity_manager.commit_changes()
            self.render()
            self.fps_queue.append(1.0/dt)
            if framecount == 0:
                print sum(self.fps_queue)/len(self.fps_queue)

            # self.average_fps = (self.average_fps + 1.0/dt)/2
            # self.window.title = '{:f}'.format(1.0/dt)

        sdl2hl.quit()

    def handle_physics(self, dt):
        if self.box2d_world is not None:
            velocity_iters = 6
            position_iters = 2
            self.box2d_world.Step(dt, velocity_iters, position_iters)
            self.box2d_world.ClearForces()


    def handle_events(self):
        events = self.input_manager.process_events()
        for event in events:
            if event.target == 'ENGINE':
                if event.action == 'QUIT' and event.value > 0:
                    self.quit()
                elif event.action == 'CLEAR' and event.value > 0:
                    self.resource_manager.clear()
                elif event.action == 'FULLSCREEN' and event.value > 0:
                    if sdl2hl.WindowFlags.fullscreen in self.window.flags:
                        self.window.set_fullscreen(0)
                    else:
                        self.window.set_fullscreen(sdl2hl.WindowFlags.fullscreen)
            else:
                if self.entity_manager.has_by_name(event.target):
                    self.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):

        for entity, tag in self.update_layers:
            if entity is None:
                to_update = self.entity_manager.get_by_tag(tag)
                for e in to_update:
                    e.handle('update', dt)
            else:
                r = rectangle.from_entity(entity)
                to_update = self.entity_manager.get_in_area(tag, r)
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



def get():
    return _instance
