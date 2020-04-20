from math import sin, cos, radians
from typing import NamedTuple


class Vec(NamedTuple):
    x: float
    y: float

    def __add__(self, other):
        try:
            return Vec(self.x + other[0], self.y + other[1])
        except:
            return NotImplemented

    def __sub__(self, other):
        try:
            return Vec(self.x - other[0], self.y - other[1])
        except:
            return NotImplemented

    def __mul__(self, other):
        try:
            if isinstance(other, (int, float)):
                return Vec(self.x * other, self.y * other)
            else:
                return self.x * other[0] + self.y * other[1]
        except:
            return NotImplemented

    def __truediv__(self, other):
        try:
            return Vec(self.x / other, self.y / other)
        except:
            return NotImplemented

    def rotate(self, degrees):
        if degrees == 0:
            return self
        else:
            return Vec(self.x * cos(radians(degrees)) + self.y * sin(radians(degrees)),
                       self.y * cos(radians(degrees)) - self.x * sin(radians(degrees)))


class Rect(NamedTuple):
    x: float
    y: float
    w: float
    h: float
    a: float = 0

    @classmethod
    def from_entity(cls, entity):
        try:
            a = entity.angle
        except AttributeError:
            a = 0
        return cls(entity.pos.x, entity.pos.y, entity.size.x, entity.size.y, a)

    @property
    def top_left(self):
        if self.a == 0:
            return Vec(self.x - self.w/2, self.y + self.h/2)
        else:
            return Vec(self.x - cos(radians(self.a)) * self.w/2 - sin(radians(self.a)) * self.h/2,
                    self.y + cos(radians(self.a)) * self.h/2 - sin(radians(self.a)) * self.w/2)

    @property
    def top_right(self):
        if self.a == 0:
            return Vec(self.x + self.w / 2, self.y + self.h / 2)
        else:
            return Vec(self.x + cos(radians(self.a)) * self.w/2 - sin(radians(self.a)) * self.h/2,
                    self.y + cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2)

    @property
    def bottom_left(self):
        if self.a == 0:
            return Vec(self.x - self.w/2 , self.y - self.h/2)
        else:
            return Vec(self.x - cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2,
                    self.y - cos(radians(self.a)) * self.h/2 - sin(radians(self.a)) * self.w/2)

    @property
    def bottom_right(self):
        if self.a == 0:
            return Vec(self.x + self.w/2, self.y - self.h/2)
        else:
            return Vec(self.x + cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2,
                    self.y - cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2)

    @property
    def center(self):
        return Vec(self.x, self.y)

    @property
    def corners(self):
        return (self.top_left, self.bottom_left, self.bottom_right, self.top_right)

    @property
    def bottom(self):
        return self.y - cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2

    @property
    def top(self):
        return self.y + cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2

    @property
    def left(self):
        return self.x - cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2

    @property
    def right(self):
        return self.x + cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2

    def bounding_rect(self):
        cosw = self.w * cos(radians(self.a))
        sinw = self.w * sin(radians(self.a))
        cosh = self.h * cos(radians(self.a))
        sinh = self.h * sin(radians(self.a))

        nwidth = int(max(cosw + sinh, cosw - sinh, -1 * cosw + sinh, -1 * cosw - sinh))
        nheight = int(max(sinw + cosh, sinw - cosh, -1 * sinw + cosh, -1 * sinw - cosh))

        return Rect(self.x, self.y, nwidth, nheight)

    def contains(self, p):
        x = p[0]
        y = p[1]
        if self.a == 0:
            return self.x - self.w/2 <= x <= self.x + self.w/2 and self.y - self.h/2 <= y <= self.y + self.h/2
        else:
            #TODO check rotated rects
            return False

    def intersects(self, other):
        if self.a == 0 and other.a == 0:
            a_x, a_y = self.bottom_left
            a_w, a_h = self.w, self.h
            b_x, b_y = other.bottom_left
            b_w, b_h = other.w, other.h

            if (a_x > b_x + b_w
                    or b_x > a_x + a_w
                    or a_y > b_y + b_h
                    or b_y > a_y + a_h):
                return False
            else:
                return True
        else:
            for r in [self, other]:
                for i in range(4):
                    p1 = r.corners[i]
                    p2 = r.corners[(i + 1) % 4]
                    normal = (p2[1] - p1[1], p1[0] - p2[0])
                    min_a = None
                    max_a = None
                    for p in self.corners:
                        projected = normal[0] * p[0] + normal[1] * p[1]
                        if min_a is None or projected < min_a:
                            min_a = projected
                        if max_a is None or projected > max_a:
                            max_a = projected

                    min_b = None
                    max_b = None
                    for p in other.corners:
                        projected = normal[0] * p[0] + normal[1] * p[1]
                        if min_b is None or projected < min_b:
                            min_b = projected
                        if max_b is None or projected > max_b:
                            max_b = projected
                    if max_a < min_b or max_b < min_a:
                        return False

            return True