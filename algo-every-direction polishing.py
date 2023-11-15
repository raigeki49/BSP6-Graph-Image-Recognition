import glob
from PIL import Image
import numpy as np
import Element
import re
import numpy as np
import IsomorphismTests

image_path1 = "randomGraph50_80 copy.png"
image_path2 = "randomGraph50_80.png"
folder_path = "newGood/"
iterations_folder_path ="iteration images/"

#functions to switch the order
def flip_i(flip_i_index, img_dimensions):

    range_i = range(1,img_dimensions[0] - 1)
    if flip_i_index:
        range_i = range(img_dimensions[0] - 1, 0, -1)
    
    return range_i

def flip_j(flip_j_index, img_dimensions):

    range_j = range(1,img_dimensions[1] - 1)
    if flip_j_index:
        range_j = range(img_dimensions[1] - 1, 0, -1)
    
    return range_j

#make a gif out of the images taken after each iteration
def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save("iterations.gif", format="GIF", append_images=frames,
               save_all=True, duration=300, loop=0)

#Extracted Adjacency List
def createExAdjList(Vertices):
    exAdj = {}

    for v1 in Vertices:
        exAdj[v1] = []

        for v2 in v1.Neighbours:
            exAdj[v1].append(v2)

    return exAdj

#Reference Adjacency List
def createReAdjList(file_path):
    reAdj = {}

    with open(file_path, "r") as f:
        for line in f:
            vertecies = re.findall(r"\d+", line)
            v1 = int(vertecies[0])
            reAdj[v1] = []

            for v2 in vertecies[1:]:
                reAdj[v1].append(int(v2))
    
    return reAdj

def render_digraph(G): #https://gist.github.com/sidharthkuruvila/f59b38215316c0cf6f7d18d21347e504
    def g():
        for p, c in G:
            yield  '{},{}'.format(p, c)

    lines = "\n".join(g())
    return """{}""".format(lines)

def extractedToCSV(Edges):
    #transform extracted graph into a format glasgow can read
    G =[]
    for edge in Edges:
        G.append(edge.Connections)
    
    with open("graph.csv", "w") as fo:
        fo.write(render_digraph(G))

def ReferenceStructToCSV(folder_path, image_path):
    #transform reference adjecency graph into a format glasgow can read
    string=""

    with open(folder_path + image_path + ".struct", "r") as f:
        for line in f:
            vertecies = re.findall(r"\d+", line)
            vertex = vertecies[0]
            for v in vertecies[1:]:
                string += vertex + "," + v + "\n"

    with open(image_path + ".csv", "w") as fu:
        fu.write(string)

def parseGraphFromImage(file_path):
    #background color
    color_white = (255, 255, 255)

    #load in graph image
    im = Image.open(file_path)
    im = im.convert('RGB')

    #create list to store objects in
    id = [[0 for i in range(im.size[0]) ] for i in range(im.size[1])]

    #lists to store Vertices and Edges in
    Vertices = []
    Edges = []
    Elements = []

    #define the order in which the pixel will be parsed
    range_i = range(1,im.size[0] - 1)
    range_j = range(1,im.size[1] - 1)

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
                    
                    #add the pixels coordinates to the Edge/Vertex element
                    id[j][i].add(i,j)

        #change the direction with which we iterate through the pixels
        if iterations%4==1:
            range_j = flip_j(True, im.size)

        elif iterations%4==2:
            range_i = flip_i(False, im.size)

        elif iterations%4==3:
            range_j = flip_j(False, im.size)

        else:
            range_i = flip_i(True, im.size)
        
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


    #clean objects list
    polished_Objects = []
    count = 0
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

    print(len(Edges))
    #connect neighboor verticies
    for edge in Edges:
        connected_verticies = edge.Connections.copy()
        v1 = connected_verticies.pop()
        v2 = connected_verticies.pop()
        v1.addNeighbour(v2)
        v2.addNeighbour(v1)

    extractedToCSV(Edges)

    return createExAdjList(Vertices)


#Graph Adjacency List in document
"""
lines = ""
for v in Vertices:
    lines += v.getNeighbours() + ",\n"

with open("graph.struct","w") as f:
    f.write(lines)
"""


extracted_graph = parseGraphFromImage(folder_path + image_path1)
reference_graph = createReAdjList(folder_path + image_path2 + ".struct")

#Heuristics & Isomorphism Test
if IsomorphismTests.heuristicTestIsomorphic(extracted_graph, reference_graph):
    IsomorphismTests.glasgowTest(image_path2)
else:
    print("The two graphs are not isomorphic")
