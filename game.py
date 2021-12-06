from player import Player
from table import Table
from view import View

class Game:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m, initial)
        self.view = View(n, m, greenWall, blueWall, rowSep)
        
        self.human = None
        self.computer = None
        self.next = None
        self.winner = None
        
    def start(self):
        if input("X/O?").upper() == "X": 
            self.human = Player(True, False)
            self.next = self.human
            self.computer = Player(False, True)
        else:
            self.computer = Player(True, True)
            self.next = self.computer
            self.human = Player(False, False)

        self.play()

    def play(self):
        while not self.isEnd():
            move = input(f"{self.next.name} is on the move!").replace('[', '').replace(']', '').split(' ')
            GP, pos, wall = move[:2], move[2:4], move[4:7]
            GP[1] = int(GP[1])
            wall[1] = int(wall[1])
            wall[2] = int(wall[2])
            pos = [int(x) for x in pos]
            print(GP)
            print(pos)
            print(wall)
            if self.validation():  
                self.view.move(self.next.move(pos, GP[1], wall), (*pos, GP[0], wall))

    def validation(self):
        return True

    def isEnd(self):
        if self.computer.isLooser((self.human.firstGP.position, self.human.secondGP.position)):
            self.winner = self.human
        elif self.human.isLooser((self.computer.firstGP.position, self.computer.secondGP.position)):
            self.winner = self.computer
        return self.winner != None


def main():
    g = Game()
    g.start()


if __name__ == "__main__":
    main()
