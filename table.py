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
                self.fields[i].append(
                    Field(i, j, set([(i + x, j + y) for x in range(-2, 3) for y in range(-2, 3) if i +
                                     x >= 0 and i + x < self.n and j + y >= 0 and j + y < self.m and abs(x) + abs(y) == 2]), initial.get((i, j), None)))

        for pos in initial.keys():
            self.view.setPosition(pos[0], pos[1], initial[pos])
        self.view.refresh()

    def isCorrectBlueWall(self, pos):
        return not (pos in self.greenWalls or [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)] if x in self.blueWalls])

    def isCorrectGreenWall(self, pos):
        return not (pos in self.blueWalls or [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])] if x in self.greenWalls])

    def setBlueWall(self, pos):
        # x1   x2   x3   x4                         x1   x2   x3   x4       => x6 gubi vezu sa x10, x11 i x14
        #                                                                   => x7 gubi vezu sa x10, x11, x15
        # x5   x6   x7   x8   = BlueWall(x6) =>     x5   x6   x7   x8
        #                                                =======            => x10 gubi vezu sa x2
        # x9   x10  x11  x12                        x9   x10  x11  x12      => x11 gubi vezu sa x3
        #
        # x13  x14  x15  x16                        x13  x14  x15  x16      => ukoliko postoji plavi zid na polju (x6[i], x6[j]-2), ili zeleni zid u x1
        #                                                                   => x6 gubi vezu sa x9, x10 gubi vezu sa x5
        #                                                                   => ukoliko postoji plavi zid na x8, ili zeleni zid u x3
        #                                                                   => x7 gubi vezu sa x12, x11 gubi vezu sa x8

        if self.isCorrectBlueWall(pos):
            self.blueWalls.add(pos)
            # lista svih potega koje treba ukloniti, odnosno formirati
            # zbog redudantnosti u kodu, poteg je formiran kao ((i, j), (pom_i, pom_j))
            # gde ce se poteg ukloniti/kreirati izmedju polja koji se identifikuju sa (i, j) i (i + pom_i, j + pom_j)
            # odnosno pom_i i pom_j su pomeraji u odnosu na prosleđeni čvor (i, j), ne identifikatori čvora koji se uklanja
            forDisconnect = []

            up1 = pos[0] - 1 > 0
            down1 = pos[0] + 1 <= self.n
            down2 = pos[0] + 2 <= self.n
            left1 = pos[1] - 1 > 0
            right1 = pos[1] + 1 <= self.m
            right2 = pos[1] + 2 <= self.m

            if down1:
                # x6 gubi vezu sa x10
                forDisconnect += [(pos, (1, 0))]
                if right1:
                    # x6 gubi vezu sa x11
                    forDisconnect += [(pos, (1, 1))]
                    # x7 gubi vezu sa x10, x11
                    forDisconnect += [((pos[0], pos[1] + 1), (1, -1)),
                                      ((pos[0], pos[1] + 1), (1, 0))]
                    if down2:
                        # x7 gubi vezu sa x15
                        forDisconnect += [((pos[0], pos[1] + 1), (2, 0))]
                    if up1:
                        # x11 gubi vezu sa x3
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (-2, 0))]
                if up1:
                    # x10 gubi vezu sa x2
                    forDisconnect += [((pos[0] + 1, pos[1]), (-2, 0))]
                if down2:
                    # x6 gubi vezu sa x14
                    forDisconnect += [(pos, (2, 0))]
                if left1 and ((pos[0], pos[1]-2) in self.blueWalls or (pos[0]-1, pos[1]-1) in self.greenWalls):
                    # x6 gubi vezu sa x9, x10 gubi vezu sa x5
                    forDisconnect += [(pos, (1, -1)),
                                      ((pos[0]+1, pos[1]), (-1, -1))]
                if right2 and ((pos[0], pos[1]+2) in self.blueWalls or (pos[0]-1, pos[1]+1) in self.greenWalls):
                    # x7 gubi vezu sa x12, x11 gubi vezu sa x8
                    forDisconnect += [((pos[0], pos[1]+1), (1, 1)),
                                      ((pos[0]+1, pos[1]+1), (-1, 1))]

            self.disconnect(forDisconnect)

    def setGreenWall(self, pos):
        # x1   x2   x3   x4                         x1   x2    x3   x4      => x6 gubi vezu sa x7, x11 i x8
        #                                                                   => x10 gubi vezu sa x7, x11, x12
        # x5   x6   x7   x8   = GreenWall(x6) =>    x5   x6  H x7   x8
        #                                                    H              => x7 gubi vezu sa x5
        # x9   x10  x11  x12                        x9   x10 H x11  x12     => x11 gubi vezu sa x9
        #
        # x13  x14  x15  x16                        x13  x14   x15  x16     => ukoliko postoji zeleni zid na polju x14, ili plavi zid na polju x9
        #                                                                   => x10 gubi vezu sa x15, x11 gubi vezu sa x14
        #                                                                   => ukoliko postoji zeleni zid na polju (x6[i]-2, x6[j]), ili plavi zid na polju x1
        #                                                                   => x6 gubi vezu sa x3, x7 gubi vezu sa x2
        #
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
                # x6 gubi vezu sa x7
                forDisconnect += [(pos, (0, 1))]
                if down1:
                    # x6 gubi vezu sa x11
                    forDisconnect += [(pos, (1, 1))]
                    # x10 gubi vezu sa x7, x11
                    forDisconnect += [((pos[0] + 1, pos[1]), (-1, 1)), ((pos[0] + 1, pos[1]), (0, 1))]
                    if left1:
                        # x11 gubi vezu sa x9
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (0, -2))]
                    if down2 and ((pos[0]+2, pos[1]) in self.greenWalls or (pos[0]+1, pos[1]-1) in self.blueWalls):
                        # x10 gubi vezu sa x15
                        # x11 gubi vezu sa x14
                        forDisconnect += [((pos[0]+1, pos[1]), (1, 1)), ((pos[0] + 1, pos[1] + 1), (1, -1))]
                if left1:
                    # x7 gubi vezu sa x5
                    forDisconnect += [((pos[0], pos[1] + 1), (0, -2))]
                if up1 and ((pos[0]-2, pos[1]) in self.greenWalls or (pos[0]-1, pos[1]-1) in self.blueWalls):
                    # x6 gubi vezu sa x3
                    # x7 gubi vezu sa x2
                    forDisconnect += [(pos, (-1, 1)), ((pos[0], pos[1] + 1), (-1, -1))]
            if right2:
                # x6 gubi vezu sa x8
                forDisconnect += [(pos, (0, 2))]
                if down1:
                    # x10 gubi vezu sa x12
                    forDisconnect += [((pos[0] + 1, pos[1]), (0, 2))]
            self.disconnect(forDisconnect)

    def disconnect(self, vals):
        for (x, y) in vals:
            self.fields[x[0]-1][x[1]-1].disconnect(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])

    def connect(self, vals):
        for (x, y) in vals:
            self.fields[x[0] - 1][x[1] - 1].connect(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])

    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[0] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.view.move(name, currentPos, nextPos, wall)

    def setGamePiece(self, name, position):
        forConnect = []
        forDisconnect = []
        for i in range (0, self.n):
            


    def areConnected(self, currentPos, followedPos):
        return (followedPos[0] - 1, followedPos[1] - 1) in self.fields[currentPos[0] - 1][currentPos[1] - 1].connected

    # def moveH(self, currentPos, followedPos):
    #     return followedPos[0] == currentPos[0]

    # def moveV(self, currentPos, followedPos):
    #     return followedPos[1] == currentPos[1]

