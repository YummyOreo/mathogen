import math
from typing import List, Optional

import cairo

from .object import Object
from ..utils.color import BLACK, BLUE

class CircleOutline:
    def __init__(self, color: List[float] = BLUE, width: float = 0.01):
        self.width = width
        self.color = color

    def render(self, surface, circle):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)
        context.identity_matrix()

        context.set_line_width(self.width * ((circle.width + circle.height) * 10))

        context.stroke()
        context.restore()

class Circle(Object):
    def __init__(self, position: List[float], width: float, height: float, color: List[float] = BLACK):
        self.position = position
        self.width = width
        self.height = height
        self.colo = color

        self.outline = None
        self.radians = None

        super().__init__(position, color, height, width)

    def add_outline(self, outline: Optional[CircleOutline] = None):
        if not outline:
            outline = CircleOutline()
        self.outline = outline
        return self

    def rotate(self, degrees: Optional[float] = None, radians: Optional[float] = None):
        if radians:
            self.radians = radians
        elif degrees:
            self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        context.translate(*self.position)

        if self.radians:
            context.rotate(self.radians)
        else:
            context.rotate(90 * (math.pi / 180))


        context.scale(self.width / 2.0, self.height / 2.0)
        context.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)

        context.fill_preserve()

        context.restore()

        if self.outline:
            self.outline.render(surface, self)
