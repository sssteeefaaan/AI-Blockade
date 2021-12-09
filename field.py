class Field:
    def __init__(self, i, j, connectedX, connectedO, initialFor=None):
        self.i = i
        self.j = j
        self.initialFor = initialFor
        self.connectedX = set([x for x in connectedX])
        self.connectedO = set([o for o in connectedO])

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def disconnect(self, f):
        self.disconnectX(f)
        self.disconnectO(f)

    def connectX(self, f):
        if (f.i, f.j) not in self.connectedX:
            self.connectedX.add((f.i, f.j))
            f.connectX(self)

    def disconnectX(self, f):
        if (f.i, f.j) in self.connectedX:
            self.connectedX.remove((f.i, f.j))
            f.disconnectX(self)

    def connectO(self, f):
        if (f.i, f.j) not in self.connectedO:
            self.connectedO.add((f.i, f.j))
            f.connectO(self)

    def disconnectO(self, f):
        if (f.i, f.j) in self.connectedO:
            self.connectedO.remove((f.i, f.j))
            f.disconnectO(self)

    