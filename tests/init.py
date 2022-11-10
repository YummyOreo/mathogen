from objects.text import TextTest
from objects.rect import RectTest
from objects.line import LineTests

def test_text():
    TextTest()

def test_rect():
    RectTest()

def test_lines():
    LineTests()

if __name__ == '__main__':
    # test_text()
    # test_rect()
    test_lines()
