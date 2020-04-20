import collections
import json


class JSONParser:

    def __init__(self):
        self._type_cache = {}

    def add_object_type(self, obj_type):
        self._type_cache[tuple(sorted(obj_type._fields))] = obj_type

    def parse(self, input_string):
        return self._freeze_value(json.loads(input_string))

    def parse_file(self, input_file):
        return self._freeze_value(json.load(input_file))

    def _freeze_value(self, value):
        if isinstance(value, dict):
            return self._freeze_object(value)
        elif isinstance(value, list):
            return self._freeze_array(value)
        else:
            return value

    def _freeze_object(self, obj):
        for key, value in obj.items():
            obj[key] = self._freeze_value(value)

        obj_type = None
        obj_keys = tuple(sorted(obj.keys()))
        if obj_keys in self._type_cache:
            obj_type = self._type_cache[obj_keys]
        else:
            obj_type = collections.namedtuple(', '.join(obj_keys), obj_keys)
            self._type_cache[obj_keys] = obj_type

        return obj_type(**obj)

    def _freeze_array(self, array):
        for index, value in enumerate(array):
            array[index] = self._freeze_value(value)

        return tuple(array)
