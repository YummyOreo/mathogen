import cairo
from .object import Object
from .line import Line
from ..utils.color import BLACK

from typing import List, Tuple
import math

class ArcBetween(Object):
    def __init__(self, line_1: Line, line_2: Line, magnitude: float = 0.1, width: float = 0.03, color: List[float] = BLACK):
        self.line_1 = line_1
        self.line_2 = line_2

        self.intersection = self.get_intersection_point()

        self.color = color
        self.magnitude = magnitude
        self.width = width

        super().__init__(self.intersection, self.color)

    def get_intersection_point(self) -> List[float]:
        xdiff = (self.line_1.pos_start[0] - self.line_1.pos_end[0], self.line_2.pos_start[0] - self.line_2.pos_end[0])
        ydiff = (self.line_1.pos_start[1] - self.line_1.pos_end[1], self.line_2.pos_start[1] - self.line_2.pos_end[1])

        div = self.get_det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')

        d = (self.get_det(self.line_1.pos_start, self.line_1.pos_end), self.get_det(self.line_2.pos_start, self.line_2.pos_end))
        x = self.get_det(d, xdiff) / div
        y = self.get_det(d, ydiff) / div
        return [x, y]

    def get_vectors(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        vA = (self.line_1.pos_start[0] - self.line_1.pos_end[0], self.line_1.pos_start[-1] - self.line_1.pos_end[-1])
        vB = (self.line_2.pos_start[0] - self.line_2.pos_end[0], self.line_2.pos_start[-1] - self.line_2.pos_end[-1])

        return (vA, vB)

    def make_vectors(self, line_1, line_2):
        vA = [(line_1[0][0]-line_1[1][0]), (line_1[0][1]-line_1[1][1])]
        vB = [(line_2[0][0]-line_2[1][0]), (line_2[0][1]-line_2[1][1])]
        return [vA, vB]

    def get_det(self, vA, vB) -> float:
        return vA[0] * vB[1] - vA[1] * vB[0]

    def get_dot(self, vA, vB) -> float:
        return vA[0] * vB[0] + vA[1] * vB[1]

    def get_angle(self) -> float:
        vA, vB = self.get_vectors()

        dot_product = self.get_dot(vA, vB)
        magnitude_a = self.get_dot(vA, vA) ** 0.5
        magnitude_b = self.get_dot(vB, vB) ** 0.5

        angle = math.acos(dot_product/magnitude_b/magnitude_a)

        return angle

    def get_clockwise_angle(self, line_1, line_2):
        vA, vB = self.make_vectors(line_1, line_2)

        dot_product = self.get_dot(vA, vB)
        det = self.get_det(vA, vB)
        return math.atan2(det, dot_product)

    def get_add_angle(self):
        line_0 = [self.intersection, [self.intersection[0] + 1, self.intersection[1]]]
        angle_1 = self.get_clockwise_angle(line_0, self.line_1)
        angle_2 = self.get_clockwise_angle(line_0, self.line_2)

        angle_1_deg = angle_1 * (180/math.pi)
        angle_2_deg = angle_2 * (180/math.pi)

        if angle_1_deg + angle_2_deg < 0:
            add_angle = angle_1_deg if angle_1_deg < angle_2_deg else angle_2_deg
        elif angle_1_deg < 0 or angle_2_deg < 0:
            if abs(angle_1_deg) > abs(angle_2_deg):
                add_angle = angle_1_deg
            else:
                add_angle = angle_2_deg
        elif abs(angle_1_deg) > abs(angle_2_deg):
            add_angle = angle_2_deg
        else:
            add_angle = angle_1_deg

        if add_angle < 0:
            add_angle += 360

        return add_angle * (180/math.pi)

    def render(self, surface):
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        angle_between = self.get_angle()

        add_angle = self.get_add_angle()

        context.set_line_width(self.width)

        radius = self.magnitude

        context.arc(self.intersection[0], self.intersection[1], radius, angle_between, angle_between + add_angle)

        context.stroke()
        context.save()
