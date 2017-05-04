import awesomeengine
import behaviors
import modes

def go():
    e = awesomeengine.Engine('res')
    e.behavior_manager.register_module(behaviors)

    e.create_window(title='Hello World!', size=(1280,480))

    manager = awesomeengine.Entity('manager')
    e.entity_manager.add(manager)

    e.add_mode('main', modes.MainMode())
    e.add_mode('welcome', modes.WelcomeMode())
    e.add_mode('button', modes.ButtonTestMode())

    e.change_mode('welcome')
    

    e.run()

if __name__ == '__main__':
    go()
