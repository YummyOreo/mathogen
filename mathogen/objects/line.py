from typing import List
import math

from .object import Object, cairo
from ..utils.color import BLACK

class Line(Object):
    def __init__(self, position_start: List[float], position_end: List[float], color: List[float] = BLACK, width: float = 0.005):
        self.pos_start = position_start
        self.pos_end = position_end
        self.width = width

        self.color = color

        super().__init__(self.pos_start, self.color)
        super().set_width(width)

    def render(self, surface):
        context: cairo.Context = surface.context

        super().render(surface)
        context.set_line_width(self.width)

        context.move_to(self.pos_start[0], self.pos_start[1])
        context.line_to(self.pos_end[0], self.pos_end[1])

        context.stroke()
        context.restore()

    def get_slope(self):
        if (self.pos_start[0] - self.pos_end[0]) == 0:
            return math.inf
        return (self.pos_start[1] - self.pos_end[1]) / (self.pos_start[0] - self.pos_end[0])

    def get_middle(self):
        return [(self.pos_start[0] + self.pos_end[0]) / 2, (self.pos_start[1] + self.pos_end[1]) / 2]

    def super_render(self, surface):
        super().render(surface)

class CurveBetween(Line):
    def __init__(self, position_start: List[float], position_end: List[float], magnitude: float = 0.5, color: List[float] = BLACK, width: float = 0.01):
        self.pos_start = position_start
        self.pos_end = position_end

        self.magnitude = magnitude
        self.width = width

        self.color = color

        super().__init__(position_start, position_end, self.color, self.width)

    def get_perpendicular_slope(self):
        slope = self.get_slope()
        if slope == 0:
            return math.inf
        elif not math.isfinite(slope):
            return 0
        return -1/slope

    def render(self, surface):
        context: cairo.Context = surface.context

        super().render(surface)
        super().super_render(surface)

        context.set_line_width(self.width)
        context.move_to(*self.pos_start)

        perpendicular_slope = self.get_perpendicular_slope()

        middle = self.get_middle()

        if not math.isfinite(perpendicular_slope):
            point = [middle[0], middle[1] + self.magnitude]
        elif perpendicular_slope == 0:
            point = [middle[0] + self.magnitude, middle[1] + (perpendicular_slope * self.magnitude)]
        else:
            point = [middle[0] + (perpendicular_slope * self.magnitude), middle[1] + self.magnitude]

        context.curve_to(self.pos_start[0], self.pos_start[1], point[0], point[1], self.pos_end[0], self.pos_end[1])
        context.stroke()

        context.restore()
