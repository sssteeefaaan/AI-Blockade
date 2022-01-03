class Field:
    def __init__(
            self, table, position, initialFor, connectedX=set(),
            connectedO=set(),
            oneWayConnectedX=set(),
            oneWayConnectedO=set(),
            discWalls=set()):
        self.table = table
        self.position = position
        self.initialFor = initialFor[0] if initialFor else None
        self.connectedX = set(connectedX)
        self.connectedO = set(connectedO)
        self.oneWayConnectedX = set(oneWayConnectedX)
        self.oneWayConnectedO = set(oneWayConnectedO)
        self.discWalls = set(discWalls)

    def getCopy(self, table):
        return Field(table, self.position, self.initialFor, self.connectedX, self.connectedO,
                     self.oneWayConnectedX, self.oneWayConnectedO, self.discWalls)

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def connectX(self, f, mirrored=True):
        if f.position not in self.connectedX | self.discWalls:
            self.connectedX.add(f.position)
            if mirrored:
                f.connectX(self)
            else:
                f.oneWayConnectedX.add(self.position)

    def connectO(self, f, mirrored=True):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO.add(f.position)
            if mirrored:
                f.connectO(self)
            else:
                f.oneWayConnectedO.add(self.position)

    def disconnect(self, f, w=None):
        if w:
            self.discWalls.add(f.position)
            if w == "G":
                self.discWalls.add((f.position[0]+1, f.position[1]))
            else:
                self.discWalls.add((f.position[0], f.position[1]+1))
        self.disconnectX(f, w)
        self.disconnectO(f, w)

    def disconnectX(self, f, w=None):
        if (w != None or (f.initialFor != "O" and self.initialFor != "O")):
            f.oneWayConnectedX.discard(self.position)
            if f.position in self.connectedX:
                self.connectedX.discard(f.position)
                f.disconnectX(self, w)
            elif f.position in self.oneWayConnectedX:
                f.disconnectX(self, w)

    def disconnectO(self, f, w=None):
        if (w != None or (f.initialFor != "X" and self.initialFor != "X")):
            f.oneWayConnectedO.discard(self.position)
            if f.position in self.connectedO:
                self.connectedO.discard(f.position)
                f.disconnectO(self, w)
            elif f.position in self.oneWayConnectedO:
                f.disconnectO(self, w)
