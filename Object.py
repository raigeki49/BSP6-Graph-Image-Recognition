class Object:
    def __init__(self, color) -> None:
        self.pixel_coordinates = set()
        self.color = color
        self.type = 0
        self.Connections = set()

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
    
    def __str__(self):
        if self.type == 0:
            return f"Object" + self.index
        elif self.type == 1:
            return f"Vertex" + self.index
        else:
            return f"Edge" + self.index
    
    def addConnection(self, object):
        self.Connections.add(object)