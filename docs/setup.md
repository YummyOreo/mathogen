# Examples
> There is no current way to install mathogen. This will be for the folder `/tests`
```py
import sys
sys.path.append("../")

from mathogen.mathogen import Surface, Text

class SVG(Surface):
	def __init__(self):
		super().__init__(200, 200, "test.svg")

		text_world = Text([0.5, 0.5], "Hello Wold")
		text_from = Text([0.5, 0.7], "From Mathogen")

		self.add(text_world, text_from)
```
This will render "Hello World" in the middle of the SVG, and "From Mathogen" below it.

