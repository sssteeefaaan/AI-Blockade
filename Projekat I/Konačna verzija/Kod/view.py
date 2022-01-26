from termcolor import colored
import os
os.system('color')
color = {
    "X": "red",
    "O": "yellow"
}
class View:
    def __init__(self, n=11, m=14, greenWall="\u01c1", blueWall="\u2550", rowSep="\u23AF"):
        self.n = n
        self.m = m
        self.greenWall = greenWall
        self.blueWall = blueWall

        self.template = [
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55))) for j in range(1, m + 1)], "  "],
            [" ", *(" " + self.blueWall) * m, "  "],
            *[list((chr(i+48) if i < 10 else chr(i+55)) + self.greenWall + (" |") * (m - 1) + " " + self.greenWall + (chr(i+48) if i < 10 else chr(i+55)) + "\n" + " " + (" " + rowSep) * m + "  ") for i in range(1, n)],
            [(chr(n+48) if n < 10 else chr(n+55)), self.greenWall, *(" |") * (m - 1), " ", self.greenWall, (chr(n+48) if n < 10 else chr(n+55))],
            [" ", *(" " + self.blueWall) * m, "  "],
            [" ",  *[(" " + (chr(j+48) if j < 10 else chr(j+55))) for j in range(1, m + 1)], "  "]
        ]

    def showTable(self, greenWalls, blueWalls, players, xWallNumb=(9, 9), oWallNumb=(9, 9)):
        table = list()
        for t in self.template:
            table.append(list(t))

        for gw in greenWalls:
            table[gw[0] + 1] = table[gw[0] + 1][:(gw[1] << 1) + 1] + [colored(self.greenWall, "green")] + table[gw[0] + 1][(gw[1] + 1) << 1:]
            table[gw[0] + 2] = table[gw[0] + 2][:(gw[1] << 1) + 1] + [colored(self.greenWall, "green")] + table[gw[0] + 2][(gw[1] + 1) << 1:]

        for bw in blueWalls:
            table[bw[0] + 1] = table[bw[0] + 1][:(self.m + 2 + bw[1]) << 1] + [colored(self.blueWall, "blue")] + [" "] + [colored(self.blueWall, "blue")] + table[bw[0] + 1][((self.m + 2 + bw[1]) << 1) + 3:]

        for player in players.keys():
            for i in range(2):
                table[players[player][i][0] + 1] = table[players[player][i][0] + 1][:players[player][i][1]<< 1] + [colored(player, color[player])] + table[players[player][i][0] + 1][(players[player][i][1] << 1) + 1:]

        for r in table:
            for v in r:
                print(v, end="")
            print()
        print(f"\n\tWalls {colored('X', 'red')}\t\t|\tWalls {colored('O', 'yellow')}")
        print(f"\t{colored('B: ' + str(xWallNumb[0]), 'blue')}\t\t|\t{colored('B: ' + str(oWallNumb[0]), 'blue')}")
        print(f"\t{colored('G: ' + str(xWallNumb[1]), 'green')}\t\t|\t{colored('G: ' + str(oWallNumb[1]), 'green')}\n")
