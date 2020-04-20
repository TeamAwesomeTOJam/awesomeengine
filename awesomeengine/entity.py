import uuid

from awesomeengine import engine


class Entity:
    
    def __init__(self, static_data_name, **kwargs):
        self._static_data_name = static_data_name
        
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

        for behavior_name in getattr(self, 'behaviors', []):
            engine.get().behavior_manager.get(behavior_name).add(self)
                
        if not ('name' in self.__dict__ or 'name' in self.static._fields):
            self.name = str(uuid.uuid4())

    def __getattr__(self, name):
        return getattr(self.static, name)
    
    @property
    def static(self):
        return engine.get().resource_manager.get('entity', self._static_data_name)
    
    def handle(self, event, *args):
        handler_name = "handle_" + event
        for behavior_name in getattr(self, 'behaviors', []):
            behavior = engine.get().behavior_manager.get(behavior_name)
            if hasattr(behavior, handler_name):
                getattr(behavior, handler_name)(self, *args)

