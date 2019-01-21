from math import *

class MapObject():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = None
    
    def getDistance(self,other):
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        r = sqrt(pow(dx,2)+pow(dy,2))
        return r
    
    def moveTowards(self,other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = sqrt(pow(dx,2) + pow(dy,2))
        multip = self.speed/dist       
        x = multip*dx
        y = multip*dy
        self.x += x
        self.y += y