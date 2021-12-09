from player import Player
from table import Table


class Game:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, wallNumb=9, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m, initial, wallNumb, greenWall, blueWall, rowSep)
        self.wallNumb = wallNumb
        self.human = None
        self.computer = None
        self.next = None
        self.winner = None

    def start(self):
        while self.next is None:
            try:
                match input("X/o?\n"):
                    case ("X" | "x"):
                        self.human = Player(True, False, self.wallNumb)
                        self.next = self.human
                        self.computer = Player(False, True, self.wallNumb)
                    case ("O" | "o"):
                        self.computer = Player(True, True, self.wallNumb)
                        self.next = self.computer
                        self.human = Player(False, False, self.wallNumb)
                    case _:
                        raise Exception("Invalid player selection input!")
            except Exception as e:
                print(e)

        self.play()

    def play(self):
        while not self.winner:
            try:
                move = self.parseMove(input(
                    f"{self.next.name} is on the move!\n"))
                if move and self.validation(move):
                    self.table.move(self.next.name, self.next.move(
                        move[0][1], move[1], move[2]), move[1], move[2])
                    self.next = self.human if self.next.name == self.computer.name else self.computer
                    self.checkState()
            except Exception as e:
                print(e)
        print(f"{self.winner.name} won! Congrats!")

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
            ret += [tuple([int(x, base=16) for x in m[2:4]])]
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
            if move[1] == (self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position):
                raise Exception("You're already on that position!")
            if move[1] == (self.next.firstGP.position if move[0][1] == 2 else self.next.secondGP.position):
                raise Exception("Can't step on your pieces!")
            if move[1] in [self.next.firstGP.position, self.next.secondGP.position]:
                raise Exception("Can't step on your home!")
            if move[1] in ([self.human.firstGP.position, self.human.secondGP.position] if self.next == self.computer else [self.computer.firstGP.position, self.computer.secondGP.position]):
                raise Exception("Can't step on your opponent!")
            if move[2]:
                if move[2][0] == "Z":
                    if self.next.noGreenWalls < 1:
                        raise Exception(
                            "You don't have any green walls left to place...")
                    if move[2][1] > self.table.n-1 or move[2][1] < 1:
                        raise Exception("Green wall row index out of bounds!")
                    if move[2][2] > self.table.m or move[2][2] < 1:
                        raise Exception("Wall column index out of bounds!")
                    if not self.table.isCorrectGreenWall((move[2][1], move[2][2])):
                        raise Exception(
                            "Green wall cannot be set on the given position!")
                elif move[2][0] == "P":
                    if self.next.noGreenWalls < 1:
                        raise Exception(
                            "You don't have any blue walls left to place...")
                    if move[2][1] > self.table.n or move[2][1] < 1:
                        raise Exception("Wall row index out of bounds!")
                    if move[2][2] > self.table.m-1 or move[2][2] < 1:
                        raise Exception(
                            "Blue wall column index out of bounds!")
                    if not self.table.isCorrectBlueWall((move[2][1], move[2][2])):
                        raise Exception(
                            "Blue wall cannot be set on the given position!")
            if self.manhattan(self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position, move[1]) != 2:
                raise Exception(
                    "Invalid move! Only manhattan pattern moves allowed!")
            if not self.table.areConnected(self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position, move[1]):
                raise Exception("Invalid move! Something's on the way...")

        except Exception as e:
            print(e)
            return False
        return True

    def checkState(self):
        if self.computer.isWinner((self.human.home1, self.human.home2)):
            self.winner = self.computer
        elif self.human.isWinner((self.computer.home1, self.computer.home2)):
            self.winner = self.human

    def manhattan(self, currentPos, followedPos):
        return abs(currentPos[0] - followedPos[0]) + abs(currentPos[1] - followedPos[1])


def main():
    n = m = ""
    while not str.isdigit(n) or int(n) < 11 or int(n) > 22:
        n = input(
            "Input number of rows in the table (Empty for the default minimum value of 11, the max is 22): ")
        n = n if n else "11"
    while not str.isdigit(m) or int(m) < 14 or int(m) > 28:
        m = input(
            "Input number of columns in the table (Empty for the default minimum value of 14, the maximum is 28): ")
        m = m if m else "14"
    initial = {}
    while len(initial.keys()) < 2:
        temp = input(
            f"Input {len(initial)+1}. initial position for X (Empty for the default value of ({4 if len(initial) == 0 else 8}, 4)): ")
        temp = temp if temp else f"({4 if len(initial) == 0 else 8}, 4)"
        initial[tuple(map(lambda x: int(x), temp.replace(
            "(", "").replace(")", "").replace(",", "").split(" ")))] = "X"
    while len(initial.keys()) < 4:
        temp = input(
            f"Input {len(initial)-1}. initial position for O (Empty for the default value of ({4 if len(initial)-1 == 1 else 8}, 11)): ")
        temp = temp if temp else f"({4 if len(initial)-1 == 1 else 8}, 11)"
        initial[tuple(map(lambda x: int(x), temp.replace(
            "(", "").replace(")", "").replace(",", "").split(" ")))] = "O"
    wallNumb = ""
    while not str.isdigit(wallNumb) or int(wallNumb) < 9 or int(wallNumb) > 18:
        wallNumb = input(
            "Input the number of blue/green walls each player has (Empty for the default minimum value of 9, the max is 18): ")
        wallNumb = wallNumb if wallNumb else "9"

    g = Game(int(n), int(m), initial, int(wallNumb))
    g.start()


if __name__ == "__main__":
    main()
