class Vertex:
    def __init__(self, color) -> None:
        self.pixel_coordinates = set()
        self.color = color

    def add(self,x,y):
        self.pixel_coordinates.add((x,y)) 

    def remove(self,x,y):
        self.pixel_coordinates.remove((x,y))

    def get_size(self):
        return len(self.pixel_coordinates)