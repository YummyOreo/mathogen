from typing import List, Optional, Any
import cairo

from .object import Object
from ..utils.color import BLACK, BLUE
from ..utils.temp import create_temp
from ..constants import TEMP_FILE_FOLDER

import math
from matplotlib import mathtext, font_manager
import matplotlib as mpl
mpl.rcParams["savefig.transparent"] = True

slant = {
        "normal": cairo.FONT_SLANT_NORMAL,
        "italic": cairo.FONT_SLANT_ITALIC,
        }
weight = {
        "normal": cairo.FONT_WEIGHT_NORMAL,
        "bold": cairo.FONT_WEIGHT_BOLD
        }

class Text(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position": List[float],
                "text": str,
                font: {} = {
                    "font_face": str = "sans",
                    "slant": str = "normal",
                    "weight": str = "bold",
                    "size": int = 0.05
                    }
                "color": List[float] = BLACK
                }
        '''
        options: Any = {"color": BLACK}
        font = { "font_face": "sans", "slant": "normal", "weight": "bold", "size": 0.05}
        options.update(user_options)
        if not ("font" in options):
            options["font"] = {}
        options["font"].update(font)
        options.update(user_options)

        self.position = options["position"]
        self.text = options["text"]

        self.font = options["font"]
        self.font["slant"] = slant[self.font["slant"]]
        self.font["weight"] = weight[self.font["weight"]]

        self.color = options["color"]

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color)

    def add_outline(self, outline_options = {}):
        '''
        user_options = {
                "width": float = 0.002,
                "color": List[float] = BLUE
                }
        '''
        outline = {"width": 0.002, "color": BLUE}
        outline.update(outline_options)
        self.outline = outline
        return self

    def rotate(self, degrees: float):
        self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        '''
        Renders the text and the outline (if given).
        '''
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        if self.radians:
            context.rotate(self.radians)

        context.select_font_face(self.font["font_face"], self.font["slant"], self.font["weight"])
        context.set_font_size(self.font["size"])

        surface.move_to(self.position)

        context.text_path(self.text)

        context.fill_preserve()

        if self.outline:
            self.render_outline(surface)

        context.restore()

    def render_outline(self, surface):
        if not self.outline: return
        context: cairo.Context = surface.context
        surface.set_color(self.outline["color"])

        context.set_line_width(self.outline["width"])

        context.stroke()

class Tex(Object):
    def __init__(self, user_options):
        '''
        user_options = {
                "position": List[float],
                "text": str,
                font: {} = {
                    "font_face": str = "serif",
                    "size": int = 0.5
                    }
                "color": List[float] = BLUE
                }
        '''
        options: Any = {"color": BLACK}
        font = { "font_face": "serif", "size": 0.05}
        options.update(user_options)
        if not ("font" in options):
            options["font"] = {}
        options["font"].update(font)

        self.position = options["position"]
        self.text = options["text"]

        self.font = options["font"]
        self.font["width"] = math.sqrt(self.font["size"]) / 2
        self.font["height"] = self.font["width"]

        self.color = options["color"]

        self.outline = None
        self.radians = None

        super().__init__(self.position, self.color)


    def rotate(self, degrees: float):
        self.radians = degrees * (math.pi / 180)
        return self

    def render(self, surface):
        '''
        Renders the LaTeX
        '''
        create_temp()

        textFont = font_manager.FontProperties(size=30, family=self.font["font_face"], math_fontfamily="cm")
        mathtext.math_to_image(self.text, f"{TEMP_FILE_FOLDER}tex.temp", prop=textFont, dpi=300, format="png", color=self.color)

        image_surface = cairo.ImageSurface.create_from_png(f"{TEMP_FILE_FOLDER}tex.temp")
        img_height = image_surface.get_height()
        img_width = image_surface.get_width()

        width_ratio = float(self.font["width"]) / float(img_width)
        height_ratio = float(self.font["height"]) / float(img_height)
        scale_xy = min(height_ratio, width_ratio)

        # scale image and add it
        context: cairo.Context = surface.context

        context.save()
        surface.set_color(self.color)

        if self.radians:
            context.rotate(self.radians)

        context.translate(*self.position)
        context.scale(scale_xy, scale_xy)
        context.set_source_surface(image_surface)
        context.paint()
        context.restore()
