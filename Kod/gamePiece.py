class GamePiece:
    def __init__(self, home=(1, 1), position=(1, 1)):
        self.position = position
        self.home = home

    def move(self, position):
        prev = self.position
        self.position = position
        return prev

    def getCopy(self):
        return GamePiece(self.home, self.position)
