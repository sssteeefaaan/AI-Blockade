class View:
    def __init__(self, n=11, m=14, greenWall="\u01c1", blueWall="\u2550", rowSep = "\u23AF"):
        self.n = n
        self.m = m
        self.greenWall = greenWall
        self.blueWall = blueWall
        
        self.template = [
            [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
            [" ", *(" " + self.blueWall) * m, "  "],
            *[list("{0:x}".format(j).upper() + self.greenWall +  (" |") * (m - 1) + " " + self.greenWall + "{0:x}".format(j).upper() + "\n" + " " + (" " + rowSep)* m + "  ") for j in range(1, n)],
            ["{0:x}".format(n).upper(), self.greenWall, *(" |") * (m - 1), " ", self.greenWall, "{0:x}".format(n).upper()],
            [" ", *(" " + self.blueWall) * m, "  "],
            [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
        ]
        self.refresh()
    
    def setPosition(self, i, j, placeholder=" ", refresh = False):
        self.template[i + 1] = self.template[i + 1][:j << 1] + [placeholder] + self.template[i + 1][(j << 1) + 1:]
        if refresh:
            self.refresh()
        
    def setBlueWall(self, i, j, refresh = False):
        self.template[i + 1] = self.template[i + 1][:(self.m + 2 + j) << 1] + [self.blueWall] + " " + self.blueWall + self.template[i + 1][((self.m + 2 + j) << 1) + 3:]
        if refresh:
            self.refresh()
        
    def setGreenWall(self, i, j, refresh = False):
        self.template[i + 1] = self.template[i + 1][:(j << 1) + 1] + [self.greenWall] + self.template[i + 1][(j + 1) << 1:]
        self.template[i + 2] = self.template[i + 2][:(j << 1) + 1] + [self.greenWall] + self.template[i + 2][(j + 1) << 1:]
        if refresh:
            self.refresh()
        
    def refresh(self):
        for r in self.template:
            for v in r:
                print(v, end="")
            print()

    def move(self, current, next):
        self.setPosition(current[0], current[1])
        self.setPosition(next[0], next[1], placeholder = next[2])
        if next[3] != None:
            if next[3][0].upper() == 'Z':
                self.setGreenWall(next[3][1], next[3][2])
            elif next[3][0].upper() == 'P':
                self.setBlueWall(next[3][1], next[3][2])
        self.refresh()