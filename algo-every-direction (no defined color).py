import glob
import subprocess
from PIL import Image
import numpy as np
import Object

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
Objects = []


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

                    id[j][i] = Object.Object(tuple(np.random.choice(range(256), size=3)))
                    Objects.append(id[j][i])
                    pixel_changed += 1


                    """if pixel == color_black:
                        
                        id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                        Edges.append(id[j][i])
                        pixel_changed += 1
                    else:

                        id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                        Vertices.append(id[j][i])
                        pixel_changed += 1"""
                
                #add the pixels coordinates to the Edge/Vertex object
                id[j][i].add(i,j)

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

        for object in Objects:
            pixels = object.pixel_coordinates
            for pixel in pixels:
                image.putpixel(pixel, object.color)

        image.save(folder_path + iteration + ".png")
    print("Iteration:" + iteration)
    iterations +=1
    print("pixel changed:" + str(pixel_changed) + "\n")

make_gif("iteration images")


polished_Objects = []
count = 0
#clean Bbjects list
for object in Objects:
       if not(object.get_size() == 0):
              count += 1
              object.index = str(count)
              polished_Objects.append(object)

Objects = polished_Objects.copy()

neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
for object in polished_Objects:
    for pixel in object.pixel_coordinates:
        i,j = pixel
        neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
        for y,x in neighbors:
            if not(id[y][x]==object) and not(id[y][x]==0):
                object.addConnection(id[y][x])

Objects = polished_Objects.copy()

for object in Objects:
    if len(object.Connections) == 1 or len(object.Connections) > 2:
        Vertices.append(object)
        object.type = 1
        polished_Objects.remove(object)

Objects = polished_Objects.copy()
flag = False
for object in Objects:
    flag = False
    for pixel in object.pixel_coordinates:
        i,j = pixel
        neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
        for y,x in neighbors:
            if not(id[y][x]==0) and id[y][x].type==1 and not(flag):
                Edges.append(object)
                object.type = 2
                polished_Objects.remove(object)
                flag = True

Objects = polished_Objects.copy()

for object in Objects:
    Vertices.append(object)
    object.type = 1
    polished_Objects.remove(object)

G =[]
for edge in Edges:
    G.append(edge.Connections)

def render_digraph(G): #https://gist.github.com/sidharthkuruvila/f59b38215316c0cf6f7d18d21347e504
    def g():
        for p, c in G:
            yield  '{},{}'.format(p, c)

    lines = "\n".join(g())
    return """{}""".format(lines)

with open("graph.csv", "w") as fo:
  fo.write(render_digraph(G))

print("\ncompare Expected and Extracted: \n")
result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --induced --format csv graph.csv graph2.csv"], shell=True, text=True)
print(result.stdout)

print("\ncompare Extracted and Expected: \n")
result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --induced --format csv graph.csv graph2.csv"], shell=True, text=True)
print(result.stdout)