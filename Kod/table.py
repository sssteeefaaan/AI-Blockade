from player import Player
from field import Field


class Table:
    def __init__(self, n=11, m=14, blueWalls=set(), greenWalls=set(), X=None, O=None, xPaths=[None]*4, oPaths=[None]*4):
        self.n = n
        self.m = m
        self.blueWalls = set(blueWalls)
        self.greenWalls = set(greenWalls)
        self.fields = dict()
        self.X = X.getCopy() if X else None
        self.O = O.getCopy() if O else None
        self.xPaths = list(xPaths)
        self.oPaths = list(oPaths)

    def getCopy(self):
        copy = Table(self.n, self.m, self.blueWalls,
                     self.greenWalls, self.X, self.O, self.xPaths, self.oPaths)
        for key in self.fields.keys():
            copy.fields[key] = self.fields[key].getCopy(copy)
        return copy

    def getData(self):
        return (self.greenWalls, self.blueWalls, {"X": self.X.getCurrectPositions(), "O": self.O.getCurrectPositions()}, self.X.getWallNumber(), self.O.getWallNumber())

    def onInit(self, initial, players):
        self.setPlayers(players)
        self.setFields(initial)
        self.setPaths()

    def setPlayers(self, players):
        for player in players.keys():
            if player == "X":
                self.X = Player("X", *players[player])
            elif player == "O":
                self.O = Player("O", *players[player])

    def setFields(self, initial):
        connectInitialX = list()
        connectInitialO = list()
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                pos = (i, j)
                connected = set(Table.createManhattan(
                    pos, 1, self.n, self.m, 2))
                self.fields[pos] = Field(self, pos, initial.get(
                    pos, None), connected, connected)
                match initial.get(pos, None):
                    case "X1" | "X2":
                        manGen = list(map(lambda x: ((pos[0] - x[0], pos[1] - x[1]), x),
                                      Table.createManhattanGeneric(pos, 1, self.n, self.m, 1)))
                        connectInitialO += list(
                            filter(
                                lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <= self.n and 0 < x[0][1] <=
                                self.m and 0 < x[0][1] + x[1][1] <= self.m, manGen))
                    case "O1" | "O2":
                        manGen = list(map(lambda x: ((pos[0] - x[0], pos[1] - x[1]), x),
                                      Table.createManhattanGeneric(pos, 1, self.n, self.m, 1)))
                        connectInitialX += list(
                            filter(
                                lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <= self.n and 0 < x[0][1] <=
                                self.m and 0 < x[0][1] + x[1][1] <= self.m, manGen))
        for k in initial.keys():
            self.setGamePiece({
                'previous position': (-100, -100),
                'position': k,
                'name': initial[k][0],
                'choice': int(initial[k][1])
            })
        self.connectO(connectInitialO, False)
        self.connectX(connectInitialX, False)

    def setPaths(self):
        self.setPathsX()
        self.setPathsO()

    def setPathsX(self):
        self.xPaths = self.findPathsX(self.X.getCurrectPositions(), self.O.getInitialPositions())

    def setPathsO(self):
        self.oPaths = self.findPathsO(self.O.getCurrectPositions(), self.X.getInitialPositions())

    def checkState(self):
        if self.O.isWinner(self.X.getInitialPositions()):
            self.winner = self.O
        elif self.X.isWinner(self.O.getInitialPositions()):
            self.winner = self.X

    def setBlueWall(self, wall):
        if wall['next'] == 'X':
            self.X.noBlueWalls -= 1
        else:
            self.O.noBlueWalls -= 1
        pos = wall['position']

        self.blueWalls.add(pos)
        forDisconnect = []
        up1 = (pos[0] - 1) > 0
        down1 = (pos[0] + 1) <= self.n
        down2 = (pos[0] + 2) <= self.n
        left1 = (pos[1] - 1) > 0
        right1 = (pos[1] + 1) <= self.m
        right2 = (pos[1] + 2) <= self.m

        if down1:
            forDisconnect += [(pos, (1, 0))]
            if right1:
                forDisconnect += [(pos, (1, 1))]
                forDisconnect += [((pos[0], pos[1] + 1), (1, -1)),
                                  ((pos[0], pos[1] + 1), (1, 0))]
                if down2:
                    forDisconnect += [((pos[0], pos[1] + 1), (2, 0))]
                if up1:
                    forDisconnect += [((pos[0] + 1, pos[1] + 1), (-2, 0))]
            if up1:
                forDisconnect += [((pos[0] + 1, pos[1]), (-2, 0))]
            if down2:
                forDisconnect += [(pos, (2, 0))]
            if left1 and (
                (pos[0],
                 pos[1] - 2) in self.blueWalls or (pos[0] - 1, pos[1] - 1) in self.greenWalls
                    or (pos[0] + 1, pos[1] - 1) in self.greenWalls):
                forDisconnect += [(pos, (1, -1)),
                                  ((pos[0]+1, pos[1]), (-1, -1))]
            if right2 and (
                (pos[0],
                 pos[1] + 2) in self.blueWalls or (pos[0] - 1, pos[1] + 1) in self.greenWalls
                    or (pos[0] + 1, pos[1] + 1) in self.greenWalls):
                forDisconnect += [((pos[0], pos[1]+1), (1, 1)),
                                  ((pos[0]+1, pos[1]+1), (-1, 1))]

        self.disconnect(forDisconnect, "B")

    def setGreenWall(self, wall):
        if wall['next'] == 'X':
            self.X.noGreenWalls -= 1
        else:
            self.O.noGreenWalls -= 1
        pos = wall['position']

        self.greenWalls.add(pos)
        forDisconnect = []
        up1 = (pos[0] - 1) > 0
        down1 = (pos[0] + 1) <= self.n
        down2 = (pos[0] + 2) <= self.n
        left1 = (pos[1] - 1) > 0
        right1 = (pos[1] + 1) <= self.m
        right2 = (pos[1] + 2) <= self.m

        if right1:
            forDisconnect += [(pos, (0, 1))]
            if down1:
                forDisconnect += [(pos, (1, 1))]
                forDisconnect += [((pos[0] + 1, pos[1]), (-1, 1)),
                                  ((pos[0] + 1, pos[1]), (0, 1))]
                if left1:
                    forDisconnect += [((pos[0] + 1, pos[1] + 1), (0, -2))]
                if down2 and ((pos[0] + 2, pos[1]) in self.greenWalls
                              or (pos[0] + 1, pos[1] - 1) in self.blueWalls or (pos[0] + 1, pos[1] + 1) in self.blueWalls):
                    forDisconnect += [((pos[0]+1, pos[1]), (1, 1)),
                                      ((pos[0] + 1, pos[1] + 1), (1, -1))]
            if up1 and (
                (pos[0] - 2, pos[1]) in self.greenWalls or (pos[0] - 1, pos[1] - 1) in self.blueWalls
                    or (pos[0] - 1, pos[1] + 1) in self.blueWalls):
                forDisconnect += [(pos, (-1, 1)),
                                  ((pos[0], pos[1] + 1), (-1, -1))]
            if left1:
                forDisconnect += [((pos[0], pos[1] + 1), (0, -2))]
        if right2:
            forDisconnect += [(pos, (0, 2))]
            if down1:
                forDisconnect += [((pos[0] + 1, pos[1]), (0, 2))]
        self.disconnect(forDisconnect, "G")

    def setGamePiece(self, gamePiece):
        gamePiece['previous position'] = self.X.movePiece(
            gamePiece) if gamePiece['name'] == "X" else self.O.movePiece(gamePiece)

        forConnect = list(
            map(
                lambda x: ((gamePiece['position'][0] - x[0] * 2, gamePiece['position'][1] - x[1] * 2),
                           x),
                Table.createManhattanGeneric(gamePiece['position'],
                                             1, self.n, self.m, 1)))
        forConnect = list(
            filter(
                lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <= self.n and 0 < x[0][1] <= self.m and 0 <
                x[0][1] + x[1][1] <= self.m, forConnect))
        forPrevConnect = list(map(lambda x: ((gamePiece['previous position'][0] - x[0] * 2, gamePiece['previous position'][
                              1] - x[1] * 2), x), Table.createManhattanGeneric(gamePiece['previous position'], 1, self.n, self.m, 1)))
        forPrevConnect = list(
            filter(
                lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <= self.n and 0 < x[0][1] <= self.m and 0 <
                x[0][1] + x[1][1] <= self.m, forPrevConnect))
        forDisconnect = Table.createManhattanGeneric(gamePiece['position'], 1, self.n, self.m, 2)
        forDisconnect = list(zip([gamePiece['position']]*len(forDisconnect), forDisconnect))
        forPrevDisconnect = Table.createManhattanGeneric(gamePiece['previous position'], 1, self.n, self.m, 2)
        forPrevDisconnect = list(zip([gamePiece['previous position']]*len(forPrevDisconnect), forPrevDisconnect))
        if gamePiece['name'] == "X":
            self.disconnectO(forDisconnect + forPrevConnect)
            self.connectO(forConnect, False, gamePiece['position'])
            self.connectO(forPrevDisconnect)
        else:
            self.disconnectX(forDisconnect + forPrevConnect)
            self.connectX(forConnect, False, gamePiece['position'])
            self.connectX(forPrevDisconnect)

    def connect(self, vals):
        for (x, y) in vals:
            self.fields[x].connect(self.fields[(x[0] + y[0], x[1] + y[1])])

    def connectX(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if x
                   in self.fields[position].connectedO]
            for (x, y) in con:
                self.fields[x].connectX(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
        else:
            for (x, y) in vals:
                self.fields[x].connectX(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)

    def connectO(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if x
                   in self.fields[position].connectedX]
            for (x, y) in con:
                self.fields[x].connectO(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
        else:
            for (x, y) in vals:
                self.fields[x].connectO(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)

    def disconnect(self, vals, w=None):
        for (x, y) in vals:
            self.fields[x].disconnect(
                self.fields[(x[0] + y[0], x[1] + y[1])], w)

    def disconnectX(self, vals):
        for (x, y) in vals:
            self.fields[x].disconnectX(
                self.fields[(x[0] + y[0], x[1] + y[1])])

    def disconnectO(self, vals):
        for (x, y) in vals:
            self.fields[x].disconnectO(
                self.fields[(x[0] + y[0], x[1] + y[1])])

    def areConnected(self, currentPos, followedPos, name="X"):
        if name == "X":
            return followedPos in self.fields[currentPos].connectedX
        else:
            return followedPos in self.fields[currentPos].connectedO

    def isCorrectBlueWall(self, pos):
        return not(
            pos in self.greenWalls or
            [x for x in [(pos[0],
                          pos[1] - 1),
                         pos, (pos[0],
                               pos[1] + 1)] if x in self.blueWalls])

    def isCorrectGreenWall(self, pos):
        return not(
            pos in self.blueWalls or
            [x for x in [(pos[0] - 1, pos[1]),
                         pos, (pos[0] + 1, pos[1])] if x in self.greenWalls])

    def isConnectedBlueWall(self, pos):
        return ((pos[0], pos[1] - 2) in self.blueWalls or
                (pos[0], pos[1] + 2) in self.blueWalls or
                [(pos[0] + x, pos[1] + y)
                 for x in range(-1, 2)
                 for y in range(-1, 2)
                 if (pos[0] + x, pos[1] + y) in self.greenWalls])

    def isConnectedGreenWall(self, pos):
        return ((pos[0] - 2, pos[1]) in self.greenWalls or
                (pos[0] + 2, pos[1]) in self.greenWalls or
                [(pos[0] + x, pos[1] + y)
                 for x in range(-1, 2)
                 for y in range(-1, 2)
                 if (pos[0] + x, pos[1] + y) in self.blueWalls])

    def canBothPlayersFinish(self, updateX=False, updateO=False):
        return self.canPlayerXFinish(updateX) and self.canPlayerOFinish(updateO)

    def canPlayerXFinish(self, update=False):
        if update:
            self.setPathsX()
        return None not in self.xPaths

    def canPlayerOFinish(self, update=False):
        if update:
            self.setPathsO()
        return None not in self.oPaths

    def findPathsX(self, xPos, endPos):
        paths = [False] * 4
        queue = {
            'first game piece': {
                'heads': {
                    xPos[0]: 0
                },
                'processing': [[xPos[0]]],
                'partial paths': [[xPos[0]]]
            },
            'second game piece': {
                'heads': {
                    xPos[1]: 0
                },
                'processing': [[xPos[1]]],
                'partial paths': [[xPos[1]]]
            },
            'first initial': {
                'tails': {
                    endPos[0]: 0
                },
                'processing': [[endPos[0]]],
                'partial paths': [[endPos[0]]]
            },
            'second initial': {
                'tails': {
                    endPos[1]: 0
                },
                'processing': [[endPos[1]]],
                'partial paths': [[endPos[1]]]
            }
        }
        while None not in paths and False in paths:
            if queue['first game piece']['processing']:
                current, *queue['first game piece']['processing'] = queue['first game piece']['processing']
                for n in self.fields[current[-1]].connectedX:
                    if not paths[0]:
                        ind = queue['first initial']['tails'].get(n, None)
                        if ind != None:
                            paths[0] = current + queue['first initial']['partial paths'][ind]
                            if paths[1]:
                                queue['first game piece']['processing'].clear()
                    if not paths[1]:
                        ind = queue['second initial']['tails'].get(n, None)
                        if ind != None:
                            paths[1] = current + queue['second initial']['partial paths'][ind]
                            if paths[0]:
                                queue['first game piece']['processing'].clear()
                    if not queue['first game piece']['heads'].get(n, None):
                        queue['first game piece']['heads'][n] = len(queue['first game piece']['partial paths'])
                        queue['first game piece']['partial paths'] += [current + [n]]
                        queue['first game piece']['processing'] += [current + [n]]
            else:
                if not paths[0]:
                    paths[0] = None
                if not paths[1]:
                    paths[1] = None
            if queue['second game piece']['processing']:
                current, *queue['second game piece']['processing'] = queue['second game piece']['processing']
                for n in self.fields[current[-1]].connectedX:
                    if not paths[2]:
                        ind = queue['first initial']['tails'].get(n, None)
                        if ind != None:
                            paths[2] = current + queue['first initial']['partial paths'][ind]
                            if paths[3]:
                                queue['second game piece']['processing'].clear()
                    if not paths[3]:
                        ind = queue['second initial']['tails'].get(n, None)
                        if ind != None:
                            paths[3] = current + queue['second initial']['partial paths'][ind]
                            if paths[2]:
                                queue['second game piece']['processing'].clear()
                    if not queue['second game piece']['heads'].get(n, None):
                        queue['second game piece']['heads'][n] = len(queue['second game piece']['partial paths'])
                        queue['second game piece']['partial paths'] += [current + [n]]
                        queue['second game piece']['processing'] += [current + [n]]
            else:
                if not paths[2]:
                    paths[2] = None
                if not paths[3]:
                    paths[3] = None
            if queue['first initial']['processing']:
                current, *queue['first initial']['processing'] = queue['first initial']['processing']
                for n in self.fields[current[0]].connectedX | self.fields[current[0]].oneWayConnectedX:
                    if current[0] in self.fields[n].connectedX:
                        if not paths[0]:
                            ind = queue['first game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[0] = queue['first game piece']['partial paths'][ind] + current
                                if paths[2]:
                                    queue['first initial']['processing'].clear()
                        if not paths[2]:
                            ind = queue['second game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[2] = queue['second game piece']['partial paths'][ind] + current
                                if paths[0]:
                                    queue['first initial']['processing'].clear()
                        if not queue['first initial']['tails'].get(n, None):
                            queue['first initial']['tails'][n] = len(queue['first initial']['partial paths'])
                            queue['first initial']['partial paths'] += [[n] + current]
                            queue['first initial']['processing'] += [[n] + current]
            else:
                if not paths[0]:
                    paths[0] = None
                if not paths[2]:
                    paths[2] = None
            if queue['second initial']['processing']:
                current, *queue['second initial']['processing'] = queue['second initial']['processing']
                for n in self.fields[current[0]].connectedX | self.fields[current[0]].oneWayConnectedX:
                    if current[0] in self.fields[n].connectedX:
                        if not paths[1]:
                            ind = queue['first game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[1] = queue['first game piece']['partial paths'][ind] + current
                                if paths[3]:
                                    queue['second initial']['processing'].clear()
                        if not paths[3]:
                            ind = queue['second game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[3] = queue['second game piece']['partial paths'][ind] + current
                                if paths[1]:
                                    queue['second initial']['processing'].clear()
                        if not queue['second initial']['tails'].get(n, None):
                            queue['second initial']['tails'][n] = len(queue['second initial']['partial paths'])
                            queue['second initial']['partial paths'] += [[n] + current]
                            queue['second initial']['processing'] += [[n] + current]
            else:
                if not paths[1]:
                    paths[1] = None
                if not paths[3]:
                    paths[3] = None
        return paths

    def findPathsO(self, oPos, endPos):
        paths = [False] * 4
        queue = {
            'first game piece': {
                'heads': {
                    oPos[0]: 0
                },
                'processing': [[oPos[0]]],
                'partial paths': [[oPos[0]]]
            },
            'second game piece': {
                'heads': {
                    oPos[1]: 0
                },
                'processing': [[oPos[1]]],
                'partial paths': [[oPos[1]]]
            },
            'first initial': {
                'tails': {
                    endPos[0]: 0
                },
                'processing': [[endPos[0]]],
                'partial paths': [[endPos[0]]]
            },
            'second initial': {
                'tails': {
                    endPos[1]: 0
                },
                'processing': [[endPos[1]]],
                'partial paths': [[endPos[1]]]
            }
        }
        while None not in paths and False in paths:
            if queue['first game piece']['processing']:
                current, *queue['first game piece']['processing'] = queue['first game piece']['processing']
                for n in self.fields[current[-1]].connectedO:
                    if not paths[0]:
                        ind = queue['first initial']['tails'].get(n, None)
                        if ind != None:
                            paths[0] = current + queue['first initial']['partial paths'][ind]
                            if paths[1]:
                                queue['first game piece']['processing'].clear()
                    if not paths[1]:
                        ind = queue['second initial']['tails'].get(n, None)
                        if ind != None:
                            paths[1] = current + queue['second initial']['partial paths'][ind]
                            if paths[0]:
                                queue['first game piece']['processing'].clear()
                    if not queue['first game piece']['heads'].get(n, None):
                        queue['first game piece']['heads'][n] = len(queue['first game piece']['partial paths'])
                        queue['first game piece']['partial paths'] += [current + [n]]
                        queue['first game piece']['processing'] += [current + [n]]
            else:
                if not paths[0]:
                    paths[0] = None
                if not paths[1]:
                    paths[1] = None
            if queue['second game piece']['processing']:
                current, *queue['second game piece']['processing'] = queue['second game piece']['processing']
                for n in self.fields[current[-1]].connectedO:
                    if not paths[2]:
                        ind = queue['first initial']['tails'].get(n, None)
                        if ind != None:
                            paths[2] = current + queue['first initial']['partial paths'][ind]
                            if paths[3]:
                                queue['second game piece']['processing'].clear()
                    if not paths[3]:
                        ind = queue['second initial']['tails'].get(n, None)
                        if ind != None:
                            paths[3] = current + queue['second initial']['partial paths'][ind]
                            if paths[2]:
                                queue['second game piece']['processing'].clear()
                    if not queue['second game piece']['heads'].get(n, None):
                        queue['second game piece']['heads'][n] = len(queue['second game piece']['partial paths'])
                        queue['second game piece']['partial paths'] += [current + [n]]
                        queue['second game piece']['processing'] += [current + [n]]
            else:
                if not paths[2]:
                    paths[2] = None
                if not paths[3]:
                    paths[3] = None
            if queue['first initial']['processing']:
                current, *queue['first initial']['processing'] = queue['first initial']['processing']
                for n in self.fields[current[0]].connectedO | self.fields[current[0]].oneWayConnectedO:
                    if current[0] in self.fields[n].connectedO:
                        if not paths[0]:
                            ind = queue['first game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[0] = queue['first game piece']['partial paths'][ind] + current
                                if paths[2]:
                                    queue['first initial']['processing'].clear()
                        if not paths[2]:
                            ind = queue['second game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[2] = queue['second game piece']['partial paths'][ind] + current
                                if paths[0]:
                                    queue['first initial']['processing'].clear()
                        if not queue['first initial']['tails'].get(n, None):
                            queue['first initial']['tails'][n] = len(queue['first initial']['partial paths'])
                            queue['first initial']['partial paths'] += [[n] + current]
                            queue['first initial']['processing'] += [[n] + current]
            else:
                if not paths[0]:
                    paths[0] = None
                if not paths[2]:
                    paths[2] = None
            if queue['second initial']['processing']:
                current, *queue['second initial']['processing'] = queue['second initial']['processing']
                for n in self.fields[current[0]].connectedO | self.fields[current[0]].oneWayConnectedO:
                    if current[0] in self.fields[n].connectedO:
                        if not paths[1]:
                            ind = queue['first game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[1] = queue['first game piece']['partial paths'][ind] + current
                                if paths[3]:
                                    queue['second initial']['processing'].clear()
                        if not paths[3]:
                            ind = queue['second game piece']['heads'].get(n, None)
                            if ind != None:
                                paths[3] = queue['second game piece']['partial paths'][ind] + current
                                if paths[1]:
                                    queue['second initial']['processing'].clear()
                        if not queue['second initial']['tails'].get(n, None):
                            queue['second initial']['tails'][n] = len(queue['second initial']['partial paths'])
                            queue['second initial']['partial paths'] += [[n] + current]
                            queue['second initial']['processing'] += [[n] + current]
            else:
                if not paths[1]:
                    paths[1] = None
                if not paths[3]:
                    paths[3] = None
        return paths

    def showPaths(self, refresh=True):
        if refresh:
            self.setPaths()
        print("Shortest paths:")
        print("\tX1 => O1", self.xPaths[0])
        print("\tX1 => O2", self.xPaths[1])
        print("\tX2 => O1", self.xPaths[2])
        print("\tX2 => O2", self.xPaths[3])
        print("\tO1 => X1", self.oPaths[0])
        print("\tO1 => X2", self.oPaths[1])
        print("\tO2 => X1", self.oPaths[2])
        print("\tO2 => X2", self.oPaths[3])

    @ staticmethod
    def createManhattan(currentPos, low, highN, highM, dStep):
        return list(map(lambda x: (currentPos[0] + x[0], currentPos[1] + x[1]),
                        Table.createManhattanGeneric(currentPos, low, highN, highM, dStep)))

    @ staticmethod
    def createManhattanGeneric(currentPos, low, highN, highM, dStep=2):
        return [(x, y) for x in range(-dStep, dStep+1) for y in range(-dStep, dStep+1) if low <= (currentPos[0] +
                x) <= highN and low <= (currentPos[1] + y) <= highM and Table.isManhattan((0, 0), (x, y), dStep)]

    @ staticmethod
    def isManhattan(currentPos, followedPos, dStep):
        return abs(currentPos[0] - followedPos[0]) + abs(currentPos[1] - followedPos[1]) == dStep
