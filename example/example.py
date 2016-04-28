import awesomeengine
import components

e = awesomeengine.Engine('res')
e.component_manager.register_module(components)

e.create_window(title='Hello World!', size=(1280,480))

box = e.add_entity('smile')
c = e.add_entity('camera')
c2 = e.add_entity('camera2')
e.entity_manager.commit_changes()

cam1 = e.create_camera(c, 0, 0, 640, 480)
cam2 = e.create_camera(c2, 640, 0, 640, 480)

cam2.background_colour = (100,100,100,255)

e.run()