
import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Circle, CircleOutline, BLUE

class CircleTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        blue = BLUE.copy()
        blue[-1] = 0.5
        circle = Circle([0.1, 0.2], 0.03, 0.02, blue).rotate(10).add_outline(CircleOutline(color=BLUE))

        self.add(circle)
