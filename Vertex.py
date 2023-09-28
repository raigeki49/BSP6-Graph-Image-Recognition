class Vertex:
    def __init__(self, color) -> None:
        self.pixel_coordinates = []
        self.color = color

    def add(self,x,y):
        self.pixel_coordinates.append((x,y)) 

    def remove(self,x,y):
        self.pixel_coordinates.remove((x,y))