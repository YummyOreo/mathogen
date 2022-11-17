from typing import List, Any
import math
import cairo

from .object import Object
from ..utils.color import BLACK

class Line(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position_start": List[float],
                "position_end": List[float],
                "width": float = 0.006,
                "position_end": List[float] = BLACK
                }
        '''
        options: Any = {"color": BLACK, "width": 0.005}
        options.update(user_options)

        self.pos_start = options["position_start"]
        self.pos_end = options["position_end"]
        self.width = options["width"]

        self.color = options["color"]

        super().__init__(self.pos_start, self.color, self.width)

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        context.set_line_width(self.width)

        context.move_to(self.pos_start[0], self.pos_start[1])
        context.line_to(self.pos_end[0], self.pos_end[1])

        context.stroke()
        context.restore()

    def get_slope(self):
        if (self.pos_start[0] - self.pos_end[0]) == 0:
            return math.inf
        return (self.pos_start[1] - self.pos_end[1]) / (self.pos_start[0] - self.pos_end[0])

    def get_diff(self) -> List[float]:
        return [self.pos_start[0] - self.pos_end[0], self.pos_start[1] - self.pos_end[1]]

    def get_middle(self):
        return [(self.pos_start[0] + self.pos_end[0]) / 2, (self.pos_start[1] + self.pos_end[1]) / 2]

class CurveBetween(Line):
    def __init__(self, user_options):
        '''
        user_options = {
                "position_start": List[float],
                "position_end": List[float],
                "width": float = 0.005,
                "color": List[float] = BLACK,
                magnitude: float = 0.5
                }
        '''
        options: Any = {"color": BLACK, "width": 0.005, "magnitude": 0.5}
        options.update(user_options)

        self.pos_start = options["position_start"]
        self.pos_end = options["position_end"]

        self.magnitude = options["magnitude"]
        self.width = options["width"]

        self.color = options['color']

        super().__init__(options)

    def get_perpendicular_slope(self):
        slope = self.get_slope()
        if slope == 0:
            return math.inf
        elif not math.isfinite(slope):
            return 0
        return -1/slope

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

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
