import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Circle, BLUE

class CircleTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        blue = BLUE.copy()
        blue[-1] = 0.5
        circle = Circle({"position": [0.1, 0.2], "width": 0.03, "height": 0.02, "color": blue}).rotate(10).add_outline()

        self.add(circle)
