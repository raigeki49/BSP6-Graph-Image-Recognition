import numpy as np
class Object:
    def __init__(self, color) -> None:
        self.pixel_coordinates = set()
        self.color = color
        self.type = 0
        self.Connections = set()
        self.index = 0
        self.Verticies = set()

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
        """if self.type == 0:
            return f"Object" + self.index
        elif self.type == 1:
            return f"Vertex" + self.index
        else:
            return f"Edge" + self.index"""
        return str(self.index)

    def addConnection(self, object):
        self.Connections.add(object)

    def addVertex(self, vertex):
        self.Verticies.add(vertex)

    def getVerticies(self):
        if len(self.Verticies)==0:
            return str(self.index) + " : { }"
        else:
            string = str(self.index) + " : {"
            for vertex in self.Verticies:
                string += str(vertex) +", "
            return string[:-2] + "}"
        
    def getDimensions(self):
        min_y = np.inf
        max_y = 0
        min_x = np.inf
        max_x = 0
        for coor in self.pixel_coordinates:
            if coor[0]>max_x:
                max_x=coor[0]

            if coor[0]<min_x:
                min_x=coor[0]

            if coor[1]>max_y:
                max_y=coor[1]

            if coor[1]<min_y:
                min_y=coor[1]
            
        return [min_x, max_x, min_y, max_y]
        