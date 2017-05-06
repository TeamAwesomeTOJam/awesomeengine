import sdl2hl
import sdl2hl.mixer
import sdl2hl.ttf

import basicbehaviors
import camera
import clock
import behaviormanager
import entity
import entitymanager
import input
import resourcemanager
import collections
import rectangle

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
        self.resource_manager.register_loader('animation', resourcemanager.LoadAnimation)
        self.resource_manager.register_loader('image', resourcemanager.LoadImage)
        self.resource_manager.register_loader('sprite', resourcemanager.LoadSprite)
        self.resource_manager.register_loader('sound', resourcemanager.LoadSound)
        self.resource_manager.register_loader('font', resourcemanager.LoadFont)
        self.resource_manager.register_loader('text', resourcemanager.LoadText)
        self.resource_manager.register_loader('map', resourcemanager.LoadJSONMap)
        self.resource_manager.register_saver('map', resourcemanager.SaveJSONMap)

        self.behavior_manager = behaviormanager.BehaviorManager()
        self.behavior_manager.register_module(basicbehaviors)

        self.entity_manager = entitymanager.EntityManager()

        self.window = None

        self.input_manager = input.InputManager()

        self.running = True
        self.current_mode = None
        self.modes = {}

        self.show_telemetry = False
        self.telemetry_font = self.resource_manager.get('font', ('LiberationSans-Regular', 24))

        self.fps_queue = collections.deque(maxlen=10)

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

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def run(self):
        timer = clock.Clock()

        while self.running:
            dt = timer.tick(60)
            self.fps_queue.append(1.0/dt)
            self.handle_events()
            self.update(dt)
            self.entity_manager.commit_changes()
            self.draw()

        sdl2hl.quit()

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
                elif event.action == 'TELEMETRY' and event.value > 0:
                    self.show_telemetry = not self.show_telemetry
            else:
                self.modes[self.current_mode].handle_event(event)

    def update(self, dt):
        self.modes[self.current_mode].update(dt)

    def draw(self):
        self.modes[self.current_mode].draw()

        if self.show_telemetry:
            mean_fps = sum(self.fps_queue) / len(self.fps_queue)
            surface = self.telemetry_font.render_solid('%.0f' % mean_fps, (255, 255, 0))
            texture = sdl2hl.Texture.from_surface(self.renderer, surface)
            self.renderer.copy(texture, dest_rect=sdl2hl.Rect(0, 0, surface.w, surface.h))
            
        self.renderer.present()

    def quit(self):
        self.running = False

    def change_mode(self, new_mode):
        if self.current_mode is not None:
            self.modes[self.current_mode].leave()
            self.entity_manager.commit_changes()

        self.current_mode = new_mode
        self.modes[self.current_mode].enter()
        self.entity_manager.commit_changes()


def get():
    return _instance
