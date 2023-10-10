import glob
from PIL import Image, ImageDraw
import numpy as np
import Vertex, Edge
import os

image_path = "goodGraphs/graph3.png"

folder_path ="iteration images/"
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

range_i = range(1,im.size[0] - 1)
range_j = range(1,im.size[1] - 1)

def flip_i(flip_i_index):
    global range_i
    range_i = range(1,im.size[0] - 1)
    if flip_i_index:
        range_i = range(im.size[0] - 1, 0, -1)

def flip_j(flip_j_index):
    global range_j
    range_j = range(1,im.size[1] - 1)
    if flip_j_index:
        range_j = range(im.size[1] - 1, 0, -1)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save("iterations.gif", format="GIF", append_images=frames,
               save_all=True, duration=300, loop=0)

#Identify the pixel
iterations = 0
pixel_changed = 0

while (iterations == 0 or pixel_changed > 0) and iterations <= 20:
    pixel_changed = 0

    for j in range_j:
        for i in range_i:
            pixel = im.getpixel((i,j))

            if not(pixel == color_white):

                flag = False

                #define in what order the neighbors should be checked
                if iterations%4==1:
                    neighbors = [[j - 1,i + 1],[j - 1,i],[j - 1,i - 1],[j,i + 1],[j,i - 1],[j + 1,i + 1],[j + 1,i],[j + 1,i - 1]]

                elif iterations%4==2:
                    neighbors = [[j + 1,i + 1],[j + 1,i],[j + 1,i - 1],[j,i + 1],[j,i - 1],[j - 1,i + 1],[j - 1,i],[j - 1,i - 1]]

                elif iterations%4==3:
                    neighbors = [[j + 1,i - 1],[j + 1,i],[j + 1,i + 1],[j,i - 1],[j,i + 1],[j - 1,i - 1],[j - 1,i],[j - 1,i + 1]]

                else:
                    neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]

                #center pixel tries to copy the object of the neighboor pixel
                for x,y in neighbors:
                    if (id[j][i] == 0 or iterations>0) and not(flag):
                        if (pixel == im.getpixel((y, x))) and not(id[x][y]==0):

                            if id[j][i] == 0 or id[j][i].compare(id[x][y]):
                                if not(id[j][i]==id[x][y]):
                                    if not(id[j][i]==0):
                                        id[j][i].remove(i,j)
                                    pixel_changed += 1
                                    id[j][i] = id[x][y]
                                    flag = True

                
                #If the pixel has found no neighboor whose object it can copy it will create its own object.
                if id[j][i] == 0 and not(flag):
                    if pixel == color_black:
                        
                        id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                        Edges.append(id[j][i])
                        pixel_changed += 1
                    else:

                        id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                        Vertices.append(id[j][i])
                        pixel_changed += 1
                
                #add the pixels coordinates to the Edge/Vertex object
                id[j][i].add(i,j)

                #Give neighbors the center pixels object
                """if n==0:
                    for x,y in neighbors:
                        if pixel == im.getpixel((y, x)):
                            if not(id[x][y]==0):
                                id[x][y].remove(y, x)
                            id[x][y] = id[j][i]
                            id[x][y].add(y, x)"""

    #change the direction with which we iterate through the pixels
    if iterations%4==1:
        flip_j(True)

    elif iterations%4==2:
        flip_i(False)

    elif iterations%4==3:
        flip_j(False)

    else:
        flip_i(True)
    
    iteration = str(iterations)
    if not(pixel_changed==0):

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

        image.save(folder_path + iteration + ".png")
    print("Iteration:" + iteration)
    iterations +=1
    print("pixel changed:" + str(pixel_changed) + "\n")



#make Edge and Vertex lists
polished_Edges = []
polished_Vertices = []
for edge in Edges:
       if not(edge.get_size() == 0):
              polished_Edges.append(edge)

for vertex in Vertices:
       if not(vertex.get_size() == 0):
              polished_Vertices.append(vertex)

#print(len(polished_Edges))
#print(len(polished_Vertices))

make_gif("iteration images")

neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]

for edge in polished_Edges:
    for pixel in edge.pixel_coordinates:
        #print(pixel)
        if not(edge.full):
            i,j = pixel
            neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
            for y,x in neighbors:
                if type(id[y][x])==Vertex.Vertex:
                    edge.addVertex(id[y][x])

G =[]
for edge in polished_Edges:
    G.append(edge.Verticies)

def render_digraph(G):
    def g():
        for p, c in G:
            yield  '"{}" -> "{}"'.format(p, c)

    lines = "\n".join(g())

    def f():
        for p, c in G:
            yield  '"{}" -> "{}"'.format(c, p)
    
    lines = lines + "\n".join(f())
    return """
    digraph {{
    {}
    }}
    """.format(lines)

with open("graph.dot", "w") as fo:
  fo.write(render_digraph(G))