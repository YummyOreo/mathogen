import math
from typing import Any

import cairo

from .object import Object
from ..utils.color import BLACK, BLUE

class Circle(Object):
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

        super().__init__(self.position, self.color, self.height, self.width)

    def add_outline(self, outline_options = {}):
        '''
        user_options = {
                "width": float = 0.3,
                "color": List[float] = BLUE
                }
        '''
        outline = {"color": BLUE, "width": 0.3}
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
            self.render_outline(surface)

    def render_outline(self, surface):
        if not self.outline: return
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.outline["color"])

        context.identity_matrix()

        context.set_line_width(self.outline["width"])


        context.stroke()
        context.restore()
