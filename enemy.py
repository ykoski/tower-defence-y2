from mapobject import MapObject
from coordinates import Coordinates
from math import *

class Enemy(MapObject):
    
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def __init__(self,x,y,speed,hp,gamemap,moveto,etype):
        MapObject.__init__(self, x, y)
        self.map = gamemap
        self.speed = speed
        self.maxHp = hp
        self.hp = hp
        self.etype = etype
        self.r = 0
        
        self.dead = False
        self.goal = False
        self.moveTowards = moveto
        self.coord = None
        self.setCoordinates()     
        self.getNext()
        
        self.direction = None
        self.getDirection()

    
    def move(self):
        self.setCoordinates()
        if self.isPastCenter():
            self.getNext()
            self.getDirection()
        dx = (self.moveTowards.x+self.map.squareSize/2)-self.x
        dy = (self.moveTowards.y+self.map.squareSize/2)-self.y
        dist = sqrt(pow(dx,2) + pow(dy,2))
        multip = self.speed/dist       
        x = multip*dx
        y = multip*dy
        
        self.x += x
        self.y += y
        
        
    def setCoordinates(self):
        x = floor(self.x/self.map.squareSize)
        y = floor(self.y/self.map.squareSize)
        self.coord = Coordinates(x,y)
    
    def getDirection(self):
        if self.moveTowards.coord.x == self.coord.x + 1 and self.moveTowards.coord.y == self.coord.y:
            #right
            self.direction = 1
        elif self.moveTowards.coord.x == self.coord.x and self.moveTowards.coord.y == self.coord.y+1:
            #down
            self.direction = 2
        elif self.moveTowards.coord.x == self.coord.x -1 and self.moveTowards.coord.y == self.coord.y:
            #left
            self.direction = 3
        elif self.moveTowards.coord.x == self.coord.x and self.moveTowards.coord.y == self.coord.y-1:
            #up
            self.direction = 0
    
    def getNext(self):
        if self.coord.x >= 0 and self.coord.y >= 0 and self.coord.x <= len(self.map.map)-1 and self.coord.y <= len(self.map.map[0])-1:
            self.moveTowards = self.map.map[self.coord.y][self.coord.x].cameFrom
    
    def isPastCenter(self):
        # UP = 0 RIGHT = 1 DOWN = 2 LEFT = 3
        if self.direction == 0 and self.y > self.moveTowards.y+20: #up
            return True
        elif self.direction == 1 and self.x > self.moveTowards.x+20: #right
            return True
        elif self.direction == 2 and self.y>self.moveTowards.y+20: #down
            return True
        elif self.direction == 3 and self.x < self.moveTowards.x+20: #left
            return True
        else:
            return False
    
    def getHit(self,damage):
        self.hp -= damage
        if self.hp <= 0:
            self.dead = True
        
        
        
        