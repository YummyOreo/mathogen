import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Line, CurveBetween

from typing import List

class LineTests(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        line = Line({"position_start": [0.1, 0.2], "position_end": [0.5, 0.5]})
        curve = CurveBetween({"position_start": [0.1, 0.2], "position_end": [0.5, 0.5], "magnitude": -0.1})
        self.add(line, curve)
