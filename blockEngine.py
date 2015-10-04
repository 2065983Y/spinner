import Block
from objects import Solid, Gate, DropBox, Coin


class BlockEngine(object):
    def __init__(self):
        self.tiles = None

    def parseLevel(self, level):
        tiles = []
        y = 0
        for li in level:
            x = 0
            temp = []
            for el in li:
                temp += [el]
                if el == 'S':
                    Solid((x*16, y*16))
                elif el == 'D':
                    DropBox((x*16, y*16))
                elif el == 'G':
                    Gate((x*16, y*16))
                elif el == 'C':
                    Coin((x*16, y*16))
                x += 1
            y += 1
            tiles += [temp]
        self.tiles = tiles
        #print 'rotating....'
        #self.printTiles()
        #self.rotateLeft()
        return self.tiles

    #m = 9
    #n = 20
    def rotateRight(self):
        temp = [[0 for x in xrange(len(self.tiles))] for y in xrange(len(self.tiles[0]))]

        for y in xrange(len(self.tiles)):
            for x in xrange(len(self.tiles[0])):
                #print 'm = ', len(self.tiles), ' n = ', len(self.tiles[x])
                #print 'tile', self.tiles[len(self.tiles) - 1 - x][y], x, y
                #print self.tiles[0]
                #print self.tiles[0][10]
                #print y, -x + len(self.tiles[0]) - 1
                temp[x][y] = self.tiles[y][-x + len(self.tiles[0]) - 1]
            #print 'pass'
        self.tiles = temp
        #self.printTiles()
        return self.tiles

    # def rotateRight(self, matrix):
    #     temp = [[0 for x in xrange(len(matrix))] for y in xrange(len(matrix[0]))]
    #
    #     for y in xrange(len(matrix)):
    #         for x in xrange(len(matrix)):
    #             #print 'm = ', len(self.tiles), ' n = ', len(self.tiles[x])
    #             #print 'tile', self.tiles[len(self.tiles) - 1 - x][y], x, y
    #             #print self.tiles[0]
    #             #print self.tiles[0][10]
    #             #print y, -x + len(self.tiles[0]) - 1
    #             temp[x][y] = matrix[y][-x + len(matrix[0]) - 1]
    #         #print 'pass'
    #     matrix = temp
    #     self.tiles = temp
    #     #self.printTiles()
    #     return matrix

    def rotateLeft(self):
        self.rotateRight()
        self.rotateRight()
        return self.rotateRight()
        # temp = [[0 for x in xrange(len(self.tiles))] for y in xrange(len(self.tiles[0]))]
        #
        # for y in xrange(len(self.tiles)):
        #     for x in xrange(len(self.tiles[0])):
        #         temp[y][-x+len(temp)-1] = self.tiles[x][y]
        # self.tiles = temp
        # return self.tiles

    # def rotateLeft(self, matrix):
    #     self.rotateRight(matrix)
    #     self.rotateRight(matrix)
    #     return self.rotateRight(matrix)

    def printTiles(self):
        for x in self.tiles:
            print x

    def rotateLeftTile(self, (x, y), maxY):
        return (-y-1+maxY,x)
        #temp[x][y] = self.tiles[y][-x + len(self.tiles[0]) - 1]

    def rotateRightTile(self, (x, y), maxX):
        return (y, maxX - 1 - x)
        #temp[x][y] = self.tiles[y][-x + len(self.tiles[0]) - 1]

    def parseMatrix(self, matrix):
        y = 0
        for li in matrix:
            x = 0
            temp = []
            for el in li:
                temp += [el]
                if el == 'S':
                    Solid((x*16, y*16))
                elif el == 'D':
                    DropBox((x*16, y*16))
                elif el == 'G':
                    Gate((x*16, y*16))
                elif el == 'C':
                    Coin((x*16, y*16))
                x += 1
            y += 1
