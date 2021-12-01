from player import Player
from table import Table
from view import View

class Game:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m, initial)
        self.view = View(n, m, greenWall, blueWall, rowSep)
        
        self.human = None
        self.computer = None
        
    def play(self):
        first = input("X/O?").upper() == "X"
        self.human = Player(first, False)
        self.computer = Player(not first, True)
        print(f"You are playing {'1st' if first else '2nd'}!")

def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
