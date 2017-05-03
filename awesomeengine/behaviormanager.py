from behavior import Behavior


class BehaviorManager(object):

    def __init__(self):
        self.behaviors = {}
        
    def register_behavior(self, behavior):
        self.behaviors[behavior.__class__.__name__] = behavior
        
    def register_module(self, module):
        for name, value in module.__dict__.iteritems():
            try:
                if not name.startswith('_') and isinstance(value, type) and issubclass(value, Behavior):
                    self.behaviors[name] = value()
            except Exception , e:
                print e
        
    def get(self, name):
        return self.behaviors[name]

        
