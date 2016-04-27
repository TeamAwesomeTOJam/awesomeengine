from abc import ABCMeta, abstractmethod


class Component:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def remove(self, entity):
        pass

def verify_attrs(entity, attrs):
    missing_attrs = []
    for attr in attrs:
        if isinstance(attr, tuple):
            attr, default = attr
            if not hasattr(entity, attr):
                setattr(entity, attr, default)
        else:
            if not hasattr(entity, attr):
                missing_attrs.append(attr)
    if len(missing_attrs) > 0:
        raise AttributeError("entity [%s] is missing required attributes [%s]" % (entity._static_data_name, missing_attrs))