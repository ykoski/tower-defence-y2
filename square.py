from mapobject import MapObject
from coordinates import Coordinates

class Square(MapObject):
    
    def __init__(self, squareSize, isWall, x, y):
        MapObject.__init__(self, squareSize*x, squareSize*y)
        self.coord = Coordinates(x,y)
        self.isWall = isWall
        self.size = squareSize
        self.cameFrom = None
        self.shape = None