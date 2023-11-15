import numpy as np
class Element:
    def __init__(self, color) -> None:
        self.pixel_coordinates = set()
        self.color = color
        self.type = 0
        self.Connections = set()
        self.index = 0
        self.Neighbours = set()

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
        return str(self.index)

    def addConnection(self, object):
        self.Connections.add(object)

    def addNeighbour(self, vertex):
        self.Neighbours.add(vertex)

    def getNeighbours(self):
        if len(self.Neighbours)==0:
            return str(self.index) + " : { }"
        else:
            string = str(self.index) + " : {"
            for vertex in self.Neighbours:
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
    
    def getCenter(self):
        dimensions = self.getDimensions()
        center_x = (dimensions[1] + dimensions[0])/2
        center_y = (dimensions[3] + dimensions[2])/2

        return [center_x, center_y]
        