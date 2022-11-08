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

class CurveBetween(Object):
    def __init__(self, position_start: List[float], position_end: List[float], magnitude: float = 0.5, color: List[float] = BLACK, width: float = 0.01):
        self.pos_start = position_start
        self.pos_end = position_end

        self.magnitude = magnitude
        self.width = width

        self.color = color

        super().__init__(self.pos_start, self.color)

    def get_perpendicular_slope(self, position_1: List[float], position_2: List[float]) -> List[float]:
        x_inc = (position_2[0] - position_1[0])
        y_inc = (position_2[1] - position_1[1])

        return [y_inc * -1, x_inc]

    def get_middle(self, pos_1: List[float], pos_2: List[float]):
        return [(pos_1[0] + pos_2[0]) / 2, (pos_1[1] + pos_2[1]) / 2]

    def render(self, surface):
        context: cairo.Context = surface.context

        super().render(surface)

        context.set_line_width(self.width)
        context.move_to(*self.pos_start)

        perpendicular_slope = self.get_perpendicular_slope(self.pos_start, self.pos_end)

        middle = self.get_middle(self.pos_start, self.pos_end)

        x_inc = perpendicular_slope[0] * self.magnitude
        y_inc = perpendicular_slope[1] * self.magnitude

        point = [middle[0] + x_inc, middle[1] + y_inc]

        context.curve_to(*self.pos_start, *point, *self.pos_end)
        context.stroke()

        context.restore()
