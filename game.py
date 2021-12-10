from player import Player
from table import Table


class Game:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, wallNumb=9, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m, initial, wallNumb,
                           greenWall, blueWall, rowSep)
        self.X = None
        self.O = None
        self.next = None
        self.winner = None

    def start(self, wallNumb, initial):
        while self.next is None:
            try:
                xPos = [x for x in initial.keys() if initial[x] == "X"]
                oPos = [o for o in initial.keys() if initial[o] == "O"]
                match input("X/o?\n"):
                    case ("X" | "x"):
                        self.X = Player(
                            True, False, wallNumb, xPos[0], xPos[1])
                        self.next = self.X
                        self.O = Player(
                            False, True, wallNumb, oPos[0], oPos[1])
                    case ("O" | "o"):
                        self.O = Player(
                            True, True, wallNumb, oPos[0], oPos[1])
                        self.next = self.O
                        self.X = Player(
                            False, False, wallNumb, xPos[0], xPos[1])
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
                    self.next = self.X if self.next.name == self.O.name else self.O
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
            if not move[2] and self.next.noBlueWalls + self.next.noGreenWalls > 0:
                raise Exception("You didn't put up a wall!")
            if move[2]:
                if move[2][1] > self.table.n-1 or move[2][1] < 1:
                        raise Exception("Wall row index out of bounds!")
                if move[2][2] > self.table.m-1 or move[2][2] < 1:
                    raise Exception("Wall column index out of bounds!")
                if move[2][0] == "Z":
                    if self.next.noGreenWalls < 1:
                        raise Exception(
                            "You don't have any green walls left to place...")
                    if not self.table.isCorrectGreenWall((move[2][1], move[2][2])):
                        raise Exception(
                            "Green wall cannot be set on the given position!")
                elif move[2][0] == "P":
                    if self.next.noGreenWalls < 1:
                        raise Exception(
                            "You don't have any blue walls left to place...")
                    if not self.table.isCorrectBlueWall((move[2][1], move[2][2])):
                        raise Exception(
                            "Blue wall cannot be set on the given position!")
            if not self.table.areConnected(self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position, move[1], move[0][0]):
                raise Exception("Invalid move!")
        except Exception as e:
            print(e)
            return False
        return True

    def checkState(self):
        if self.O.isWinner((self.X.firstGP.home, self.X.secondGP.home)):
            self.winner = self.O
        elif self.X.isWinner((self.O.firstGP.home, self.O.secondGP.home)):
            self.winner = self.X

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
    g.start(int(wallNumb), initial)

if __name__ == "__main__":
    main()
