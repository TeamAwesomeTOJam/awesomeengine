import engine
import rectangle


class SimpleLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):
        for entity in engine.get_engine().entity_manager.get_by_tag(self.tag):
            entity.handle('draw', camera)

class SimpleCroppedLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):
        for entity in engine.get_engine().entity_manager.get_in_area(self.tag, rectangle.from_entity(camera.entity)):
            entity.handle('draw', camera)

class DepthSortedLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):

        entities_to_draw = sorted(engine.get_engine().entity_manager.get_in_area(self.tag, rectangle.from_entity(camera.entity), precise=False),
                                  key=lambda entity: rectangle.from_entity(entity).bottom)

        for entity in entities_to_draw:
            entity.handle('draw', camera)

class SolidBackgroundLayer(object):

    def __init__(self, color):
        self.color = color

    def draw(self, camera):
        camera.clear(self.color)