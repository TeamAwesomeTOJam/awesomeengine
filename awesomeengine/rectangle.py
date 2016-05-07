from math import sin, cos, radians

def from_entity(entity):
    try:
        a = entity.angle
    except AttributeError:
        a = 0
    return Rect(entity.x, entity.y, entity.width, entity.height, a)

class Rect(object):

    def __init__(self, x, y, width, height, angle = 0):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.a = angle

    def __str__(self):
        return 'Rect({},{},{},{},{})'.format(self.x, self.y, self.w, self.h, self.a)

    @property
    def top_left(self):
        return (self.x - cos(radians(self.a)) * self.w/2 - sin(radians(self.a)) * self.h/2,
                self.y + cos(radians(self.a)) * self.h/2 - sin(radians(self.a)) * self.w/2)

    @property
    def top_right(self):
        return (self.x + cos(radians(self.a)) * self.w/2 - sin(radians(self.a)) * self.h/2,
                self.y + cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2)

    @property
    def bottom_left(self):
        return (self.x - cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2,
                self.y - cos(radians(self.a)) * self.h/2 - sin(radians(self.a)) * self.w/2)

    @property
    def bottom_right(self):
        return (self.x + cos(radians(self.a)) * self.w/2 + sin(radians(self.a)) * self.h/2,
                self.y - cos(radians(self.a)) * self.h/2 + sin(radians(self.a)) * self.w/2)

    @property
    def center(self):
        return (self.x, self.y)

    @property
    def corners(self):
        return [self.top_left, self.bottom_left, self.bottom_right, self.top_right]

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
