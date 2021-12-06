class View:
    def __init__(self, n=11, m=14, greenWall="\u01c1", blueWall="\u2550", rowSep = "\u23AF"):
        self.n = n
        self.m = m
        self.greenWall = greenWall
        self.blueWall = blueWall
        
        self.template = [
            [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
            [" ", (" " + self.blueWall) * m, "  "],
            *["{0:x}".format(j).upper() + self.greenWall +  (" |") * (m - 1) + " " + self.greenWall + "{0:x}".format(j).upper() + "\n" +
            " " + (" " + rowSep)* m + "  " for j in range(1, n - 1)],
            *["{0:x}".format(n - 1).upper() + self.greenWall +  (" |") * (m - 1) + " " + self.greenWall + "{0:x}".format(n-1).upper()],
            [" ", (" " + self.blueWall) * m, "  "],
            [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
        ]
        self.refresh()
    
    def setPosition(self, i, j, placeholder=" ", refresh = False):
        self.template[i + 1] = self.template[i + 1][:j << 1] + placeholder + self.template[i + 1][(j << 1) + 1:]
        if refresh:
            self.refresh()
        
    def setBlueWall(self, i, j, refresh = False):
        self.template[i + 1] = self.template[i + 1][:(self.m + 2 + j) << 1] + self.blueWall + " " + self.blueWall + self.template[i + 1][((self.m + 2 + j) << 1) + 3:]
        if refresh:
            self.refresh()
        
    def setGreenWall(self, i, j, refresh = False):
        self.template[i + 1] = self.template[i + 1][:(j << 1) + 1] + self.greenWall + self.template[i + 1][(j + 1) << 1:]
        self.template[i + 2] = self.template[i + 2][:(j << 1) + 1] + self.greenWall + self.template[i + 2][(j + 1) << 1:]
        if refresh:
            self.refresh()
        
    def refresh(self):
        for r in self.template:
            for v in r:
                print(v, end="")
            print()

    def move(self, current, next):
        self.setPosition(current[0], current[1])
        self.setPosition(next[0], next[1], next[2])
        if next[3] != None:
            if next[3][0].lower() == 'z':
                self.setGreenWall(next[3][1], next[3][2])
            elif next[3][0].lower() == 'p':
                self.setBlueWall(next[3][1], next[3][2])
        self.refresh()
            
def main():
    proba = View()
    while True:
        proba.setPosition(int(input("Unesite vrstu: ")), int(input("Unesite kolonu: ")), input("Unesite igraca: "))
        if input("Unesite vrstu zida: ").upper() == "P":
            proba.setBlueWall(int(input("Unesite vrstu plavog: ")), int(input("Unesite kolonu: ")))
        else:
            proba.setGreenWall(int(input("Unesite vrstu zelenog: ")), int(input("Unesite kolonu: ")))

if __name__ == "__main__":
    main()