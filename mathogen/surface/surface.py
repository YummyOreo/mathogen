from typing import List
import cairo

class Surface:
    '''
    Inits the surface,
    - scales the context to the width and height
    - sets the color to black
    - saves the context and surface
    '''
    def __init__(self, width: int, height: int, filename: str):
        self.width = width
        self.height = height
        self.scaled_width = width
        self.scaled_height = height
        self.surface = cairo.SVGSurface(filename, width, height)

        self.context: cairo.Context = cairo.Context(self.surface)

        self.context.scale(self.width, self.height)

        self.color = [0, 0, 0, 1]
        self.context.set_source_rgba(*self.color)

    # Sets the color to a given color
    def set_color(self, color: List[float]):
        # To save (little) performance. If it is already set to the same thing, don't re-set it
        if self.color == color:
            return

        self.color = color

        self.context.set_source_rgba(*color)

    # moving the context
    def move_to(self, position: List[float]):
        self.context.move_to(position[0], position[1])

    # Add/render a object
    def add(self, *objects):
        for object in objects:
            object.render(self)

    '''
    Changes the scale in the context
    the scale is how much 1 is multiplied by.
    Ie, if the scale is = to the width and heigh, then 1 will = the width and height
    '''
    def change_scale(self, width: int, heigh: int):
        self.scaled_width = width
        self.scaled_height = heigh

        self.context.scale(width, heigh)
