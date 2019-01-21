
class Player():
    
    def __init__(self,gold,hp):
        self.gold = gold
        self.points = 0
        self.hp = hp
        self.lose = False
    
    def loseHp(self,amount):
        self.hp -= amount
    
    def getPoints(self,amount):
        self.points += amount
    
    def getGold(self,amount):
        self.gold += amount
    
    def updatePlayer(self):
        if self.hp <= 0:
            self.lose = True
        