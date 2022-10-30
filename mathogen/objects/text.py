from typing import List, Optional
import cairo

from .object import Object
from ..utils.color import BLACK, BLUE

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

class Font:
    def __init__(self, font: str = "sans", font_slant: str = "normal", font_weight: str= "bold", font_size: float = 0.05):
        '''
        Defines the font for a Text object

            font (str): The font family of the text
                Default: "sans"
            font_slant (str): How slanted the font it
                Options:
                    "normal"
                    "italic"
                Default: "normal"
            font_weight (str): How weighted the font is
                Options:
                    "bold"
                    "normal"
                Default: "bold"
            font_size (float): How big the font is
                Default: 0.05
        '''
        self.font = font
        self.font_size = font_size
        self.font_slant = slant[font_slant]
        self.font_weight = weight[font_weight]

class TextOutline:
    def __init__(self, outline_width: float = 0.002, outline_color: List[float] = BLUE):
        '''
        Draws the outline for a Text object

            outline_width (float): The width of the outline
                Default: 0.002
            outline_color ([R: float, G: float, B: float, A: float]): The color of the outline
                Default: [0.235294118, 0.858823529, 0.82745098, 1] (BLUE)
        '''
        self.outline_width = outline_width
        self.outline_color = outline_color

    def render(self, surface):
        '''
        Renders the outline given a surface
        !! Important: !!
            You have to render the Text first, then call this
        '''
        context: cairo.Context = surface.context
        surface.set_color(self.outline_color)

        context.set_line_width(self.outline_width)

        context.stroke()

class Text(Object):
    def __init__(self, position: List[float], text: str, font: Optional[Font] = None, color: List[float] = BLACK):
        '''
        For drawing text to the screen. Not math text, see Tex

            position ([X: float, Y: float]): The position at which the text will be drawn

            text (str): The text that will be drawn to the screen

            font (Font): The font options that will be used when drawing the text to the screen
                Default: The default Font object arguments

            color ([R: float, G: float, B: float, A: float]): The color of the text
                Default: [0, 0, 0, 1] (BLACK)
        '''
        self.position = position
        self.text = text

        if not font:
            font = Font()
        self.font = font

        self.color = color

        self.outline = None

        super().__init__(position, color)

    def add_outline(self, outline: TextOutline):
        '''
        Adds a outline to the text. This should be done before rendering

            outline: The outline objcet to be used when rendering, see TextOutline
        '''
        self.outline = outline

    def render(self, surface):
        '''
        Renders the text and the outline (if given).
        '''
        context: cairo.Context = surface.context

        super().render(surface)

        context.select_font_face(self.font.font, self.font.font_slant, self.font.font_weight)
        context.set_font_size(self.font.font_size)

        surface.move_to(self.position)

        context.text_path(self.text)

        context.fill_preserve()

        if self.outline:
            self.outline.render(surface)

        context.restore()

class TexFont:
    def __init__(self, font: str = "serif", size: float = 0.5):
        '''
        Defines the font for a Tex object (Math Text)

            font (str): The font family of the text
                Default: "serif"
            size (float): How big the font is
                Default: 0.5
        '''
        self.font = font
        self.width = math.sqrt(size) / 2
        self.heigh = math.sqrt(size) / 2

class Tex(Object):
    def __init__(self, position: List[float], text: str, font: Optional[TexFont] = None, color: List[float] = BLUE):
        '''
        Renders LaTeX to the screen using MatPlotLib.

            position ([X: float, Y: float]): The position at which the text will be drawn

            text (str): the text to be darwn

            font (TexFont): The font options that will be used when drawing the text to the screen
                Default: The default TexFont object arguments

            color ([R: float, G: float, B: float, A: float]): The color of the text
                Default: [0.235294118, 0.858823529, 0.82745098, 1] (BLUE)
        '''
        self.position = position
        self.text = text

        if not font:
            font = TexFont()
        self.font = font

        self.color = color

        super().__init__(position, color)

    def render(self, surface):
        '''
        Renders the LaTeX
        '''
        textFont = font_manager.FontProperties(size=30, family=self.font.font, math_fontfamily="cm")
        mathtext.math_to_image(self.text, "mathTex.png", prop=textFont, dpi=300, format="png", color=self.color)

        image_surface = cairo.ImageSurface.create_from_png("mathTex.png")
        img_height = image_surface.get_height()
        img_width = image_surface.get_width()

        width_ratio = float(self.font.width) / float(img_width)
        height_ratio = float(self.font.heigh) / float(img_height)
        scale_xy = min(height_ratio, width_ratio)

        # scale image and add it
        context: cairo.Context = surface.context

        super().render(surface)

        context.translate(*self.position)
        context.scale(scale_xy, scale_xy)
        context.set_source_surface(image_surface)
        context.paint()
        context.restore()
