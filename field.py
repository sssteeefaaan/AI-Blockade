class Field:
    def __init__(self, i, j, connected, initialFor=None):
        self.i = i
        self.j = j
        self.initialFor = initialFor
        self.connectedX = set()
        self.connectedO = set()
        for c in connected:
            self.connectedX.add(c)
            self.connectedO.add(c)
        
    # ako je initialForX onda sve susede te pozicije dodajemo O, i suprotno za initalForO 
    # ako je initialForX onda iz connectedX izbaci putem disconnect f-je (sve susede iz manhattan pattern-a)

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

    