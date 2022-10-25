import math
from typing import List

import cairo

from matplotlib import mathtext, font_manager
import matplotlib as mpl
mpl.rcParams["savefig.transparent"] = True

def set_rgba(context: cairo.Context, rgb):
    context.set_source_rgba(rgb[0]/255, rgb[1]/255, rgb[2]/255, rgb[3])

# add rotate, see circle
def text(context, text: str, pos: List[float], color: List[float]):
    context.save()
    # sets text stuff
    context.select_font_face("sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(0.15)

    # were it will be
    context.move_to(pos[0], pos[1])
    # the color
    set_rgba(context, [color[0], color[1], color[2], 0.5])
    # what it will be
    context.text_path(text)
    # fills it
    context.fill_preserve()

    # the outline color
    set_rgba(context, color)
    # width of the outline
    context.set_line_width(0.005)
    context.stroke()
    context.restore()

# add rotate, see circle
def rect(context: cairo.Context, x: float, y: float, width: float, height: float, color: List[float], outline_width: float):
    context.save()
    # xColor border
    set_rgba(context, color)

    # With the width of this
    # This effects it when you use context.stroke()
    context.set_line_width(outline_width)

    # Makes it and applies the stroke
    context.rectangle(x, y, width, height)
    context.stroke()

    # The inner part, black
    context.rectangle(x, y, width, height)
    # Sets the color to black
    set_rgba(context, [0, 0, 0, 1])
    # fills it in
    context.fill()
    context.restore()

def circle(context: cairo.Context, x: float, y: float, width: float, height: float, color: List[float], outline_width: float):

    # starts a "container"
    context.save()
    context.translate(x, y)

    # color for inner fill
    set_rgba(context, [color[0], color[1], color[2], 0.5])

    # rotate clockwise
    # degrees * (pi / 180)
    context.rotate(90 * (math.pi / 180))

    context.scale(width / 2.0, height / 2.0)
    context.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)

    # fills the shape
    context.fill_preserve()

    # resets it to after the save fun / closes the "container"
    # this is so the scale and rotate does not apply
    context.restore()

    # stroke
    # reset identity matrix so line_width is a constant
    # width in device-space, not user-space
    context.save()
    set_rgba(context, color)
    context.identity_matrix()
    # scales with the scale
    context.set_line_width(outline_width * ((width + height) * 10))

    context.stroke()
    context.restore()

def arch1(context: cairo.Context, x: List[float], y: List[float], color: List[float], invert: bool, multi_x: float, multi_y: float):
    context.set_line_width(0.01)
    set_rgba(context, color)

    context.move_to(x[0], y[0])

    if not invert:
        multi_x = 0 - multi_x
    else:
        multi_y = 0 - multi_y

    y_avg = (y[0] + y[1]) / 2
    x_avg = (x[0] + x[1]) / 2

    x_curve = x_avg + multi_x
    y_curve = y_avg + multi_y

    print(y_curve, x_curve)

    context.curve_to(x[0], y[0], x_curve, y_curve, x[1], y[1])
    context.stroke()
    circle(context, x[0], y[0], .05, .05, [0, 0, 0, 1], 2)
    circle(context, x[1], y[1], .05, .05, [0, 0, 0, 1], 2)
    circle(context, x_curve, y_curve, .05, .05, [0, 0, 0, 1], 2)

def mathTex(context: cairo.Context, x: float, y: float, width: float, height: float, text: str, color: List[float]):

    textFont = font_manager.FontProperties(size=30, family="serif", math_fontfamily="cm")
    mathtext.math_to_image(text, "mathTex.png", prop=textFont, dpi=300, format="png", color=(color[0]/255, color[1]/255, color[2]/255, color[3]))

    image_surface = cairo.ImageSurface.create_from_png("mathTex.png")
    img_height = image_surface.get_height()
    img_width = image_surface.get_width()

    width_ratio = float(width) / float(img_width)
    height_ratio = float(height) / float(img_height)
    scale_xy = min(height_ratio, width_ratio)

    # scale image and add it
    context.save()
    context.translate(x, y)
    context.scale(scale_xy, scale_xy)
    context.set_source_surface(image_surface)
    context.paint()
    context.restore()

    # returns this because it will be different than the one inputted as it is dependent on the image created by matplotlib
    return [width_ratio, height_ratio]

def arch2(context: cairo.Context, pos_start: List[float]):
    print(pos_start)
    context.save()
    context.restore()
    pass

"""
Add rotation to everything!
Everything is drawn on top of each other (if 2 things will take the same space, the last thing will be on top of the other)
"""
with cairo.SVGSurface("example.svg", 1000, 1000) as surface:
    context = cairo.Context(surface)
    # Can't change this
    # To change the scale, do context.set_font_size(x)
    # what everything will be * by (1 = scaled num). have inputs be / by this num
    # possibly upscale it by 100 so it is easy to work with (input / 100)
    context.scale(1000, 1000)

    # for bordered bg
    #rect(context, 0.01, 0.01, 1 - 0.02, 1 - 0.02, [135, 55, 55, 1], 0.01)
    # for non-bordered bg
    #rect(context, 0.0, 0.0, 1, 1, [135, 55, 55, 1], 0.01)

    circle(context, 0.2, 0.1, 0.03, 0.1, [82, 182, 209, 1], 2)

    text(context, "test1", [0.1, 0.4], [82, 182, 209, 1])
    text(context, "test 100", [0.1, 0.55], [82, 182, 209, 1])

    # write math in LaTeX
    # this uses matplotlib to render the LaTeX then cairo scales it to the correct scale
    mathTex(context, 0.1, 0.1, 0.5, 0.5, r"Math $e = mc^2 \hspace{2} \sqrt[3]{8}=8^{\frac{1}{3}}=2$", [82, 182, 209, 1])
    mathTex(context, 0.2, 0.2, 0.5, 0.5, r"Math $e = mc^2$", [82, 182, 209, 1])

    # a curve between 2 objects
    """
    for a curve: you can choose from a x offset and a y offset
    you can also choose from a inverted or not
    """
    arch1(context, [0.1, 0.1], [0.1, 0.7],[82, 182, 209, 1], False, 0.2, 0)
    """
    Trying to improve arch1
    """
    arch2(context, [0.1, 0.1])

