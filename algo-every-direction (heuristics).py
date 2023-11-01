import glob
import subprocess
from PIL import Image
import numpy as np
import Element
import re
import numpy as np

image_path = "randomGraph50_80_bubbles.png"
folder_path = "newGood/"
iterations_folder_path ="iteration images/"
#colors in the image graph1
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red = (237, 28, 36)
color_green = (34, 177, 76)

#load in graph image
im = Image.open(folder_path + image_path)
im = im.convert('RGB')

#create list to store objects in
id = [[0 for i in range(im.size[0]) ] for i in range(im.size[1])]

#lists to store Vertices and Edges in
Vertices = []
Edges = []
Elements = []


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

while (iterations == 0 or pixel_changed > 0) and iterations <= 200:
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

                #center pixel tries to copy the element of the neighboor pixel
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

                
                #If the pixel has found no neighboor whose element it can copy it will create its own element.
                if id[j][i] == 0 and not(flag):

                    id[j][i] = Element.Element(tuple(np.random.choice(range(256), size=3)))
                    Elements.append(id[j][i])
                    pixel_changed += 1


                    """if pixel == color_black:
                        
                        id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                        Edges.append(id[j][i])
                        pixel_changed += 1
                    else:

                        id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                        Vertices.append(id[j][i])
                        pixel_changed += 1"""
                
                #add the pixels coordinates to the Edge/Vertex element
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

        for element in Elements:
            pixels = element.pixel_coordinates
            for pixel in pixels:
                image.putpixel(pixel, element.color)

        image.save(iterations_folder_path + iteration + ".png")
    print("Iteration:" + iteration)
    iterations +=1
    print("pixel changed:" + str(pixel_changed) + "\n")

make_gif("iteration images")


polished_Objects = []
count = 0
#clean objects list
for element in Elements:
       if not(element.get_size() == 0):
              count += 1
              element.index = str(count)
              polished_Objects.append(element)

Elements = polished_Objects.copy()

#detect circles/Verticies
e1 = 1
potential_Circle = []

for element in Elements:
    dimensions = element.getDimensions()
    if abs((dimensions[1] - dimensions[0]) - (dimensions[3] - dimensions[2])) <= e1:
        potential_Circle.append(element)
    else:
        Edges.append(element)

e2 = 0.15
for element in potential_Circle:
    dimensions = element.getDimensions()
    area = (dimensions[1] - dimensions[0]) * (dimensions[3] - dimensions[2])
    circle_area = element.get_size()

    if abs((circle_area/area) - (np.pi/4)) <= e2:
        Vertices.append(element)
    else:
        Edges.append(element)

#find connections
neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
for edge in Edges:
    for pixel in edge.pixel_coordinates:
        i,j = pixel
        neighbors = [[j - 1,i - 1],[j - 1,i],[j - 1,i + 1],[j,i - 1],[j,i + 1],[j + 1,i - 1],[j + 1,i],[j + 1,i + 1]]
        for y,x in neighbors:
            if id[y][x] in Vertices:
                edge.addConnection(id[y][x])

#edge splitting
wrong_Edges = []
for edge in Edges:
    if len(edge.Connections)>2:
        wrong_Edges.append(edge)
        Edges.remove(edge)

for edge in wrong_Edges:
    edge_verticies = edge.Connections
    remaining_verticies = edge_verticies.copy()
    for v1 in edge_verticies:
        remaining_verticies.remove(v1)
        for v2 in remaining_verticies:
            flag = 0
            v1_center = v1.getCenter()
            v2_center = v2.getCenter()
            edge_center = [int((v2_center[0] + v1_center[0])/2), int((v2_center[1] + v1_center[1])/2)]
            neighbors = [[edge_center[1] - 1,edge_center[0] - 1],[edge_center[1] - 1,edge_center[0]],[edge_center[1] - 1,edge_center[0] + 1],[edge_center[1],edge_center[0] - 1],[edge_center[1],edge_center[0] + 1],[edge_center[1] + 1,edge_center[0] - 1],[edge_center[1] + 1,edge_center[0]],[edge_center[1] + 1,edge_center[0] + 1],[edge_center[1],edge_center[0]]]
            for y,x in neighbors:
                if not(id[y][x] == edge):
                    flag += 1
            if(flag >=3):
                continue
            else:
                element = Element.Element((255,255,255))
                element.addConnection(v1)
                element.addConnection(v2)
                Edges.append(element)

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

string=""

with open(folder_path + image_path + ".struct", "r") as f:
    for line in f:
        vertecies = re.findall(r"\d+", line)
        vertex = vertecies[0]
        for v in vertecies[1:]:
            string += vertex + "," + v + "\n"

with open(image_path + ".csv", "w") as fu:
    fu.write(string)


#Heuristics:
not_isomorphic = False

print("\nCheck Order:")
def getOrder():
    with open(image_path +".csv", "r") as f:
        return int(f.readlines()[-1].split(",")[0]) + 1 #first vertex is 0

if len(Vertices) == getOrder():
    print(" Same Order")
else:
    print(" Not Same Order")
    not_isomorphic = True

print("\nCheck Size:")
def getSize():
    with open(image_path +".csv", "r") as f:
        return int(len(f.readlines()))/2

size = getSize()
if len(Edges) == size:
    print(" Same Size")
else:
    print(" Not Same Size")
    not_isomorphic = True

print("\nCheck Degree Sequence:")
if len(Edges)*2 == size*2: #Degree sequence equal to 2 times the size of the graph
    print(" Same Degree Sequence")
else:
    print(" Not Degree Sequence")
    not_isomorphic = True

print("\nNumber of connected components:")
#get component number for reference graph using DFS. https://www.baeldung.com/cs/graph-connected-components
component_count_reference = 0
visited = {}
adj = {}

with open(folder_path + image_path + ".struct", "r") as f:
    for line in f:
        vertecies = re.findall(r"\d+", line)
        vertex = int(vertecies[0])
        adj[vertex] = []
        for v in vertecies[1:]:
            adj[vertex].append(int(v))

for k in adj:
    visited[k] = False

def DFS(k):
    visited[k] = True
    for p in adj[k]:
        if not(visited[p]):
            DFS(p)

for k in visited:
    if not(visited[k]):
        DFS(k)
        component_count_reference += 1


#get component number for extracted graph using DFS.
component_count_extracted = 0
visited = {}
adj = {}

with open("graph.csv", "r") as f:
    for line in f:
        vertecies = re.findall(r"\d+", line)

        vertex = int(vertecies[0])
        visited[vertex] = False
        vertex2 = int(vertecies[1])
        visited[vertex2] = False

        if not(vertex in adj):
            adj[vertex] = []
        adj[vertex].append(vertex2)

        if not(vertex2 in adj):
            adj[vertex2] = []
        adj[vertex2].append(vertex)

for k in visited:
    if not(visited[k]):
        DFS(k)
        component_count_extracted += 1

if component_count_reference == component_count_extracted: 
    print(" Same Component Count")
else:
    print(" Not Same Component Count")
    not_isomorphic = True

if not(not_isomorphic):
    print("\ncompare Expected and Extracted: \n")
    result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --format csv --induced graph.csv "+ image_path +".csv"], shell=True, text=True, stdout = subprocess.PIPE)

    lines = result.stdout.splitlines()
    for line in lines:
        if line.startswith("status"):
            print(line)

    print("\ncompare Extracted and Expected: \n")
    result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --format csv --induced "+ image_path +".csv graph.csv"], shell=True, text=True, stdout = subprocess.PIPE)

    lines = result.stdout.splitlines()
    for line in lines:
        if line.startswith("status"):
            print(line)
else:
    print("The two graphs are not isomorphic")