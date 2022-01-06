class Field:
    def __init__(
            self, position, initialFor, connectedX=frozenset(),
            connectedO=frozenset(),
            oneWayConnectedX=frozenset(),
            oneWayConnectedO=frozenset(),
            discWalls=frozenset()):
        self.position = position
        self.initialFor = initialFor[0] if initialFor else None
        self.connectedX = frozenset(connectedX)
        self.connectedO = frozenset(connectedO)
        self.oneWayConnectedX = frozenset(oneWayConnectedX)
        self.oneWayConnectedO = frozenset(oneWayConnectedO)
        self.discWalls = frozenset(discWalls)

    def getCopy(self):
        return Field(self.position, self.initialFor, self.connectedX, self.connectedO,
                     self.oneWayConnectedX, self.oneWayConnectedO, self.discWalls)

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def connectX(self, f, mirrored=True):
        if f.position not in self.connectedX | self.discWalls:
            self.connectedX |= frozenset({f.position})
            if mirrored:
                f.connectX(self)
            else:
                f.oneWayConnectedX |= frozenset({self.position})

    def connectO(self, f, mirrored=True):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO |= frozenset({f.position})
            if mirrored:
                f.connectO(self)
            else:
                f.oneWayConnectedO |= frozenset({self.position})

    def disconnect(self, f, w=None):
        if w:
            self.discWalls |= frozenset({f.position})
            if w == "G":
                self.discWalls |= frozenset({(f.position[0]+1, f.position[1])})
            else:
                self.discWalls |= frozenset({(f.position[0], f.position[1]+1)})
        self.disconnectX(f, w)
        self.disconnectO(f, w)

    def disconnectX(self, f, w=None):
        if (w != None or (f.initialFor != "O" and self.initialFor != "O")):
            f.oneWayConnectedX = f.oneWayConnectedX.difference(frozenset({self.position}))
            if f.position in self.connectedX:
                self.connectedX = self.connectedX.difference(frozenset({f.position}))
                f.disconnectX(self, w)
            elif f.position in self.oneWayConnectedX:
                f.disconnectX(self, w)

    def disconnectO(self, f, w=None):
        if (w != None or (f.initialFor != "X" and self.initialFor != "X")):
            f.oneWayConnectedO = f.oneWayConnectedO.difference(frozenset({self.position}))
            if f.position in self.connectedO:
                self.connectedO = self.connectedO.difference(frozenset({f.position}))
                f.disconnectO(self, w)
            elif f.position in self.oneWayConnectedO:
                f.disconnectO(self, w)
