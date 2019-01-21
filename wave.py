from math import floor
from enemy import Enemy
from random import randint

class Wave():
    
    def __init__(self,x,y,map):
        self.x = x
        self.y = y
        self.map = map
        self.spawnTime = 20
        self.delay = 0
        self.level = 0
        self.active = False
        self.enemies = []
    
    def generateEnemies(self):
        self.level = self.level+1
        points = 10 + self.level + floor(self.level/2) + floor(self.level/5)
        while points > 0:
            int = randint(0,(3*self.level+10))
            if int >= 22 and points >= 10:
                self.enemies.append(2)
                points -= 10
            elif int > 15 and int < 22 and points >= 5:
                self.enemies.append(1)
                points -= 5
            else:
                self.enemies.append(0)
                points -= 1
        
    def spawnEnemies(self):
        
        newenemy = None
        if len(self.enemies) != 0:
            e = self.enemies.pop()
            if e == 0:
                newenemy = Enemy(self.x,self.y,6,100,self.map,self.map.map[self.map.start.y][self.map.start.x],0)
            elif e == 1:
                newenemy = Enemy(self.x,self.y,4,500,self.map,self.map.map[self.map.start.y][self.map.start.x],1)
            elif e == 2:
                newenemy = Enemy(self.x,self.y,2,1000,self.map,self.map.map[self.map.start.y][self.map.start.x],2)
            self.delay = self.spawnTime + randint(0,10)
        else:
            self.active = False
        return newenemy
            