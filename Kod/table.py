from player import Player
from field import Field


class Table:
    def __init__(self, n=11, m=14, blueWalls=frozenset(), greenWalls=frozenset(), X=None, O=None):
        self.n = n
        self.m = m
        self.blueWalls = frozenset(blueWalls)
        self.greenWalls = frozenset(greenWalls)
        self.fields = dict()
        self.X = X.getCopy() if X else None
        self.O = O.getCopy() if O else None

    def getCopy(self):
        copy = Table(self.n, self.m, self.blueWalls,
                     self.greenWalls, self.X, self.O)
        for key in self.fields.keys():
            copy.fields[key] = self.fields[key].getCopy(copy)
        return copy

    def getData(self):
        return (self.greenWalls, self.blueWalls, {"X": self.X.getCurrectPositions(), "O": self.O.getCurrectPositions()}, self.X.getWallNumber(), self.O.getWallNumber())

    def onInit(self, initial, players):
        self.setPlayers(players)
        self.setFields(initial)

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
            self.setGamePiece((-100, -100), (k[0], k[1]), initial.get(k)[0])
        self.connectO(connectInitialO, False)
        self.connectX(connectInitialX, False)

    def checkState(self):

        if self.O.isWinner((self.X.firstGP.home, self.X.secondGP.home)):
            self.winner = self.O
        elif self.X.isWinner((self.O.firstGP.home, self.O.secondGP.home)):
            self.winner = self.X

    def setBlueWall(self, pos):
        self.blueWalls |= frozenset({pos})
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

        self.disconnect(forDisconnect, "P")

    def setGreenWall(self, pos):
        self.greenWalls |= frozenset({pos})
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
        self.disconnect(forDisconnect, "Z")

    def setGamePiece(self, prevPos, position, name="X"):
        forConnect = list(map(lambda x: ((position[0] - x[0] * 2, position[1] - x[1] * 2),
                          x), Table.createManhattanGeneric(position, 1, self.n, self.m, 1)))
        forConnect = list(filter(lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <=
                          self.n and 0 < x[0][1] <= self.m and 0 < x[0][1] + x[1][1] <= self.m, forConnect))
        forPrevConnect = list(map(lambda x: (
            (prevPos[0] - x[0] * 2, prevPos[1] - x[1] * 2), x), Table.createManhattanGeneric(prevPos, 1, self.n, self.m, 1)))
        forPrevConnect = list(filter(lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <=
                              self.n and 0 < x[0][1] <= self.m and 0 < x[0][1] + x[1][1] <= self.m, forPrevConnect))
        forDisconnect = Table.createManhattanGeneric(
            position, 1, self.n, self.m, 2)
        forDisconnect = list(zip([position]*len(forDisconnect), forDisconnect))
        forPrevDisconnect = Table.createManhattanGeneric(
            prevPos, 1, self.n, self.m, 2)
        forPrevDisconnect = list(
            zip([prevPos]*len(forPrevDisconnect), forPrevDisconnect))
        if name == "X":
            self.disconnectO(forDisconnect + forPrevConnect)
            self.connectO(forConnect, False, position)
            self.connectO(forPrevDisconnect)
        else:
            self.disconnectX(forDisconnect + forPrevConnect)
            self.connectX(forConnect, False, position)
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

    def canBothPlayersFinish(self):
        return self.canPlayerXFinish() and self.canPlayerOFinish()

    def canPlayerXFinish(self):
        paths = self.findPathsX(self.X.getCurrectPositions(), self.O.getInitialPositions())
        return None not in paths

    def canPlayerOFinish(self):
        paths = self.findPathsO(self.O.getCurrectPositions(), self.X.getInitialPositions())
        return None not in paths

    def findPathsX(self, xPos, endPos):
        paths = [False] * 4
        queue = {
            'first game piece': {
                'heads': {
                    xPos[0]: 0
                },
                'visited': set(),
                'processing': [[xPos[0]]],
                'partial paths': [[xPos[0]]]
            },
            'second game piece': {
                'heads': {
                    xPos[1]: 0
                },
                'visited': set(),
                'processing': [[xPos[1]]],
                'partial paths': [[xPos[1]]]
            },
            'first initial': {
                'tails': {
                    endPos[0]: 0
                },
                'visited': set(),
                'processing': [[endPos[0]]],
                'partial paths': [[endPos[0]]]
            },
            'second initial': {
                'tails': {
                    endPos[1]: 0
                },
                'visited': set(),
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
                    if n not in queue['first game piece']['visited']:
                        queue['first game piece']['heads'][n] = len(queue['first game piece']['partial paths'])
                        queue['first game piece']['partial paths'] += [current + [n]]
                        queue['first game piece']['processing'] += [current + [n]]
                        queue['first game piece']['visited'].add(n)
                queue['first game piece']['heads'].pop(current[-1])
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
                    if n not in queue['second game piece']['visited']:
                        queue['second game piece']['heads'][n] = len(queue['second game piece']['partial paths'])
                        queue['second game piece']['partial paths'] += [current + [n]]
                        queue['second game piece']['processing'] += [current + [n]]
                        queue['second game piece']['visited'].add(n)
                queue['second game piece']['heads'].pop(current[-1])
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
                        if n not in queue['first initial']['visited']:
                            queue['first initial']['tails'][n] = len(queue['first initial']['partial paths'])
                            queue['first initial']['partial paths'] += [[n] + current]
                            queue['first initial']['processing'] += [[n] + current]
                            queue['first initial']['visited'].add(n)
                queue['first initial']['tails'].pop(current[0])
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
                        if n not in queue['second initial']['visited']:
                            queue['second initial']['tails'][n] = len(queue['second initial']['partial paths'])
                            queue['second initial']['partial paths'] += [[n] + current]
                            queue['second initial']['processing'] += [[n] + current]
                            queue['second initial']['visited'].add(n)
                queue['second initial']['tails'].pop(current[0])
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
                'visited': set(),
                'processing': [[oPos[0]]],
                'partial paths': [[oPos[0]]]
            },
            'second game piece': {
                'heads': {
                    oPos[1]: 0
                },
                'visited': set(),
                'processing': [[oPos[1]]],
                'partial paths': [[oPos[1]]]
            },
            'first initial': {
                'tails': {
                    endPos[0]: 0
                },
                'visited': set(),
                'processing': [[endPos[0]]],
                'partial paths': [[endPos[0]]]
            },
            'second initial': {
                'tails': {
                    endPos[1]: 0
                },
                'visited': set(),
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
                    if n not in queue['first game piece']['visited']:
                        queue['first game piece']['heads'][n] = len(queue['first game piece']['partial paths'])
                        queue['first game piece']['partial paths'] += [current + [n]]
                        queue['first game piece']['processing'] += [current + [n]]
                        queue['first game piece']['visited'].add(n)
                queue['first game piece']['heads'].pop(current[-1])
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
                    if n not in queue['second game piece']['visited']:
                        queue['second game piece']['heads'][n] = len(queue['second game piece']['partial paths'])
                        queue['second game piece']['partial paths'] += [current + [n]]
                        queue['second game piece']['processing'] += [current + [n]]
                        queue['second game piece']['visited'].add(n)
                queue['second game piece']['heads'].pop(current[-1])
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
                        if n not in queue['first initial']['visited']:
                            queue['first initial']['tails'][n] = len(queue['first initial']['partial paths'])
                            queue['first initial']['partial paths'] += [[n] + current]
                            queue['first initial']['processing'] += [[n] + current]
                            queue['first initial']['visited'].add(n)
                queue['first initial']['tails'].pop(current[0])
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
                        if n not in queue['second initial']['visited']:
                            queue['second initial']['tails'][n] = len(queue['second initial']['partial paths'])
                            queue['second initial']['partial paths'] += [[n] + current]
                            queue['second initial']['processing'] += [[n] + current]
                            queue['second initial']['visited'].add(n)
                queue['second initial']['tails'].pop(current[0])
            else:
                if not paths[1]:
                    paths[1] = None
                if not paths[3]:
                    paths[3] = None
        return paths

    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[0] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.setGamePiece(currentPos, nextPos, name)

        xPaths = self.findPathsX(self.X.getCurrectPositions(), self.O.getInitialPositions())
        oPaths = self.findPathsO(self.O.getCurrectPositions(), self.X.getInitialPositions())

        if None not in xPaths:
            print("Shortest path X1 to O1:", xPaths[0])
            print("Shortest path X1 to O2:", xPaths[1])
            print("Shortest path X2 to O1:", xPaths[2])
            print("Shortest path X2 to O2:", xPaths[3])
        else:
            print("Player X can't finish!")
        if None not in oPaths:
            print("Shortest path O1 to X1:", oPaths[0])
            print("Shortest path O1 to X2:", oPaths[1])
            print("Shortest path O2 to X1:", oPaths[2])
            print("Shortest path O2 to X2:", oPaths[3])
        else:
            print("Player O can't finish!")

    @staticmethod
    def createManhattan(currentPos, low, highN, highM, dStep):
        return list(map(lambda x: (currentPos[0] + x[0], currentPos[1] + x[1]),
                        Table.createManhattanGeneric(currentPos, low, highN, highM, dStep)))

    @staticmethod
    def createManhattanGeneric(currentPos, low, highN, highM, dStep=2):
        return [(x, y) for x in range(-dStep, dStep+1) for y in range(-dStep, dStep+1) if low <= (currentPos[0] +
                x) <= highN and low <= (currentPos[1] + y) <= highM and Table.isManhattan((0, 0), (x, y), dStep)]

    @staticmethod
    def isManhattan(currentPos, followedPos, dStep):
        return abs(currentPos[0] - followedPos[0]) + abs(currentPos[1] - followedPos[1]) == dStep
