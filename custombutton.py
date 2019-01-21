from PyQt5.Qt import QGraphicsPolygonItem, QGraphicsRectItem,\
    QGraphicsPixmapItem, QPixmap
from PyQt5.QtGui import QBrush, QPen, QColor


class CustomButton(QGraphicsPixmapItem):
    
    def __init__(self,x,y,pmap,ttype):
        super(CustomButton,self).__init__()
        self.activated = False
        self.setPixmap(pmap)
        self.type = ttype
        self.setX(x)
        self.setY(y)
    
    def mousePressEvent(self, event):
        if self.activated:
            self.activated = False
        else:
            self.activated = True
        