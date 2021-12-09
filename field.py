class Field:
    def __init__(self, i, j, connectedX, connectedO, initialFor=None):
        self.i = i
        self.j = j
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
            self.discWalls.add((f.i,f.j))
            if w=="Z":
                self.discWalls.add((f.i+1,f.j))
            else:
                self.discWalls.add((f.i,f.j+1))

    def connectX(self, f):
        if (f.i, f.j) not in self.connectedX | self.discWalls:
            self.connectedX.add((f.i, f.j))
            f.connectX(self)

    def disconnectX(self, f, w=None):
        if (f.i, f.j) in self.connectedX:
            self.connectedX.remove((f.i, f.j))
            f.disconnectX(self)

    def connectO(self, f):
        if (f.i, f.j) not in self.connectedO | self.discWalls:
            self.connectedO.add((f.i, f.j))
            f.connectO(self)

    def disconnectO(self, f, w=None):
        if (f.i, f.j) in self.connectedO:
            self.connectedO.remove((f.i, f.j))
            f.disconnectO(self)

    