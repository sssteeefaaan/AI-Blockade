class Field:
    def __init__(self, table, position, initialFor, connectedX=set(), connectedO=set(), oneWayConnectedX=set(), oneWayConnectedO=set(), discWalls=set(), nextHopToX=[(None, 99999), (None, 99999)], nextHopToO=[(None, 99999), (None, 99999)]):
        self.table = table
        self.position = position
        self.initialFor = initialFor[0] if initialFor else None
        self.connectedX = set(connectedX)
        self.connectedO = set(connectedO)
        self.oneWayConnectedX = set(oneWayConnectedX)
        self.oneWayConnectedO = set(oneWayConnectedO)
        self.nextHopToX = list(nextHopToX)
        self.nextHopToO = list(nextHopToO)
        self.discWalls = set(discWalls)
        match initialFor:
            case "X1":
                self.nextHopToX[0] = (position, 0)
            case "X2":
                self.nextHopToX[1] = (position, 0)
            case "O1":
                self.nextHopToO[0] = (position, 0)
            case "O2":
                self.nextHopToO[1] = (position, 0)

    def getCopy(self, table):
        return Field(table, self.position, self.initialFor, self.connectedX, self.connectedO, self.oneWayConnectedX, self.oneWayConnectedO, self.discWalls, self.nextHopToX, self.nextHopToO)

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
            if w == "Z":
                self.discWalls.add((f.position[0]+1, f.position[1]))
            else:
                self.discWalls.add((f.position[0], f.position[1]+1))
        self.disconnectX(f, w)
        self.disconnectO(f, w)

    def disconnectX(self, f, w=None):
        if (w != None or (f.initialFor != "O" and self.initialFor != "O")):
            if f.position == self.nextHopToX[0][0]:
                self.annihilateNextHopToX(0)
            if f.position == self.nextHopToX[1][0]:
                self.annihilateNextHopToX(1)
            f.oneWayConnectedX.discard(self.position)
            if f.position in self.connectedX:
                self.connectedX.discard(f.position)
                f.disconnectX(self, w)
            elif f.position in self.oneWayConnectedX:
                f.disconnectX(self, w)

    def disconnectO(self, f, w=None):
        if (w != None or (f.initialFor != "X" and self.initialFor != "X")):
            if f.position == self.nextHopToO[0][0]:
                self.annihilateNextHopToO(0)
            if f.position == self.nextHopToO[1][0]:
                self.annihilateNextHopToO(1)
            f.oneWayConnectedO.discard(self.position)
            if f.position in self.connectedO:
                self.connectedO.remove(f.position)
                f.disconnectO(self, w)
            elif f.position in self.oneWayConnectedO:
                f.disconnectO(self, w)

    def annihilateNextHopToX(self, ind=0):
        if self.nextHopToX[ind][0] != self.position:
            self.nextHopToX[ind] = (None, 99999)
            for n in self.connectedO | self.oneWayConnectedO:
                if self.table.fields[n].nextHopToX[ind][0] == self.position:
                    self.table.fields[n].annihilateNextHopToX(ind)

    def annihilateNextHopToO(self, ind=0):
        if self.nextHopToO[ind][0] != self.position:
            self.nextHopToO[ind] = (None, 99999)
            for n in self.connectedX | self.oneWayConnectedX:
                if self.table.fields[n].nextHopToO[ind][0] == self.position:
                    self.table.fields[n].annihilateNextHopToO(ind)

    def notifyNextHopToX(self, f, ind=0, change=False):
        for n in self.connectedO:
            if self.table.fields[n].nextHopToX[ind][1] < (self.nextHopToX[ind][1]-1):
                self.nextHopToX[ind] = (
                    self.table.fields[n].position, self.table.fields[n].nextHopToX[ind][1]+1)
                change = True
        if change:
            for n in self.connectedO | self.oneWayConnectedO:
                if self.table.fields[n] != f:
                    self.table.fields[n].notifyNextHopToX(self, ind)

    def notifyNextHopToO(self, f, ind=0, change=False):
        for n in self.connectedX:
            if self.table.fields[n].nextHopToO[ind][1] < (self.nextHopToO[ind][1]-1):
                self.nextHopToO[ind] = (
                    self.table.fields[n].position, self.table.fields[n].nextHopToO[ind][1]+1)
                change = True
        if change:
            for n in self.connectedX | self.oneWayConnectedX:
                if self.table.fields[n] != f:
                    self.table.fields[n].notifyNextHopToO(self, ind)

    def getShortestPathToX(self, ind=0):
        path = []
        nextHop = self
        while nextHop != None:
            path += [nextHop.position]
            if nextHop != self.table.fields[nextHop.nextHopToX[ind][0]]:
                nextHop = self.table.fields[nextHop.nextHopToX[ind][0]]
            else:
                nextHop = None
        return path

    def getShortestPathToO(self, ind=0):
        path = []
        nextHop = self
        while nextHop != None:
            path += [nextHop.position]
            if nextHop != self.table.fields[nextHop.nextHopToO[ind][0]]:
                nextHop = self.table.fields[nextHop.nextHopToO[ind][0]]
            else:
                nextHop = None
        return path
