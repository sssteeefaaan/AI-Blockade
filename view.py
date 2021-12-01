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
    
    def setPosition(self, i, j, placeholder=" "):
        self.template[i + 1] = self.template[i + 1][:j << 1] + placeholder + self.template[i + 1][(j << 1) + 1:]
        self.refresh()
        
    def setBlueWall(self, i, j):
        self.template[i + 1] = self.template[i + 1][:(self.m + 2 + j) << 1] + self.blueWall + " " + self.blueWall + self.template[i + 1][((self.m + 2 + j) << 1) + 3:]
        self.refresh()
        
    def setGreenWall(self, i, j):
        self.template[i + 1] = self.template[i + 1][:(j << 1) + 1] + self.greenWall + self.template[i + 1][(j + 1) << 1:]
        self.template[i + 2] = self.template[i + 2][:(j << 1) + 1] + self.greenWall + self.template[i + 2][(j + 1) << 1:]
        self.refresh()
        
    def refresh(self):
        for r in self.template:
            for v in r:
                print(v, end="")
            print()
            
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