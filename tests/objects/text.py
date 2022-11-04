import sys

sys.path.append("../")

from mathogen.mathogen import Surface, Text, Font, TextOutline, Tex, TexFont

'''
Test for the creating, and rendering of text and LaTeX
'''
class TextTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        '''
        Makes a LaTeX object
        This should render the Mass–energy equivalence equation
        '''
        tex_text = Tex([0.1, 0.1], "$e = mc^2$", font=TexFont(size=0.1))

        '''
        This makes a Text object
        This should render the words "This is a text"
        '''
        text = Text([0.5, 0.5], "This is a test")
        '''
        This adds a blue outline to the text
        '''
        text.add_outline(TextOutline())

        '''
        Renders both
        '''
        self.add(tex_text, text)
