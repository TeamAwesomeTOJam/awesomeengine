import weakref

import engine
import spatialmap


GRID_SIZE = 32


class EntityManager(object):
    
    def __init__(self):
        self.entities = set()
        self._entities_by_name = weakref.WeakValueDictionary()
        self._entities_by_tag = {}
        self._spatial_maps = {None: spatialmap.SpatialMap(GRID_SIZE)}
        self._remove_list = []
        self._add_list = []
    
    def add(self, *args):
        self._add_list += args

    def add_from_map(self, map_name):
        entity_info = engine.get().resource_manager.get('map', map_name)
        for static_data_name, kwargs in entity_info:
            e = entity.Entity(static_data_name, **kwargs)
            self.add_entity(e)
    
    def save_to_map(self, map_name, filter=None):
        entity_info = []
        for entity in self.entities:
            if filter is not None and not filter(entity):
                continue
        
            static_data_name = entity._static_data_name
            kwargs = entity.__dict__.copy()
            del kwargs['_static_data_name']
            
            entity_info.append((static_data_name, kwargs))
            
        engine.get().resource_manager.save('map', map_name, entity_info)
    
    def remove(self, *args):     
        self._remove_list += args
    
    def clear(self):
        self._remove_list += self.entities
    
    def commit_changes(self):
        for entity in self._remove_list:
            for tag in getattr(entity, 'tags', []):
                self._entities_by_tag[tag].remove(entity)
                try:
                    self._spatial_maps[tag].remove(entity)
                except KeyError:
                    pass
            self._spatial_maps[None].remove(entity)
            del self._entities_by_name[entity.name]
            self.entities.remove(entity)
            
        for entity in self._add_list:
            self.entities.add(entity)
            self._entities_by_name[entity.name] = entity
            self._spatial_maps[None].add(entity)
            
            for tag in getattr(entity, 'tags', []):
                if not tag in self._entities_by_tag:
                    self._entities_by_tag[tag] = weakref.WeakSet()
                self._entities_by_tag[tag].add(entity)
                
                if not tag in self._spatial_maps:
                    self._spatial_maps[tag] = spatialmap.SpatialMap(GRID_SIZE)
                self._spatial_maps[tag].add(entity)
        
        self._add_list = []
        self._remove_list = []
    
    def update_position(self, entity):
        self._spatial_maps[None].update(entity)
        for tag in entity.tags:
            self._spatial_maps[tag].update(entity)
        
    def get_by_name(self, name):
        return self._entities_by_name[name]

    def has_by_name(self, name):
        return name in self._entities_by_name
        
    def get_by_tag(self, tag):
        try:
            return self._entities_by_tag[tag]
        except KeyError:
            return set()
    
    def get_in_area(self, tag, rect, precise=True):
        try:
            return self._spatial_maps[tag].get(rect, precise)
        except KeyError:
            return set()
