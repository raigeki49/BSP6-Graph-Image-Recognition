from PIL import Image, ImageDraw
import numpy as np
import Vertex, Edge

image_path = "goodGraphs/graph3.png"

file_name = "first iteration"

#colors in the image graph1
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red = (237, 28, 36)
color_green = (34, 177, 76)

#load in graph image
im = Image.open(image_path)
im = im.convert('RGB')

#create list to store objects in
id = [[0 for i in range(im.size[0]) ] for i in range(im.size[1])]

#lists to store Vertices and Edges in
Vertices = []
Edges = []


#colors = {0}

#Define a way to change the order of iteration to improve subsequent passes
# def f(flip_i_index)
# range_i = range(1,im.size[1] - 1)
# if flip_i_index:
# 	range_i = range(im.size[1] - 1, 0, -1)
# for i in range(range_i):

#Identify the pixel
for j in range(1,im.size[1] - 1):
    for i in range(1,im.size[0] - 1):
        pixel = im.getpixel((i,j))

        if not(pixel == color_white):

            flag = False
            neighbors = [[j + 1,i + 1],[j + 1,i],[j + 1,i - 1],[j,i + 1],[j,i - 1],[j - 1,i + 1],[j - 1,i],[j - 1,i - 1]]

            #center pixel tries to copy the object of the neighboor pixel
            for x,y in neighbors:
                if id[j][i] == 0 and not(flag):
                    if (pixel == im.getpixel((y, x))) and not(id[x][y]==0):  
                        id[j][i] = id[x][y]
                        flag = True
            
            #If the pixel has found no neighboor whose object it can copy it will create its own object.
            if id[j][i] == 0 and not(flag):
                if pixel == color_black:
                    
                    id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                    #id[j][i] = Edge.Edge(pixel)
                    Edges.append(id[j][i])
                else:

                    id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                    #id[j][i] = Vertex.Vertex(pixel)
                    Vertices.append(id[j][i])
            
            #add the pixels coordinates to the Edge/Vertex object
            id[j][i].add(i,j)

            #Give neighbors the center pixels object
            for x,y in neighbors:

                if pixel == im.getpixel((y, x)):
                    if not(id[x][y]==0):
                        id[x][y].remove(y, x)
                    id[x][y] = id[j][i]
                    id[x][y].add(y, x)



  
#draw image
image = Image.new("RGB", im.size, (255, 255, 255))

for vertex in Vertices:
    pixels = vertex.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, vertex.color)

for edge in Edges:
    pixels = edge.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, edge.color)

image.save(file_name + ".png")

#make Edge and Vertex lists
polished_Edges = []
polished_Vertices = []
for edge in Edges:
       if not(edge.get_size() == 0):
              polished_Edges.append(edge)

for vertex in Vertices:
       if not(vertex.get_size() == 0):
              polished_Vertices.append(vertex)

print(len(polished_Edges))
print(len(polished_Vertices))