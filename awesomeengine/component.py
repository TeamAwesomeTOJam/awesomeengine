from abc import ABCMeta


class Component:
    __metaclass__ = ABCMeta

    def add(self, entity):
        self.verify_attrs(entity)
    
        for event, handler in self.event_handlers:
            entity.register_handler(event, handler)

    def remove(self, entity):
        for event, handler in self.event_handlers:
            entity.unregister_handler(event, handler)
        
    def verify_attrs(self, entity):
        missing_attrs = []
        for attr in self.required_attrs:
            if isinstance(attr, tuple):
                attr, default = attr
                if not hasattr(entity, attr):
                    setattr(entity, attr, default)
            else:
                if not hasattr(entity, attr):
                    missing_attrs.append(attr)
        if len(missing_attrs) > 0:
            raise AttributeError(
                "entity [%s] is missing required attributes [%s]" 
                % (entity._static_data_name, missing_attrs))
