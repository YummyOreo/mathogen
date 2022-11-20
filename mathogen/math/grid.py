from typing import Any, List

import cairo

from ..objects.object import Object
from ..objects.rect import Rect
from ..utils.color import BLACK, create_color

class Grid(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position": List[float],
                "rows": float,
                "columns": float,
                "color": List[float] = BLACK
                "outline_width": float = 0.001
                "box_width": float = 0.1,
                "box_height": float = 0.1,
                "box_style": str = "rect"
                    Options:
                        [
                            "rect"
                        ]
                }
        '''
        options: Any = {"color": BLACK, "box_width": 0.1, "box_height": 0.1, "box_style" : "rect", "outline_width": 0.001}
        options.update(user_options)

        self.position = options['position']
        self.rows = options["rows"]
        self.columns = options["columns"]

        self.outline_color = options["color"]
        self.outline_width = options["outline_width"]

        self.box = {
                "box_width": options["box_width"],
                "box_height": options["box_height"],
                "box_style": options["box_style"]
                }

        self.width = self.rows * self.box["box_width"]
        self.height = self.columns * self.box["box_height"]

        self.fill_color = create_color(0, 0, 0, 0)
        self.radians = None

        super().__init__(self.position, self.outline_color, self.width, self.height)

    def add_fill(self, color: List[float]):
        self.fill_color = color
        return self

    def render(self, surface):
        context: cairo.Context = surface.context

        rects = []
        for row in range(self.rows):
            for column in range(self.columns):
                pos = [(row * self.box["box_width"]) + self.position[0], (column * self.box["box_height"]) + self.position[1]]
                rect = Rect({
                    "position": pos,
                    "width": self.box["box_width"],
                    "height": self.box["box_height"],
                    "color": self.fill_color
                    }).add_outline({
                        "color": self.outline_color,
                        "width": self.outline_width
                        })
                rects.append(rect)
        surface.add(*rects)
