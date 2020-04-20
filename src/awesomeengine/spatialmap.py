from awesomeengine.geometry import Rect


class SpatialMap:
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = {}
        self.reverse_map = {}
    
    def add(self, entity):
        try:
            r = Rect.from_entity(entity)
            if r is None:
                return
            grid_squares = self._get_grid_squares(r)
            for square in grid_squares:
                if not square in self.map:
                    self.map[square] = set()
                    
                self.map[square].add(entity)
                
            self.reverse_map[entity] = grid_squares
        except AttributeError:
            pass
            
    def remove(self, entity):
        try:
            for square in self.reverse_map[entity] | self._get_grid_squares(Rect.from_entity(entity)):
                if square in self.map:
                    self.map[square].discard(entity)
                    if len(self.map[square]) == 0:
                        del self.map[square]
                
            del self.reverse_map[entity]
        except AttributeError:
            pass
                
    def update(self, entity):
        try:
            old_squares = self.reverse_map[entity]
            new_squares = self._get_grid_squares(Rect.from_entity(entity))

            for square in old_squares - new_squares:
                self.map[square].discard(entity)

            for square in new_squares - old_squares:
                if not square in self.map:
                    self.map[square] = set()

                self.map[square].add(entity)

            self.reverse_map[entity] = new_squares
        except KeyError:
            pass
    
    def get(self, rect):
        possible_intersections = set()
        for square in self._get_grid_squares(rect):
            if square in self.map:
                possible_intersections.update(self.map[square])

        return possible_intersections

    def _get_grid_squares(self, rect):
        r = rect.bounding_rect()
        x,y = r.bottom_left
        min_grid_x = int(x / self.grid_size)
        max_grid_x = int((x + r.w) / self.grid_size + 1)
        min_grid_y = int(y / self.grid_size)
        max_grid_y = int((y + r.h) / self.grid_size + 1)
        return set((x, y) for x in range(min_grid_x, max_grid_x + 1) for y in range(min_grid_y, max_grid_y + 1))
