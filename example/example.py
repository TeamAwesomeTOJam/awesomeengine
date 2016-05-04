import awesomeengine
import components

def go():
    e = awesomeengine.Engine('res')
    e.component_manager.register_module(components)

    e.create_window(title='Hello World!', size=(1280,480))

    box = e.add_entity('smile')
    h_smile = e.add_entity('hud_smile')
    c = e.add_entity('camera')
    c2 = e.add_entity('camera2')
    e.entity_manager.commit_changes()

    l = awesomeengine.layer.SimpleCroppedLayer('draw')
    l2 = awesomeengine.layer.SolidBackgroundLayer((0,0,0,255))
    l3 = awesomeengine.layer.SolidBackgroundLayer((100,100,100,255))

    cam1 = e.create_camera(c, layers=[l2, l], hud=[h_smile])
    cam2 = e.create_camera(c2, layers=[l3, l])


    e.run()

if __name__ == '__main__':
    go()