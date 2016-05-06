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

class GridLayer(object):

    def draw(self, camera):
        r = rectangle.from_entity(camera.entity).bounding_rect()

        grid_size = 32
        c = (255,0,0,255)


        min_grid_x = int(r.left / grid_size)
        max_grid_x = int(r.right / grid_size + 1)
        min_grid_y = int(r.bottom / grid_size)
        max_grid_y = int(r.top / grid_size + 1)

        for x in range(min_grid_x, max_grid_x):
            camera.draw_line(c,(x*grid_size, r.top), (x*grid_size, r.bottom))

        for y in range(min_grid_y, max_grid_y):
            camera.draw_line(c, (r.left, y*grid_size), (r.right, y*grid_size))
