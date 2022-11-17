import cairo
from .object import Object
from ..utils.color import BLACK

from typing import List, Optional
import math

class Arc(Object):
    def __init__(self, center: List[float], radians: float, magnitude: float = 0.1, color: List[float] = BLACK, width: float = 0.03):
        self.center = center
        self.magnitude = magnitude
        self.arc_radians = radians

        self.color = color
        self.stroke_width = width

        self.radians = None

        super().__init__(self.center, self.color)

    def rotate(self, degrees: float):
        self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        context.set_line_width(self.stroke_width)

        start = 0
        end = self.arc_radians
        if self.radians:
            start = self.radians
            end = start + self.arc_radians

        context.arc(self.center[0], self.center[1], self.magnitude, start, end)

        context.stroke()
        context.restore()
