from field import Field


class Table:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}):
        self.n = n
        self.m = m

        self.blueWalls = set()
        self.greenWalls = set()

        self.fields = []
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
                    
                # Connected X i connected Ox ????
                # Initial se razlikuju i na svoje inital ne mogu da stanu, ali na tudje initial mogu i to cak ukoliko je
                # udaljeno 1
                self.fields[i].append(Field(i, j, connected, initial.get((i, j), False)))

    # x1   x2   x3   x4                         x1   x2   x3   x4       => x6 gubi vezu sa x9, x10, x11 i x14
    #                                                                   => x7 gubi vezu sa x10, x11, x12, x15
    # x5   x6   x7   x8   = BlueWall(x6) =>     x5   x6   x7   x8       => x5 gubi vezu sa x10
    #                                                =======            => x8 gubi vezu sa x11
    # x9   x10  x11  x12                        x9   x10  x11  x12      => x2 gubi vezu sa x10
    #                                                                   => x3 gubi vezu sa x11
    # x13  x14  x15  x16                        x13  x14  x15  x16      => x14 dobija vezu sa x10
    #                                                                   => x15 dobija vezu sa x11
    #                                                                   => x2 dobija vezu sa x6
    #                                                                   => x3 dobija vezu sa x7
    def setBlueWall(self, pos):
        if pos not in self.greenWalls:
            if not [x for x in [(pos[0] - 1, pos[1]), pos, (pos[0] + 1, pos[1])] if x in self.blueWalls]:
                self.blueWalls.add(pos)
                forDisconnect = []
                forConnect = []
                # if pos[0] + 1 <= self.n:
                #     forDisconnect += [(pos, x) for x in [(pos[0] + 1, pos[1] + y) for y in range(-1, 2) if pos[1] + y <= self.m and pos[1] + y > 0]]
                #     if pos[0] + 2 <= self.n:
                #         forDisconnect += [(pos, (pos[0] + 2, pos[1]))]
                # if pos[1] + 1 <= self.m:
                #     if pos[0] + 1 <= self.n:
                #         forDisconnect += [((pos[0], pos[1] + 1), x) for x in [(pos[0] + 1, pos[1] + y) for y in range(1, 3) if pos[1] + y <= self.m and pos[1] + y > 0]]
                #         if pos[0] + 2 <= self.n:
                #             forDisconnect += [((pos[0], pos[1] + 1), (pos[0] + 2, pos[1] + 1))]
                # if pos[1] - 1 > 0:
                #     forDisconnect += [((pos[0] + 1, pos[1]), (pos[0], pos[1] - 1))]
                # [(pos, x) for x in [(pos[0], pos[1] - 1), (pos[0], pos[1] - 1), (pos[0], pos[1] - 1), (pos[0], pos[1] - 1)]]

                self.disconnect(forDisconnect)
                self.connect(forConnect)
                return True
        return False

    # x1   x2   x3   x4                         x1   x2    x3   x4      => x6 gubi vezu sa x3, x7, x11 i x8
    #                                                                   => x10 gubi vezu sa x7, x11, x15, x12
    # x5   x6   x7   x8   = GreenWall(x6) =>    x5   x6  H x7   x8      => x2 gubi vezu sa x7
    #                                                    H              => x14 gubi vezu sa x11
    # x9   x10  x11  x12                        x9   x10 H x11  x12     => x9 gubi vezu sa x11
    #                                                                   => x5 gubi vezu sa x7
    # x13  x14  x15  x16                        x13  x14   x15  x16     => x8 gubi vezu sa x6
    #                                                                   => x12 gubi vezu sa x10
    #                                                                   => x9 dobija vezu sa x10
    #                                                                   => x5 dobija vezu sa x6
    #                                                                   => x8 dobija vezu sa x7
    #                                                                   => x12 dobija vezu sa x11
    def setGreenWall(self, pos):
        if pos not in self.blueWalls:
            if not [x for x in [(pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1)] if x in self.greenWalls]:
                self.greenWalls.add(pos)
                forDisconnect = []
                forConnect = []
                #
                # Implement
                #
                self.disconnect(forDisconnect)
                self.connect(forConnect)
                return True
        return False

    def disconnect(self, vals):
        for (x, y) in vals:
            if x[0] <= self.n and x[0] > 0 and x[0] + y[0] <= self.n and x[0] + y[0] > 0:
                if x[1] <= self.m and x[1] > 0 and x[1] + y[1] <= self.m and x[1] + y[1] > 0:
                    self.fields[x[0]][x[1]].disconnect(
                        self.fields[x[0] + y[0]][x[1] + y[1]])

    def connect(self, vals):
        for (x, y) in vals:
            if x[0] <= self.n and x[0] > 0 and x[0] + y[0] <= self.n and x[0] + y[0] > 0:
                if x[1] <= self.m and x[1] > 0 and x[1] + y[1] <= self.m and x[1] + y[1] > 0:
                    self.fields[x[0]][x[1]].connect(
                        self.fields[x[0] + y[0]][x[1] + y[1]])
