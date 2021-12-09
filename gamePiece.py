class GamePiece:
    def __init__(self, position=(1, 1)):
        self.position = position
    
    def move(self, position:tuple[int, int]):
        self.position = position