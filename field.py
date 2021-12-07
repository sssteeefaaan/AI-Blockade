class Field:
    def __init__(self, i, j, connected, isInital=False):
        self.i = i
        self.j = j
        self.connected = set()

    def connect(self, f: Field):
        if (f.i, f.i) not in self.connected:
            self.connected.add((f.i, f.i))
            f.connect(self)
    
    def disconnect(self, f: Field):
        if (f.i, f.i) in self.connected:
            self.connected.remove((f.i, f.i))
            f.disconnect(self)
