import sys
sys.path.append("..")

from mathogen.mathogen import Surface, BLUE, Line, RED

class ArcTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        line_1 = Line([0.1, 0.1], [0.5, 0.5])
        line_2 = Line([0.1, 0.5], [0.3, 0.1])

        self.add(line_1, line_2)

