def showTable(n=11, m=14, verticalWall="\u01c1", horizontalWall="\u2550", rowSep = "\u23AF"):
    table = [
        [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
        [" ", (" " + horizontalWall) * m, "  "],
        *["{0:x}".format(j).upper() + verticalWall +  (" |") * (m - 1) + " " + verticalWall + "{0:x}".format(j).upper() + "\n" +
          " " + (" " + rowSep)* m + "  " for j in range(1, n - 1)],
        *["{0:x}".format(n - 1).upper() + verticalWall +  (" |") * (m - 1) + " " + verticalWall + "{0:x}".format(n-1).upper()],
        [" ", (" " + horizontalWall) * m, "  "],
        [" ",  *[(" {0:x}".format(i).upper()) for i in range(1, m + 1)], "  "],
    ]
    
        
    table[5] = table[5][:4] + "X" + table[5][5:]
    for r in table:
        for v in r:
            print(v, end="")
        print()
showTable()
