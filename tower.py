from mapobject import MapObject

class Tower(MapObject):
    
    def __init__(self,x,y,damage,trange,firerate,projSpeed,ttype):
        MapObject.__init__(self, x, y)
        self.ttype = ttype
        self.damage = damage
        self.firerate = firerate
        self.rest = False
        self.waitTime = 0
        self.range = trange
        self.projSpeed = projSpeed
    
    def fire(self):
        self.rest = True
        self.waitTime = self.firerate
    
    def canFire(self,enemy):
        if self.getDistance(enemy) < self.range and self.rest == False:
            return True
    
    def readyToFire(self):
        if self.waitTime == 0:
            self.rest = False
        else:
            self.waitTime -= 1