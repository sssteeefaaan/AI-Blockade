from field import Field
from view import View


class Table:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, wallNumb=9, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m
        self.view = View(n, m, wallNumb, greenWall, blueWall, rowSep)

        self.blueWalls = set()
        self.greenWalls = set()

        self.fields = []
        self.onInit(initial)

    def onInit(self, initial):
        for i in range(0, self.n):
            self.fields.append([])
            for j in range(0, self.m):
                connectedX = set(self.createManhattan((i, j), 2))
                connectedO = set(self.createManhattan((i, j), 2))
                self.fields[i].append(
                    Field(i, j, connectedX, connectedO, initial.get((i, j), None)))

        for pos in initial.keys():
            self.view.setPosition(pos[0], pos[1], initial[pos])
        self.view.refresh()

    def setBlueWall(self, pos):
        if self.isCorrectBlueWall(pos):
            self.blueWalls.add(pos)
            forDisconnect = []

            up1 = pos[0] - 1 > 0
            down1 = pos[0] + 1 <= self.n
            down2 = pos[0] + 2 <= self.n
            left1 = pos[1] - 1 > 0
            right1 = pos[1] + 1 <= self.m
            right2 = pos[1] + 2 <= self.m

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
                if left1 and ((pos[0], pos[1]-2) in self.blueWalls or (pos[0]-1, pos[1]-1) in self.greenWalls):
                    forDisconnect += [(pos, (1, -1)),
                                      ((pos[0]+1, pos[1]), (-1, -1))]
                if right2 and ((pos[0], pos[1]+2) in self.blueWalls or (pos[0]-1, pos[1]+1) in self.greenWalls):
                    forDisconnect += [((pos[0], pos[1]+1), (1, 1)),
                                      ((pos[0]+1, pos[1]+1), (-1, 1))]

            self.disconnect(forDisconnect, "P")

    def setGreenWall(self, pos):
        if self.isCorrectGreenWall(pos):
            self.greenWalls.add(pos)
            forDisconnect = []

            up1 = pos[0] - 1 > 0
            down1 = pos[0] + 1 <= self.n
            down2 = pos[0] + 2 <= self.n
            left1 = pos[1] - 1 > 0
            right1 = pos[1] + 1 <= self.m
            right2 = pos[1] + 2 <= self.m

            if right1:
                forDisconnect += [(pos, (0, 1))]
                if down1:
                    forDisconnect += [(pos, (1, 1))]
                    forDisconnect += [((pos[0] + 1, pos[1]), (-1, 1)), ((pos[0] + 1, pos[1]), (0, 1))]
                    if left1:
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (0, -2))]
                    if down2 and ((pos[0]+2, pos[1]) in self.greenWalls or (pos[0]+1, pos[1]-1) in self.blueWalls):
                        forDisconnect += [((pos[0]+1, pos[1]), (1, 1)), ((pos[0] + 1, pos[1] + 1), (1, -1))]
                    forDisconnect += [((pos[0], pos[1] + 1), (0, -2))]
                if up1 and ((pos[0]-2, pos[1]) in self.greenWalls or (pos[0]-1, pos[1]-1) in self.blueWalls):
                    forDisconnect += [(pos, (-1, 1)), ((pos[0], pos[1] + 1), (-1, -1))]
            if right2:
                forDisconnect += [(pos, (0, 2))]
                if down1:
                    forDisconnect += [((pos[0] + 1, pos[1]), (0, 2))]
            self.disconnect(forDisconnect, "Z")

    def setGamePiece(self, prevPos, position, name="X"):
        forConnect = list(map(lambda x: (x, (x[0] - position[0], x[1] - position[1])),
                                     self.createManhattan(position, 1)))
        forConnect = list(filter(lambda x: x[0][0] + x[1][0] > 0 and x[0][0] + x[1][0] <= self.n and x[0][1] + x[1][1] > 0 and x[0][1] + x[1][1] <= self.m, forConnect))
        forPrevConnect = list(map(lambda x: (x, (x[0] - prevPos[0], x[1] - prevPos[1])),
                                     self.createManhattan(prevPos, 1)))
        forPrevConnect = list(filter(lambda x: x[0][0] + x[1][0] > 0 and x[0][0] + x[1][0] <= self.n and x[0][1] + x[1][1] > 0 and x[0][1] + x[1][1] <= self.m, forPrevConnect))
        
        forDisconnect = self.createManhattanGeneric(position, 2)
        forDisconnect = list(zip([position]*len(forDisconnect), forDisconnect))
        forPrevDisconnect = self.createManhattanGeneric(prevPos, 2)
        forPrevDisconnect = list(zip([prevPos]*len(forPrevDisconnect), forPrevDisconnect))
        
        if name == "X":
            self.disconnectO(forDisconnect + forPrevConnect)
            self.connectO(forConnect + forPrevDisconnect)
        else:
            self.disconnectX(forDisconnect + forPrevConnect)
            self.connectX(forConnect + forPrevDisconnect)

    def createManhattan(self, currentPos, n):
        return list(map(lambda x: (currentPos[0]+ x[0], currentPos[1] + x[1]), self.createManhattanGeneric(currentPos, n)))
        
    def createManhattanGeneric(self, currentPos, n):
        return [(x, y) for x in range(-2, 3) for y in range(-2, 3) if currentPos[0] +
                                     x >= 0 and currentPos[0] + x < self.n and currentPos[1] + y >= 0 and currentPos[1] + y < self.m and abs(x) + abs(y) == n]
            
    def disconnect(self, vals, w=None):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnect(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]], w)

    def connect(self, vals):
        for (x, y) in vals:
            self.fields[x[0] - 1][x[1] - 1].connect(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])
            
    def disconnectX(self, vals):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnectX(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])

    def connectX(self, vals):
        for (x, y) in vals:
            self.fields[x[0] - 1][x[1] - 1].connectX(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])
            
    def disconnectO(self, vals):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnectO(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])

    def connectO(self, vals):
        for (x, y) in vals:
            self.fields[x[0] - 1][x[1] - 1].connectO(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])
            
    def areConnected(self, currentPos, followedPos, name="X"):
        if name == "X":
            return (followedPos[0] - 1, followedPos[1] - 1) in self.fields[currentPos[0] - 1][currentPos[1] - 1].connectedX
        else:
            return (followedPos[0] - 1, followedPos[1] - 1) in self.fields[currentPos[0] - 1][currentPos[1] - 1].connectedO
        
    def isCorrectBlueWall(self, pos):
            return not (pos in self.greenWalls or [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)] if x in self.blueWalls])

    def isCorrectGreenWall(self, pos):
        return not (pos in self.blueWalls or [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])] if x in self.greenWalls])
        
    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[0] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.setGamePiece(currentPos, nextPos, name)
        self.view.move(name, currentPos, nextPos, wall)
