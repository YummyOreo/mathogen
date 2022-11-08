from typing import List

from .object import Object, cairo
from ..utils.color import BLACK

class Line(Object):
    def __init__(self, position_start: List[float], position_end: List[float], color: List[float] = BLACK, width: float = 0.005):
        self.pos_start = position_start
        self.pos_end = position_end
        self.width = width

        self.color = color

        super().__init__(self.pos_start, self.color)

    def render(self, surface):
        context: cairo.Context = surface.context

        super().render(surface)
        context.set_line_width(self.width)

        context.move_to(*self.pos_start)
        context.line_to(*self.pos_end)

        context.stroke()
        context.restore()
