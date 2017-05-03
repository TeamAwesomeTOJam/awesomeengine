import awesomeengine
from awesomeengine.camera import Camera


class MainMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()
        box = e.add_entity('smile')
        h_smile = e.add_entity('hud_smile')
        c = e.add_entity('camera')
        c2 = e.add_entity('camera2')
        m = e.add_entity('mouse')

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
            e.remove_entity(ent)

    def handle_event(self, event):
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in self.cams:
            c.render()


class WelcomeMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()
        h = e.add_entity('hello')

        c = e.add_entity('welcome_camera')

        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer,c,[l2], [h])

        self.entities = [h, c]
        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get()
        for ent in self.entities:
            e.remove_entity(ent)

    def handle_event(self, event):
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in self.cams:
            c.render()
