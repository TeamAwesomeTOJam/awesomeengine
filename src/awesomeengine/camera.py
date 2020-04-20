from abc import ABC, abstractmethod

from awesomeengine import engine
from awesomeengine.geometry import Rect, Vec


class Camera(ABC):

    @abstractmethod
    def world_to_screen(self, screen_rect, point):
        pass

    @abstractmethod
    def world_to_screen_angle(self, a):
        pass

    @abstractmethod
    def screen_to_world(self, screen_rect, point):
        pass

    @abstractmethod
    def entities(self):
        pass

    @abstractmethod
    def before_draw(self):
        pass


class NullCamera(Camera):

    def __init__(self):
        pass

    def world_to_screen(self, screen_rect, point):
        return point

    def world_to_screen_angle(self, a):
        return a

    def screen_to_world(self, screen_rect, point):
        return point

    def entities(self):
        return []

    def before_draw(self):
        pass


class TopDownCamera(Camera):

    def __init__(self, world, entity=None):
        self.world = world
        self.world_rect = None
        self.entity = entity

    def world_to_screen(self, screen_rect, point):
        world_displacement = point - self.world_rect.center
        rotated_world_displacement = world_displacement.rotate(-self.world_rect.a)

        screen_displacement = Vec(int(rotated_world_displacement.x * screen_rect.w / self.world_rect.w),
                                  -int(rotated_world_displacement.y * screen_rect.h / self.world_rect.h))
        screen_point = screen_rect.center + screen_displacement

        return screen_point

    def world_to_screen_angle(self, a):
        return self.world_rect.angle - a

    def screen_to_world(self, screen_rect, point):
        screen_displacement = point - screen_rect.center
        rotated_world_displacement = Vec(screen_displacement.x * self.world_rect.w / screen_rect.w,
                                         -screen_displacement.y * self.world_rect.h / screen_rect.h)
        world_displacement = rotated_world_displacement.rotate(self.world_rect.a)
        world_point = self.world_rect.center + world_displacement

        return world_point

    def entities(self):
        engine.get().entity_manager.get_in_area(self.world, self.world_rect)

    def before_draw(self):
        e = engine.get().entity_manager.get_by_name(self.target)
        self.world_rect = Rect.from_entity(e)