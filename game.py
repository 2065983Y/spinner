from ImageFile import _tilesort
from retrogamelib import button, font, display, gameobject
from retrogamelib.util import *
from retrogamelib.constants import *
from blockEngine import *
from objects import Player, DropBox, Gate, Solid
from retrogamelib import clock
from levels import LEVELS
from pygame import draw


class Game(object):

    def __init__(self):
        self.objects = gameobject.Group()
        self.coins = gameobject.Group()
        self.dropBs = gameobject.Group()
        self.solids = gameobject.Group()
        self.font = font.Font(GAMEBOY_FONT, (50, 50, 50))
        self.gates = gameobject.Group()
        self.background = load_image("data/bg.png")
        self.levelCompleted = False
        #Player.groups = [self.objects]

        self.level = 0
        Player.groups = [self.objects]
        Solid.groups = [self.objects, self.solids]
        Gate.groups = [self.objects, self.gates]
        DropBox.groups = [self.objects, self.dropBs]
        Coin.groups = [self.objects, self.coins]


        self.engine = BlockEngine()
        self.camera = pygame.Rect(0, 0, GBRES[0], GBRES[1])
        self.matrix = 0

    def startLevel(self, level):
        self.show_win_screen = False
        self.player = Player()
        if self.lives > 0:
            for obj in self.objects:
                obj.kill()
            self.player = Player()
            self.matrix = self.engine.parseLevel(level)
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
        clock.tick()
        for object in self.objects:
            if (object.rect.right >= self.camera.left and \
                object.rect.left <= self.camera.right) or \
                object.always_update == True:
                object.update(self.engine.tiles)
                object.always_update = True

        self.camera.centerx = self.player.rect.centerx
        if self.camera.left < 0:
            self.camera.left = 0
        if self.camera.right > len(self.engine.tiles[0])*16:
            self.camera.right = len(self.engine.tiles[0])*16

        # Make sure we don't move off the far left of the level
        if self.player.rect.left < 0:
            self.player.rect.left = 0

        if self.player.rect.bottom > 144:
            self.player.rect.bottom = 144

        # Get rich quick!

        if button.is_pressed(B_BUTTON):
            #print len(self.objects)
            #print self.player in self.objects
            self.player.falling = True
            #print self.player.rect
            #print 'right= ', self.player.rect.right, 'left= ', self.player.rect.left ,'top= ', self.player.rect.top, 'bottom= ', \
            #    self.player.rect.bottom
            (x, y) = (self.player.rect.left, self.player.rect.top)
            (newX, newY) = self.engine.rotateLeftTile((x, y), 144)
            self.player.rect.left = newX
            self.player.rect.top = newY
            for obj in self.objects:
                if not obj == self.player:
                    obj.kill()
            self.matrix = self.engine.rotateLeft()
            self.engine.parseMatrix(self.matrix)

        if button.is_pressed(A_BUTTON):
            self.player.falling = True
            (x, y) = (self.player.rect.left, self.player.rect.top)
            (newX, newY) = self.engine.rotateLeftTile((x, y), 144)
            self.player.rect.left = newX
            self.player.rect.top = newY
            for obj in self.objects:
                if not obj == self.player:
                    obj.kill()
            self.matrix = self.engine.rotateRight()
            self.engine.parseMatrix(self.matrix)

        for c in self.coins:
            if self.player.rect.colliderect(c.rect):
                c.kill()
                c.looted = True
                #print self.engine.tiles[c.rect.centerx // 16][(c.rect.centery // 16) - 1]
                #self.engine.tiles[c.rect.centerx // 16][(c.rect.centery // 16) - 1] = '.'
                self.score += 25
                #Poof(c.rect.center)
                play_sound("data/coin.ogg")

        for s in self.solids:
            if self.player.rect.colliderect(s.rect):
                cX = s.rect.centerx
                cY = s.rect.centery
                pX = self.player.rect.centerx
                pY = self.player.rect.centery
                if (pX-cX) == 0:
                    self.player.rect.bottom = s.rect.top
                else:
                    slope = (pY-cY)/(pX-cX)
                    if slope == 0:
                        if pX>cX:
                            self.player.rect.left = s.rect.right
                        else:
                            self.player.rect.right = s.rect.left
                    elif slope > 0 and slope <= 16.0/11:
                        #slu4ai I
                        self.player.rect.left = s.rect.right
                    elif slope < 0 and slope >= -16.0/11:
                        #slu4ai III
                        self.player.rect.right = s.rect.left
                    else:
                        #slu4ai II
                        self.player.rect.bottom = s.rect.top

        for s in self.dropBs:
            if self.player.rect.colliderect(s.rect):
                cX = s.rect.centerx
                cY = s.rect.centery
                pX = self.player.rect.centerx
                pY = self.player.rect.centery
                if (pX-cX) == 0:
                    self.player.rect.bottom = s.rect.top
                else:
                    slope = (pY-cY)/(pX-cX)
                    if slope == 0:
                        if pX>cX:
                            self.player.rect.left = s.rect.right
                        else:
                            self.player.rect.right = s.rect.left
                    elif slope > 0 and slope <= 16.0/11:
                        #slu4ai I
                        self.player.rect.left = s.rect.right
                    elif slope < 0 and slope >= -16.0/11:
                        #slu4ai III
                        self.player.rect.right = s.rect.left
                    else:
                        #slu4ai II
                        self.player.rect.bottom = s.rect.top

        for db in self.dropBs:
            print "tile", self.matrix[db.x][db.y], db.x, db.y
            if(db.y + 1 < len(self.matrix)):
                if self.matrix[db.x][db.y + 1] == '.' or self.matrix[db.x][db.y + 1] == 'C':
                    temp = self.matrix[db.x][db.y + 1]
                    self.matrix[db.x][db.y+1] = 'D'
                    self.matrix[db.x][db.y] = temp
                    db.y = db.y + 1


        for g in self.gates:
            if self.player.rect.colliderect(g.rect):
                self.levelCompleted = True
                '''
                if self.player.falling:
                    self.player.rect.bottom = s.rect.top
                    #x = self.player.rect.centerx // 16
                    #y = self.player.rect.centery // 16
                    #self.player.rect.centerx = x
                    #self.player.rect.centery = y
                    #print self.matrix[y][x]
                    #self.player.falling = False
                    self.player.facing = 0


                #print self.player.facing
                if self.player.facing == 1:
                    if self.player.rect.bottom - 1 < s.rect.top:
                        print 'collide'
                        self.player.rect.right = s.rect.left
                elif self.player.facing == -1:
                    if self.player.rect.bottom - 1 < s.rect.top:
                        print 'collide'
                        self.player.rect.left = s.rect.right
'''
                #print self.player.rect.right, s.rect.left
                #print "collide"


    def draw(self):
        clock.tick()
        screen = display.get_surface()

        screen.fill(GB_SCREEN_COLOR)
        screen.blit(self.background, ((-self.camera.x/2) % 160, 0))
        screen.blit(self.background, (((-self.camera.x/2) - 160) % -160, 0))
        screen.blit(self.background, (((-self.camera.x/2) + 160) % 160, 0))

        # screen.blit(self.image, (self.rect.x - camera.x + self.offsetx,
        #     self.rect.y - camera.y + self.offsety))

        for object in self.objects:
            object.draw(screen, self.camera)

        ren = self.font.render("score    level      x%d" % self.lives)
        screen.blit(ren, (4, 4))
        ren = self.font.render("%06d    %d-1" % (self.score, self.level-1))
        screen.blit(ren, (4, 14))
        #screen.blit(self.lifeicon, (160-30, 2))

        if self.levelCompleted:
            self.levelCompleted = False
            self.level += 1
            print "lvl", self.level
            self.startLevel(LEVELS[self.level])
       # if not self.player.alive() and not self.dead:
       #     self.start_level(LEVELS[self.level-2])

        display.update()

        # clock.tick()
        # for object in self.objects:
        #     if (object.rect.right >= self.camera.left and \
        #         object.rect.left <= self.camera.right) or \
        #         object.always_update == True:
        #         object.update(self.engine.tiles)
        #         object.always_update = True