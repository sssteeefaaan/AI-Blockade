from view import View
from table import Table
from sys import setrecursionlimit

setrecursionlimit(128000)


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
        self.view.showTable(self.table.greenWalls, self.table.blueWalls, {"X": xPos, "O": oPos}, wallNumber, wallNumber)
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
        while not self.winner:
            parsedMove = Game.parseMove(input(f"{self.next.name} is on the move!\n"))
            if parsedMove['correct']:
                if parsedMove['game piece']:
                    move = self.validateGamePieceMove(parsedMove['game piece'])
                    if move['valid']:
                        self.table.setGamePiece(move['game piece'])
                elif parsedMove['blue wall']:
                    move = self.validateBlueWall(parsedMove['blue wall'] | {'next': self.next.name})
                    if move['valid']:
                        if move.get('virtual', None):
                            self.table = move['virtual']
                        else:
                            self.table.setBlueWall(move['blue wall'])
                else:
                    move = self.validateGreenWall(parsedMove['green wall'] | {'next': self.next.name})
                    if move['valid']:
                        if move.get('virtual', None):
                            self.table = move['virtual']
                        else:
                            self.table.setGreenWall(move['green wall'])
                if move['valid']:
                    self.table.showPaths(True)
                    self.view.showTable(*self.table.getData())
                    self.next = self.table.X if self.next.name == self.table.O.name else self.table.O
                    self.table.checkState()
                else:
                    print(move['message'])
            else:
                print(parsedMove['message'])
        print(f"{self.winner.name} won! Congrats!")

    def genNewStates(self):
        states = {
            'blue wall': list(),
            'green wall': list(),
            'game piece': list()
        }
        if self.next.noBlueWalls > 0:
            for i in range(1, self.table.n):
                for j in range(1, self.table.m):
                    if self.table.isCorrectBlueWall((i, j)):
                        temp = self.table.getCopy()
                        temp.setBlueWall({
                            'position': (i, j),
                            'next': self.next.name
                        })
                        if not self.table.isConnectedBlueWall((i, j)) or temp.canBothPlayersFinish(True, True):
                            states['blue wall'].append(temp)
        if self.next.noGreenWalls > 0:
            for i in range(1, self.table.n):
                for j in range(1, self.table.m):
                    if self.table.isCorrectGreenWall((i, j)):
                        temp = self.table.getCopy()
                        temp.setGreenWall({
                            'position': (i, j),
                            'next': self.next.name
                        })
                        if not self.table.isConnectedGreenWall((i, j)) or temp.canBothPlayersFinish(True, True):
                            states['green wall'].append(temp)
        if self.next.name == "X":
            positions = self.next.getCurrectPositions()
            for choice in range(1, 3):
                for newPos in self.table.fields[positions[choice - 1]].connectedX:
                    states['game piece'].append(self.table.getCopy())
                    states['game piece'][-1].setGamePiece({
                        'previous position': positions[choice - 1],
                        'position': newPos,
                        'name': "X",
                        'choice': choice
                    })
        elif self.next.name == "O":
            positions = self.next.getCurrectPositions()
            for choice in range(1, 3):
                for newPos in self.table.fields[positions[choice - 1]].connectedO:
                    states['game piece'].append(self.table.getCopy())
                    states['game piece'][-1].setGamePiece({
                        'previous position': positions[choice - 1],
                        'position': newPos,
                        'name': "O",
                        'choice': choice
                    })
        return states

    def validateGamePieceMove(self, move):
        ret = {'valid': False}
        if self.next.name != move['name']:
            ret['message'] = "Not your turn!"
        elif 1 > move['position'][0] > self.table.n:
            ret['message'] = "Row index out of bounds!"
        elif 1 > move['position'][1] > self.table.m:
            ret['message'] = "Column index out of bounds!"
        elif move['position'] in self.next.getCurrectPositions():
            ret['message'] = "You're already on that position!"
        elif not self.table.areConnected(self.next.getCurrectPositions()[move['choice'] - 1], move['position'], move['name']):
            ret['message'] = "Can't move there!"
        else:
            ret['valid'] = True
            ret['game piece'] = move
        return ret

    def validateBlueWall(self, wall):
        ret = {'valid': False, 'message': ""}
        if self.next.getWallNumber()[0] < 1:
            ret['message'] = "No blue walls left!"
        elif 1 > wall['position'][0] > self.table.n - 1:
            ret['message'] = "Row index out of bounds!"
        elif 1 > wall['position'][1] > self.table.m - 1:
            ret['message'] = "Column index out of bounds!"
        elif not self.table.isCorrectBlueWall(wall['position']):
            ret['message'] = "Can't put a blue wall on the given position!"
        elif not self.table.isConnectedBlueWall(wall['position']):
            ret['valid'] = True
            ret['blue wall'] = wall
        else:
            temp = self.table.getCopy()
            temp.setBlueWall(wall)
            if not temp.canPlayerXFinish(True):
                ret['message'] += "Player X can't finish!"
            if not temp.canPlayerOFinish(True):
                ret['message'] += "Player O can't finish!"
            if temp.canBothPlayersFinish():
                ret['valid'] = True
                ret['virtual'] = temp
        return ret

    def validateGreenWall(self, wall):
        ret = {'valid': False, 'message': ""}
        if self.next.getWallNumber()[1] < 1:
            ret['message'] = "No green walls left!"
        elif 1 > wall['position'][0] > self.table.n - 1:
            ret['message'] = "Row index out of bounds!"
        elif 1 > wall['position'][1] > self.table.m - 1:
            ret['message'] = "Column index out of bounds!"
        elif not self.table.isCorrectGreenWall(wall['position']):
            ret['message'] = "Can't put a green wall on the given position!"
        elif not self.table.isConnectedGreenWall(wall['position']):
            ret['valid'] = True
            ret['green wall'] = wall
        else:
            temp = self.table.getCopy()
            temp.setGreenWall(wall)
            if not temp.canPlayerXFinish(True):
                ret['message'] += "Player X can't finish!"
            if not temp.canPlayerOFinish(True):
                ret['message'] += "Player O can't finish!"
            if temp.canBothPlayersFinish():
                ret['valid'] = True
                ret['virtual'] = temp
        return ret

    @staticmethod
    def parseMove(stream):
        ret = {
            'correct': False,
            'message': None,
            'green wall': None,
            'blue wall': None,
            'game piece': None
        }
        m = stream.replace('[', '').replace(']', '').upper().split(' ')
        if m[0] in ['X', 'O']:
            if m[1] not in ['1', '2']:
                ret['message'] = "Invalid piece ID!"
            else:
                try:
                    ret['game piece'] = {
                        'name': m[0],
                        'choice': int(m[1]),
                        'position': tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[2:4]])
                    }
                    ret['correct'] = True
                except Exception as e:
                    ret['message'] = "Incorrect possitional coordinates!"
        elif m[0] == 'B':
            try:
                ret['blue wall'] = {'position': tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[1:3]])}
                ret['correct'] = True
            except Exception as e:
                ret['message'] = "Incorrect possitional coordinates!"
        elif m[0] == 'G':
            try:
                ret['green wall'] = {'position': tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[1:3]])}
                ret['correct'] = True
            except Exception as e:
                ret['message'] = "Incorrect possitional coordinates!"
        else:
            ret['message'] = "Invalid move choice!"
        return ret


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
        initial[tuple(map(lambda x: int(x), temp.replace("(", "").replace(
            ")", "").replace(",", "").split(" ")))] = f"X{len(initial)+1}"
    while len(initial.keys()) < 4:
        temp = input(
            f"Input {len(initial)-1}. initial position for O (Empty for the default value of ({4 if len(initial)-1 == 1 else 8}, 11)): ")
        temp = temp if temp else f"({4 if len(initial)-1 == 1 else 8}, 11)"
        initial[tuple(map(lambda x: int(x), temp.replace("(", "").replace(
            ")", "").replace(",", "").split(" ")))] = f"O{len(initial)-1}"
    wallNumb = ""
    while not str.isdigit(wallNumb) or int(wallNumb) < 9 or int(wallNumb) > 18:
        wallNumb = input(
            "Input the number of blue/green walls each player has (Empty for the default minimum value of 9, the max is 18): ")
        wallNumb = wallNumb if wallNumb else "9"

    g = Game(int(n), int(m))
    g.start(initial | {'wallNumber': int(wallNumb)})


if __name__ == "__main__":
    main()
