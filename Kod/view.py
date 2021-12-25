class View:
    def __init__(self, n=11, m=14, wallNumb={'xBlue': 9, 'xGreen': 9, 'oBlue': 9, 'oGreen': 9}, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m
        self.greenWall = greenWall
        self.blueWall = blueWall
        self.wallNumb = dict(wallNumb)

        self.template = [
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55)))
                     for j in range(1, m + 1)], "  "],
            [" ", *(" " + self.blueWall) * m, "  "],
            *[list((chr(i+48) if i < 10 else chr(i+55)) + self.greenWall + (" |") * (m - 1) + " " + self.greenWall +
                   (chr(i+48) if i < 10 else chr(i+55)) + "\n" + " " + (" " + rowSep) * m + "  ") for i in range(1, n)],
            [(chr(n+48) if n < 10 else chr(n+55)), self.greenWall, *(" |") *
             (m - 1), " ", self.greenWall, (chr(n+48) if n < 10 else chr(n+55))],
            [" ", *(" " + self.blueWall) * m, "  "],
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55)))
                     for j in range(1, m + 1)], "  "]
        ]

    def setPosition(self, i, j, placeholder=" ", refresh=False):
        self.template[i + 1] = self.template[i + 1][:j << 1] + \
            [placeholder] + self.template[i + 1][(j << 1) + 1:]
        if refresh:
            self.refresh()

    def setBlueWall(self, i, j, wallUpdate, refresh=False):
        self.template[i + 1] = self.template[i + 1][:(self.m + 2 + j) << 1] + [
            self.blueWall] + [" "] + [self.blueWall] + self.template[i + 1][((self.m + 2 + j) << 1) + 3:]
        self.wallNumb[wallUpdate] -= 1
        if refresh:
            self.refresh()

    def setGreenWall(self, i, j, wallUpdate, refresh=False):
        self.template[i + 1] = self.template[i +
                                             1][:(j << 1) + 1] + [self.greenWall] + self.template[i + 1][(j + 1) << 1:]
        self.template[i + 2] = self.template[i +
                                             2][:(j << 1) + 1] + [self.greenWall] + self.template[i + 2][(j + 1) << 1:]
        self.wallNumb[wallUpdate] -= 1
        if refresh:
            self.refresh()

    def refresh(self):
        for r in self.template:
            for v in r:
                print(v, end="")
            print()
        print("\n\tWalls X\t\t|\tWalls O")
        print(
            f"\tB: {self.wallNumb['xBlue']}\t\t|\tB: {self.wallNumb['oBlue']}")
        print(
            f"\tG: {self.wallNumb['xGreen']}\t\t|\tG: {self.wallNumb['oGreen']}\n")

    def move(self, name, currentPos, nextPos, wall):
        self.setPosition(currentPos[0], currentPos[1])
        self.setPosition(nextPos[0], nextPos[1], name)
        if wall:
            if wall[0].upper() == 'Z':
                self.setGreenWall(wall[1], wall[2], name.lower()+"Green")
            elif wall[0].upper() == 'P':
                self.setBlueWall(wall[1], wall[2], name.lower()+"Blue")
        self.refresh()
