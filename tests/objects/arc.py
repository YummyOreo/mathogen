import sys
sys.path.append("..")

from mathogen.mathogen import Surface, RED, Arc
import math

class ArcTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        arc = Arc([0.5, 0.5], 320 * (math.pi/180), color=RED).rotate(90)

        self.add(arc)

