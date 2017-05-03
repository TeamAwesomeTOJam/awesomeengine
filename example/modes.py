import awesomeengine
from awesomeengine import Entity
from awesomeengine.camera import Camera


class MainMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()

        box = Entity('smile')
        h_smile = Entity('hud_smile')
        c = Entity('camera')
        c2 = Entity('camera2')
        m = Entity('mouse')
        
        e.entity_manager.add(box, h_smile, c, c2, m)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))
        l3 = awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255))

        cam1 = Camera(awesomeengine.get().renderer,c,[l2, l], hud=[h_smile])
        cam2 = Camera(awesomeengine.get().renderer, c2, [l3, l], hud=[h_smile])

        self.cams = [cam1, cam2]
        self.entities = [box, h_smile, c, c2, m]

    def leave(self):
        e = awesomeengine.get()

        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        e = awesomeengine.get()
    
        if event.target == 'GAME':
            if event.action == 'SAVE_MAP':
                e.entity_manager.save_to_map('test')
    
        elif e.entity_manager.has_by_name(event.target):
            e.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in self.cams:
            c.render()


class WelcomeMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()
        
        h = Entity('hello')
        c = Entity('welcome_camera')
        e.entity_manager.add(h, c)
        
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer,c,[l2], [h])

        self.entities = [h, c]
        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in self.cams:
            c.render()
