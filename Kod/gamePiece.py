class GamePiece:
    def __init__(self, position=(1, 1)):
        self.position = position
        self.home = position

    def move(self, position):
        prev = self.position
        self.position = position
        return prev
