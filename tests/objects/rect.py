import sys
from typing import List

sys.path.append("../")

from mathogen.mathogen import Surface, Rect, RectOutline, BLUE

'''
Test for the creating, and rendering of a rectangle
'''
class RectTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        rectangle: Rect = Rect([0.1, 0.1], 0.4, 0.4)
        rectangle.add_outline(RectOutline())

        mid: List[float] = [x - 0.05 for x in rectangle.get_middle()]
        rectangle_2: Rect = Rect(mid, 0.1, 0.1, color=BLUE)

        '''
        Renders both
        '''
        self.add(rectangle, rectangle_2)
