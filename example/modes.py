import awesomeengine

class MainMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()
        box = e.add_entity('smile')
        h_smile = e.add_entity('hud_smile')
        c = e.add_entity('camera')
        c2 = e.add_entity('camera2')

        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))
        l3 = awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255))

        cam1 = e.create_camera(c, layers=[l2, l], hud=[h_smile])
        cam2 = e.create_camera(c2, layers=[l3, l])

        self.cams = [cam1, cam2]
        self.entities = [box, h_smile, c, c2]

        e.add_update_layer('update')

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)

        e.remove_update_layer('update')

class WelcomeMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()
        h = e.add_entity('hello')

        c = e.add_entity('welcome_camera')

        # l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = e.create_camera(c, layers=[l2], hud=[h])

        self.entities = [h, c]
        self.cams = [cam]



    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)