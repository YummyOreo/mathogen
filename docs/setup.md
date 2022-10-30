# Examples
> There is no current way to install mathogen. This will be for the folder `/tests`
```py
import sys
sys.path.append("../")

from mathogen.mathogen import Surface, Text

class SVG(Surface):
    def __init__(self):
        '''
        Calles the __init__ class in Surface

        The first 2 numbers are the width and height
        The last string is the output file
        '''
        super().__init__(200, 200, "test.svg")

        '''
        This defiends 2 text objects

        The first one defineds "Hello World" @ half the width, and half the height (or center)

        The second one defineds "Hello World" @ half the width, but 0.7 of the height
        '''
        text_world = Text([0.5, 0.5], "Hello Wold")
        text_from = Text([0.5, 0.7], "From Mathogen")

        '''
        Adds and renders the given objcets
        '''
        self.add(text_world, text_from)

SVG()
```
This will render "Hello World" in the middle of the SVG, and "From Mathogen" below it.

![](https://github.com/YummyOreo/mathogen/blob/main/docs/images/test.svg)
