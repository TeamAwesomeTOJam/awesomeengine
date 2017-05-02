import awesomeengine
import behaviors
import modes

def go():
    e = awesomeengine.Engine('res')
    e.behavior_manager.register_module(behaviors)

    e.create_window(title='Hello World!', size=(1280,480))

    e.add_entity('manager')

    e.add_mode('main', modes.MainMode())
    e.add_mode('welcome', modes.WelcomeMode())

    e.change_mode('welcome')


    e.run()

if __name__ == '__main__':
    go()
