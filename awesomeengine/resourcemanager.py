import json
import os
import engine
import freezejson
import sdl2hl
import sdl2hl.ttf


class ResourceManager(object):
    
    def __init__(self, prefix):
        self.prefix = prefix
        self.loaders = {}
        self.cache = {}
    
    def register_loader(self, res_type, loader):
        self.loaders[res_type] = loader
    
    def get(self, res_type, key):
        try:
            return self.cache[(res_type, key)]
        except KeyError:
            value = self.loaders[res_type](self.prefix, key)
            self.cache[(res_type, key)] = value
            return value
    
    def clear(self):
        self.cache = {}
        
    
def LoadEntityData(prefix, key):
    with open(os.path.join(prefix, 'entities', key + '.json')) as in_file:
        definition = json.load(in_file)
    
    if 'animations' in definition:
        for animation in definition['animations'].values():
            if 'frame_dir' in animation:
                frame_dir = os.path.join(prefix, 'images', animation['frame_dir'])
                frames = sorted(os.listdir(frame_dir))
                animation['frames'] = []
                for frame in frames:
                    animation['frames'].append(os.path.join(frame_dir, frame))
    
    if 'includes' in definition:
        flattened = {}
        for include_name in definition['includes']:
            include = engine.get_engine().resource_manager.get('entity', include_name)
            for field in include._fields:
                flattened[field] = getattr(include, field)
        for key, value in definition.iteritems():
            if key.endswith('+'):
                base_key = key[:-1]
                flattened[base_key] = flattened.get(base_key, tuple()) + tuple(value)
            else:
                flattened[key] = value
        definition = flattened

    return freezejson.freeze_value(definition)
    
def LoadImage(prefix, key):
    texture = sdl2hl.image.load_texture(engine.get_engine().renderer, os.path.join(prefix, 'images', key))

    return texture

def LoadInputMapping(prefix, key):
    with open(os.path.join(prefix, 'inputmaps', key + '.json')) as in_file:
        mapping = json.load(in_file)
        
    return mapping

def LoadAnimation(prefix, key):
    with open(os.path.join(prefix, 'animations', key + '.json')) as in_file:
        animation = json.load(in_file)

    if 'frame_dir' in animation:
        frame_dir = os.path.join(prefix, 'images', animation['frame_dir'])
        frames = sorted(os.listdir(frame_dir))
        animation['frames'] = []
        for frame in frames:
            animation['frames'].append(os.path.join(frame_dir, frame))

    return freezejson.freeze_value(animation)
                    
def LoadSound(prefix, key):
    return sdl2hl.mixer.Chunk.from_path(os.path.join(prefix, 'sounds', key + '.ogg'))

def LoadText(prefix, key):
    f = open(os.path.join(prefix, 'text', key),'r')
    return f.read()

def LoadInputMapping(prefix, key):
    with open(os.path.join(prefix, 'inputmaps', key + '.json')) as in_file:
        mapping = json.load(in_file)

    return mapping

def LoadFont(prefix, key):
    return sdl2hl.ttf.Font.from_path(os.path.join(prefix, 'fonts', key[0] + '.ttf'),key[1])
    
def LoadMap(prefix, key):
    with open(os.path.join(prefix, 'maps', key + '.csv')) as in_file:
        section = 0
        y = 0
        legend = {}
        entities = []
        
        for line in in_file:
            if section == 0:
                if line.split(',')[0] == '':
                    section = 1
                else:
                    tile_size = line.split(',')
                    tile_width = int(tile_size[0])
                    tile_height = int(tile_size[1])
            elif section == 1:
                if line.split(',')[0] == '':
                    section = 2
                else:
                    split_line = line.split(',')
                    legend[split_line[0].strip()] = [e.strip() for e in split_line[1:] if e.strip() != '']
            elif section == 2:
                for x, cell in enumerate(line.split(',')):
                    if cell.strip() != '':
                        for entity in legend[cell.strip()]:
                            entity_data = engine.get_engine().resource_manager.get('entity', entity)
                            entities.append((entity, {'x': x*tile_width + entity_data.width/2.0, 'y': y*tile_height + entity_data.height/2.0}))
                y -= 1
        return entities

