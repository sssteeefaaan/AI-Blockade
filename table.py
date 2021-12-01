from field import Field


class Table:
    def __init__(self, n=11, m=14, initial={(4, 4): 'X', (8, 4): 'X', (4, 11): 'O', (8, 11): 'O'}):
        self.n = n
        self.m = m

        self.fields = []
        for i in range(0, self.n):
            self.fields.append([])
            for j in range(0, self.m):
                self.fields[i].append(Field(i, j, None, initial.get((i, j), False)))

    def setBlueWall(self):
        raise "Not implemented!"
    
    def setGreenWall(self):
        raise "Not implemented!"