import weakref

import engine
import entity
import spatialmap


GRID_SIZE = 128


class EntityManager(object):
    
    def __init__(self):
        self.entities = set()
        self._entities_by_name = weakref.WeakValueDictionary()
        self._entities_by_tag = {}
        self._spatial_maps = {}
        self._remove_set = set()
        self._add_set = set()
    
    def add(self, *args):
        for entity in args:
            if entity.name in self._entities_by_name:
                found = False
                for e in self._remove_set:
                    if e.name == entity.name:
                        found = True
                        break
                if not found:
                    raise KeyError('Entity with name %s already exists.' % entity.name)
        self._add_set |= set(args)

    def add_from_map(self, map_name):
        entity_info = engine.get().resource_manager.get('map', map_name)
        for static_data_name, kwargs in entity_info:
            e = entity.Entity(static_data_name, **kwargs)
            self.add(e)
    
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
        self._remove_set |= set(args)
    
    def clear(self):
        self._remove_set |= self.entities
    
    def commit_changes(self):
        for entity in self._remove_set:
            for tag in getattr(entity, 'tags', []):
                self._entities_by_tag[tag].remove(entity)
                try:
                    self._spatial_maps[tag].remove(entity)
                except KeyError:
                    pass
            del self._entities_by_name[entity.name]
            self.entities.remove(entity)
            
        for entity in self._add_set:
            self.entities.add(entity)
            self._entities_by_name[entity.name] = entity

            for tag in getattr(entity, 'tags', []):
                if not tag in self._entities_by_tag:
                    self._entities_by_tag[tag] = weakref.WeakSet()
                self._entities_by_tag[tag].add(entity)
                
                if not tag in self._spatial_maps:
                    self._spatial_maps[tag] = spatialmap.SpatialMap(GRID_SIZE)
                self._spatial_maps[tag].add(entity)
        
        self._add_set.clear()
        self._remove_set.clear()
    
    def update_position(self, entity):
        for tag in entity.tags:
            self._spatial_maps[tag].update(entity)

    def update_all_positions(self):
        for e in self.entities:
            self.update_position(e)
        
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
