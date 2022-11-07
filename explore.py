import math
from typing import List

import cairo

from matplotlib import mathtext, font_manager
import matplotlib as mpl
mpl.rcParams["savefig.transparent"] = True

# import numpy as np

"""
Possibly use multiple threads to render
"""

# When impl this, check if the current rgba is the rgba that is being set, if it is, then don't do anything
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
    set_rgba(context, color)
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

# The x and y is the intersection point
def arc1(context: cairo.Context, x: float, y: float, angle_end: float, angle_start: float):
    context.set_line_width(0.01)
    set_rgba(context, [0, 0, 0, 1])

    # The larger the radius, the larger the arch will be
    radius = 0.1

    # angle1 = 0 * (math.pi / 180.0)  # angles are specified
    # angle2 = angle #* (math.pi / 180.0)  # in radians

    # Still need to fix angle3 and find out why
    # angle1 = 195 * (math.pi/ 180)
    angle1 = angle_start
    angle2 = (angle_end + angle1)

    # Change to arc_negitive to do the outside angle
    # The x and y is the intersection point
    context.arc(x, y, radius, angle1, angle2)
    context.stroke()

    return
    # draws lines based on the arc/angle
    context.set_source_rgba(1, 0.2, 0.2, 0.6)
    context.set_line_width(0.01)

    # defindes te arch for the line to start and end at
    context.arc(x, y, radius + 0.2, angle1, angle1)
    context.line_to(x, y)

    context.arc(x, y, radius + 0.2, 0, 0)
    context.line_to(x, y)

    context.arc(x, y, radius + 0.2, angle2, angle2)
    context.line_to(x, y)
    context.stroke()

def arcTo(context: cairo.Context, x, y, line_1: List[List[float]], line_2):
    # Get the angle between the 2 lines

    angle: float = ang(line_1, line_2)

    # Gets the line 0 (the line were the arc starts from + the starting angle, this goes clockwise)
    line_0 = [line_1[0], [0.8, line_1[0][-1]]]

    # Gets the angle going clockwise for each
    # If the closest one is anticlockwise then it will be negitive, and will be given as anticlockwise
    angle_1_clockwise = clockwise_ang(line_0, line_1)
    angle_2_clockwise = clockwise_ang(line_0, line_2)

    # both are anticlockwise
    if angle_1_clockwise < 0 and angle_2_clockwise < 0:
        # then the furthest one is the smallest one (because it is negitive, the smallest one will be the closest to 0 going clockwise)
        furthest_angle = angle_1_clockwise if angle_1_clockwise < angle_2_clockwise else angle_2_clockwise
    # if only one is clockwise
    elif (angle_1_clockwise < 0 and not angle_2_clockwise < 0) or (not angle_1_clockwise < 0 and angle_2_clockwise < 0):
        # convert them to their absolute value
        # then if angle 1 is bigger then angle 2
        if abs(angle_1_clockwise) > abs(angle_2_clockwise):
            # angle 1 is the furthest angle
            furthest_angle = angle_1_clockwise
        # if angle 2 is bigger than angle 1
        else:
            # anle 2 is the furthest angle
            furthest_angle = angle_2_clockwise
    # if line 1 is greater than line 2
    elif abs(angle_1_clockwise) > abs(angle_2_clockwise):
        # then the angle has to start at line 2 because line 1 is further from 0 going clockwise
        furthest_angle = angle_2_clockwise
    # if line 2 is greater
    else:
        # then the angle has to start at line 1 because line 2 is further from 0 going clockwise
        furthest_angle = angle_1_clockwise

    # if the angle is negitive, this means that it is closest, but we have it going anticlockwise, so we must convert it
    if furthest_angle < 0:
        furthest_angle += 360
    start_angle: float = furthest_angle

    # Render the arc
    arc1(context, x, y, abs(angle * (math.pi/180)), abs(start_angle * (math.pi/180)))


def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA: List[List[float]], lineB: List[List[float]]):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg

def clockwise_ang(lineA: List[List[float]], lineB: List[List[float]]):
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    dot_prod = dot(vA, vB)
    det = vA[0] * vB[1] - vA[1] * vB[0]
    return math.atan2(det, dot_prod) * (180/math.pi)

def line(context: cairo.Context, x: float, y: float, end_x: float, end_y: float, color: List[float]):
    set_rgba(context, color)
    context.set_line_width(0.005)
    context.move_to(x, y)
    context.line_to(end_x, end_y)
    context.stroke()

def curve_between(context: cairo.Context, pos_1: List[float], pos_2: List[float]):
    context.set_line_width(0.01)
    set_rgba(context, [0, 0, 0, 1])

    context.move_to(*pos_1)

    # Gets a point that is perpendicular to the middle of the line

    # Gets the slope that the perpendicular line would be
    perpendicular_slope = get_perpendicular_slope(pos_1, pos_2)

    # Gets the midpoint of the line
    mid = get_middle(pos_1, pos_2)

    # gets a point on that perpendicular line
    # perpendicular_point = [mid[0] + perpendicular_slope[0], mid[1] + perpendicular_slope[1]]
    # Inverted
    perpendicular_point = [mid[0] - perpendicular_slope[0], mid[1] - perpendicular_slope[1]]

    context.curve_to(*pos_1, *perpendicular_point, *pos_2)
    context.stroke()
    circle(context, perpendicular_point[0], perpendicular_point[1], 0.02, 0.02, [0, 0, 0, 1], 1)

def get_perpendicular_slope(pos_1: List[float], pos_2: List[float]):
    x_inc = (pos_2[0] - pos_1[0])
    y_inc = (pos_2[1] - pos_1[1])

    return [y_inc * -1, x_inc]

def get_middle(pos_1: List[float], pos_2: List[float]):
    return [(pos_1[0] + pos_2[0]) / 2, (pos_1[1] + pos_2[1]) / 2]

# Better rounded rectangle
# Replace it
def rect_curve(context: cairo.Context, pos: List[float], width: float, height: float, curve: float, fill_color: List[float], outline_color: List[float]):
    context.set_line_width(0.003)
    # a custom shape, that could be wrapped in a function
    x0 = pos[0]
    y0 = pos[1]
    rect_width =  width
    rect_height = height
    radius = curve  # and an approximate curvature radius

    x1 = x0 + rect_width
    y1 = y0 + rect_height

    if rect_width / 2 < radius:
        if rect_height / 2 < radius:
            context.move_to(x0, (y0 + y1) / 2)
            context.curve_to(x0, y0, x0, y0, (x0 + x1) / 2, y0)
            context.curve_to(x1, y0, x1, y0, x1, (y0 + y1) / 2)
            context.curve_to(x1, y1, x1, y1, (x1 + x0) / 2, y1)
            context.curve_to(x0, y1, x0, y1, x0, (y0 + y1) / 2)
        else:
            context.move_to(x0, y0 + radius)
            context.curve_to(x0, y0, x0, y0, (x0 + x1) / 2, y0)
            context.curve_to(x1, y0, x1, y0, x1, y0 + radius)
            context.line_to(x1, y1 - radius)
            context.curve_to(x1, y1, x1, y1, (x1 + x0) / 2, y1)
            context.curve_to(x0, y1, x0, y1, x0, y1 - radius)
    else:
        if rect_height / 2 < radius:
            context.move_to(x0, (y0 + y1) / 2)
            context.curve_to(x0, y0, x0, y0, x0 + radius, y0)
            context.line_to(x1 - radius, y0)
            context.curve_to(x1, y0, x1, y0, x1, (y0 + y1) / 2)
            context.curve_to(x1, y1, x1, y1, x1 - radius, y1)
            context.line_to(x0 + radius, y1)
            context.curve_to(x0, y1, x0, y1, x0, (y0 + y1) / 2)
        else:
            context.move_to(x0, y0 + radius)
            context.curve_to(x0, y0, x0, y0, x0 + radius, y0)
            context.line_to(x1 - radius, y0)
            context.curve_to(x1, y0, x1, y0, x1, y0 + radius)
            context.line_to(x1, y1 - radius)
            context.curve_to(x1, y1, x1, y1, x1 - radius, y1)
            context.line_to(x0 + radius, y1)
            context.curve_to(x0, y1, x0, y1, x0, y1 - radius)

    context.close_path()

    set_rgba(context, fill_color)
    context.fill_preserve()
    set_rgba(context, outline_color)
    context.stroke()

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
    # rect(context, 0.01, 0.01, 1 - 0.02, 1 - 0.02, [135, 55, 55, 1], 0.01)
    # for non-bordered bg
    # rect(context, 0.0, 0.0, 1, 1, [135, 55, 55, 1], 0.01)

    # circle(context, 0.2, 0.1, 0.03, 0.1, [82, 182, 209, 1], 2)

    # text(context, "test1", [0.1, 0.4], [82, 182, 209, 1])
    # text(context, "test 100", [0.1, 0.55], [82, 182, 209, 1])

    # write math in LaTeX
    # this uses matplotlib to render the LaTeX then cairo scales it to the correct scale

    # mathTex(context, 0.1, 0.1, 0.5, 0.5, r"Math $e = mc^2 \hspace{2} \sqrt[3]{8}=8^{\frac{1}{3}}=2$", [82, 182, 209, 1])
    # mathTex(context, 0.2, 0.2, 0.5, 0.5, r"Math $e = mc^2$", [82, 182, 209, 1])

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

    # arc1(context, 0.5, 0.1)

    """
    Gets a point on a line
    You should convert this into a function
    then make a func to join 2 points
    """

    # line_1 = [[0.5, 0.5], [0.7, 0.4]]
    # line_2 = [[0.5, 0.5], [0.4, 0.2]]
    # line(context, line_1[0][0], line_1[0][1], line_1[1][0], line_1[1][1], [82, 182, 209, 1])
    # line(context, line_2[0][0], line_2[0][1], line_2[1][0], line_2[1][1], [82, 182, 209, 1])

    # arcTo(context, line_1[0][0], line_1[0][1], line_1, line_2)

    # curve_between(context, [0.1, 0.1], [0.2, 0.2])

    rect_curve(context, [0.3, 0.6], 0.2, 0.2, 0.05, [0, 0, 0, 1], [244, 255, 0, 1])

