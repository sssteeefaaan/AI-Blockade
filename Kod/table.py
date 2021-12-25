from field import Field
from view import View


class Table:
    def __init__(self, n=11, m=14, initial={(4, 4): "X1", (8, 4): "X2", (4, 11): "O1", (8, 11): "O2"}, wallNumb=9, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m
        self.view = View(n, m, {'xBlue': wallNumb, 'xGreen': wallNumb,
                         'oBlue': wallNumb, 'oGreen': wallNumb}, greenWall, blueWall, rowSep)
        self.blueWalls = set()
        self.greenWalls = set()
        self.fields = []
        self.X = None
        self.O = None
        self.onInit(initial)

    def onInit(self, initial):
        connectInitialX = []
        connectInitialO = []
        for i in range(0, self.n):
            self.fields.append([])
            for j in range(0, self.m):
                connectedX = set(Table.createManhattan(
                    (i, j), 0, self.n-1, self.m-1, 2))
                connectedO = set(Table.createManhattan(
                    (i, j), 0, self.n-1, self.m-1, 2))

                self.fields[i].append(
                    Field(self, (i, j), connectedX, connectedO, initial.get((i+1, j+1), None)))

                match initial.get((i+1, j+1), None):
                    case "X1" | "X2":
                        position = (i+1, j+1)
                        manGen = list(map(lambda x: ((position[0] - x[0], position[1] - x[1]), x),
                                          Table.createManhattanGeneric(position, 1, self.n, self.m, 1)))
                        connectInitialO += list(filter(lambda x: 0 < x[0][0] + x[1][0] <=
                                                       self.n and 0 < x[0][1] + x[1][1] <= self.m, manGen))
                    case "O1" | "O2":
                        position = (i+1, j+1)
                        manGen = list(map(lambda x: ((position[0] - x[0], position[1] - x[1]), x),
                                          Table.createManhattanGeneric(position, 1, self.n, self.m, 1)))
                        connectInitialX += list(filter(lambda x: 0 < x[0][0] + x[1][0] <=
                                                       self.n and 0 < x[0][1] + x[1][1] <= self.m, manGen))

        for k in initial.keys():
            self.setGamePiece(
                (-100, -100), (k[0] + 1, k[1] + 1), initial.get(k)[0])

        self.connectO(connectInitialO, False)
        self.connectX(connectInitialX, False)

        for row in self.fields:
            for f in row:
                for i in range(2):
                    f.findNextHopToX(i)
                    f.findNextHopToO(i)

        for pos in initial.keys():
            self.view.setPosition(pos[0], pos[1], initial[pos][0])
        self.view.refresh()

    def checkState(self):
        if self.O.isWinner((self.X.firstGP.home, self.X.secondGP.home)):
            self.winner = self.O
        elif self.X.isWinner((self.O.firstGP.home, self.O.secondGP.home)):
            self.winner = self.X

    def setBlueWall(self, pos):
        if self.isCorrectBlueWall(pos):
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
        if self.isCorrectGreenWall(pos):
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
                    forDisconnect += [((pos[0], pos[1] + 1), (0, -2))]
                if up1 and ((pos[0]-2, pos[1]) in self.greenWalls or (pos[0]-1, pos[1]-1) in self.blueWalls or (pos[0]-1, pos[1]+1) in self.blueWalls):
                    forDisconnect += [(pos, (-1, 1)),
                                      ((pos[0], pos[1] + 1), (-1, -1))]
            if right2:
                forDisconnect += [(pos, (0, 2))]
                if down1:
                    forDisconnect += [((pos[0] + 1, pos[1]), (0, 2))]
            self.disconnect(forDisconnect, "Z")

    def setGamePiece(self, prevPos, position, name="X"):
        forConnect = list(map(lambda x: ((position[0] - x[0] * 2, position[1] - x[1] * 2), x),
                              Table.createManhattanGeneric(position, 1, self.n, self.m, 1)))
        forConnect = list(filter(lambda x: 0 < x[0][0] + x[1][0] <
                                 self.n and 0 < x[0][1] + x[1][1] < self.m, forConnect))
        forPrevConnect = list(map(lambda x: ((prevPos[0] - x[0] * 2, prevPos[1] - x[1] * 2), x),
                                  Table.createManhattanGeneric(prevPos, 1, self.n, self.m, 1)))
        forPrevConnect = list(filter(lambda x: 0 < x[0][0] + x[1][0] <
                                     self.n and 0 < x[0][1] + x[1][1] < self.m, forPrevConnect))
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
            self.fields[x[0] - 1][x[1] - 1].connect(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                f.findNextHopToX(0)
                f.findNextHopToX(1)
                f.findNextHopToO(0)
                f.findNextHopToO(1)

    def connectX(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if (x[0]-1, x[1]-1)
                   in self.fields[position[0] - 1][position[1] - 1].connectedO]
            for (x, y) in con:
                self.fields[x[0] - 1][x[1] - 1].connectX(
                    self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]], mirrored)
        else:
            for (x, y) in vals:
                self.fields[x[0] - 1][x[1] - 1].connectX(
                    self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]], mirrored)
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                f.findNextHopToO(0)
                f.findNextHopToO(1)

    def connectO(self, vals, mirrored=True, position=None):
        if position:
            con = [(x, y) for (x, y) in vals if (x[0]-1, x[1]-1)
                   in self.fields[position[0] - 1][position[1] - 1].connectedX]
            for (x, y) in con:
                self.fields[x[0] - 1][x[1] - 1].connectO(
                    self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]], mirrored)
        else:
            for (x, y) in vals:
                self.fields[x[0] - 1][x[1] - 1].connectO(
                    self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]], mirrored)
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                f.findNextHopToX(0)
                f.findNextHopToX(1)

    def disconnect(self, vals, w=None):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnect(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]], w)
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                if f.nextHopToX[0][0] == None:
                    f.findNextHopToX(0)
                if f.nextHopToX[1][0] == None:
                    f.findNextHopToX(1)
                if f.nextHopToO[0][0] == None:
                    f.findNextHopToO(0)
                if f.nextHopToO[1][0] == None:
                    f.findNextHopToO(1)

    def disconnectX(self, vals):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnectX(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                if f.nextHopToO[0][0] == None:
                    f.findNextHopToO(0)
                if f.nextHopToO[1][0] == None:
                    f.findNextHopToO(1)

    def disconnectO(self, vals):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnectO(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])
        for (x, y) in vals:
            for f in [self.fields[x[0] - 1][x[1] - 1], self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]]]:
                if f.nextHopToX[0][0] == None:
                    f.findNextHopToX(0)
                if f.nextHopToX[1][0] == None:
                    f.findNextHopToX(1)

    def areConnected(self, currentPos, followedPos, name="X"):
        if name == "X":
            return (followedPos[0] - 1, followedPos[1] - 1) in self.fields[currentPos[0] - 1][currentPos[1] - 1].connectedX
        else:
            print(self.fields[currentPos[0] - 1][currentPos[1] - 1].connectedO)
            return (followedPos[0] - 1, followedPos[1] - 1) in self.fields[currentPos[0] - 1][currentPos[1] - 1].connectedO

    def isCorrectBlueWall(self, pos):
        return not (pos in self.greenWalls or
                    [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)]
                     if x in self.blueWalls])

    def isCorrectGreenWall(self, pos):
        return not (pos in self.blueWalls
                    or [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])]
                        if x in self.greenWalls])

    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[0] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.setGamePiece(currentPos, nextPos, name)
        self.view.move(name, currentPos, nextPos, wall)
        if self.canPlayerXFinish():
            xPos1 = self.X.firstGP.position
            xPos2 = self.X.secondGP.position
            print("Shortest path X1 to O1:",
                  self.fields[xPos1[0]-1][xPos1[1]-1].getShortestPathToO(0))
            print("Shortest path X1 to O2:",
                  self.fields[xPos1[0]-1][xPos1[1]-1].getShortestPathToO(1))
            print("Shortest path X2 to O1:",
                  self.fields[xPos2[0]-1][xPos2[1]-1].getShortestPathToO(0))
            print("Shortest path X2 to O2:",
                  self.fields[xPos2[0]-1][xPos2[1]-1].getShortestPathToO(1))
        else:
            print("Player X can't finish!")
        if self.canPlayerOFinish():
            oPos1 = self.O.firstGP.position
            oPos2 = self.O.secondGP.position
            print("Shortest path O1 to X1:",
                  self.fields[oPos1[0]-1][oPos1[1]-1].getShortestPathToX(0))
            print("Shortest path O1 to X2:",
                  self.fields[oPos1[0]-1][oPos1[1]-1].getShortestPathToX(1))
            print("Shortest path O2 to X1:",
                  self.fields[oPos2[0]-1][oPos2[1]-1].getShortestPathToX(0))
            print("Shortest path O2 to X2:",
                  self.fields[oPos2[0]-1][oPos2[1]-1].getShortestPathToX(1))
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

    def canBothPlayersFinish(self):
        return self.canPlayerXFinish() and self.canPlayerOFinish()

    def canPlayerXFinish(self):
        xPos1 = self.X.firstGP.position
        xPos2 = self.X.secondGP.position
        cond = self.fields[xPos1[0]-1][xPos1[1]-1].nextHopToO[0][0]
        cond = cond and self.fields[xPos1[0]-1][xPos1[1]-1].nextHopToO[1][0]
        cond = cond and self.fields[xPos2[0]-1][xPos2[1]-1].nextHopToO[0][0]
        cond = cond and self.fields[xPos2[0]-1][xPos2[1]-1].nextHopToO[1][0]
        return cond

    def canPlayerOFinish(self):
        oPos1 = self.O.firstGP.position
        oPos2 = self.O.secondGP.position
        cond = self.fields[oPos1[0]-1][oPos1[1]-1].nextHopToX[0][0]
        cond = cond and self.fields[oPos1[0]-1][oPos1[1]-1].nextHopToX[1][0]
        cond = cond and self.fields[oPos2[0]-1][oPos2[1]-1].nextHopToX[0][0]
        cond = cond and self.fields[oPos2[0]-1][oPos2[1]-1].nextHopToX[1][0]
        return cond
