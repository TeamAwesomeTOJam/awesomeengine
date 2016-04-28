import weakref
import rectangle


class SpatialMap(object):
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = {}
        self.reverse_map = weakref.WeakKeyDictionary()
    
    def add(self, entity):
        try:
            grid_squares = self._get_grid_squares(rectangle.from_entity(entity))
            for square in grid_squares:
                if not square in self.map:
                    self.map[square] = weakref.WeakSet()
                    
                self.map[square].add(entity)
                
            self.reverse_map[entity] = grid_squares
        except AttributeError:
            pass
                
    def remove(self, entity):
        try:
            for square in self.reverse_map[entity] | self._get_grid_squares(rectangle.from_entity(entity)):
                if square in self.map:
                    self.map[square].discard(entity)
                    if len(self.map[square]) == 0:
                        del self.map[square]
                
            del self.reverse_map[entity]
        except AttributeError:
            pass
    
    def update(self, entity):
        old_squares = self.reverse_map[entity]
        new_squares = self._get_grid_squares(rectangle.from_entity(entity))
        
        for square in old_squares - new_squares:
            self.map[square].discard(entity)
            if len(self.map[square]) == 0:
                del self.map[square]
                
        for square in new_squares - old_squares:
            if square in self.map:
                self.map[square].add(entity)
            else:
                self.map[square] = {entity}
                
        self.reverse_map[entity] = new_squares  
    
    def get(self, rect, precise=True):
        possible_intersections = set()
        for square in self._get_grid_squares(rect):
            if square in self.map:
                possible_intersections.update(self.map[square])
        
        if precise:
            intersections = set()
            for entity in possible_intersections:
                if self._rects_intersect(rect, rectangle.from_entity(entity)):
                    intersections.add(entity)
            return intersections

        return possible_intersections
    
    def _rects_intersect(self, a, b):
        if a.a == 0 and b.a == 0:
            a_x, a_y = a.bottom_left
            a_w, a_h = a.w, a.h
            b_x, b_y = b.bottom_left
            b_w, b_h = b.w, b.h

            if (a_x > b_x + b_w
                    or b_x > a_x + a_w
                    or a_y > b_y + b_h
                    or b_y > a_y + a_h):
                return False
            else:
                return True
        else:
            # return False
            for r in [a, b]:
                for i in range(4):
                    p1 = r.corners[i]
                    p2 = r.corners[(i + 1) % 4]
                    normal = (p2[1] - p1[1], p1[0] - p2[0])
                    min_a = None
                    max_a = None
                    for p in a.corners:
                        projected = normal[0] * p[0] + normal[1] * p[1]
                        if min_a == None or projected < min_a:
                            min_a = projected
                        if max_a == None or projected > max_a:
                            max_a = projected

                    min_b = None
                    max_b = None
                    for p in b.corners:
                        projected = normal[0] * p[0] + normal[1] * p[1]
                        if min_b == None or projected < min_b:
                            min_b = projected
                        if max_b == None or projected > max_b:
                            max_b = projected
                    if max_a < min_b or max_b < min_a:
                        return False

            return True


        
    def _get_grid_squares(self, rect):
        r = rect.bounding_rect()
        min_grid_x = int(r.bottom_left[0] / self.grid_size)
        max_grid_x = int((r.bottom_left[0] + r.w) / self.grid_size + 1)
        min_grid_y = int(r.bottom_left[1] / self.grid_size)
        max_grid_y = int((r.bottom_left[1] + r.h) / self.grid_size + 1)
        return set((x, y) for x in range(min_grid_x, max_grid_x + 1) for y in range(min_grid_y, max_grid_y + 1))
