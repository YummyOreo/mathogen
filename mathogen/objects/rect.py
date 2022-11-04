import math
from typing import List, Optional

import cairo

from .object import Object
from ..utils.color import BLACK, BLUE

class RectOutline:
    def __init__(self, color: List[float] = BLUE, width: float = 0.01):
        self.width = width
        self.color = color

    def render(self, surface):
        context: cairo.Context = surface.context

        context.set_line_width(self.width)

        surface.set_color(self.color)

        context.stroke()

class Rect(Object):
    def __init__(self, position: List[float], width: float, height: float, color: List[float] = BLACK):
        self.position = position
        self.width = width
        self.height = height
        self.color = color

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color, self.width, self.height)

    def add_outline(self, outline: RectOutline):
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

        if self.radians:
            context.rotate(self.radians)

        if self.outline:
            context.rectangle(self.position[0], self.position[1], self.width, self.height)
            self.outline.render(surface)

        context.rectangle(self.position[0], self.position[1], self.width, self.height)

        surface.set_color(self.color)

        context.fill()
        context.restore()


