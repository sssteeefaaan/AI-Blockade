class Field:
    def __init__(self, table, position, connectedX, connectedO, initialFor=None):
        self.table = table
        self.position = position
        self.initialFor = initialFor[0] if initialFor else None
        self.connectedX = set([x for x in connectedX])
        self.connectedO = set([o for o in connectedO])
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

    def findNextHopToX(self, ind=0):
        change = False
        for neighbour in self.connectedO:
            neighbourField = self.table.fields[neighbour[0]][neighbour[1]]
            if neighbourField.nextHopToX[ind][0] not in [self, None] and neighbourField.nextHopToX[ind][1] < (self.nextHopToX[ind][1]-1):
                self.nextHopToX[ind] = (
                    neighbourField, neighbourField.nextHopToX[ind][1] + 1)
                change = True
        if change:
            for n in [x for x in self.connectedO if x is not self.nextHopToX[ind][0]]:
                self.table.fields[n[0]][n[1]].findNextHopToX(ind)

    def findNextHopToO(self, ind=0):
        change = False
        for neighbour in self.connectedX:
            neighbourField = self.table.fields[neighbour[0]][neighbour[1]]
            if neighbourField.nextHopToO[ind][0] not in [self, None] and neighbourField.nextHopToO[ind][1] < (self.nextHopToO[ind][1]-1):
                self.nextHopToO[ind] = (
                    neighbourField, neighbourField.nextHopToO[ind][1] + 1)
                change = True
        if change:
            for n in [x for x in self.connectedX if x is not self.nextHopToO[ind][0]]:
                self.table.fields[n[0]][n[1]].findNextHopToO(ind)

    def getShortestPathToX(self, ind=0):
        path = []
        nextHop = self
        while nextHop.nextHopToX[ind][0] != nextHop:
            path += [nextHop.position]
            nextHop = nextHop.nextHopToX[ind][0]
        path += [nextHop.position]
        return path

    def getShortestPathToO(self, ind=0):
        path = []
        nextHop = self
        while nextHop.nextHopToO[ind][0] != nextHop:
            path += [nextHop.position]
            nextHop = nextHop.nextHopToO[ind][0]
        path += [nextHop.position]
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
            if f is self.nextHopToO[0][0]:
                self.nextHopToO[0] = (None, 99999)
                self.findNextHopToO(0)
            if f is self.nextHopToO[1][0]:
                self.nextHopToO[1] = (None, 99999)
                self.findNextHopToO(1)

    def disconnectX(self, f, w=None):
        if (w != None or (f.initialFor != "O" and self.initialFor != "O")) and f.position in self.connectedX:
            self.connectedX.remove(f.position)
            f.disconnectX(self, w)
            if f is self.nextHopToO[0][0]:
                self.nextHopToO[0] = (None, 99999)
            if f is self.nextHopToO[1][0]:
                self.nextHopToO[1] = (None, 99999)

    def connectO(self, f, mirrored=True):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO.add(f.position)
            if mirrored:
                f.connectO(self)

    def disconnectO(self, f, w=None):
        if (w != None or (f.initialFor != "X" and self.initialFor != "X")) and f.position in self.connectedO:
            self.connectedO.remove(f.position)
            f.disconnectO(self, w)
            if f is self.nextHopToX[0][0]:
                self.nextHopToX[0] = (None, 99999)
            if f is self.nextHopToX[1][0]:
                self.nextHopToX[1] = (None, 99999)
