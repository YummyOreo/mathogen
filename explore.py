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

def curve1(context: cairo.Context, x: List[float], y: List[float], color: List[float], invert: bool, multi_x: float, multi_y: float):
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

def curve2(context: cairo.Context, pos_start: List[float]):
    context.set_line_width(0.01)

    x, y = pos_start
    x1, y1 = 0.4, 0.9
    x2, y2 = 0.6, 0.1
    x3, y3 = 0.9, 0.5

    context.move_to(x, y)
    context.curve_to(x1, y1, x2, y2, x3, y3)

    context.stroke()

    circle(context, x, y, .05, .05, [0, 0, 0, 1], 2)

    circle(context, x1, y1, .05, .05, [0, 0, 0, 1], 2)

    circle(context, x2, y2, .05, .05, [0, 0, 0, 1], 2)

    circle(context, x3, y3, .05, .05, [0, 0, 0, 1], 2)

    # context.set_source_rgba(1, 0.2, 0.2, 0.6)
    # context.set_line_width(0.03)
    # context.move_to(x, y)
    # context.line_to(x1, y1)
    # context.move_to(x2, y2)
    # context.line_to(x3, y3)
    # context.stroke()

def arc1(context: cairo.Context, x: float, y: float):
    context.set_line_width(0.01)

    # The larger the radius, the larger the arch will be
    radius = 0.1

    angle1 = 45.0 * (math.pi / 180.0)  # angles are specified
    angle2 = 180.0 * (math.pi / 180.0)  # in radians

    context.arc(x, y, radius, angle1, angle2,)
    context.stroke()


    # draws lines based on the arc/angle
    context.set_source_rgba(1, 0.2, 0.2, 0.6)
    context.set_line_width(0.01)

    # defindes te arch for the line to start and end at
    context.arc(x, y, radius + 0.2, angle1, angle1)
    context.line_to(x, y)


    context.stroke()

    context.arc(x, y, radius + 0.2, angle2, angle2)
    context.line_to(x, y)
    context.stroke()

def arcTo(context: cairo.Context, x, y, slope_1, slope_2):
    # Get slopes
    # Get the angle between the 2 lines
    # Get the starting angle and ending angle needed for the arc
    # Render the arc
    arc1(context, x, y)

def line(context: cairo.Context, x: float, y: float, end_x: float, end_y: float):
    set_rgba(context, [0, 0, 0, 1])
    context.set_line_width(0.01)
    context.move_to(x, y)
    context.line_to(end_x, end_y)
    context.stroke()

    # The slope of the line
    return (end_y - y) / (end_x - x)
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
    # curve1(context, [0.1, 0.1], [0.1, 0.7],[82, 182, 209, 1], False, 0.2, 0)
    """
    Trying to improve arch1
    """
    # curve2(context, [0.1, 0.5])

    arc1(context, 0.5, 0.1)

    """
    Gets a point on a line
    You should convert this into a function
    then make a func to join 2 points
    """
    slope = line(context, 0.1, 0.2, 0.2, 0.3)
    point_x = 0.2
    point_y = (slope * point_x) + 0.1
    circle(context, point_x, point_y, 0.03, 0.03, [82, 182, 209, 1], 2)
    arcTo(context, 0.1, 0.2, point_x, point_x)
