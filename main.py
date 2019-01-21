import sys
from PyQt5.QtWidgets import QApplication
from game import Game
from gui import GUI


def main():
    # Create game object
    global app
    app = QApplication(sys.argv)
    game = Game()

    gui = GUI(game)
        
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()