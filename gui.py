from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsItem, QPushButton, QSizePolicy
from PyQt5.Qt import QGraphicsRectItem, QPixmap, QGraphicsPixmapItem,\
    QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QLabel,\
    QPoint, QFont, QPainter, QGraphicsLineItem, QMessageBox, QInputDialog,\
    QLineEdit
from math import floor
from PyQt5.QtGui import QBrush, QPen, QColor
from custombutton import CustomButton

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self,game):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.btn1 = QPushButton("New wave",self)
        self.btn1.move(660,600)
        self.btn1.clicked.connect(self.activateWave)        
        
        items = ("level1", "level2", "level3", "level4","level5")
        item, ok = QInputDialog.getItem(self, "Select level","levels", items, 0, False)
        self.game = game
        self.game.loadMap(item)
        #self.start.addButton(QAbstractButton, QMessageBox_ButtonRole)
        self.map = game.map.map
        
        self.initWindow()
        self.loadTextures()

        self.drawMap()
        self.drawHp()
        self.squares()
        self.placeButtons()
        self.drawPlayerStats()
        self.drawTowerPrices()
        self.updateGame()
        self.placeTower = 0 # 0 for not active, 1 for arrow, 2 for gun and 3 for laser  
        self.timer = QtCore.QTimer()
        self.timer.start(50) # Milliseconds
        self.timer.timeout.connect(self.updateGame)
    
    def initWindow(self):
        self.setGeometry(40, 40, 800, 640)
        self.setWindowTitle('Tower Defense')
        #self.setFixedSize(self.size())
        self.show()
        self.showFullScreen()
        # Add a scene for drawing 2d objects
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 640, 640)

        # Add a view for showing the scene
        self.view = QGraphicsView(self.scene, self)
        self.view.show()
        self.view.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.view.adjustSize()
        self.horizontal.addWidget(self.view)
    
    def closeGui(self):
        self.close()

    
    def drawMap(self):
        dark = QColor(20,20,20)
        light = QColor(211,211,211)
        brush = QBrush()
        pen = QPen()
        pen.setColor(QColor(0, 0, 0, 75))
        # Create graphic objects for map squares
        for y in range(0,len(self.map)):
            for x in range(0,len(self.map[y])):
                shape = QGraphicsRectItem(self.map[y][x].size*x,self.map[y][x].size*y,self.map[y][x].size,self.map[y][x].size)
                if self.map[y][x].isWall:
                    brush.setTexture(self.grass)
                else:
                    brush.setTexture(self.gravel)
                self.map[y][x].shape = shape
                shape.setPen(pen)
                shape.setBrush(brush)
                self.scene.addItem(shape)
    
    def loadTextures(self):
        self.grass = QPixmap("grass.png")
        self.gravel = QPixmap("gravel2.png")
        self.arrow = QPixmap("arrow.png")
        self.kappa = QPixmap("kappa.png")
        self.miro = QPixmap("pikkumiro.png")
        self.heart = QPixmap("heart.png")

 
    def visualizeBfs(self):
        shape = QGraphicsRectItem(self.square.size*self.square.coord.x,self.square.size*self.square.coord.y,
                                  self.square.size,self.square.size)
        shape.setBrush(QColor(0,255,0))
        self.scene.addItem(shape)
        self.update()
        self.square = self.square.cameFrom
        
    def drawEnemies(self):
        # Go through enemies in the game and draw them
        for enemy in self.game.enemies:
            if enemy.shape == None:
                if enemy.etype == 0:
                    shape = QGraphicsEllipseItem(0,0,20,20)
                    enemy.r = 10
                elif enemy.etype == 1:
                    shape = QGraphicsEllipseItem(0,0,30,30)
                    enemy.r = 15
                elif enemy.etype == 2:
                    shape = QGraphicsEllipseItem(0,0,40,40)
                    enemy.r = 20
                shape.setBrush(QColor(0,255,0))
                shape.setX(enemy.x)
                shape.setY(enemy.y)
                self.scene.addItem(shape)
                enemy.shape = shape
            ratio = enemy.hp/enemy.maxHp
            enemy.shape.setBrush(QColor((1-ratio)*255,ratio*255,0))
            enemy.shape.setX(enemy.x-enemy.r)
            enemy.shape.setY(enemy.y-enemy.r)
            if enemy.shape.collidesWithItem(self.game.endSquare.shape):
                if self.game.player.lose == False:
                    self.game.player.hp -= 1
                    self.scene.removeItem(self.health.pop())
                enemy.goal=True
            if enemy.dead:
                if enemy.etype == 0:
                    self.game.player.getGold(10)
                    self.game.player.getPoints(100)
                elif enemy.etype == 1:
                    self.game.player.getGold(50)
                    self.game.player.getPoints(500)
                elif enemy.etype == 2:
                    self.game.player.getGold(120)
                    self.game.player.getPoints(1000)
            if enemy.dead or enemy.goal:
                self.scene.removeItem(enemy.shape)
                self.game.enemies.remove(enemy)
            self.update()
    
    def drawTowers(self):
        for tower in self.game.towers:
            if tower.shape == None:
                shape = QGraphicsRectItem(0,0,40,40)
                shape.setX(tower.x)
                shape.setY(tower.y)
                if tower.ttype == 1:
                    shape.setBrush(QColor(120,100,20))
                elif tower.ttype == 2:
                    shape.setBrush(QColor(70,70,50))
                elif tower.ttype ==3:
                    shape.setBrush(QColor(20,20,20))
                self.scene.addItem(shape)
                tower.shape = shape
                #r = QGraphicsEllipseItem(tower.x+20-tower.range,tower.y+20-tower.range,tower.range*2,tower.range*2)
                #self.scene.addItem(r)
            if tower.ttype == 3:
                for enemy in self.game.enemies:
                    if tower.canFire(enemy):
                        if enemy in tower.firesAt:
                            i = tower.firesAt.index(enemy)
                            tower.lines[i].setLine(tower.x+20,tower.y+20,enemy.x,enemy.y)
                        else:
                            line = QGraphicsLineItem(tower.x+20,tower.y+20,enemy.x,enemy.y)
                            line.setPen(QColor(255,0,0))
                            self.scene.addItem(line)
                            tower.firesAt.append(enemy)
                            tower.lines.append(line)
                        enemy.hp -= tower.damage
                        if enemy.hp <= 0:
                            i = tower.firesAt.index(enemy)
                            self.scene.removeItem(tower.lines[i])
                    else:
                        if enemy in tower.firesAt:
                            i = tower.firesAt.index(enemy)
                            self.scene.removeItem(tower.lines[i])
    
    def drawProjectiles(self):
        for projectile in self.game.projectiles:
            if projectile.shape == None:
                if projectile.ptype == 1:
                    shape = QGraphicsPixmapItem(self.arrow)
                elif projectile.ptype == 2:
                    shape = QGraphicsEllipseItem(0,0,5,5)
                    shape.setBrush(QColor(0,0,0))
                shape.setX(projectile.x)
                shape.setY(projectile.y)
                self.scene.addItem(shape)
                projectile.shape = shape
            projectile.shape.setX(projectile.x)
            projectile.shape.setY(projectile.y)
            if projectile.ptype == 1:
                projectile.shape.setRotation(projectile.rotation)
            if projectile.shape.collidesWithItem(projectile.enemy.shape):
                projectile.enemy.getHit(projectile.damage)
                self.scene.removeItem(projectile.shape)
                self.game.projectiles.remove(projectile)
            self.update()
    
    def updateGame(self):
        self.game.updateAll()
        self.checkButtons()
        self.drawEnemies()
        self.drawTowers()
        self.drawProjectiles()
        self.checkGameOver()
        self.updatePlayerStats()
        if self.game.over:
            box = QMessageBox()
            box.setWindowTitle("Game Over")
            box.setText("You got "+str(self.game.player.points)+" points.")
            box.setStandardButtons(QMessageBox.Ok)
            box.buttonClicked.connect(self.closeGui)
            retval = box.exec_()
        
    def mousePressEvent(self, event):
        if self.placeTower != 0:  
            pos = event.pos()
            x = floor(pos.x()/self.game.squareSize)
            y = floor(pos.y()/self.game.squareSize)
            self.game.addTower(x,y,self.placeTower)
            self.placeTower = 0
    
    def placeButtons(self):
        for b in self.game.buttons:
            self.scene.addItem(b)
    
    def checkButtons(self):
        for b in self.game.buttons:
            if b.activated and b.type == 1:
                self.placeTower = 1
            elif b.activated and b.type ==2:
                self.placeTower = 2
            elif b.activated and b.type == 3:
                self.placeTower = 3
        if self.game.buttons[0].activated == False and self.game.buttons[1].activated == False and self.game.buttons[2].activated == False:
            self.placeTower = 0
    
    def squares(self):
        shape2 = QGraphicsRectItem(0,0,40,40)
        shape2.setX(self.game.endSquare.x)
        shape2.setY(self.game.endSquare.y)
        shape2.setBrush(QColor(0,0,200,0))
        shape2.setPen(QColor(0,0,0,0))
        self.scene.addItem(shape2)
        self.game.endSquare.shape = shape2
        
        self.update()
    
    def drawHp(self):
        self.health = []
        hpcount = self.game.player.hp
        for i in range(0,hpcount):
            heart = QGraphicsPixmapItem(self.heart)
            heart.setY(660)
            heart.setX(20+i*50)
            self.scene.addItem(heart)
            self.health.append(heart)
        
    
    def activateWave(self):
        if not self.game.wave.active:
            self.game.wave.active = True
            self.game.wave.generateEnemies()
    
    def checkGameOver(self):
        if self.game.player.lose:
            self.game.over = True
    
    def drawPlayerStats(self):
        font = QFont("Arial",20)
        self.gold = QLabel("Gold: " + str(self.game.player.gold))
        self.gold.setFont(font)
        self.gold.move(QPoint(545,660))
        self.points = QLabel("Points: " + str(self.game.player.points))
        self.points.setFont(font)
        self.points.move(QPoint(545,705))
        self.wavenum = QLabel("Wave number: " + str(self.game.wave.level))
        self.wavenum.setFont(font)
        self.wavenum.move(QPoint(20,705))
        self.scene.addWidget(self.wavenum)
        self.scene.addWidget(self.gold)
        self.scene.addWidget(self.points)
    
    
    def updatePlayerStats(self):
        self.gold.setText("Gold: "+str(self.game.player.gold))
        self.points.setText("Points: "+str(self.game.player.points))
        self.wavenum.setText("Wave number: " + str(self.game.wave.level))
        wg = self.gold.fontMetrics().width(self.gold.text())
        wp = self.points.fontMetrics().width(self.points.text())
        wn = self.wavenum.fontMetrics().width(self.wavenum.text())
        self.wavenum.setFixedWidth(wn)
        self.gold.setFixedWidth(wg)
        self.points.setFixedWidth(wp)
    
    def drawTowerPrices(self):
        font = QFont("Arial",15)
        arrowtower = QLabel("50")
        arrowtower.setFont(font)
        arrowtower.move(QPoint(650,70))
        self.scene.addWidget(arrowtower)

        guntower = QLabel("100")
        guntower.setFont(font)
        guntower.move(QPoint(650,150))
        self.scene.addWidget(guntower)

        lasertower = QLabel("500")
        lasertower.setFont(font)
        lasertower.move(QPoint(650,230))
        self.scene.addWidget(lasertower)
        
        

        
        
            

        