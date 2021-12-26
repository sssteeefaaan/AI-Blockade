from player import Player
from field import Field


class Table:
    def __init__(self, n=11, m=14, blueWalls=set(), greenWalls=set(), X=None, O=None):
        self.n = n
        self.m = m
        self.blueWalls = set(blueWalls)
        self.greenWalls = set(greenWalls)
        self.fields = dict()
        self.X = X.getCopy() if X else None
        self.O = O.getCopy() if O else None

    def getCopy(self):
        copy = Table(self.n, self.m, self.blueWalls,
                     self.greenWalls, self.X, self.O)
        for key in self.fields.keys():
            copy.fields[key] = self.fields[key].getCopy(copy)
        return copy

    def onInit(self, initial, players):
        self.setPlayers(players)
        self.setFields(initial)
        self.setNextHops(initial)

    def setPlayers(self, players):
        for player in players.keys():
            if player == "X":
                self.X = Player("X", *players[player])
            elif player == "O":
                self.O = Player("O", *players[player])

    def setFields(self, initial):
        connectInitialX = []
        connectInitialO = []
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
                        connectInitialO += list(filter(lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <=
                                                       self.n and 0 < x[0][1] <= self.m and 0 < x[0][1] + x[1][1] <= self.m, manGen))
                    case "O1" | "O2":
                        manGen = list(map(lambda x: ((pos[0] - x[0], pos[1] - x[1]), x),
                                          Table.createManhattanGeneric(pos, 1, self.n, self.m, 1)))
                        connectInitialX += list(filter(lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <=
                                                       self.n and 0 < x[0][1] <= self.m and 0 < x[0][1] + x[1][1] <= self.m, manGen))
        for k in initial.keys():
            self.setGamePiece(
                (-100, -100), (k[0], k[1]), initial.get(k)[0])
        self.connectO(connectInitialO, False)
        self.connectX(connectInitialX, False)

    def setNextHops(self, initial):
        for pos in initial.keys():
            match initial[pos]:
                case "X1":
                    self.fields[pos].nextHopToX[0] = (pos, 0)
                    self.fields[pos].notifyNextHopToX(
                        self.fields[pos], 0, True)
                case "X2":
                    self.fields[pos].nextHopToX[1] = (pos, 0)
                    self.fields[pos].notifyNextHopToX(
                        self.fields[pos], 1, True)
                case "O1":
                    self.fields[pos].nextHopToO[0] = (pos, 0)
                    self.fields[pos].notifyNextHopToO(
                        self.fields[pos], 0, True)
                case "O2":
                    self.fields[pos].nextHopToO[1] = (pos, 0)
                    self.fields[pos].notifyNextHopToO(
                        self.fields[pos], 1, True)

    def getData(self):
        return (self.greenWalls, self.blueWalls, {"X": self.X.getCurrectPositions(), "O": self.O.getCurrectPositions()}, self.X.getWallNumber(), self.O.getWallNumber())

    def checkState(self):
        if self.O.isWinner((self.X.firstGP.home, self.X.secondGP.home)):
            self.winner = self.O
        elif self.X.isWinner((self.O.firstGP.home, self.O.secondGP.home)):
            self.winner = self.X

    def setBlueWall(self, pos):
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
            if left1 and ((pos[0], pos[1]-2) in self.blueWalls or (pos[0]-1, pos[1]-1) in self.greenWalls or (pos[0]+1, pos[1]-1) in self.greenWalls):
                forDisconnect += [(pos, (1, -1)),
                                  ((pos[0]+1, pos[1]), (-1, -1))]
            if right2 and ((pos[0], pos[1]+2) in self.blueWalls or (pos[0]-1, pos[1]+1) in self.greenWalls or (pos[0]+1, pos[1]+1) in self.greenWalls):
                forDisconnect += [((pos[0], pos[1]+1), (1, 1)),
                                  ((pos[0]+1, pos[1]+1), (-1, 1))]

        self.disconnect(forDisconnect, "P")

    def setGreenWall(self, pos):
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
                if down2 and ((pos[0]+2, pos[1]) in self.greenWalls or (pos[0]+1, pos[1]-1) in self.blueWalls or (pos[0]+1, pos[1]+1) in self.blueWalls):
                    forDisconnect += [((pos[0]+1, pos[1]), (1, 1)),
                                      ((pos[0] + 1, pos[1] + 1), (1, -1))]
            if up1 and ((pos[0]-2, pos[1]) in self.greenWalls or (pos[0]-1, pos[1]-1) in self.blueWalls or (pos[0]-1, pos[1]+1) in self.blueWalls):
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
        forConnect = list(map(lambda x: ((position[0] - x[0] * 2, position[1] - x[1] * 2), x),
                              Table.createManhattanGeneric(position, 1, self.n, self.m, 1)))
        forConnect = list(filter(lambda x: 0 < x[0][0] <= self.n and 0 < x[0][0] + x[1][0] <=
                                 self.n and 0 < x[0][1] <= self.m and 0 < x[0][1] + x[1][1] <= self.m, forConnect))
        forPrevConnect = list(map(lambda x: ((prevPos[0] - x[0] * 2, prevPos[1] - x[1] * 2), x),
                                  Table.createManhattanGeneric(prevPos, 1, self.n, self.m, 1)))
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
        for (x, y) in vals:
            f = self.fields[(x[0] + y[0], x[1] + y[1])]
            self.fields[x].notifyNextHopToX(f, 0, False)
            self.fields[x].notifyNextHopToX(f, 1, False)
            self.fields[x].notifyNextHopToO(f, 0, False)
            self.fields[x].notifyNextHopToO(f, 1, False)

    def connectX(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if x
                   in self.fields[position].connectedO]
            for (x, y) in con:
                self.fields[x].connectX(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
            for (x, y) in vals:
                f = self.fields[(x[0] + y[0], x[1] + y[1])]
                self.fields[x].notifyNextHopToO(f, 0, False)
                self.fields[x].notifyNextHopToO(f, 1, False)
        else:
            for (x, y) in vals:
                self.fields[x].connectX(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
            for (x, y) in vals:
                f = self.fields[(x[0] + y[0], x[1] + y[1])]
                self.fields[x].notifyNextHopToO(f, 0, False)
                self.fields[x].notifyNextHopToO(f, 1, False)

    def connectO(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if x
                   in self.fields[position].connectedX]
            for (x, y) in con:
                self.fields[x].connectO(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
            for (x, y) in vals:
                f = self.fields[(x[0] + y[0], x[1] + y[1])]
                self.fields[x].notifyNextHopToX(f, 0, False)
                self.fields[x].notifyNextHopToX(f, 1, False)
        else:
            for (x, y) in vals:
                self.fields[x].connectO(
                    self.fields[(x[0] + y[0], x[1] + y[1])], mirrored)
            for (x, y) in vals:
                f = self.fields[(x[0] + y[0], x[1] + y[1])]
                self.fields[x].notifyNextHopToX(f, 0, False)
                self.fields[x].notifyNextHopToX(f, 1, False)

    def disconnect(self, vals, w=None):
        for (x, y) in vals:
            self.fields[x].disconnect(
                self.fields[(x[0] + y[0], x[1] + y[1])], w)
        for (x, y) in vals:
            self.fields[x].notifyNextHopToX(None, 0, False)
            self.fields[x].notifyNextHopToX(None, 1, False)
            self.fields[x].notifyNextHopToO(None, 0, False)
            self.fields[x].notifyNextHopToO(None, 1, False)

    def disconnectX(self, vals):
        for (x, y) in vals:
            self.fields[x].disconnectX(
                self.fields[(x[0] + y[0], x[1] + y[1])])
        for (x, y) in vals:
            self.fields[x].notifyNextHopToO(None, 0, False)
            self.fields[x].notifyNextHopToO(None, 1, False)

    def disconnectO(self, vals):
        for (x, y) in vals:
            self.fields[x].disconnectO(
                self.fields[(x[0] + y[0], x[1] + y[1])])
        for (x, y) in vals:
            self.fields[x].notifyNextHopToX(None, 0, False)
            self.fields[x].notifyNextHopToX(None, 1, False)

    def areConnected(self, currentPos, followedPos, name="X"):
        if name == "X":
            return followedPos in self.fields[currentPos].connectedX
        else:
            return followedPos in self.fields[currentPos].connectedO

    def isCorrectBlueWall(self, pos):
        return not (pos in self.greenWalls or
                    [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)]
                     if x in self.blueWalls])

    def isCorrectGreenWall(self, pos):
        return not (pos in self.blueWalls
                    or [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])]
                        if x in self.greenWalls])

    def canBothPlayersFinish(self):
        return self.canPlayerXFinish() and self.canPlayerOFinish()

    def canPlayerXFinish(self):
        xPos1 = self.X.firstGP.position
        xPos2 = self.X.secondGP.position
        return None not in [self.fields[xPos1].nextHopToO[0][0], self.fields[xPos1].nextHopToO[1][0], self.fields[xPos2].nextHopToO[0][0], self.fields[xPos2].nextHopToO[1][0]]

    def canPlayerOFinish(self):
        oPos1 = self.O.firstGP.position
        oPos2 = self.O.secondGP.position
        return None not in [self.fields[oPos1].nextHopToX[0][0], self.fields[oPos1].nextHopToX[1][0], self.fields[oPos2].nextHopToX[0][0], self.fields[oPos2].nextHopToX[1][0]]

    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[0] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.setGamePiece(currentPos, nextPos, name)
        if self.canPlayerXFinish():
            xPos1 = self.X.firstGP.position
            xPos2 = self.X.secondGP.position
            print("Shortest path X1 to O1:",
                  self.fields[xPos1].getShortestPathToO(0))
            print("Shortest path X1 to O2:",
                  self.fields[xPos1].getShortestPathToO(1))
            print("Shortest path X2 to O1:",
                  self.fields[xPos2].getShortestPathToO(0))
            print("Shortest path X2 to O2:",
                  self.fields[xPos2].getShortestPathToO(1))
        else:
            print("Player X can't finish!")
        if self.canPlayerOFinish():
            oPos1 = self.O.firstGP.position
            oPos2 = self.O.secondGP.position
            print("Shortest path O1 to X1:",
                  self.fields[oPos1].getShortestPathToX(0))
            print("Shortest path O1 to X2:",
                  self.fields[oPos1].getShortestPathToX(1))
            print("Shortest path O2 to X1:",
                  self.fields[oPos2].getShortestPathToX(0))
            print("Shortest path O2 to X2:",
                  self.fields[oPos2].getShortestPathToX(1))
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
