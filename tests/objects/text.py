import sys
sys.path.append("..")

from mathogen.mathogen import Surface, Text, Tex

'''
Test for the creating, and rendering of text and LaTeX
'''
class TextTest(Surface):
    def construct(self):
        self.init(200, 200, "test.svg")

        '''
        Makes a LaTeX object
        This should render the Mass–energy equivalence equation

        This also rotates it 10 radians
        '''
        tex_text = Tex({"position": [0.1, 0.1], "text": "$e = mc^2$", "font":{"size": 0.1}}).rotate(10)
        # tex_text = Tex({"position": [0.1, 0.1], "text": "$e = mc^2$"}).rotate(10)

        '''
        This makes a Text object
        This should render the words "This is a text"

        this also rotates it 10 radians
        '''
        text = Text({"position": [0.5, 0.5], "text": "This is a test"}).rotate(10)
        '''
        This adds a blue outline to the text
        '''
        text.add_outline()

        '''
        Renders both
        '''
        self.add(tex_text, text)
