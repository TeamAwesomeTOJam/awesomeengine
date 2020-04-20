import collections

from awesomeengine import (basicbehaviors,
                           clock,
                           behaviormanager,
                           entitymanager,
                           input,
                           resourcemanager)
from awesomeengine._ffi.SDL import *
from awesomeengine._ffi.SDL_mixer import *
from awesomeengine._ffi.SDL_ttf import *


_instance = None


class Engine(object):

    def __init__(self, game_name, resource_path, screen_width=1280, screen_height=720):
        global _instance
        _instance = self

        SDL_Init(SDL_INIT_EVERYTHING)
        Mix_Init(MIX_INIT_OGG)
        Mix_OpenAudio(48000, AUDIO_U16LSB, 2, 128)
        Mix_AllocateChannels(64)
        TTF_Init()

        self.resource_manager = resourcemanager.ResourceManager(resource_path)
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

        self.input_manager = input.InputManager()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self._window = SDL_CreateWindow(game_name.encode(),
                                           SDL_WINDOWPOS_UNDEFINED,
                                           SDL_WINDOWPOS_UNDEFINED,
                                           screen_width,
                                           screen_height,
                                           0)
        self._renderer = SDL_CreateRenderer(self.window, 0)

        self.running = True
        self.current_mode = None
        self.modes = {}

        self.fps_queue = collections.deque(maxlen=10)

    def add_mode(self, name, mode):
        self.modes[name] = mode

    def run(self):
        timer = clock.Clock()

        while self.running:
            dt = timer.tick(60)
            if dt < 0.1:
                self.fps_queue.append(1.0/dt)
                self.handle_events()
                self.update(dt)
                self.entity_manager.commit_changes()
                self.draw()

        SDL_Quit()

    def handle_events(self):
        events = self.input_manager.process_events()
        for event in events:
            if event.target == 'ENGINE':
                if event.action == 'QUIT' and event.value > 0:
                    self.quit()
                elif event.action == 'CLEAR' and event.value > 0:
                    self.resource_manager.clear()
                elif event.action == 'FULLSCREEN' and event.value > 0:
                    if SDL_GetWindowFlags(self.window) & SDL_WINDOW_FULLSCREEN:
                        SDL_SetWindowFullscreen(self.window, 0)
                    else:
                        SDL_SetWindowFullscreen(self.window, SDL_WINDOW_FULLSCREEN)
                elif event.action == 'TELEMETRY' and event.value > 0:
                    self.show_telemetry = not self.show_telemetry
            else:
                self.modes[self.current_mode].handle_event(event)

    def update(self, dt):
        self.modes[self.current_mode].update(dt)

    def draw(self):
        self.modes[self.current_mode].draw()
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


def get() -> Engine:
    return _instance
