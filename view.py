from traceback import print_stack


class View:
    def __init__(self, n=11, m=14, wallNumb=9, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m
        self.greenWall = greenWall
        self.blueWall = blueWall

        self.template = [
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55)))
                     for j in range(1, m + 1)], "  "],
            [" ", *(" " + self.blueWall) * m, "  "],
            *[list((chr(i+48) if i < 10 else chr(i+55)) + self.greenWall + (" |") * (m - 1) + " " + self.greenWall +
                   (chr(i+48) if i < 10 else chr(i+55)) + "\n" + " " + (" " + rowSep) * m + "  ") for i in range(1, n)],
            [(chr(n+48) if n < 10 else chr(n+55)), self.greenWall, *(" |") *
             (m - 1), " ", self.greenWall, "{0:x}".format(n).upper()],
            [" ", *(" " + self.blueWall) * m, "  "],
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55)))
                     for j in range(1, m + 1)], "  "],
            ["Number of walls:"],
            ["*X:"],
            [" -P: ", wallNumb],
            [" -Z: ", wallNumb],
            ["*O:"],
            [" -P: ", wallNumb],
            [" -Z: ", wallNumb]
        ]

    def setPosition(self, i, j, placeholder=" ", refresh=False):
        try:
            self.template[i + 1] = self.template[i + 1][:j << 1] + \
                [placeholder] + self.template[i + 1][(j << 1) + 1:]
            if refresh:
                self.refresh()
        except Exception as e:
            print(e)

    def setBlueWall(self, i, j, wallNumbUpdate, refresh=False):
        try:
            self.template[i + 1] = self.template[i + 1][:(self.m + 2 + j) << 1] + [
                self.blueWall] + [" "] + [self.blueWall] + self.template[i + 1][((self.m + 2 + j) << 1) + 3:]
            self.template[-wallNumbUpdate][1]-=1
            if refresh:
                self.refresh()
        except Exception as e:
            print(e)

    def setGreenWall(self, i, j, wallNumbUpdate, refresh=False):
        try:
            self.template[i + 1] = self.template[i +
                                                 1][:(j << 1) + 1] + [self.greenWall] + self.template[i + 1][(j + 1) << 1:]
            self.template[i + 2] = self.template[i +
                                                 2][:(j << 1) + 1] + [self.greenWall] + self.template[i + 2][(j + 1) << 1:]
            self.template[-wallNumbUpdate][1]-=1
            if refresh:
                self.refresh()
        except Exception as e:
            print(e)

    def refresh(self):
        for r in self.template:
            for v in r:
                print(v, end="")
            print()

    def move(self, name, currentPos, nextPos, wall):
        try:
            self.setPosition(currentPos[0], currentPos[1])
            self.setPosition(nextPos[0], nextPos[1], name)
            if wall:
                if wall[0].upper() == 'Z':
                    self.setGreenWall(wall[1], wall[2], 1 + (3 if name=="X" else 0))
                elif wall[0].upper() == 'P':
                    self.setBlueWall(wall[1], wall[2], 2 + (3 if name=="X" else 0))
            self.refresh()
        except Exception as e:
            print(e)
