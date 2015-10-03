from ImageFile import _tilesort
from retrogamelib import button, font, display
from retrogamelib.util import *
from retrogamelib.constants import *
from blockEngine import *
from objects import Player
from retrogamelib import clock
from pygame import draw


class Game(object):

    def __init__(self):
        self.font = font.Font(GAMEBOY_FONT, (50, 50, 50))
        self.background = load_image("data/bg.png")
        #Player.groups = [self.objects]
        self.engine = BlockEngine()
        self.camera = pygame.Rect(0, 0, GBRES[0], GBRES[1])

    def startLevel(self, level):
        self.show_win_screen = False
        self.player = Player()
        if self.lives > 0:
           # for obj in self.objects:
           #     obj.kill()
            #self.player = Player()
            self.engine.parseLevel(level)
            self.camera.centerx = self.player.rect.centerx
        else:
            self.won = False
            self.playing = False
            self.lose()
        self.tiles = self.engine.parseLevel(level)

    def loop(self):
        self.playing = True
        while self.playing:
           self.handle_input()
           self.update()
           self.draw()

    def handle_input(self):
        button.handle_input()
        if button.is_pressed(START):
            self.pause()
        if button.is_pressed(A_BUTTON) and button.is_held(SELECT):
            self.playing = False

    def update(self):
        pass

    def draw(self):
        clock.tick()
        screen = display.get_surface()

        screen.fill(GB_SCREEN_COLOR)
        screen.blit(self.background, ((-self.camera.x/2) % 160, 0))
        screen.blit(self.background, (((-self.camera.x/2) - 160) % -160, 0))
        screen.blit(self.background, (((-self.camera.x/2) + 160) % 160, 0))

        screen.blit(self.image, (self.rect.x - camera.x + self.offsetx,
            self.rect.y - camera.y + self.offsety))

        # clock.tick()
        # for object in self.objects:
        #     if (object.rect.right >= self.camera.left and \
        #         object.rect.left <= self.camera.right) or \
        #         object.always_update == True:
        #         object.update(self.engine.tiles)
        #         object.always_update = True