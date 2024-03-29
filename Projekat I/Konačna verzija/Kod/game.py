from view import View
from table import Table
from sys import setrecursionlimit
from time import monotonic

setrecursionlimit(128000)

class Game:
    def __init__(self, n=11, m=14, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.table = Table(n, m)
        self.view = View(n, m, greenWall, blueWall, rowSep)
        self.next = None
        self.winner = None
        Game.oo = float("inf")
        Game.r = 1
        Game.minmaxDepth = 1

    def start(self, initial):
        xPos = [x for x in initial.keys() if initial[x] in ["X1", "X2"]]
        oPos = [o for o in initial.keys() if initial[o] in ["O1", "O2"]]
        wallNumber = (initial['wallNumber'], initial['wallNumber'])
        initial.pop('wallNumber')
        self.view.showTable(self.table.greenWalls, self.table.blueWalls, {"X": xPos, "O": oPos}, wallNumber, wallNumber)
        while not self.next:
            match input("X/o?\n"):
                case ("X" | "x"):
                    playerInfo = {
                        "X": (False, wallNumber, xPos),
                        "O": (True, wallNumber, oPos)
                    }
                case ("O" | "o"):
                    playerInfo = {
                        "X": (True, wallNumber, xPos),
                        "O": (False, wallNumber, oPos)
                    }
                case _:
                    print("Invalid player selection input!")
                    continue
            self.table.onInit(initial, playerInfo)
            self.next = self.table.X
        self.play()

    def play(self):
        while not self.winner:
            if self.next.isComputer:
                currTime = monotonic()
                temp = Game.minmax(self.table, Game.minmaxDepth, self.next, ([self.table], -Game.oo), ([self.table], Game.oo))
                print(f"Minmax {Game.minmaxDepth} time {monotonic() - currTime}s!")
                if len(temp) < 2:
                    self.winner = self.table.X if self.next.name == "O" else self.table.O
                else:
                    self.table = temp[1]
                self.nextMove()
            else:
                parsedMove = Game.parseMove(
                    input(f"{self.next.name} is on the move!\n"))
                if not parsedMove['errors']:
                    move = self.validateMove(parsedMove)
                    if not move['errors']:
                        if move.get('virtual', None):
                            self.table = move['virtual']
                        self.table.playMove(move)
                        self.nextMove()
                    else:
                        print(move['errors'])
                else:
                    print(parsedMove['errors'])
        print(f"{self.winner.name} won! Congrats!")

    def nextMove(self):
        self.next = self.table.X if self.next.name == self.table.O.name else self.table.O
        self.winner = self.table.findWinner()
        self.table.showPaths(True)
        self.view.showTable(*self.table.getData())

    @staticmethod
    def generateNewStates(currentState, player):
        onTheMoveReff = currentState.X if player == "X" else currentState.O
        nextReff = currentState.O if player == "X" else currentState.X
        states = {
            'blue wall': frozenset(),
            'green wall': frozenset()
        }
        positions = nextReff.getCurrentPositions()
        if onTheMoveReff.noGreenWalls > 0:
            grow = 0
            while not states['green wall']:
                for pos in positions:
                    for i in range(pos[0] - (Game.r + grow), pos[0] + Game.r + grow):
                        if 0 < i < currentState.n:
                            for j in range(pos[1] - (Game.r + grow), pos[1] + Game.r + grow):
                                if 0 < j < currentState.m and currentState.isCorrectGreenWall((i, j)):
                                    temp = currentState.getCopy()
                                    temp.setGreenWall({
                                        'position': (i, j),
                                        'next': onTheMoveReff.name
                                    })
                                    if not currentState.isConnectedGreenWall((i, j)) or temp.canBothPlayersFinish(True, True):
                                        states['green wall'] |= frozenset({temp})
                grow += 1
        if onTheMoveReff.noBlueWalls > 0:
            grow = 0
            while not states['blue wall']:
                for pos in positions:
                    for i in range(pos[0] - (Game.r + grow), pos[0] + Game.r + grow):
                        if 0 < i < currentState.n:
                            for j in range(pos[1] - (Game.r + grow), pos[1] + Game.r + grow):
                                if 0 < j < currentState.m and currentState.isCorrectBlueWall((i, j)):
                                    temp = currentState.getCopy()
                                    temp.setBlueWall({
                                        'position': (i, j),
                                        'next': onTheMoveReff.name
                                    })
                                    if not currentState.isConnectedBlueWall((i, j)) or temp.canBothPlayersFinish(True, True):
                                        states['blue wall'] |= frozenset({temp})
                grow += 1
        gp = {'name': onTheMoveReff.name}
        positions = onTheMoveReff.getCurrentPositions()
        if gp['name'] == "X":
            if not states['blue wall'] and not states['green wall']:
                currentState.setPathsX()
                for (newPos, choice) in zip(currentState.xPaths, [1, 1, 2, 2]):
                    gp['position'] = newPos[min(1, len(newPos) - 1)]
                    gp['choice'] = choice
                    temp = currentState.getCopy()
                    temp.setGamePiece(dict(gp))
                    yield temp
            else:
                for choice in range(1, 3):
                    gp['choice'] = choice
                    for newPos in currentState.fields[positions[choice - 1]].connectedX:
                        gp['position'] = newPos
                        for gws in states['green wall']:
                            temp = gws.getCopy()
                            temp.setGamePiece(dict(gp))
                            yield temp
                        for bws in states['blue wall']:
                            temp = bws.getCopy()
                            temp.setGamePiece(dict(gp))
                            yield temp
                
        elif gp['name'] == "O":
            if not states['blue wall'] and not states['green wall']:
                currentState.setPathsO()
                for (newPos, choice) in zip(currentState.oPaths, [1, 1, 2, 2]):
                    gp['position'] = newPos[min(1, len(newPos) - 1)]
                    gp['choice'] = choice
                    temp = currentState.getCopy()
                    temp.setGamePiece(dict(gp))
                    yield temp
            else:
                for choice in range(1, 3):
                    gp['choice'] = choice
                    for newPos in currentState.fields[positions[choice - 1]].connectedO:
                        gp['position'] = newPos
                        for gws in states['green wall']:
                            temp = gws.getCopy()
                            temp.setGamePiece(dict(gp))
                            yield temp
                        for bws in states['blue wall']:
                            temp = bws.getCopy()
                            temp.setGamePiece(dict(gp))
                            yield temp
        return

    @staticmethod
    def maxValue(states, depth, player, alpha, beta):
        if depth == 0:
            return (states, Game.evaluateState(states[-1], player))
        else:
            for branchState in Game.generateNewStates(states[-1], player):
                alpha = max(alpha, Game.minValue(states + [branchState], depth - 1, player, alpha, beta), key=lambda x: x[1])
                if alpha[1] >= beta[1]:
                    return beta
        return alpha

    @staticmethod
    def minValue(states, depth, player, alpha, beta):
        if depth == 0:
            return (states, Game.evaluateState(states[-1], player))
        else:
            for branchState in Game.generateNewStates(states[-1], player):
                beta = min(beta, Game.maxValue(states + [branchState], depth - 1, player, alpha, beta), key=lambda x: x[1])
                if beta[1] <= alpha[1]:
                    return alpha
        return beta

    @staticmethod
    def minmax(state, depth, player, alpha, beta):
        value = Game.maxValue([state], depth, player.name, alpha, beta)
        return value[0]

    @staticmethod
    def evaluateState(state, player):
        if state.findWinner():
            return Game.oo - 1
        else:
            if state.canBothPlayersFinish(True, True):
                xMinPath = len(min(state.xPaths, key=lambda x: len(x)))
                oMinPath = len(min(state.oPaths, key=lambda x: len(x)))
                if player == "X":
                    return oMinPath + 1 / xMinPath
                else:
                    return xMinPath + 1 / oMinPath
            else:
                return -Game.oo + 1

    def validateMove(self, move):
        validGamePiece = self.validateGamePieceMove(move['game piece'])
        validWall = self.validateWall(move['wall'])
        return validGamePiece | validWall | {'errors': validGamePiece['errors'] + validWall['errors']}

    def validateGamePieceMove(self, move):
        ret = {'errors': ""}
        if self.next.name != move['name']:
            ret['errors'] += "Not your turn!\n"
        if 1 > move['position'][0] > self.table.n:
            ret['errors'] += "Row index out of bounds!\n"
        if 1 > move['position'][1] > self.table.m:
            ret['errors'] += "Column index out of bounds!\n"
        if move['position'] in self.next.getCurrentPositions():
            ret['errors'] += "You're already on that position!\n"
        if not self.table.areConnected(
                self.next.getCurrentPositions()[move['choice'] - 1],
                move['position'],
                move['name']):
            ret['errors'] += "Can't move there!\n"
        if not ret['errors']:
            ret['game piece'] = move
        return ret

    def validateWall(self, wall):
        ret = {'errors': ""}
        if not wall:
            if sum(self.next.getWallNumber()) > 0:
                ret['errors'] = "You must put up a wall!\n"
        else:
            wall |= {'next': self.next.name}
            if wall['type'] == 'B':
                ret |= self.validateBlueWall(wall)
            elif wall['type'] == 'G':
                ret |= self.validateGreenWall(wall)
        return ret

    def validateBlueWall(self, wall):
        ret = {'errors': ""}
        if self.next.getWallNumber()[0] < 1:
            ret['errors'] += "No blue walls left!\n"
        if 1 > wall['position'][0] > self.table.n - 1:
            ret['errors'] += "Row index out of bounds!\n"
        if 1 > wall['position'][1] > self.table.m - 1:
            ret['errors'] += "Column index out of bounds!\n"
        if not self.table.isCorrectBlueWall(wall['position']):
            ret['errors'] += "Can't put a blue wall on the given position!\n"
        if not ret['errors']:
            if not self.table.isConnectedBlueWall(wall['position']):
                ret['blue wall'] = wall
            else:
                temp = self.table.getCopy()
                temp.setBlueWall(wall)
                if temp.canBothPlayersFinish(True, True):
                    ret['virtual'] = temp
                else:
                    if not temp.canPlayerXFinish():
                        ret['errors'] += "Player X can't finish!\n"
                    if not temp.canPlayerOFinish():
                        ret['errors'] += "Player O can't finish!\n"
        return ret

    def validateGreenWall(self, wall):
        ret = {'errors': ""}
        if self.next.getWallNumber()[1] < 1:
            ret['errors'] += "No green walls left!\n"
        if 1 > wall['position'][0] > self.table.n - 1:
            ret['errors'] += "Row index out of bounds!\n"
        if 1 > wall['position'][1] > self.table.m - 1:
            ret['errors'] += "Column index out of bounds!\n"
        if not self.table.isCorrectGreenWall(wall['position']):
            ret['errors'] += "Can't put a green wall on the given position!\n"
        if not ret['errors']:
            if not self.table.isConnectedGreenWall(wall['position']):
                ret['green wall'] = wall
            else:
                temp = self.table.getCopy()
                temp.setGreenWall(wall)
                if temp.canBothPlayersFinish(True, True):
                    ret['virtual'] = temp
                else:
                    if not temp.canPlayerXFinish():
                        ret['errors'] += "Player X can't finish!\n"
                    if not temp.canPlayerOFinish():
                        ret['errors'] += "Player O can't finish!\n"
        return ret

    @staticmethod
    def parseMove(stream):
        ret = {
            'errors': "",
            'wall': {},
            'game piece': {}
        }
        m = stream.replace('[', '').replace(']', '').upper().split(' ')
        if len(m) < 1 or m[0]not in ['X', 'O']:
            ret['errors'] += "Invalid player choice!\n"
        if len(m) < 2 or m[1] not in ['1', '2']:
            ret['errors'] += "Invalid piece identificator!\n"
        if len(m) < 4:
            ret['errors'] += "Missing the new position for the game piece!\n"
        if not ret['errors']:
            try:
                ret['game piece'] = {
                    'name': m[0],
                    'choice': int(m[1]),
                    'position': tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[2:4]])
                }
            except Exception as e:
                ret['errors'] += "Incorrect game piece possitional coordinates!\n"
        if len(m) > 4:
            wErr = ""
            if m[4] not in ['B', 'G']:
                wErr += "Invalid wall identificator!\n"
            if len(m) < 7:
                wErr += "Missing the new position for the wall!\n"
            if not wErr:
                try:
                    ret['wall'] = {
                        'type': m[4],
                        'position': tuple([ord(x)-55 if x >= 'A' else ord(x)-48 for x in m[5:7]])
                    }
                except Exception as e:
                    wErr += "Incorrect wall possitional coordinates!\n"
            ret['errors'] += wErr
        return ret


def main():
    n = m = ""
    while not str.isdigit(n) or int(n) < 5 or int(n) > 22:
        n = input("Input the number of rows in the table in range [5-22] (Empty for the recommended value of 11): ")
        n = n if n else "11"
    n = int(n)
    while not str.isdigit(m) or int(m) < 5 or int(m) > 28:
        m = input("Input the number of columns in the table in range [5-22] (Empty for the recommended value of 14): ")
        m = m if m else "14"
    m = int(m)
    initial = {}
    while len(initial.keys()) < 2:
        temp = input(f"Input {len(initial)+1}. initial position for X (Empty for the recommended value of ({4 if len(initial) == 0 else 8}, 4)): ")
        temp = temp if temp else f"({4 if len(initial) == 0 else 8}, 4)"
        temp = tuple(map(lambda x: int(x) if str.isdigit(x) else 0, temp.replace("(", "")
                                                .replace(")", "")
                                                .replace(",", "")
                                                .split(" ")))
        if len(temp) == 2 and 0 < temp[0] < n and 0 <  temp[1] < m and not initial.get(temp, None):
            initial[temp] = f"X{len(initial)+1}"
    while len(initial.keys()) < 4:
        temp = input(f"Input {len(initial)-1}. initial position for O (Empty for the recommended value of ({4 if len(initial)-1 == 1 else 8}, 11)): ")
        temp = temp if temp else f"({4 if len(initial)-1 == 1 else 8}, 11)"
        temp = tuple(map(lambda x: int(x) if str.isdigit(x) else 0, temp.replace("(", "")
                                                .replace(")", "")
                                                .replace(",", "")
                                                .split(" ")))
        if len(temp) == 2 and 0 < temp[0] < n and 0 <  temp[1] < m and not initial.get(temp, None):
            initial[temp] = f"O{len(initial)-1}"
    wallNumb = ""
    while not str.isdigit(wallNumb) or int(wallNumb) < 0 or int(wallNumb) > (n*m)//8 - 1:
        wallNumb = input(f"Input the number of blue/green walls each player has [0-{(n*m)//8 - 1}] (Empty for the recommended value of 9): ")
        wallNumb = wallNumb if wallNumb else "9"

    g = Game(n, m)
    g.start(initial | {'wallNumber': int(wallNumb)})


if __name__ == "__main__":
    main()
