import awesomeengine
import components

e = awesomeengine.Engine('res')
e.component_manager.register_module(components)

e.create_window(title='Hello World!', size=(640,480))

box = e.add_entity('smile')
c = e.add_entity('camera')
e.entity_manager.commit_changes()

e.create_camera(c, 0, 0, 640, 480)

e.run()