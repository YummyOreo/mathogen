import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Rect, BLUE, RoundRect

from typing import List

'''
Test for the creating, and rendering of a rectangle
'''
class RectTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        rectangle: Rect = Rect({"position": [0.1, 0.1], "width": 0.4, "height": 0.4})
        rectangle.add_outline().rotate(10)

        mid: List[float] = [x - 0.05 for x in rectangle.get_middle()]
        rectangle_2: RoundRect = RoundRect({"position": mid, "width": 0.2, "height": 0.1, "radius": 0.5})
        rectangle_2.rotate(19)
        rectangle_2.add_outline()

        '''
        Renders both
        '''
        self.add(rectangle, rectangle_2)
