class Field:
    def __init__(self, position, connectedX, connectedO, initialFor=None):
        self.position = position
        self.initialFor = initialFor
        self.connectedX = set([x for x in connectedX])
        self.connectedO = set([o for o in connectedO])
        self.discWalls = set()

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def disconnect(self, f, w=None):
        self.disconnectX(f, w)
        self.disconnectO(f, w)
        if w:
            self.discWalls.add(f.position)
            if w=="Z":
                self.discWalls.add((f.position[0]+1, f.position[1]))
            else:
                self.discWalls.add((f.position[0], f.position[1]+1))

    def connectX(self, f):
        if f.position not in self.connectedX | self.discWalls:
            self.connectedX.add(f.position)
            f.connectX(self)

    def disconnectX(self, f, w=None):
        if (w!=None or (f.initialFor!="O" and self.initialFor!="O")) and f.position in self.connectedX:
            self.connectedX.remove(f.position)
            f.disconnectX(self)

    def connectO(self, f):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO.add(f.position)
            f.connectO(self)

    def disconnectO(self, f, w=None):
        if (w!=None or (f.initialFor!="X" and self.initialFor!="X")) and f.position in self.connectedO:
            self.connectedO.remove(f.position)
            f.disconnectO(self)