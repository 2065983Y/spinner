from retrogamelib.util import load_image
from retrogamelib import gameobject
import pygame


class Collidable(gameobject.Object):
    def __init__(self):
        gameobject.Object.__init__(self)
        self.offsetx = 0
        self.offsety = 0
        self.always_update = False

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
                if isinstance(tile, Platform):
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
                if tile.slant == 0:
                    self.rect_respond(dx, dy, tile)
                else:
                    self.slant_respond(dx, dy, tile)

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

    def slant_respond(self, dx, dy, tile):
        top = None
        if tile.slant < 0:
            if self.rect.left >= tile.rect.left:
                x = self.rect.left - tile.rect.left
                top = tile.rect.top+x-1
        if tile.slant > 0:
            if self.rect.right <= tile.rect.right:
                x = tile.rect.right - self.rect.right
                top = tile.rect.top+x-1
        if top:
            if self.rect.bottom > top:
                self.rect.bottom = top
                self.on_collision(0, dy)


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


class Player(Collidable):
    def __init__(self):
        #Collidable.__init__(self)

        self.right_images = [
            load_image("data/bubbman-1.png"),
            load_image("data/bubbman-2.png"),
        ]
        self.left_images = []
        for img in self.right_images:
            self.left_images.append(pygame.transform.flip(img, 1, 0))

        self.images = self.right_images
        self.image = self.images[0]
        self.rect = pygame.Rect(8, 16, 6, 16)

        self.facing = 1
        self.jump_speed = 0
        self.frame = 0
        self.jumping = True
        self.offsetx = -5
        self.z = 0


class Solid(Collidable):
    pass


class DropBox(Collidable):
    pass


class Gate(Collidable):
    pass