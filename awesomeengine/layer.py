import engine
import rectangle
import Box2D


class SimpleLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):
        for entity in engine.get().entity_manager.get_by_tag(self.tag):
            entity.handle('draw', camera)

class SimpleCroppedLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):
        for entity in engine.get().entity_manager.get_in_area(self.tag, rectangle.from_entity(camera.entity)):
            entity.handle('draw', camera)

class DepthSortedLayer(object):

    def __init__(self, tag):
        self.tag = tag

    def draw(self, camera):

        entities_to_draw = sorted(engine.get().entity_manager.get_in_area(self.tag, rectangle.from_entity(camera.entity), precise=False),
                                  key=lambda entity: rectangle.from_entity(entity).bottom)

        for entity in entities_to_draw:
            entity.handle('draw', camera)

class SolidBackgroundLayer(object):

    def __init__(self, color):
        self.color = color

    def draw(self, camera):
        camera.clear(self.color)

class GridLayer(object):

    def __init__(self, colour, size):
        self.colour = colour
        self.size = size

    def draw(self, camera):
        r = rectangle.from_entity(camera.entity).bounding_rect()

        min_grid_x = int(r.left / self.size)
        max_grid_x = int(r.right / self.size + 1)
        min_grid_y = int(r.bottom / self.size)
        max_grid_y = int(r.top / self.size + 1)

        for x in range(min_grid_x, max_grid_x):
            camera.draw_line(self.colour,(x*self.size, r.top), (x*self.size, r.bottom))

        for y in range(min_grid_y, max_grid_y):
            camera.draw_line(self.colour, (r.left, y*self.size), (r.right, y*self.size))

class PhysicsLayer(object):

    def draw(self, camera):
        world = engine.get().box2d_world

        query = DrawQueryCallback(camera)

        rect = rectangle.from_entity(camera.entity).bounding_rect()

        aabb = Box2D.b2AABB(lowerBound=Box2D.b2Vec2(rect.bottom_left),upperBound=Box2D.b2Vec2(rect.top_right))

        world.QueryAABB(query, aabb)


class DrawQueryCallback(Box2D.b2QueryCallback):

    def __init__(self, camera):
        Box2D.b2QueryCallback.__init__(self)

        self.camera = camera

    def ReportFixture(self, fixture):
        points = fixture.shape.vertices
        transformed_points = map(fixture.body.GetWorldPoint, points)
        transformed_points.append(transformed_points[0])
        self.camera.draw_lines((255,0,0,255), transformed_points)
        return True
