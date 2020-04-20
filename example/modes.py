from awesomeengine import engine
from awesomeengine.camera import TopDownCamera
from awesomeengine import Entity
from awesomeengine import Rect
from awesomeengine.mode import Mode
from awesomeengine.view import View


class MainMode(Mode):

    def enter(self):
        e = engine.get()

        box = Entity('smile')
        h_smile = Entity('hud_smile')
        c = Entity('camera')
        c2 = Entity('camera2')
        #m = Entity('mouse')
        
        e.entity_manager.add(box, h_smile, c, c2, m)

        full_screen_rect = Rect(0, 0, e.screen_width, e.screen_height)
        game_view = View(full_screen_rect, TopDownCamera('game', 'camera'))
        hud_view = View(full_screen_rect, TopDownCamera('hud', 'camera2'))

        self.views = (game_view, hud_view)
        self.entities = (box, h_smile, c, c2)

    def leave(self):
        e = engine.get()

        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        e = engine.get()
    
        if event.target == 'GAME':
            if event.action == 'SAVE_MAP':
                e.entity_manager.save_to_map('test')
    
        elif e.entity_manager.has_by_name(event.target):
            e.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in engine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for v in self.views:
            v.draw()


class WelcomeMode(Mode):

    def enter(self):
        e = engine.get()
        
        h = Entity('hello')
        c = Entity('welcome_camera')

        e.entity_manager.add(h, c)

        view = View(Rect(0, 0, e.screen_width, e.screen_height), TopDownCamera('game', 'welcome_camera'))

        self.entities = (h, c)
        self.views = (view,)

    def leave(self):
        e = engine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        if engine.get().entity_manager.has_by_name(event.target):
            engine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in engine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for v in self.view:
            v.draw()

class ButtonTestMode(Mode):

    def enter(self):
        e = engine.get()
        c = Entity('button_cam')
        button = Entity('button')
        m = Entity('button_mouse')
        h = Entity('hud_button')

        e.entity_manager.add(button, c, m, h)

        view = View(Rect(0, 0, e.screen_width, e.screen_height), TopDownCamera('game', 'button_cam'))

        self.entities = (button, c, m, h)
        self.view = (view,)

    def leave(self):
        e = engine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        if engine.get().entity_manager.has_by_name(event.target):
            engine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in engine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for v in self.views:
            v.draw()
            
