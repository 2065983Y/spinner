from retrogamelib import button
from retrogamelib import font
from retrogamelib.util import *
from retrogamelib.constants import *


class Game(object):
    def __init__(self):
        self.font = font.Font(GAMEBOY_FONT, (50, 50, 50))
        self.background = load_image("data/bg.png")