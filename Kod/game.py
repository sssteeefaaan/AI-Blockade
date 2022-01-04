from view import View
from table import Table
from sys import setrecursionlimit
from time import monotonic_ns

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
            if self.next.isComputer:
                self.table = Game.minimax(self.table, 1, self.next, ([self.table], -50), ([self.table], 50))
                self.next = self.table.X if self.next.name == self.table.O.name else self.table.O
                self.winner = self.table.findWinner()
                self.table.showPaths(True)
                self.view.showTable(*self.table.getData())
            else:
                parsedMove = Game.parseMove(input(f"{self.next.name} is on the move!\n"))
                if not parsedMove['errors']:
                    move = self.validateMove(parsedMove)
                    if not move['errors']:
                        if move.get('virtual', None):
                            self.table = move['virtual']
                        self.table.playMove(move)
                        self.next = self.table.X if self.next.name == self.table.O.name else self.table.O
                        self.winner = self.table.findWinner()
                        self.table.showPaths(True)
                        self.view.showTable(*self.table.getData())
                    else:
                        print(move['errors'])
                else:
                    print(parsedMove['errors'])
        print(f"{self.winner.name} won! Congrats!")

    @staticmethod
    def genNewStates(currentState, player):
        print(f"Generating new states for player {player}... please be patient...")
        currTime = monotonic_ns()
        playerReff = currentState.X if player == "X" else currentState.O
        states = {
            'blue wall': list(),
            'green wall': list(),
            'new': list()
        }
        if playerReff.noBlueWalls > 0:
            for i in range(1, currentState.n):
                for j in range(1, currentState.m):
                    if currentState.isCorrectBlueWall((i, j)):
                        temp = currentState.getCopy()
                        temp.setBlueWall({
                            'position': (i, j),
                            'next': playerReff.name
                        })
                        if not currentState.isConnectedBlueWall((i, j)) or temp.canBothPlayersFinish(True, True):
                            states['blue wall'].append(temp)
        if playerReff.noGreenWalls > 0:
            for i in range(1, currentState.n):
                for j in range(1, currentState.m):
                    if currentState.isCorrectGreenWall((i, j)):
                        temp = currentState.getCopy()
                        temp.setGreenWall({
                            'position': (i, j),
                            'next': playerReff.name
                        })
                        if not currentState.isConnectedGreenWall((i, j)) or temp.canBothPlayersFinish(True, True):
                            states['green wall'].append(temp)
        gp = {'name': playerReff.name}
        if gp['name'] == "X":
            positions = playerReff.getCurrectPositions()
            for choice in range(1, 3):
                gp['choice'] = choice
                if not states['blue wall'] and not states['green wall']:
                    for newPos in currentState.fields[positions[choice - 1]].connectedX:
                        gp['position'] = newPos
                        temp = currentState.getCopy()
                        temp.setGamePiece(dict(gp))
                        if temp.canBothPlayersFinish(True, True):
                            states['new'].append(temp)
                else:
                    for newPos in currentState.fields[positions[choice - 1]].connectedX:
                        gp['position'] = newPos
                        for bws in states['blue wall']:
                            temp = bws.getCopy()
                            temp.setGamePiece(dict(gp))
                            # if temp.canBothPlayersFinish(True, True):
                            states['new'].append(temp)
                        for gws in states['green wall']:
                            temp = gws.getCopy()
                            temp.setGamePiece(dict(gp))
                            # if temp.canBothPlayersFinish(True, True):
                            states['new'].append(temp)
        elif gp['name'] == "O":
            positions = playerReff.getCurrectPositions()
            for choice in range(1, 3):
                gp['choice'] = choice
                if not states['blue wall'] and not states['green wall']:
                    for newPos in currentState.fields[positions[choice - 1]].connectedO:
                        gp['position'] = newPos
                        temp = currentState.getCopy()
                        temp.setGamePiece(dict(gp))
                        # if temp.canBothPlayersFinish(True, True):
                        states['new'].append(temp)
                else:
                    for newPos in currentState.fields[positions[choice - 1]].connectedO:
                        gp['position'] = newPos
                        for bws in states['blue wall']:
                            temp = bws.getCopy()
                            temp.setGamePiece(dict(gp))
                            # if temp.canBothPlayersFinish(True, True):
                            states['new'].append(temp)
                        for gws in states['green wall']:
                            temp = gws.getCopy()
                            temp.setGamePiece(dict(gp))
                            # if temp.canBothPlayersFinish(True, True):
                            states['new'].append(temp)
        print(f"Generated {len(states['new'])} for {monotonic_ns() - currTime}ns!")
        return states['new']

    @staticmethod
    def maxValue(states, depth, player, alpha, beta):
        if depth == 0:
            return (states, Game.evaluateState(states[-1], player))
        else:
            for branchState in Game.genNewStates(states[-1], player):
                alpha = max(alpha, Game.minValue(states + [branchState], depth - 1, "X" if player ==
                            "O" else "O", alpha, beta), key=lambda x: x[1])
                if alpha[1] >= beta[1]:
                    return beta
        return alpha

    @staticmethod
    def minValue(states, depth, player, alpha, beta):
        if depth == 0:
            return (states, Game.evaluateState(states[-1], player))
        else:
            for branchState in Game.genNewStates(states[-1], player):
                beta = min(beta, Game.maxValue(states + [branchState], depth - 1, "X" if player ==
                           "O" else "O", alpha, beta), key=lambda x: x[1])
                if beta[1] <= alpha[1]:
                    return alpha
        return beta

    @staticmethod
    def minimax(state, depth, player, alpha, beta):
        return Game.maxValue([state], depth, player.name, alpha, beta)[0][1]

    @staticmethod
    def evaluateState(state, player):
        winner = state.findWinner()
        if winner:
            if winner.name == player:
                return -49
                # Vraca [beginingState] ukoliko je manje ili jednako alpha (-50)
            else:
                return 49
                # Vraca [beginingState] ukoliko je vece ili jednako beta (50)
        else:
            if state.canBothPlayersFinish(True, True):
                xMin = min(map(lambda x: len(x), state.xPaths))
                oMin = min(map(lambda x: len(x), state.oPaths))
                if player == "X":
                    return xMin - oMin
                else:
                    return oMin - xMin
            else:
                # Invalid state!!!! Should never be played/generated
                return -49

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
        if move['position'] in self.next.getCurrectPositions():
            ret['errors'] += "You're already on that position!\n"
        if not self.table.areConnected(
                self.next.getCurrectPositions()[move['choice'] - 1],
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
