from types import List

RED = [255/255, 131/255, 96/255, 1]

DARK_RED = [192/255, 98/255, 72/255, 1]

YELLOW = [232/255, 226/255, 136/255, 1]

DARK_YELLOW = [244/255, 179/255, 116/255, 1]

GREEN = [125/255, 206/255, 130/255, 1]

DARK_GREEN = [63/255, 75/255, 59/255, 1]

BLUE = [60/255, 219/255, 211/255, 1]

DARK_BLUE = [46/255, 94/255, 170/255, 1]

PURPLE = [96/255, 73/255, 90/255, 1]

DARK_PURPLE = [36/255, 16/255, 35/255, 1]

BLACK = [4/255, 4/255, 3/255, 1]

GRAY = [48/255, 48/255, 47/255, 1]

WHITE = [226/255, 228/255, 246/255, 1]


def create_color(red, green, blue, alfa=1) -> List[float]:
    '''
    Converts conventional RGBA to RGBA that is usable for this Lib
    '''
    return [red/255, green/255, blue/255, alfa]
