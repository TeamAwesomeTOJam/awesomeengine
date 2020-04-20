from awesomeengine.engine import Engine
from awesomeengine.entity import Entity

from .behaviors import ChangeMode
from .modes import MainMode, WelcomeMode, ButtonTestMode


def go():
    e = Engine('Example Game', 'res')
    e.behavior_manager.register_behavior(ChangeMode)

    manager = Entity('manager')
    e.entity_manager.add(manager)

    e.add_mode('main', MainMode())
    e.add_mode('welcome', WelcomeMode())
    e.add_mode('button', ButtonTestMode())

    e.change_mode('welcome')

    e.run()


if __name__ == '__main__':
    go()
