class Field:
    def __init__(self, table, position, connectedX, connectedO, initialFor=None):
        self.table = table
        self.position = position
        self.initialFor = initialFor[0] if initialFor else None
        self.connectedX = set([x for x in connectedX])
        self.connectedO = set([o for o in connectedO])
        self.oneWayConnectedX = set()
        self.oneWayConnectedO = set()
        self.discWalls = set()
        self.nextHopToX = [(None, 99999), (None, 99999)]
        self.nextHopToO = [(None, 99999), (None, 99999)]

        match initialFor:
            case "X1":
                self.nextHopToX[0] = (self, 0)
            case "X2":
                self.nextHopToX[1] = (self, 0)
            case "O1":
                self.nextHopToO[0] = (self, 0)
            case "O2":
                self.nextHopToO[1] = (self, 0)

    def findNextHopToX(self, ind=0, f=None):
        change = False
        if f and f == self.nextHopToX[ind][0]:
            self.nextHopToX[ind] = (None, 99999)
            change = True
        for neighbour in self.connectedO:
            neighbourField = self.table.fields[neighbour[0]][neighbour[1]]
            if neighbourField.nextHopToX[ind][0] not in [self, None] and neighbourField.nextHopToX[ind][1] < (self.nextHopToX[ind][1]-1):
                self.nextHopToX[ind] = (
                    neighbourField, neighbourField.nextHopToX[ind][1] + 1)
                change = True
        if change:
            for n in self.connectedO | self.oneWayConnectedO:
                if not f or f.position != n:
                    self.table.fields[n[0]][n[1]].findNextHopToX(ind, self)

    def findNextHopToO(self, ind=0, f=None):
        change = False
        if f and f == self.nextHopToO[ind][0]:
            self.nextHopToO[ind] = (None, 99999)
            change = True
        for neighbour in self.connectedX:
            neighbourField = self.table.fields[neighbour[0]][neighbour[1]]
            if neighbourField.nextHopToO[ind][0] not in [self, None] and neighbourField.nextHopToO[ind][1] < (self.nextHopToO[ind][1]-1):
                self.nextHopToO[ind] = (
                    neighbourField, neighbourField.nextHopToO[ind][1] + 1)
                change = True
        if change:
            for n in self.connectedX | self.oneWayConnectedX:
                if not f or f.position != n:
                    self.table.fields[n[0]][n[1]].findNextHopToO(ind, self)

    def getShortestPathToX(self, ind=0):
        path = []
        try:
            nextHop = self
            while nextHop and nextHop.nextHopToX[ind][0] != nextHop:
                print(nextHop.position, nextHop.connectedO)
                path += [nextHop.position]
                nextHop = nextHop.nextHopToX[ind][0]
            path += [nextHop.position]
        except Exception as e:
            print(e)
        return path

    def getShortestPathToO(self, ind=0):
        path = []
        try:
            nextHop = self
            while nextHop and nextHop.nextHopToO[ind][0] != nextHop:
                print(nextHop.position, nextHop.connectedX)
                path += [nextHop.position]
                nextHop = nextHop.nextHopToO[ind][0]
            path += [nextHop.position]
        except Exception as e:
            print(e)
        return path

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def disconnect(self, f, w=None):
        if w:
            self.discWalls.add(f.position)
            if w == "Z":
                self.discWalls.add((f.position[0]+1, f.position[1]))
            else:
                self.discWalls.add((f.position[0], f.position[1]+1))
        self.disconnectX(f, w)
        self.disconnectO(f, w)

    def connectX(self, f, mirrored=True):
        if f.position not in self.connectedX | self.discWalls:
            self.connectedX.add(f.position)
            if mirrored:
                f.connectX(self)
            else:
                f.oneWayConnectedX.add(self.position)

    def disconnectX(self, f, w=None):
        if (w != None or (f.initialFor != "O" and self.initialFor != "O")):
            if f.position in self.connectedX:
                self.connectedX.discard(f.position)
                f.oneWayConnectedX.discard(self.position)
                f.disconnectX(self, w)
                if f is self.nextHopToO[0][0]:
                    self.nextHopToO[0] = (None, 99999)
                if f is self.nextHopToO[1][0]:
                    self.nextHopToO[1] = (None, 99999)
            elif f.position in self.oneWayConnectedX:
                f.disconnectX(self, w)

    def connectO(self, f, mirrored=True):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO.add(f.position)
            if mirrored:
                f.connectO(self)
            else:
                f.oneWayConnectedO.add(self.position)

    def disconnectO(self, f, w=None):
        if (w != None or (f.initialFor != "X" and self.initialFor != "X")):
            if f.position in self.connectedO:
                self.connectedO.remove(f.position)
                f.oneWayConnectedO.discard(self.position)
                f.disconnectO(self, w)
                if f is self.nextHopToX[0][0]:
                    self.nextHopToX[0] = (None, 99999)
                if f is self.nextHopToX[1][0]:
                    self.nextHopToX[1] = (None, 99999)
            elif f.position in self.oneWayConnectedO:
                f.disconnectO(self, w)
