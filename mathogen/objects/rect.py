import math
from typing import Any

import cairo

from .object import Object
from ..utils.color import BLACK, BLUE

class Rect(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position": List[float],
                "width": float,
                "height": float,
                "color": List[float] = BLACK
                }
        '''
        options: Any = {"color": BLACK}
        options.update(user_options)

        self.position = options["position"]
        self.width = options["width"]
        self.height = options["height"]
        self.color = options["color"]

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color, self.width, self.height)

    def add_outline(self, outline_options = {}):
        '''
        user_options = {
                "width": float = 0.1,
                "color": List[float] = BLUE
                }
        '''
        outline = {"color": BLUE, "width": 0.01}
        outline.update(outline_options)

        self.outline = outline
        return self

    def rotate(self, degrees: float):
        self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()

        if self.radians:
            context.rotate(self.radians)

        if self.outline:
            context.rectangle(self.position[0], self.position[1], self.width, self.height)
            self.render_outline(surface)

        context.rectangle(self.position[0], self.position[1], self.width, self.height)

        surface.set_color(self.color)

        context.fill()
        context.restore()

    def render_outline(self, surface):
        if not self.outline: return
        context: cairo.Context = surface.context

        context.set_line_width(self.outline["width"])

        surface.set_color(self.outline["color"])

        context.stroke()

class RoundRect(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position": List[float],
                "width": float,
                "height": float,
                "radius": float (degrees),
                "color": List[float] = BLACK
                }
        '''
        options: Any = {"color": BLACK}
        options.update(user_options)

        self.position = options["position"]
        self.width = options["width"]
        self.height = options["height"]
        self.color = options["color"]

        self.radius = options["radius"] * (math.pi / 180)

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color, self.width, self.height)

    def add_outline(self, outline_options = {}):
        '''
        user_options = {
                "width": float = 0.01,
                "color": List[float] = BLUE
                }
        '''
        outline = {"color": BLUE, "width": 0.01}
        outline.update(outline_options)

        self.outline = outline
        return self

    def rotate(self, degrees: float):
        self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        if self.radians:
            context.rotate(self.radians)

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
            self.render_outline(surface)

        context.restore()

    def render_outline(self, surface):
        if not self.outline: return
        context: cairo.Context = surface.context

        surface.set_color(self.outline["color"])

        context.set_line_width(self.outline["width"])
        context.stroke()

