from gamePiece import GamePiece


class Player:
    def __init__(self, playsFirst=True, isComputer=False, noBlueWalls = 9, noGreenWalls = 9, initialPos1st = None, initialPos2nd=None):
        if playsFirst:
            self.firstGP = GamePiece("X", initialPos1st if initialPos1st else (4, 4))
            self.secondGP = GamePiece("X", initialPos2nd if initialPos2nd else (8, 4))
        else:
            self.firstGP = GamePiece("O", initialPos1st if initialPos1st else (4, 11))
            self.secondGP = GamePiece("O", initialPos2nd if initialPos2nd else (8, 11))
        
        self.noBlueWalls = noBlueWalls
        self.noGreenWalls = noGreenWalls
        
        self.isComputer = isComputer
    
    def move(self, positon, is1st, wallColor=None):
        if is1st:
            self.firstGP.position=positon
        else:
            self.secondGP.position=positon
            
        if wallColor=='green':
            self.noGreenWalls-=1
        elif wallColor=='blue':
            self.noBlueWalls -=1
    
    