from square import Square
from coordinates import Coordinates

class Map():
    
    def __init__(self,squareSize,level):
        self.squareSize = squareSize
        self.width = 600
        self.height = 600
        self.level = level
        self.map = self.loadMap()
    
    def loadMap(self):
        filename = self.level + ".txt"
        file = open(filename,"r")
        map = []
        mapline = []
        idcount = 1
        xcount = 0
        ycount = 0
        for line in file:
            line = line.rstrip("\n")
            for c in line:
                if c == "X":
                    newsquare = Square(self.squareSize,True,xcount,ycount)
                else:
                    newsquare = Square(self.squareSize,False,xcount,ycount)
                if c == "1":
                    self.start = Coordinates(xcount,ycount)
                elif c == "2":
                    self.end = Coordinates(xcount,ycount)
                idcount += 1
                xcount +=1
                mapline.append(newsquare)
            xcount=0
            map.append(mapline)
            mapline = []
            ycount += 1
        file.close()
        return map       


