import sys

sys.path.append("../")

from mathogen.mathogen import Surface, Text, Font, TextOutline, Tex, TexFont

class Svg(Surface):
    def __init__(self):
        super().__init__(200, 200, "test.svg")

        text = Tex([0.1, 0.1], "This is $y = mc^2$", font=TexFont(size=0.1))

        text2 = Text([0.5, 0.5], "This is a test")
        self.add(text, text2)

Svg()
