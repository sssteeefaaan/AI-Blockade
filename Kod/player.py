from gamePiece import GamePiece


class Player:
    def __init__(
            self, name, isComputer=False, wallNumb=(9, 9),
            initialPositions=(None, None),
            currentPositions=(None, None)):
        self.name = name
        self.firstGP = GamePiece(initialPositions[0], currentPositions[0])
        self.secondGP = GamePiece(initialPositions[1], currentPositions[1])
        self.noBlueWalls = wallNumb[0]
        self.noGreenWalls = wallNumb[1]
        self.isComputer = isComputer

    def getCopy(self):
        return Player(
            self.name, self.isComputer, self.getWallNumber(),
            self.getInitialPositions(),
            self.getCurrectPositions())

    def getInitialPositions(self):
        return (self.firstGP.home, self.secondGP.home)

    def getCurrectPositions(self):
        return (self.firstGP.position, self.secondGP.position)

    def getWallNumber(self):
        return (self.noBlueWalls, self.noGreenWalls)

    def isWinner(self, positions):
        return self.firstGP.position in positions or self.secondGP.position in positions

    def movePiece(self, gamePiece):
        if gamePiece['choice'] == 1:
            return self.firstGP.move(gamePiece['position'])
        return self.secondGP.move(gamePiece['position'])
