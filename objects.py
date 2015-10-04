from retrogamelib.util import load_image
from retrogamelib import gameobject
import pygame
from retrogamelib import button
from retrogamelib.constants import *


class Collidable(gameobject.Object):
    def __init__(self):
        gameobject.Object.__init__(self, self.groups)
        self.offsetx = 0
        self.offsety = 0
        self.always_update = False

    def dispose(self):
        print self.groups

    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.x + self.offsetx,
            self.rect.y - camera.y + self.offsety))

    def on_collision(self, dx, dy):
        pass

    def get_surrounding(self, pos):
        center = (pos[0], pos[1])
        topleft     = (pos[0]-1, pos[1]-1)
        midtop      = (pos[0],   pos[1]-1)
        topright    = (pos[0]+1, pos[1]-1)
        midleft     = (pos[0]-1, pos[1])
        midright    = (pos[0]+1, pos[1])
        bottomleft  = (pos[0]-1, pos[1]+1)
        midbottom   = (pos[0],   pos[1]+1)
        bottomright = (pos[0]+1, pos[1]+1)
        return (topleft, midtop, topright, midleft, midright,
            bottomleft, midbottom, bottomright, center)

    def move(self, dx, dy, tiles):
        sides = [0, 0, 0, 0]
        tile_pos = (self.rect.centerx//16, self.rect.centery//16)

        coltiles = []
        for pos in self.get_surrounding(tile_pos):
            if pos[0] > -1 and pos[0] < len(tiles[0]) and \
                pos[1] > -1 and pos[1] < len(tiles):
                tile = tiles[pos[1]][pos[0]]
                if isinstance(tile, Solid):
                    coltiles.append(tile)

        if dx != 0:
            self.__move(dx, 0, coltiles)
        if dy != 0:
            self.__move(0, dy, coltiles)

    def __move(self, dx, dy, tiles):
        self.rect.x += dx
        self.rect.y += dy
        collided = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.rect_respond(dx, dy, tile)

    def rect_respond(self, dx, dy, tile):
        if dx > 0:
            self.rect.right = tile.rect.left
        elif dx < 0:
            self.rect.left = tile.rect.right
        if dy > 0:
            self.rect.bottom = tile.rect.top
        elif dy < 0:
            self.rect.top = tile.rect.bottom
        self.on_collision(dx, dy)


class Platform(Collidable):

    def __init__(self, pos, imagepos, slant=0):
        Collidable.__init__(self)
        self.sheet = load_image("data/platform.png")
        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.image.blit(self.sheet, (-imagepos[0]*16,
            -imagepos[1]*16, 16, 16))
        self.rect = self.image.get_rect(topleft = pos)
        self.slant = slant  #1 for up slope right, -1 for down slope right
        self.z = -3

    def update(self, tiles):
        gameobject.Object.update(self)


class Coin(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self)
        self.images = [
            load_image("data/coin-1.png"), load_image("data/coin-2.png"),
            load_image("data/coin-3.png"), load_image("data/coin-4.png"),
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.always_update = True
        self.z = -2
        self.looted = False

    def update(self, tiles):
        self.frame += 1
        self.image = self.images[self.frame/4 % 4]


class Player(Collidable):
    def __init__(self):
        Collidable.__init__(self)
        self.right_images = [
            load_image("data/bubbman-1.png"),
            load_image("data/bubbman-2.png"),
        ]
        self.left_images = []
        for img in self.right_images:
            self.left_images.append(pygame.transform.flip(img, 1, 0))

        self.images = self.right_images
        self.image = self.images[0]
        self.rect = pygame.Rect(0, 144 - 16, 6, 16)

        self.facing = 1
        self.falling = False
        self.jump_speed = 0
        self.frame = 0
        self.jumping = True
        self.offsetx = -5
        self.z = 0

    def on_collision(self, dx, dy):
        print 'collided'

    def update(self, tiles):
        self.frame += 1
        imgframe = 0

        moving = False
        if button.is_held(LEFT):
            self.facing = -1
            moving = True
            self.move(-2, 0, tiles)
        if button.is_held(RIGHT):
            self.facing = 1
            moving = True
            self.move(2, 0, tiles)
        if button.is_held(B_BUTTON):
            pass
        if button.is_pressed(A_BUTTON):
            if not self.jumping:
                play_sound("data/jump.ogg")
                self.jump_speed = -5
                self.jumping = True

        if self.facing < 0:
            self.images = self.left_images
        else:
            self.images = self.right_images

        if moving:
            imgframe = self.frame/3 % 2
        if self.jumping:
            imgframe = 1

        self.image = self.images[imgframe]

        if button.is_held(A_BUTTON):
            self.jump_speed += 0.4
        else:
            self.jump_speed += 0.8
        if self.jump_speed > 5:
            self.jump_speed = 5

        self.move(0, self.jump_speed, tiles)
        if self.jump_speed > 3:
            self.jumping = True


class Solid(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self)
        self.image = load_image('data/solid.png')
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def update(self, tiles):
        gameobject.Object.update(self)


class DropBox(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self)
        self.image = load_image('data/dropBox.png')
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def update(self, tiles):
        gameobject.Object.update(self)


class Gate(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self)
        self.image = load_image('data/portal.png')
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def update(self, tiles):
        gameobject.Object.update(self)