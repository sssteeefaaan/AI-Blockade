from view import View
from player import Player
from table import Table


class Game:
    def __init__(self, n=11, m=14, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m)
        self.view = View(n, m, greenWall, blueWall, rowSep)
        self.next = None
        self.winner = None

    def start(self, initial):
        xPos = [x for x in initial.keys() if initial[x] in ["X1", "X2"]]
        oPos = [o for o in initial.keys() if initial[o] in ["O1", "O2"]]
        wallNumber = (initial['wallNumber'], initial['wallNumber'])
        initial.pop('wallNumber')
        self.view.showTable(self.table.greenWalls, self.table.blueWalls, {
                            "X": xPos, "O": oPos}, wallNumber, wallNumber)
        while not self.next:
            match input("X/o?\n"):
                case ("X" | "x"):
                    playerInfo = {"X": (False, wallNumber, xPos, xPos), "O": (
                        True, wallNumber, oPos, oPos)}
                case ("O" | "o"):
                    playerInfo = {"X": (True, wallNumber, oPos, oPos), "O": (
                        False, wallNumber, oPos, oPos)}
                case _:
                    print("Invalid player selection input!")
                    continue
            self.table.onInit(initial, playerInfo)
            self.next = self.table.X
        self.play()

    def play(self):
        test = 5
        while not self.winner:
            parsedMove = Game.parseMove(input(
                f"{self.next.name} is on the move!\n"))
            if parsedMove[0]:
                move = parsedMove[1]
                validated = self.validation(move)
                if validated[0]:
                    test -= 1
                    self.table.move(self.next.name, self.next.move(
                        move[0][1], move[1], move[2]), move[1], move[2])
                    self.view.showTable(*self.table.getData())
                    self.next = self.table.X if self.next.name == self.table.O.name else self.table.O
                    self.table.checkState()
                    if not test:
                        temp = self.table.getCopy()

                    if test == -5:
                        self.table = temp
                else:
                    print(validated[1])
            else:
                print(parsedMove[1])
        print(f"{self.winner.name} won! Congrats!")

    def validation(self, move):
        if self.next.name != move[0][0]:
            return (False, "Not your turn!")
        if self.table.n < move[1][0] or move[1][0] < 1:
            return (False, "Row index out of bounds!")
        if self.table.m < move[1][1] or move[1][1] < 1:
            return (False, "Column index out of bounds!")
        if move[1] == (self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position):
            return (False, "You're already on that position!")
        if move[1] == (self.next.firstGP.position if move[0][1] == 2 else self.next.secondGP.position):
            return (False, "Can't step on your pieces!")
        if not move[2] and self.next.noBlueWalls + self.next.noGreenWalls > 0:
            return (False, "You didn't put up a wall!")
        if move[2]:
            if move[2][1] > self.table.n-1 or move[2][1] < 1:
                return (False, "Wall row index out of bounds!")
            if move[2][2] > self.table.m-1 or move[2][2] < 1:
                return (False, "Wall column index out of bounds!")
            if move[2][0] == "Z":
                if self.next.noGreenWalls < 1:
                    return (False, "You don't have any green walls left to place...")
                if not self.table.isCorrectGreenWall((move[2][1], move[2][2])):
                    return (False, "Green wall cannot be set on the given position!")
            elif move[2][0] == "P":
                if self.next.noBlueWalls < 1:
                    return (False, "You don't have any blue walls left to place...")
                if not self.table.isCorrectBlueWall((move[2][1], move[2][2])):
                    return (False, "Blue wall cannot be set on the given position!")
        if not self.table.areConnected(self.next.firstGP.position if move[0][1] == 1 else self.next.secondGP.position, move[1], move[0][0]):
            return (False, "Invalid move!")
        return (True, "Valid move!")

    @staticmethod
    def parseMove(stream):
        ret = []
        m = stream.replace('[', '').replace(']', '').upper().split(' ')
        if m[0] not in ["X", "O"]:
            return (False, "Invalid player ID!")
        if m[1] not in ['1', '2']:
            return (False, "Invalid piece ID!")
        ret += [[m[0], int(m[1])]]
        if len(m) < 4:
            return (False, "Missing positional coordinates!")
        ret += [tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[2:4]])]
        if len(m) > 4:
            if m[4] not in ["Z", "P"]:
                return (False, "Invalid wall ID!")
            ret += [[m[4], *
                     [ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[5:7]]]]
        else:
            ret += [None]
        return (True, ret)

    # funkcija prvo za kopiranje trenutne tabele i odigravanja prosledjenog VALIDNOG poteza
    # zatim funkicja koja vraca sve moguce poteze
    # funkcija koja validira te poteze
    # na kraju funkcija koja vrati listu svih tabela koje bi bile nakon ovih validno odigranih poteza
    # kesiranje(maybe)?!?!?!


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
            "(", "").replace(")", "").replace(",", "").split(" ")))] = f"X{len(initial)+1}"
    while len(initial.keys()) < 4:
        temp = input(
            f"Input {len(initial)-1}. initial position for O (Empty for the default value of ({4 if len(initial)-1 == 1 else 8}, 11)): ")
        temp = temp if temp else f"({4 if len(initial)-1 == 1 else 8}, 11)"
        initial[tuple(map(lambda x: int(x), temp.replace(
            "(", "").replace(")", "").replace(",", "").split(" ")))] = f"O{len(initial)-1}"
    wallNumb = ""
    while not str.isdigit(wallNumb) or int(wallNumb) < 9 or int(wallNumb) > 18:
        wallNumb = input(
            "Input the number of blue/green walls each player has (Empty for the default minimum value of 9, the max is 18): ")
        wallNumb = wallNumb if wallNumb else "9"

    g = Game(int(n), int(m))
    g.start(initial | {'wallNumber': int(wallNumb)})


if __name__ == "__main__":
    main()
