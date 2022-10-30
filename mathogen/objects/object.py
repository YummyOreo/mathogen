from typing import List, Optional
from ..utils.color import BLACK
import cairo

class Object:
    def __init__(self, position: List[float], color: List[float], width: Optional[float] = None, height: Optional[float] = None):
        self.color = color
        self.position = position

        self.width, self.height = width, height

    def render(self, surface):
        context: cairo.Context = surface.context
        context.save()

        surface.set_color(self.color)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_position(self):
        return self.position

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_middle(self):
        '''
        Gets the middle of a regular object
            A regular object is a object that is a quadrilateral and has a defined height and width
        '''
        middle = [self.get_x() + (self.get_width() / 2), self.get_y() + (self.get_height() / 2))]
        return middle
