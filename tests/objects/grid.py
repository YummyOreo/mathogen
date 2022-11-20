import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Grid

class GridTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        grid = Grid({
            "position": [0.1, 0.1],
            "rows": 10,
            "columns": 10,
            }).add_fill([0, 1, 0, 0.5])

        self.add(grid)

