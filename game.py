import sys
from gui import GUI
from PyQt5.QtWidgets import QApplication
from breadth import BreadthSearch
from map import Map
from enemy import Enemy
from tower import Tower
from projectile import Projectile
from custombutton import CustomButton
from square import Square
from wave import Wave
from PyQt5.QtGui import QPixmap
from player import Player
from lasertower import LaserTower


class Game():
    
    def __init__(self):
        self.squareSize = 40
        self.width = 600
        self.height = 600
        self.over = False
        
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.player = Player(200,10)
    
    def loadMap(self,level):
        self.map = Map(self.squareSize,level)
        self.createSpawnAndEnd()
        self.CreateButtons()
        self.createWave()
        self.bfs = BreadthSearch(self.map)
        self.bfs.bfs(self.bfs.map.map[self.map.end.y][self.map.end.x])
    
    def createWave(self):
        self.wave = Wave(self.spawnSquare.x,self.spawnSquare.y,self.map)
    
    def updateTowers(self):
        for tower in self.towers:
            for enemy in self.enemies:
                if tower.canFire(enemy) and tower.ttype != 3:
                    tower.fire()
                    newprojectile = Projectile(tower.x+20,tower.y+20,tower.projSpeed,tower.damage,enemy,tower.ttype)
                    self.projectiles.append(newprojectile)
            tower.readyToFire()
    
    def updateEnemies(self):
        if self.wave.active == True:
            if self.wave.delay == 0:
                e = self.wave.spawnEnemies()
                if e != None:
                    self.enemies.append(e)
            else:
                self.wave.delay -= 1
        for enemy in self.enemies:
            enemy.move()
            if enemy.hp <= 0:
                enemy.dead = True
    
    def updateProjectiles(self):
        for projectile in self.projectiles:
            projectile.moveTowards(projectile.enemy)
            projectile.setRotation()

    def updateAll(self):
        self.updateTowers()
        self.updateProjectiles()
        self.updateEnemies()
        self.player.updatePlayer()
    
    def addTower(self,x,y,ttype):
        gold = [50,100,500]
        if x < len(self.map.map) and y < len(self.map.map[0]) and self.map.map[y][x].isWall and self.isFree(x,y):
            g = gold[ttype-1]
            if self.player.gold >= g:
                self.player.getGold(-g)
                if ttype == 1:
                    # Arrow tower
                    #Tower(self,x,y,damage,trange,firerate,projSpeed,ttype):
                    newtower = Tower(x*self.squareSize,y*self.squareSize,10,200,10,20,1)
                    self.buttons[0].activated = False
                elif ttype == 2:
                    newtower = Tower(x*self.squareSize,y*self.squareSize,10,150,15,20,2)  
                    self.buttons[1].activated = False
                elif ttype == 3:
                    newtower = LaserTower(x*self.squareSize,y*self.squareSize,4,100,3)
                    self.buttons[2].activated = False
                self.towers.append(newtower)

    
    def CreateButtons(self):
        gt = QPixmap("guntower.png")
        at = QPixmap("arrowtower.png")
        lt = QPixmap("lasertower.png")
        arrowTowerButton = CustomButton(650,20,at,1)
        gunTowerButton = CustomButton(650,100,gt,2)
        laserTowerButton = CustomButton(650,180,lt,3)
        
        self.buttons = []
        self.buttons.append(arrowTowerButton)
        self.buttons.append(gunTowerButton)
        self.buttons.append(laserTowerButton)
        
    
    def isFree(self,x,y):
        if len(self.towers) > 0:
            for t in self.towers:
                if t.x/self.squareSize == x and t.y/self.squareSize == y:
                    return False
        return True
    
    def createSpawnAndEnd(self):
        if self.map.start.y == 0: # Up edge
            spawnSquare = Square(self.squareSize,False,self.map.start.x,(self.map.start.y-1))
        elif self.map.start.x == 0: # Left edge
            spawnSquare = Square(self.squareSize,False,(self.map.start.x-1),self.map.start.y)
        elif self.map.start.y == len(self.map.map)-1: # down edge
            spawnSquare = Square(self.squareSize,False,self.map.start.x,(self.map.start.y+1))
        elif self.map.start.x == len(self.map.map[0])-1: # right edge
            spawnSquare = Square(self.squareSize,False,(self.map.start.x+1),self.map.start.y)
        self.spawnSquare = spawnSquare
        self.spawnSquare.cameFrom = self.map.map[self.map.start.y][self.map.start.x]

        if self.map.end.y == 0: # Up edge
            endSquare = Square(self.squareSize,False,self.map.end.x,(self.map.end.y-1.5))
        elif self.map.end.x == 0: # Left edge
            endSquare = Square(self.squareSize,False,self.map.end.x-1.5,self.map.end.y)
        elif self.map.end.y == len(self.map.map)-1: # down edge
            endSquare = Square(self.squareSize,False,self.map.end.x,self.map.end.y+1.5)
        elif self.map.end.x == len(self.map.map[0])-1: # right edge
            endSquare = Square(self.squareSize,False,(self.map.end.x+1.5,self.map.end.y))
        self.endSquare = endSquare
        self.map.map[self.map.end.y][self.map.end.x].cameFrom = endSquare 
        
"""
def main():
    # Create game object
    global app
    app = QApplication(sys.argv)
    game = Game()

    gui = GUI(game)
        
    sys.exit(app.exec_())
    
main()
"""