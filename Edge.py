class Edge:
    def __init__(self, color) -> None:
        self.pixel_coordinates = set()
        self.color = color
        self.Verticies = set()
        self.full = False
        self.index = 0

    def compare(self, other):
        if self.color < other.color:
            return False
        else:
            return True
        
    def add(self,x,y):
        self.pixel_coordinates.add((x,y)) 

    def remove(self,x,y):
        self.pixel_coordinates.remove((x,y))

    def get_size(self):
        return len(self.pixel_coordinates)
    
    def addVertex(self, vertex):
        self.Verticies.add(vertex)
        
        if len(self.Verticies) == 2:
            self.full = True

    def __str__(self):
        return f"Edge" + self.index