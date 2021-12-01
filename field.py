class Field:
    def __init__(self, i, j, connected, isInital= False):
        self.i = i
        self.j = j
        self.connected = []
    
    def setGreenWall(self, i, j):
        self.connected = list(filter(lambda x: x.i, self.connected))
        
    def setBlueWall(self, i, j):
        self.connected = list(filter(lambda x: x.i, self.connected))
        
    def setPlayer(self, i, j):
        self.connected = list(filter(lambda x: x.i, self.connected))
        