from mapobject import MapObject

class LaserTower(MapObject):
    
    def __init__(self,x,y,damage,trange,ttype):
        MapObject.__init__(self, x, y)
        self.damage = damage
        self.range = trange
        self.ttype = ttype
        self.rest = False
        self.firesAt = []
        self.lines = []
    
    def canFire(self,enemy):
        if self.getDistance(enemy) < self.range and self.rest == False:
            return True
    
    def readyToFire(self):
        self.rest = False
    