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

class RoundRectOutline(RectOutline):
    def render(self, surface):
        context: cairo.Context = surface.context

        surface.set_color(self.color)

        context.set_line_width(self.width)
        context.stroke()


class RoundRect(Object):
    def __init__(self, position: List[float], width: float, height: float, radius: float, color: List[float] = BLACK):
        self.position = position
        self.width = width
        self.height = height
        self.color = color

        self.radius = radius * (math.pi / 180)

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color, self.width, self.height)

    def add_outline(self, outline: Optional[RoundRectOutline] = None):
        if not outline:
            outline = RoundRectOutline()

        self.outline = outline

    def render(self, surface):
        context: cairo.Context = surface.context

        super().render(surface)

        x = self.position[0]
        x1 = self.position[0] + self.width
        y = self.position[1]
        y1 = self.position[1] + self.height


        if self.width / 2 < self.radius:
            if self.height / 2 < self.radius:
                context.move_to(x, (y + y1) / 2)
                context.curve_to(x, y, x, y, (x + x1) / 2, y)
                context.curve_to(x1, y, x1, y, x1, (y + y1) / 2)
                context.curve_to(x1, y1, x1, y1, (x1 + x) / 2, y1)
                context.curve_to(x, y1, x, y1, x, (y + y1) / 2)
            else:
                context.move_to(x, y + self.radius)
                context.curve_to(x, y, x, y, (x + x1) / 2, y)
                context.curve_to(x1, y, x1, y, x1, y + self.radius)
                context.line_to(x1, y1 - self.radius)
                context.curve_to(x1, y1, x1, y1, (x1 + x) / 2, y1)
                context.curve_to(x, y1, x, y1, x, y1 - self.radius)
        else:
            if self.height / 2 < self.radius:
                context.move_to(x, (y + y1) / 2)
                context.curve_to(x, y, x, y, x + self.radius, y)
                context.line_to(x1 - self.radius, y)
                context.curve_to(x1, y, x1, y, x1, (y + y1) / 2)
                context.curve_to(x1, y1, x1, y1, x1 - self.radius, y1)
                context.line_to(x + self.radius, y1)
                context.curve_to(x, y1, x, y1, x, (y + y1) / 2)
            else:
                context.move_to(x, y + self.radius)
                context.curve_to(x, y, x, y, x + self.radius, y)
                context.line_to(x1 - self.radius, y)
                context.curve_to(x1, y, x1, y, x1, y + self.radius)
                context.line_to(x1, y1 - self.radius)
                context.curve_to(x1, y1, x1, y1, x1 - self.radius, y1)
                context.line_to(x + self.radius, y1)
                context.curve_to(x, y1, x, y1, x, y1 - self.radius)

        context.close_path()

        context.fill_preserve()
        if self.outline:
            self.outline.render(surface)

        context.restore()
