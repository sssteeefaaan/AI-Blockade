from field import Field
from view import View


class Table:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m

        self.view = View(n, m, greenWall, blueWall, rowSep)

        self.blueWalls = set()
        self.greenWalls = set()

        self.fields = []
        self.onInit(initial)

    def onInit(self, initial):
        for i in range(0, self.n):
            self.fields.append([])
            for j in range(0, self.m):
                connected = []
                if i - 2 > 0:
                    connected += [(i - 2, j)]
                if i + 2 <= self.n:
                    connected += [(i + 2, j)]
                if j - 2 > 0:
                    connected = [(i, j - 2)]
                if j + 2 <= self.m:
                    connected = [(i, j + 2)]

                connected += [(i + x, j + y) for x in (1, -1) for y in (1, -1)
                              if i + x <= self.n and i + x > 0 and j + y <= self.m and j + y > 0]

                # Connected X i connected Ox ????
                # Initial se razlikuju i na svoje inital ne mogu da stanu, ali na tudje initial mogu i to cak ukoliko je
                # udaljeno 1
                self.fields[i].append(
                    Field(i, j, connected, initial.get((i, j), None)))

        for pos in initial.keys():
            self.view.setPosition(pos[0], pos[1], initial[pos])
        self.view.refresh()

    def checkBlueWall(self, pos):
        return not (pos in self.greenWalls or [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)] if x in self.blueWalls])

    def checkGreenWall(self, pos):
        return not (pos in self.blueWalls or [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])] if x in self.greenWalls])

    def setBlueWall(self, pos):
        # x1   x2   x3   x4                         x1   x2   x3   x4       => x6 gubi vezu sa x9, x10, x11 i x14
        #                                                                   => x7 gubi vezu sa x10, x11, x12, x15
        # x5   x6   x7   x8   = BlueWall(x6) =>     x5   x6   x7   x8       => x10 gubi vezu sa x5
        #                                                =======            => x10 gubi vezu sa x2
        # x9   x10  x11  x12                        x9   x10  x11  x12      => x11 gubi vezu sa x3
        #                                                                   => x11 gubi vezu sa x8
        # x13  x14  x15  x16                        x13  x14  x15  x16      => x10 dobija vezu sa x14
        #                                                                   => x11 dobija vezu sa x15
        #                                                                   => x2 dobija vezu sa x6
        #                                                                   => x3 dobija vezu sa x7
        if self.checkBlueWall(pos):
            self.blueWalls.add(pos)
            # lista svih potega koje treba ukloniti, odnosno formirati
            # zbog redudantnosti u kodu, poteg je formiran kao ((i, j), (pom_i, pom_j))
            # gde ce se poteg ukloniti/kreirati izmedju polja koji se identifikuju sa (i, j) i (i + pom_i, j + pom_j)
            # odnosno pom_i i pom_j su pomeraji u odnosu na prosleđeni čvor (i, j), ne identifikatori čvora koji se uklanja
            forDisconnect = []
            forConnect = []

            up1 = pos[0] - 1 > 0
            down1 = pos[0] + 1 <= self.n
            down2 = pos[0] + 2 <= self.n
            left1 = pos[1] - 1 > 0
            right1 = pos[1] + 1 <= self.m
            right2 = pos[1] + 2 <= self.m

            if down1:
                # x6 gubi vezu sa x9, x10, x11
                forDisconnect += [(pos, x) for x in [(1, y)
                                                     for y in range(-1, 2) if pos[1] + y <= self.m and pos[1] + y > 0]]

                if right1:
                    # x7 gubi vezu sa x10, x11, x12
                    forDisconnect += [((pos[0], pos[1] + 1), x) for x in [(1, y)
                                                                          for y in range(-1, 2) if pos[1] + 1 + y <= self.m and pos[1] + 1 + y > 0]]

                    if down2:
                        # x7 gubi vezu sa x15
                        forDisconnect += [((pos[0], pos[1] + 1), (2, 0))]

                    if up1:
                        # x11 gubi vezu sa x3
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (-2, 0))]

                    if right2:
                        # x11 gubi vezu sa x8
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (-1, 1))]
                if left1:
                    # x10 gubi vezu sa x5
                    forDisconnect += [((pos[0] + 1, pos[1]), (-1, -1))]
                if up1:
                    # x10 gubi vezu sa x2
                    forDisconnect += [((pos[0] + 1, pos[1]), (-2, 0))]

                if down2:
                    # x6 gubi vezu sa x14
                    forDisconnect += [(pos, (2, 0))]
                    # x10 dobija vezu sa x14
                    forConnect += [((pos[0] + 1, pos[1]), (1, 0))]

                    if right1:
                        # x11 dobija vezu sa x15
                        forConnect += [((pos[0] + 1, pos[1] + 1), (1, 0))]

            if up1:
                # x2 dobija vezu sa x6
                forConnect += [(pos, (-1, 0))]

                if right1:
                    # x3 dobija vezu sa x7
                    forConnect += [((pos[0], pos[1] + 1), (-1, 0))]

            self.disconnect(forDisconnect)
            self.connect(forConnect)

    def setGreenWall(self, pos):
        # x1   x2   x3   x4                         x1   x2    x3   x4      => x6 gubi vezu sa x3, x7, x11 i x8 *
        #                                                                   => x10 gubi vezu sa x7, x11, x15, x12 *
        # x5   x6   x7   x8   = GreenWall(x6) =>    x5   x6  H x7   x8      => x7 gubi vezu sa x2 *
        #                                                    H              => x7 gubi vezu sa x5 *
        # x9   x10  x11  x12                        x9   x10 H x11  x12     => x11 gubi vezu sa x14 *
        #                                                                   => x11 gubi vezu sa x9 *
        # x13  x14  x15  x16                        x13  x14   x15  x16     => x8 gubi vezu sa x6 *
        #                                                                   => x12 gubi vezu sa x10 *
        #                                                                   => x12 dobija vezu sa x11 *
        #                                                                   => x5 dobija vezu sa x6 *
        #                                                                   => x8 dobija vezu sa x7 *
        #                                                                   => x9 dobija vezu sa x10
        if self.checkGreenWall(pos):
            self.greenWalls.add(pos)
            forDisconnect = []
            forConnect = []

            up1 = pos[0] - 1 > 0
            down1 = pos[0] + 1 <= self.n
            down2 = pos[0] + 2 <= self.n
            left1 = pos[1] - 1 > 0
            right1 = pos[1] + 1 <= self.m
            right2 = pos[1] + 2 <= self.m

            if right1:
                # x6 gubi vezu sa x3, x7, x11
                forDisconnect += [(pos, x) for x in [(y, 1)
                                                     for y in range(-1, 2) if pos[0] + y <= self.n and pos[0] + y > 0]]

                if down1:
                    # x10 gubi vezu sa x7, x11, x15
                    forDisconnect += [((pos[0] + 1, pos[1]), x) for x in [(y, 1)
                                                                          for y in range(-1, 2) if pos[0] + 1 + y <= self.n and pos[0] + 1 + y > 0]]

                    if left1:
                        # x11 gubi vezu sa x9
                        forDisconnect += [((pos[0] + 1, pos[1] + 1), (0, -2))]

                if up1:
                    # x7 gubi vezu sa x2
                    forDisconnect += [((pos[0], pos[1] + 1), (-1, -1))]

                if left1:
                    # x7 gubi vezu sa x5
                    forDisconnect += [((pos[0], pos[1] + 1), (0, -2))]

                if down2:
                    # x11 gubi vezu sa x14
                    forDisconnect += [((pos[0] + 1, pos[1] + 1), (1, -1))]

            if right2:
                # x8 gubi vezu sa x6
                forDisconnect += [(pos, (0, 2))]
                # x8 dobija vezu sa x7
                forConnect += [((pos[0], pos[1] + 2), (0, -1))]

                if down1:
                    # x10 gubi vezu sa x12
                    forDisconnect += [((pos[0] + 1, pos[1]), (0, 2))]
                    # x11 dobija vezu sa x12
                    forConnect += [((pos[0] + 1, pos[1] + 1), (0, 1))]

            if left1:
                # x5 dobija vezu sa x6
                forConnect += [(pos, (0, -1))]
                if down1:
                    # x9 dobija vezu sa x10
                    forConnect += [((pos[0] + 1, pos[0] - 1), (0, 1))]

            self.disconnect(forDisconnect)
            self.connect(forConnect)

    def disconnect(self, vals):
        for (x, y) in vals:
            # if x[0] <= self.n and x[0] > 0 and x[0] + y[0] <= self.n and x[0] + y[0] > 0:
            #     if x[1] <= self.m and x[1] > 0 and x[1] + y[1] <= self.m and x[1] + y[1] > 0:
            self.fields[x[0]-1][x[1]-1].disconnect(
                self.fields[x[0]-1 + y[0]][x[1]-1 + y[1]])

    def connect(self, vals):
        for (x, y) in vals:
            # if x[0] <= self.n and x[0] > 0 and x[0] + y[0] <= self.n and x[0] + y[0] > 0:
            #     if x[1] <= self.m and x[1] > 0 and x[1] + y[1] <= self.m and x[1] + y[1] > 0:
            self.fields[x[0] - 1][x[1] - 1].connect(
                self.fields[x[0] - 1 + y[0]][x[1] - 1 + y[1]])

    def move(self, name, currentPos, nextPos, wall=None):
        if wall:
            if wall[0] == "Z":
                self.setGreenWall((wall[1], wall[2]))
            if wall[1] == "P":
                self.setBlueWall((wall[1], wall[2]))
        self.view.move(name, currentPos, nextPos, wall)
