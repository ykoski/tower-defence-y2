from mapobject import MapObject
from math import *

class Projectile(MapObject):
    
    def __init__(self,x,y,speed,damage,enemy,ptype):
        MapObject.__init__(self, x, y)
        self.speed = speed
        self.damage = damage
        self.enemy = enemy
        self.ptype = ptype
        self.rotation = 0
    
    def setRotation(self):
        dx = abs(self.enemy.x-self.x)
        dy = abs(self.enemy.y-self.y)
        
        if (dx/dy) < 0:
            a = (atan(dx/dy)*180)/pi
        else:
            a = (atan(dy/dx)*180)/pi
        
        if self.x < self.enemy.x and self.y < self.enemy.y:
            self.rotation = a
        elif self.x > self.enemy.x and self.y < self.enemy.y:
            self.rotation = a + 90
        elif self.x < self.enemy.x and self.y > self.enemy.y:
            self.rotation = 270 + a
        elif self.x > self.enemy.x and self.y > self.enemy.y:
            self.rotation = 180 + a
        
        