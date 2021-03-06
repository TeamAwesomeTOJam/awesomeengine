from abc import ABCMeta


class Behavior:
    __metaclass__ = ABCMeta

    def add(self, entity):
        verify_attrs(entity, self.required_attrs)
        
        
def verify_attrs(entity, required_attrs):
    missing_attrs = []
    for attr in required_attrs:
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
