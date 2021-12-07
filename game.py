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
        while self.next is None:
            try:
                match input("X/o?\n"):
                    case ("X" | "x"):
                        self.human = Player(True, False)
                        self.next = self.human
                        self.computer = Player(False, True)
                    case ("O" | "o"):
                        self.computer = Player(True, True)
                        self.next = self.computer
                        self.human = Player(False, False)
                    case _:
                        raise Exception("Invalid player selection input!")
            except Exception as e:
                print(e)

        self.play()

    def play(self):
        while not self.isEnd():
            try:
                move = self.parseMove(input(f"{self.next.name} is on the move!\n{'*'*10}\nMoves are in the form '(\\[[XxOo] [1-2]\] \\[[1-n] [1-m]\\]){'{1}'}( \\[[Zz] [1-n] [1-(m-1)]|[Pp] [1-(n-1)] [1-m]\\])?'\n{'*'*10}\n"))
                if move and self.validation(move):  
                    self.view.move(self.next.move(move[1], move[0][1], move[2]), (*move[1], move[0][0], move[2]))
                    self.next = self.human if self.next.name == self.computer.name else self.computer
            except Exception as e:
                print(e)

    def parseMove(self, stream):
        try:
            ret = []
            m = stream.replace('[', '').replace(']', '').upper().split(' ')
            if m[0] not in ["X", "O"]:
                raise Exception("Invalid player ID!")
            if m[1] not in ['1', '2']:
                raise Exception("Invalid piece ID!")
            ret += [[m[0], int(m[1], base=16)]]
            if len(m) < 4:
                raise Exception("Missing positional coordinates!")
            ret += [[int(x, base=16) for x in m[2:4]]]
            if len(m) > 4:
                if m[4] not in ["Z", "P"]:
                    raise Exception("Invalid wall ID!")
                ret += [[m[4], int(m[5], base=16), int(m[6], base=16)]]
            else:
                ret += [None]
            return ret
        except Exception as e:
            print(e)
            return []
        
    def validation(self, move):
        try:
            if self.next.name != move[0][0]:
                raise Exception("Not your turn!")
            if self.table.n < move[1][0] or move[1][0] < 1:
                raise Exception("Row index out of bounds!")
            if self.table.m < move[1][1] or move[1][1] < 1:
                raise Exception("Column index out of bounds!")
            if move[2] and move[2][0] == "Z":
                if move[2][1] > self.table.n-1 or move[2][1] < 1:
                    raise Exception("Green wall row index out of bounds!")
                if move[2][2] > self.table.m or move[2][2] < 1:
                    raise Exception("Wall column index out of bounds!")
            if move[2] and move[2][0] == "P":
                if move[2][1] > self.table.n or move[2][1] < 1:
                    raise Exception("Wall row index out of bounds!")
                if move[2][2] > self.table.m-1 or move[2][2] < 1:
                    raise Exception("Blue wall column index out of bounds!")
            # ukoliko je polje zauzeto igracem, dozvoljeno je kretanje U TOM SMERU ZA JEDAN
            # u suprotnom kretanje je dozvoljeno ukoliko nije postavljen zid i igrac se pomera
            # u manhattan pattern-u
        except Exception as e:
            print(e)
            return False
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
