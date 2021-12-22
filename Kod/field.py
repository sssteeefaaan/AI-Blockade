class Field:
    def __init__(self, position, connectedX, connectedO, canFinishX = (True, True), canFinishO = (True, True), initialFor=None):
        self.position = position
        self.initialFor = initialFor
        self.connectedX = set([x for x in connectedX])
        self.connectedO = set([o for o in connectedO])
        self.discWalls = set()
        self.canFinishX = canFinishX
        self.canFinishO = canFinishO

    def connect(self, f):
        self.connectX(f)
        self.connectO(f)

    def disconnect(self, f, w=None):
        if w:
            self.discWalls.add(f.position)
            if w=="Z":
                self.discWalls.add((f.position[0]+1, f.position[1]))
            else:
                self.discWalls.add((f.position[0], f.position[1]+1))
        self.disconnectX(f, w)
        self.disconnectO(f, w)

    def connectX(self, f, mirrored = True):
        if f.position not in self.connectedX | self.discWalls:
            self.connectedX.add(f.position)
            if mirrored:
                f.connectX(self)

    def disconnectX(self, f, w=None):
        if (w!=None or (f.initialFor!="O" and self.initialFor!="O")) and f.position in self.connectedX:
            self.connectedX.remove(f.position)
            f.disconnectX(self)
            # ukoliko se ukloni provera da li postoji bilo koje polje kojim bi moglo da se dodje do kraja
            # ukoliko ne postoji flag se postavi na False i svim njegovim susedima se kaze da je on False (ovo je nova f-ja)
            # ovo u oba disconnect-a, a za connect-ove slicna logika 

    def connectO(self, f, mirrored = True):
        if f.position not in self.connectedO | self.discWalls:
            self.connectedO.add(f.position)
            if mirrored:
                f.connectO(self)

    def disconnectO(self, f, w=None):
        if (w!=None or (f.initialFor!="X" and self.initialFor!="X")) and f.position in self.connectedO:
            self.connectedO.remove(f.position)
            f.disconnectO(self)