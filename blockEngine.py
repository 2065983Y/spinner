import Block


class BlockEngine(object):
    def __init__(self):
        self.tiles = None

    def parseLevel(self, level):
        tiles = []
        for li in level:
            temp = []
            for x in li:
                temp += [x]
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

        for t in temp:
            print t

        for y in xrange(0, len(self.tiles)):
            for x in xrange(0, len(self.tiles[0])):
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

    def rotateLeft(self):
        self.rotateRight()
        self.rotateRight()
        return self.rotateRight()

    def printTiles(self):
        for x in self.tiles:
            print x
