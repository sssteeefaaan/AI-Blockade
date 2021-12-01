class GamePiece:
    def __init__(self, char="X", initalPosition=(1, 1)):
        self.char = char
        self.position = initalPosition
    
    def move(self, position:tuple[int, int]):
        self.position = position