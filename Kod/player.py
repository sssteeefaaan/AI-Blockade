from gamePiece import GamePiece


class Player:
    def __init__(self, name, isComputer=False, wallNumb=(9, 9), initialPositions=(None, None), currentPositions=(None, None)):
        self.name = name
        self.firstGP = GamePiece(initialPositions[0], currentPositions[0])
        self.secondGP = GamePiece(initialPositions[1], currentPositions[1])
        self.noBlueWalls = wallNumb[0]
        self.noGreenWalls = wallNumb[1]
        self.isComputer = isComputer

    def getWallNumber(self):
        return (self.noBlueWalls, self.noGreenWalls)

    def getCurrectPositions(self):
        return (self.firstGP.position, self.secondGP.position)

    def getInitialPositions(self):
        return (self.firstGP.home, self.secondGP.home)

    def getCopy(self):
        return Player(self.name, self.isComputer, self.getWallNumber(), self.getInitialPositions(), self.getCurrectPositions())

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
