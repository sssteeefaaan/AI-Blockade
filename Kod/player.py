from gamePiece import GamePiece


class Player:
    def __init__(self, name, isComputer=False, wallNumb=9, initialPos1st=None, initialPos2nd=None):
        if name == "X":
            initial1st = initialPos1st if initialPos1st else (4, 4)
            initial2nd = initialPos2nd if initialPos2nd else (8, 4)
        else:
            initial1st = initialPos1st if initialPos1st else (4, 11)
            initial2nd = initialPos2nd if initialPos2nd else (8, 11)
        self.name = name
        self.firstGP = GamePiece(initial1st)
        self.secondGP = GamePiece(initial2nd)
        self.noBlueWalls = wallNumb
        self.noGreenWalls = wallNumb
        self.isComputer = isComputer

    def getWallNumber(self):
        return (self.noBlueWalls, self.noGreenWalls)

    def getPositions(self):
        return (self.firstGP.position, self.secondGP.position)

    def move(self, pieceNum, positon, wall=None):
        if pieceNum == 1:
            prevPos = self.firstGP.move(positon)
        else:
            prevPos = self.secondGP.move(positon)
        if wall != None:
            if wall[0].upper() == "Z":
                self.noGreenWalls -= 1
            elif wall[0].upper() == "P":
                self.noBlueWalls -= 1
        return prevPos

    def isWinner(self, positions):
        return self.firstGP.position in positions or self.secondGP.position in positions
