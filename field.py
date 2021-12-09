class Field:
    def __init__(self, i, j, connected, initialFor=None):
        self.i = i
        self.j = j
        self.initialFor = initialFor
        self.connected = set()
        for c in connected:
            self.connected.add(c)

    def connect(self, f):
        if (f.i, f.j) not in self.connected:
            self.connected.add((f.i, f.j))
            f.connect(self)

    def disconnect(self, f):
        if (f.i, f.j) in self.connected:
            self.connected.remove((f.i, f.j))
            f.disconnect(self)
