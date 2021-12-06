from gamePiece import GamePiece


class Player:
    def __init__(self, playsFirst=True, isComputer=False, noBlueWalls = 9, noGreenWalls = 9, initialPos1st = None, initialPos2nd=None):
        if playsFirst:
            self.firstGP = GamePiece(initialPos1st if initialPos1st else (4, 4))
            self.secondGP = GamePiece(initialPos2nd if initialPos2nd else (8, 4))
            self.name = 'X'
        else:
            self.firstGP = GamePiece(initialPos1st if initialPos1st else (4, 11))
            self.secondGP = GamePiece(initialPos2nd if initialPos2nd else (8, 11))
            self.name = 'O'
        
        self.noBlueWalls = noBlueWalls
        self.noGreenWalls = noGreenWalls
        
        self.isComputer = isComputer
    
    def move(self, positon, pieceNum, wall = None):
        prevPos = None
        if pieceNum == 1:
            prevPos = self.firstGP.position
            self.firstGP.position=positon
        else:
            prevPos = self.secondGP.position
            self.secondGP.position=positon
        
        if wall != None:
            if wall[0].lower() == 'z':
                self.noGreenWalls -= 1
            elif wall[0].lower() == 'p':
                self.noBlueWalls -= 1

        return prevPos

    def isLooser(self, positions):
        return (self.firstGP.position in positions or self.secondGP.position in positions)

    
    